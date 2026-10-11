#!/usr/bin/env python3
"""Freeze blind skill evaluations and check retained artifact integrity.

No model is invoked and no semantic result is inferred by this utility.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CASES = ROOT / "tests/evals/cases.json"
RUBRIC = ROOT / "tests/evals/rubric.json"
ARCHIVES = ROOT / "tests/evals/results"
SKILLS = {
    "assess-readiness": "codebase-ai-readiness",
    "generate-roadmap": "codebase-ai-readiness",
    "assess-verification": "software-verification",
    "design-strategy": "software-verification",
    "detect-ai-smells": "software-verification",
}
SOURCE_SUFFIXES = {".md", ".json", ".py", ".sh"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256(value: object, label: str) -> str:
    require(isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None,
            f"Invalid {label} digest")
    return value


def relative_path(value: object) -> Path:
    require(text(value), "Missing artifact path")
    path = Path(value)
    require(not path.is_absolute() and ".." not in path.parts and path != Path("."),
            f"Artifact paths must stay within their directory: {value}")
    return path


def artifact(directory: Path, name: object) -> Path:
    path = directory / relative_path(name)
    require(path.resolve().is_relative_to(directory.resolve()),
            f"Artifact paths must stay within their directory: {name}")
    require(path.is_file(), f"Missing artifact: {path}")
    return path


def report_artifact(directory: Path, name: object, input_names) -> Path:
    report = artifact(directory, name)
    for input_name in input_names:
        require(not report.samefile(artifact(directory, input_name)),
                "Report cannot be an input or an alias of an input")
    return report


def read_json(path: Path):
    return json.loads(path.read_text())


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n")


def source_digest(files: dict[str, str]) -> str:
    result = hashlib.sha256()
    for name, content in sorted(files.items()):
        result.update(name.encode() + b"\0" + content.encode() + b"\0")
    return result.hexdigest()


def source_files() -> dict[str, str]:
    return {
        path.relative_to(ROOT).as_posix(): path.read_bytes().decode("utf-8")
        for path in sorted((ROOT / "plugins").rglob("*"))
        if path.is_file() and path.suffix in SOURCE_SUFFIXES
    }


def implementation_digest() -> str:
    return source_digest(source_files())


def load(cases_path: Path | None = None, rubric_path: Path | None = None):
    catalog = read_json(cases_path or CASES)
    rubric = read_json(rubric_path or RUBRIC)
    require(catalog["version"] == rubric["version"] == 1, "Unsupported fixture version")
    ids = [case["id"] for case in catalog["cases"]]
    require(all(text(case_id) and re.fullmatch(r"[a-z0-9-]+", case_id) for case_id in ids),
            "Unsafe scenario ID")
    require(len(ids) == len(set(ids)) and ids, "Empty or duplicate scenario inventory")
    require(set(ids) == set(rubric["cases"]), "Scenario/rubric inventory differs")
    for case in catalog["cases"]:
        require(case["skill"] in SKILLS, "Unknown skill")
        require(text(case["prompt"]), "Empty prompt")
        require("snapshot.json" in case["files"], "Missing source identity")
        for name, content in case["files"].items():
            path = relative_path(name)
            require(text(content), f"Empty fixture: {name}")
            if path.suffix == ".json":
                json.loads(content)
        criteria = rubric["cases"][case["id"]]["criteria"]
        require(isinstance(criteria, dict) and criteria and all(text(value) for value in criteria.values()),
                "Empty rubric")
    return catalog, rubric


def snapshot(output: Path) -> None:
    load()
    files = source_files()
    require(files, "No plugin source found")
    output.mkdir(parents=True, exist_ok=False)
    shutil.copyfile(CASES, output / "cases.json")
    shutil.copyfile(RUBRIC, output / "rubric.json")
    write_json(output / "source.json", {"version": 1, "files": files})
    write_json(output / "snapshot.json", {
        "version": 1,
        "implementation_sha256": source_digest(files),
        "fixture_sha256": digest(output / "cases.json"),
        "rubric_sha256": digest(output / "rubric.json"),
    })
    print(output / "snapshot.json")


def load_snapshot(directory: Path):
    identity = read_json(artifact(directory, "snapshot.json"))
    require(identity["version"] == 1, "Unsupported snapshot version")
    cases_path = artifact(directory, "cases.json")
    rubric_path = artifact(directory, "rubric.json")
    require(identity["fixture_sha256"] == digest(cases_path), "Fixture digest mismatch")
    require(identity["rubric_sha256"] == digest(rubric_path), "Rubric digest mismatch")
    source = read_json(artifact(directory, "source.json"))
    require(source["version"] == 1 and isinstance(source["files"], dict) and source["files"],
            "Invalid source snapshot")
    for name, content in source["files"].items():
        path = relative_path(name)
        require(path.parts[0] == "plugins" and path.suffix in SOURCE_SUFFIXES and isinstance(content, str),
                f"Invalid source snapshot file: {name}")
    require(sha256(identity["implementation_sha256"], "implementation") == source_digest(source["files"]),
            "Implementation digest mismatch")
    catalog, rubric = load(cases_path, rubric_path)
    for case in catalog["cases"]:
        skill = f"plugins/{SKILLS[case['skill']]}/skills/{case['skill']}/SKILL.md"
        require(skill in source["files"], f"Missing evaluated skill source: {skill}")
    return identity, catalog, rubric, source["files"]


def prepare(case_id: str, output: Path, snapshot_directory: Path) -> None:
    identity, catalog, _, files = load_snapshot(snapshot_directory)
    case = next((item for item in catalog["cases"] if item["id"] == case_id), None)
    require(case is not None, f"Unknown case: {case_id}")
    output.mkdir(parents=True, exist_ok=False)
    for base, content in ((output / "source", files), (output / "repository", case["files"])):
        for name, value in content.items():
            path = base / relative_path(name)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(value.encode())
    skill = output.resolve() / "source/plugins" / SKILLS[case["skill"]] / "skills" / case["skill"] / "SKILL.md"
    prompt = (
        f"Use the skill at {skill} to fulfill this request:\n\n{case['prompt']}\n\n"
        f"Target repository snapshot: {output.resolve() / 'repository'}\n"
        "Read the named frozen skill and its relevant frozen references, and only this target snapshot. "
        "Do not read evaluation definitions, expected results, sibling cases, prior outputs, or live plugin source. "
        "Write the report in the target snapshot; cite evidence and preserve unknowns.\n"
    )
    (output / "TASK.txt").write_text(prompt)
    write_json(output / "preparation.json", {"case_id": case_id, **identity})
    print(output / "TASK.txt")


def retain_case(case_id: str, prepared: Path, run: Path, report_name: str) -> None:
    identity, catalog, _, files = load_snapshot(run)
    require(read_json(artifact(prepared, "preparation.json")) == {"case_id": case_id, **identity},
            "Preparation identity differs from retained snapshot")
    case = next((item for item in catalog["cases"] if item["id"] == case_id), None)
    require(case is not None, f"Unknown case: {case_id}")
    for name, content in files.items():
        require(artifact(prepared / "source", name).read_bytes() == content.encode(),
                f"Prepared source changed: {name}")
    report_path = relative_path(report_name)
    report = report_artifact(prepared / "repository", report_path.as_posix(), case["files"])
    require(report.read_bytes().strip(), "Empty assessment artifact")
    for name, content in case["files"].items():
        require(artifact(prepared / "repository", name).read_bytes() == content.encode(),
                f"Prepared input changed: {case_id}/{name}")
    destination = run / "cases" / case_id
    destination.mkdir(parents=True, exist_ok=False)
    for name in (*case["files"], report_path.as_posix()):
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(prepared / "repository" / name, target)
    print(json.dumps({
        "report": (Path("cases") / case_id / report_path).as_posix(),
        "report_sha256": digest(destination / report_path),
        "input_sha256": {name: digest(destination / name) for name in case["files"]},
        "criteria": {},
    }, indent=2))


def check_results(path: Path, integrity_only: bool = False) -> int:
    result = read_json(path)
    require(result.get("schema_version") == 2, "Unsupported result schema; migrate retained artifacts explicitly")
    for field in ("run_id", "date", "source_revision", "implementation_sha256",
                  "fixture_sha256", "rubric_sha256", "model", "configuration", "adjudicator", "limitations"):
        require(text(result.get(field)), f"Missing run metadata: {field}")
    sha256(result["implementation_sha256"], "implementation")
    cases_path = artifact(path.parent, "cases.json")
    rubric_path = artifact(path.parent, "rubric.json")
    require(result["fixture_sha256"] == digest(cases_path), "Fixture digest mismatch")
    require(result["rubric_sha256"] == digest(rubric_path), "Rubric digest mismatch")
    catalog, rubric = load(cases_path, rubric_path)
    provenance = result.get("provenance")
    require(provenance in {"retained_source", "legacy_missing_source"}, "Missing source provenance")
    if provenance == "retained_source":
        identity, _, _, _ = load_snapshot(path.parent)
        for field in ("implementation_sha256", "fixture_sha256", "rubric_sha256"):
            require(result[field] == identity[field], f"Result/snapshot identity differs: {field}")
    else:
        require(text(result.get("provenance_limitation")), "Legacy source provenance requires an explicit limitation")
        print(f"Legacy provenance warning: {result['run_id']}: {result['provenance_limitation']}")
    require(set(result["cases"]) == {case["id"] for case in catalog["cases"]}, "Incomplete scenario inventory")
    fixtures = {case["id"]: case for case in catalog["cases"]}
    counts = {"pass": 0, "fail": 0, "not_evaluated": 0}
    for case_id, case in result["cases"].items():
        report_path = relative_path(case["report"])
        case_directory = Path("cases") / case_id
        require(report_path.is_relative_to(case_directory),
                f"Report paths must stay within their case directory: {case_id}")
        report = report_artifact(path.parent / case_directory,
                                 report_path.relative_to(case_directory).as_posix(),
                                 fixtures[case_id]["files"])
        require(report.read_bytes().strip(), f"Empty assessment artifact: {report}")
        require(sha256(case.get("report_sha256"), "report") == digest(report),
                f"Report digest mismatch: {case_id}; adjudicate the changed artifact again")
        require(set(case["input_sha256"]) == set(fixtures[case_id]["files"]),
                f"Incomplete input inventory: {case_id}")
        for name, content in fixtures[case_id]["files"].items():
            input_path = artifact(path.parent / "cases" / case_id, name)
            expected = hashlib.sha256(content.encode()).hexdigest()
            require(sha256(case["input_sha256"][name], "input") == digest(input_path) == expected,
                    f"Input digest mismatch: {case_id}/{name}")
        for name, expected in case.get("additional_artifact_sha256", {}).items():
            require(sha256(expected, "additional artifact") == digest(artifact(path.parent, name)),
                    f"Additional artifact digest mismatch: {name}")
        require(set(case["criteria"]) == set(rubric["cases"][case_id]["criteria"]),
                f"Incomplete rubric: {case_id}")
        for criterion, judgment in case["criteria"].items():
            status = judgment["status"]
            require(status in counts, f"Unknown adjudication: {case_id}/{criterion}")
            require(text(judgment.get("evidence")), f"Missing rationale: {case_id}/{criterion}")
            counts[status] += 1
    print(f"{result['run_id']}: recorded adjudications {counts}. Artifact integrity checked; judgments require review.")
    if integrity_only:
        return 0
    return int(bool(counts["fail"] or counts["not_evaluated"] or provenance != "retained_source"))


def check_archives(directory: Path) -> int:
    require(directory.is_dir(), f"Missing evaluation archives: {directory}")
    archives = sorted(path for path in directory.iterdir() if path.is_dir())
    require(archives, "No retained evaluation archives")
    for run in archives:
        check_results(artifact(run, "results.json"), integrity_only=True)
    print(f"{len(archives)} retained evaluation archives passed integrity checks; no new model was executed.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("check")
    commands.add_parser("fingerprint")
    freeze = commands.add_parser("snapshot")
    freeze.add_argument("--output", type=Path, required=True)
    prep = commands.add_parser("prepare")
    prep.add_argument("case")
    prep.add_argument("--snapshot", type=Path, required=True)
    prep.add_argument("--output", type=Path, required=True)
    retain = commands.add_parser("retain-case")
    retain.add_argument("case")
    retain.add_argument("--prepared", type=Path, required=True)
    retain.add_argument("--run", type=Path, required=True)
    retain.add_argument("--report", required=True)
    results = commands.add_parser("check-results")
    results.add_argument("path", type=Path)
    archives = commands.add_parser("check-archives")
    archives.add_argument("--directory", type=Path, default=ARCHIVES)
    args = parser.parse_args()
    try:
        if args.command == "check":
            catalog, _ = load()
            print(f"{len(catalog['cases'])} independent scenarios and withheld rubrics are structurally valid. No skill was executed.")
        elif args.command == "fingerprint":
            print(json.dumps({"implementation_sha256": implementation_digest(),
                              "fixture_sha256": digest(CASES), "rubric_sha256": digest(RUBRIC)}))
        elif args.command == "snapshot":
            snapshot(args.output)
        elif args.command == "prepare":
            prepare(args.case, args.output, args.snapshot)
        elif args.command == "retain-case":
            retain_case(args.case, args.prepared, args.run, args.report)
        elif args.command == "check-archives":
            return check_archives(args.directory)
        else:
            return check_results(args.path)
    except (ValueError, KeyError, OSError, TypeError, AttributeError) as exc:
        print(f"Evaluation validation failed: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
