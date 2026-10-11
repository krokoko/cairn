#!/usr/bin/env python3
"""Freeze blind skill evaluations and check retained artifact integrity.

No model is invoked and no semantic result is inferred by this utility.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import shutil
import subprocess
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


class SourceUnavailable(ValueError):
    """A retained Git commit is not available in this local checkout."""


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


def contained_path(directory: Path, name: object) -> Path:
    path = directory / relative_path(name)
    require(path.resolve().is_relative_to(directory.resolve()),
            f"Artifact paths must stay within their directory: {name}")
    return path


def subdirectory(directory: Path, name: object) -> Path:
    path = contained_path(directory, name)
    require(path.is_dir(), f"Missing artifact directory: {path}")
    return path


def artifact(directory: Path, name: object) -> Path:
    path = contained_path(directory, name)
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


def git_source_files(revision: object) -> dict[str, str]:
    require(isinstance(revision, str) and re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", revision),
            "Git source provenance requires a full commit SHA")
    # A local replace ref must not redefine bytes attributed to an immutable commit SHA.
    command = ["git", "--no-replace-objects", "-C", str(ROOT)]
    exists = subprocess.run([*command, "cat-file", "-e", f"{revision}^{{commit}}"],
                            capture_output=True)
    if exists.returncode:
        raise SourceUnavailable(
            f"Git source commit {revision} is unavailable locally (for example, in a shallow checkout); "
            "source integrity and preparation cannot be checked. No history was fetched.")
    tree = subprocess.run([*command, "ls-tree", "-rz", revision, "--", "plugins"], capture_output=True)
    require(tree.returncode == 0, f"Cannot read plugin tree from Git commit {revision}")
    entries = []
    for entry in tree.stdout.split(b"\0"):
        if not entry:
            continue
        metadata, raw_name = entry.split(b"\t", 1)
        mode, kind, object_id = metadata.split()
        name = raw_name.decode("utf-8")
        if Path(name).suffix in SOURCE_SUFFIXES:
            require(kind == b"blob" and mode in {b"100644", b"100755"},
                    f"Git source must contain regular plugin files: {name}")
            entries.append((name, object_id))
    blobs = subprocess.run([*command, "cat-file", "--batch"],
                           input=b"".join(object_id + b"\n" for _, object_id in entries),
                           capture_output=True)
    require(blobs.returncode == 0, f"Cannot read plugin bytes from Git commit {revision}")
    stream = io.BytesIO(blobs.stdout)
    files = {}
    for name, object_id in entries:
        header = stream.readline().split()
        require(len(header) == 3 and header[:2] == [object_id, b"blob"], f"Missing Git blob: {name}")
        content = stream.read(int(header[2]))
        require(stream.read(1) == b"\n", f"Incomplete Git blob: {name}")
        files[name] = content.decode("utf-8")
    return files


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


def snapshot(output: Path, revision: str | None = None) -> None:
    load()
    files = git_source_files(revision) if revision else source_files()
    require(files, "No plugin source found")
    provenance = "git_revision" if revision else "retained_source"
    output.mkdir(parents=True, exist_ok=False)
    shutil.copyfile(CASES, output / "cases.json")
    shutil.copyfile(RUBRIC, output / "rubric.json")
    if provenance == "retained_source":
        write_json(output / "source.json", {"version": 1, "files": files})
    write_json(output / "snapshot.json", {
        "version": 2,
        "provenance": provenance,
        **({"source_revision": revision} if revision else {}),
        "implementation_sha256": source_digest(files),
        "fixture_sha256": digest(output / "cases.json"),
        "rubric_sha256": digest(output / "rubric.json"),
    })
    print(output / "snapshot.json")


def load_snapshot(directory: Path, allow_missing_source: bool = False):
    identity = read_json(artifact(directory, "snapshot.json"))
    require(identity["version"] in {1, 2}, "Unsupported snapshot version")
    cases_path = artifact(directory, "cases.json")
    rubric_path = artifact(directory, "rubric.json")
    require(identity["fixture_sha256"] == digest(cases_path), "Fixture digest mismatch")
    require(identity["rubric_sha256"] == digest(rubric_path), "Rubric digest mismatch")
    provenance = identity.get("provenance", "retained_source")
    require(provenance in {"retained_source", "git_revision"}, "Invalid snapshot source provenance")
    files = None
    if provenance == "git_revision":
        try:
            files = git_source_files(identity.get("source_revision"))
        except SourceUnavailable as exc:
            if not allow_missing_source:
                raise
            print(f"WARNING: {exc}")
    else:
        source = read_json(artifact(directory, "source.json"))
        require(source["version"] == 1 and isinstance(source["files"], dict) and source["files"],
                "Invalid source snapshot")
        files = source["files"]
    if files is not None:
        require(files, "No plugin source found")
        for name, content in files.items():
            path = relative_path(name)
            require(path.parts[0] == "plugins" and path.suffix in SOURCE_SUFFIXES and isinstance(content, str),
                    f"Invalid source snapshot file: {name}")
        require(sha256(identity["implementation_sha256"], "implementation") == source_digest(files),
                "Implementation digest mismatch")
    else:
        sha256(identity["implementation_sha256"], "implementation")
    catalog, rubric = load(cases_path, rubric_path)
    if files is not None:
        for case in catalog["cases"]:
            skill = f"plugins/{SKILLS[case['skill']]}/skills/{case['skill']}/SKILL.md"
            require(skill in files, f"Missing evaluated skill source: {skill}")
    return identity, catalog, rubric, files


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
    source_directory = subdirectory(prepared, "source")
    repository = subdirectory(prepared, "repository")
    for name, content in files.items():
        require(artifact(source_directory, name).read_bytes() == content.encode(),
                f"Prepared source changed: {name}")
    report_path = relative_path(report_name)
    report = report_artifact(repository, report_path.as_posix(), case["files"])
    require(report.read_bytes().strip(), "Empty assessment artifact")
    for name, content in case["files"].items():
        require(artifact(repository, name).read_bytes() == content.encode(),
                f"Prepared input changed: {case_id}/{name}")
    destination = contained_path(run, (Path("cases") / case_id).as_posix())
    destination.mkdir(parents=True, exist_ok=False)
    for name in (*case["files"], report_path.as_posix()):
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(repository / name, target)
    print(json.dumps({
        "report": (Path("cases") / case_id / report_path).as_posix(),
        "report_sha256": digest(destination / report_path),
        "input_sha256": {name: digest(destination / name) for name in case["files"]},
        "criteria": {},
    }, indent=2))


def inspect_results(path: Path, allow_missing_source: bool = False):
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
    require(provenance in {"retained_source", "git_revision", "legacy_missing_source"}, "Missing source provenance")
    source_complete = False
    if provenance in {"retained_source", "git_revision"}:
        identity, _, _, files = load_snapshot(path.parent, allow_missing_source=allow_missing_source)
        require(provenance == identity.get("provenance", "retained_source"),
                "Result/snapshot source provenance differs")
        for field in ("implementation_sha256", "fixture_sha256", "rubric_sha256"):
            require(result[field] == identity[field], f"Result/snapshot identity differs: {field}")
        if provenance == "git_revision":
            require(result["source_revision"] == identity["source_revision"],
                    "Result/snapshot Git revision differs")
        source_complete = files is not None
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
        case_root = subdirectory(path.parent, case_directory.as_posix())
        report = report_artifact(case_root,
                                 report_path.relative_to(case_directory).as_posix(),
                                 fixtures[case_id]["files"])
        require(report.read_bytes().strip(), f"Empty assessment artifact: {report}")
        require(sha256(case.get("report_sha256"), "report") == digest(report),
                f"Report digest mismatch: {case_id}; adjudicate the changed artifact again")
        require(set(case["input_sha256"]) == set(fixtures[case_id]["files"]),
                f"Incomplete input inventory: {case_id}")
        for name, content in fixtures[case_id]["files"].items():
            input_path = artifact(case_root, name)
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
    return result, counts, source_complete


def print_result_check(result: dict, counts: dict, source_complete: bool) -> None:
    qualification = "Source and artifact integrity checked" if source_complete else "Artifact integrity checked; source provenance incomplete"
    print(f"{result['run_id']}: recorded adjudications {counts}. {qualification}; judgments require review.")


def check_results(path: Path, integrity_only: bool = False, allow_missing_source: bool = False) -> int:
    result, counts, source_complete = inspect_results(path, allow_missing_source=allow_missing_source)
    print_result_check(result, counts, source_complete)
    if integrity_only:
        return 0
    return int(bool(counts["fail"] or counts["not_evaluated"] or not source_complete))


def check_archives(directory: Path) -> int:
    require(directory.is_dir(), f"Missing evaluation archives: {directory}")
    archives = sorted(subdirectory(directory, path.name) for path in directory.iterdir() if path.is_dir())
    require(archives, "No retained evaluation archives")
    recorded_passes = []
    for run in archives:
        path = artifact(run, "results.json")
        result, counts, source_complete = inspect_results(path, allow_missing_source=True)
        print_result_check(result, counts, source_complete)
        if source_complete and not counts["fail"] and not counts["not_evaluated"]:
            recorded_passes.append(result)
    if recorded_passes:
        latest = max(recorded_passes, key=lambda result: (result["date"], result["run_id"]))
        if latest["implementation_sha256"] != implementation_digest():
            print(f"WARNING: Live plugin source differs from the latest recorded all-pass run "
                  f"{latest['run_id']}. Its historical judgments do not evaluate the current source.")
    else:
        print("WARNING: No retained run records complete passing adjudications with source provenance.")
    print(f"{len(archives)} retained evaluation archives checked; see any provenance warnings above. "
          "No new model or semantic judge was executed.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("check")
    commands.add_parser("fingerprint")
    freeze = commands.add_parser("snapshot")
    freeze.add_argument("--output", type=Path, required=True)
    freeze.add_argument("--revision", help="Full committed source SHA; omit to retain standalone live source")
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
            print(f"{len(catalog['cases'])} scenarios and withheld rubrics are structurally valid. No skill was executed.")
        elif args.command == "fingerprint":
            print(json.dumps({"implementation_sha256": implementation_digest(),
                              "fixture_sha256": digest(CASES), "rubric_sha256": digest(RUBRIC)}))
        elif args.command == "snapshot":
            snapshot(args.output, args.revision)
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
