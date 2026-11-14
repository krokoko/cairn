#!/usr/bin/env python3
"""Check report structure and declared-state consistency, never semantic truth.

Each plugin ships its own copy and contracts so it works independently.
Default: PostToolUse JSON feedback, exit zero. --check FILE: CI exit status.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

CONTRACTS = Path(__file__).with_name("report-contracts.json")
METADATA = ("Source revision", "Assessment date", "Inspected scope", "Evidence basis")
OBSERVATIONS = {"configuration_only", "run_inspected", "not_inspectable", "stale", "not_applicable"}
OUTCOMES = {
    "completed": {"counterexample", "established_within_scope", "no_counterexample_found", "unknown"},
    "timeout": {"counterexample", "unknown"},
    "interrupted": {"counterexample", "incomplete", "unknown"},
    "skipped": {"not_run"},
    "unsupported": {"unsupported"},
    "not_run": {"not_run"},
    "unknown": {"unknown"},
    "not_applicable": {"not_applicable"},
}
CLAIMS = {"counterexample", "established_within_scope", "no_counterexample_found"}
L4_PREREQUISITES = {"L4-INTENT", "L4-ORACLES"}
L5_PREREQUISITES = {"L5-INTENT", "L5-ORACLES", "L5-ENVIRONMENT", "L5-DETECTION", "L5-RECOVERY"}
PREREQUISITES = L4_PREREQUISITES | L5_PREREQUISITES
OPTIONAL_CELLS = {"Limits", "Blockers", "Scope / limits"}
# Exact template tokens, not arbitrary bracketed references such as [ADR-7].
# Keep this vocabulary aligned with the report templates in both standalone plugins.
PLACEHOLDERS = {
    "component", "component name", "name", "placeholder", "environment", "surface", "status",
    "date", "iso date", "yyyy-mm-dd", "l0–l5", "l0–l5 or unknown", "level name", "tier name",
    "actual environment", "allowed conclusion", "allowed execution", "allowed observation",
    "all assessed surfaces and dependencies; exclusions remain outside the recommendation",
    "artifacts inspected, access limits, prior-report freshness",
    "artifacts/runs inspected and inaccessible evidence", "assertion revision, owner, invalidation rule",
    "assessment date and changes from historical method-based scores", "bounded claim and revision",
    "bounds, exclusions and review status", "bounds, exclusions, remaining gaps",
    "ceiling rationale and gaps, or reason none", "change classes/human decisions",
    "cited artifact and revision", "cited artifact/run and revision", "cited evidence or gap",
    "claim / check", "claim and check",
    "commit and relevant dirty changes, or explain unavailable identity",
    "commit plus relevant working-tree changes", "commit/snapshot and relevant uncommitted changes",
    "completed checks and supported result", "components, paths, environments, accessible settings",
    "components, paths, environments, exclusions", "config path / revision", "config/run and revision",
    "configuration and run artifacts inspected; inaccessible settings/history",
    "counts of qualified/partial/configured/none/unknown/not-applicable categories",
    "counts of qualified/partial/configured/none/unknown/not applicable categories",
    "critical paths, unknowns, justified inapplicability",
    "current adequate critical-path oracle evidence for that scope or gap",
    "current commit and relevant dirty changes, or explain unavailable identity",
    "date of planning assessment", "evidenced level or unknown",
    "exactly l0–l5; no higher than the lowest assessed surface recommendation",
    "execution/qualification not inspected", "existing check",
    'include only when mismatch detected — practices ahead of codebase or codebase ahead of practices. see `references/autonomy-levels.md`. otherwise omit or write "aligned."',
    "inspected runs/artifacts, configuration observations, unavailable evidence",
    "links, execution, and meaning separately", "list gates that exist but only as warnings or reports",
    "list of specific blockers preventing advancement to next level",
    "list smells with no coverage and their risk", "list where trend tracking would help",
    "missing evidence", "missing mappings", "missing or questionable mappings",
    "missing run evidence and relevant assumptions",
    "observed blocking/warning/informational/unknown, with evidence",
    "one paragraph: maturity of session-scoped context; what is missing",
    "partial claims, deviations, stale/unknown review", "path/run and revision",
    "paths, categories, environments, exclusions", "paths, components, dependencies and exclusions",
    "pr templates, labels, review rubric, learning docs — present or missing",
    "property, assumptions; not evidence of a completed proof",
    "proposed gate, failure addressed, qualification controls, scope/limits, completion evidence",
    "provisional score and assessed weight, or unknown", "provisional xx/100 or unknown",
    "qualification limits", "recommendation only; operating permissions remain external",
    "reports, source/config identity, environment",
    "representative change, effort/unexpected edits/regressions, or justified inapplicability",
    "representative task, scope, effort, unexpected edits, regressions and boundary violations; or not measured with a proposed exercise",
    "reviewed executable intent for the proposed operating scope or gap",
    "reviewed task criteria, prohibited overclaims, sample size, model/configuration, uncertainty",
    "scoped gate claim", "share of category weights scored; excluded categories and reasons",
    "skipped/missing/stale evidence",
    "source report path/revision/date; freshness comparison; reused, stale and unknown findings",
    "surface and dependencies", "surface and level", "target surfaces and exclusions",
    "uninspected execution or other limits", "unknown review",
    "yes/no and evidence; include unknown intent/oracles and unmet l5 gates",
}


def meaningful(value: str, *, allow_dash: bool = False) -> bool:
    value = value.strip().strip("`").strip()
    if value == "-":
        return allow_dash
    if value.startswith("[") and value.endswith("]") and value[1:-1].lower() in PLACEHOLDERS:
        return False
    if re.fullmatch(r"X+(?:/\d+)?(?:(?:, or| /) unknown)?", value):
        return False
    return bool(value) and value.lower() not in {"...", "…", "tbd", "todo"}


def sections(text: str) -> tuple[dict[str, str], set[str]]:
    """Ignore fenced examples and comments; only real H2 sections count."""
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    result: dict[str, str] = {}
    duplicates: set[str] = set()
    current = None
    fence = ""
    for line in text.splitlines():
        marker = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if marker:
            token = marker.group(1)
            if not fence:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = ""
            continue
        if fence:
            continue
        heading = re.match(r"^##\s+(.+?)(?:\s+#+)?\s*$", line)
        if heading:
            current = heading.group(1)
            if current in result:
                duplicates.add(current)
            result.setdefault(current, "")
        elif current is not None:
            result[current] += line + "\n"
    return result, duplicates


def cells(line: str) -> list[str]:
    return [cell.strip().strip("`") for cell in re.split(r"(?<!\\)\|", line.strip().strip("|"))]


def separator(line: str) -> bool:
    return line.lstrip().startswith("|") and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells(line))


def substantive(body: str) -> bool:
    """Table headers, dividers, labels and placeholders are scaffolding."""
    lines = body.splitlines()
    table_started = False
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("|"):
            if separator(line):
                table_started = True
            elif index + 1 < len(lines) and separator(lines[index + 1]):
                continue
            elif table_started:
                row = cells(line)
                # The first column commonly contains fixed template labels.
                if len(row) > 1 and meaningful(row[0]) and all(
                    meaningful(cell, allow_dash=True) for cell in row[1:]
                ):
                    return True
        else:
            table_started = False
            value = re.sub(r"^(?:[-*]|\d+\.)\s+", "", stripped)
            value = re.sub(r"^\*\*[^*]+(?::\*\*|\*\*:)\s*", "", value)
            if not value.startswith("#") and meaningful(value):
                return True
    return False


def validate_assessment_tables(body: str, name: str, errors: list[str]) -> None:
    """A completed row or surrounding prose cannot hide unfinished table rows."""
    lines = body.splitlines()
    for index, line in enumerate(lines):
        if not line.lstrip().startswith("|") or index + 1 >= len(lines) or not separator(lines[index + 1]):
            continue
        width = len(cells(line))
        rows = []
        for row_line in lines[index + 2:]:
            if not row_line.lstrip().startswith("|"):
                break
            rows.append(cells(row_line))
        if not rows:
            errors.append(f"{name}: needs a substantive row; state unknowns or exclusions explicitly.")
        elif any(len(row) != width or not meaningful(row[0]) or not all(
            meaningful(value, allow_dash=True) for value in row[1:]
        ) for row in rows):
            errors.append(f"{name}: every assessment table row needs {width} non-placeholder cells.")


def table(body: str, header: list[str], name: str, errors: list[str]) -> list[dict[str, str]]:
    lines = body.splitlines()
    matched = False
    all_rows = []
    for index, line in enumerate(lines):
        if not line.lstrip().startswith("|") or cells(line) != header:
            continue
        matched = True
        if index + 1 >= len(lines) or len(cells(lines[index + 1])) != len(header) or not all(
            re.fullmatch(r":?-{3,}:?", cell) for cell in cells(lines[index + 1])
        ):
            errors.append(f"{name}: missing Markdown table separator.")
            continue
        rows = []
        for row_line in lines[index + 2:]:
            if not row_line.lstrip().startswith("|"):
                break
            row = cells(row_line)
            if len(row) != len(header) or not all(
                meaningful(value, allow_dash=column in OPTIONAL_CELLS)
                for column, value in zip(header, row)
            ):
                errors.append(f"{name}: every assessment table row needs {len(header)} non-placeholder cells.")
                continue
            rows.append(dict(zip(header, row)))
        all_rows.extend(rows)
    if not matched:
        errors.append(f"{name}: missing table columns: {' | '.join(header)}.")
    return all_rows


def validate_ledger(rows: list[dict[str, str]], errors: list[str]) -> None:
    for row in rows:
        label = f"Evidence Ledger ({row['Claim / check']})"
        observed, execution, conclusion = (row[key] for key in ("Observation", "Execution", "Conclusion"))
        if observed not in OBSERVATIONS:
            errors.append(f"{label}: invalid Observation '{observed}'.")
        if execution not in OUTCOMES:
            errors.append(f"{label}: invalid Execution '{execution}'.")
        elif observed == "stale":
            if conclusion not in {"unknown", "incomplete"}:
                errors.append(f"{label}: stale evidence requires an unknown or incomplete current conclusion.")
        elif conclusion not in OUTCOMES[execution]:
            errors.append(f"{label}: Conclusion '{conclusion}' is incompatible with Execution '{execution}'.")
        if conclusion in CLAIMS and observed != "run_inspected":
            errors.append(f"{label}: an evidential conclusion requires run_inspected.")
        if observed == "configuration_only" and execution not in {"skipped", "not_run", "unknown"}:
            errors.append(f"{label}: configuration alone cannot establish execution.")
        if observed == "not_inspectable" and (execution != "unknown" or conclusion != "unknown"):
            errors.append(f"{label}: uninspectable evidence must retain unknown execution and conclusion.")
        if observed == "not_applicable" and (execution != "not_applicable" or conclusion != "not_applicable"):
            errors.append(f"{label}: an exclusion must use not_applicable consistently and give its reason in Limits.")
        reason = None
        if observed == "not_applicable":
            reason = "a claim/risk-based exemption reason"
        elif observed == "configuration_only" and execution == "skipped":
            reason = "the unconditional skip declaration and scope"
        elif observed == "stale" and conclusion == "incomplete":
            reason = "the unfinished current analysis"
        if reason and not meaningful(row["Limits"]):
            errors.append(f"{label}: Limits must identify {reason}; '-' is insufficient.")


def validate_autonomy(surfaces: list[dict[str, str]], gates: list[dict[str, str]], errors: list[str]) -> None:
    names = [row["Surface"] for row in surfaces]
    if len(names) != len(set(names)):
        errors.append("Surface Autonomy: duplicate surface.")
    by_surface: dict[str, dict[str, str]] = {name: {} for name in names}
    for row in gates:
        surface, gate, status = row["Surface"], row["Prerequisite"], row["Status"]
        if surface not in by_surface:
            errors.append(f"Autonomy Prerequisites: unknown surface '{surface}'.")
            continue
        if gate not in PREREQUISITES or gate in by_surface[surface]:
            errors.append(f"Autonomy Prerequisites: unknown or repeated prerequisite '{gate}' for {surface}.")
        if status not in {"met", "missing", "unknown", "not_applicable"}:
            errors.append(f"Autonomy Prerequisites: invalid Status '{status}'.")
        by_surface[surface][gate] = status
    for row in surfaces:
        name = row["Surface"]
        levels = [row[key] for key in ("Provisional level", "Evidence ceiling", "Recommended level")]
        if not all(re.fullmatch(r"L[0-5]|unknown", value) for value in levels[:2]) or not re.fullmatch(r"L[0-5]", levels[2]):
            errors.append(f"Surface Autonomy ({name}): recommendation must be L0-L5; provisional level and ceiling may be unknown.")
            continue
        known_limits = [int(value[1]) for value in levels[:2] if value != "unknown"]
        if known_limits and int(levels[2][1]) > min(known_limits):
            errors.append(f"Surface Autonomy ({name}): recommendation exceeds the provisional level or evidence ceiling.")
        if levels[1] == "unknown" and int(levels[2][1]) > 3:
            errors.append(f"Surface Autonomy ({name}): an unknown evidence ceiling cannot support L4/L5.")
        if set(by_surface[name]) != PREREQUISITES:
            errors.append(f"Autonomy Prerequisites ({name}): list both L4 and all five L5 prerequisites.")
        if int(levels[2][1]) >= 4 and any(by_surface[name].get(key) != "met" for key in L4_PREREQUISITES):
            errors.append(f"Surface Autonomy ({name}): L4/L5 requires scoped intent and oracle prerequisites met; otherwise the ceiling is L3.")
        if levels[2] == "L5" and any(by_surface[name].get(key) != "met" for key in L5_PREREQUISITES):
            errors.append(f"Surface Autonomy ({name}): L5 requires all five prerequisites met; unknown/N/A is not a waiver.")


def validate_summary(body: str, surfaces: list[dict[str, str]], errors: list[str]) -> None:
    levels = re.findall(r"^\*\*Level(?::\*\*|\*\*:)[ \t]*(.*)$", body, re.M)
    if len(levels) != 1 or not re.fullmatch(r"L[0-5]", levels[0].strip()):
        errors.append("Recommended Autonomy Level needs one '**Level**: L0-L5' value; put surface differences in Surface Autonomy.")
        return
    recommendations = [int(row["Recommended level"][1]) for row in surfaces
                       if re.fullmatch(r"L[0-5]", row["Recommended level"])]
    if recommendations and int(levels[0].strip()[1]) > min(recommendations):
        errors.append("Recommended Autonomy Level exceeds an assessed surface recommendation; use a conservative summary across all assessed surfaces.")


def validate(path: Path, contracts: dict) -> list[str] | None:
    contract = contracts.get(path.name)
    if contract is None:
        return None
    if not path.is_file():
        return ["Report file is missing or not readable."]
    found, duplicates = sections(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    parsed = {}
    for heading in contract["sections"]:
        if heading not in found:
            errors.append(f"Missing required section: '## {heading}'.")
        elif heading in duplicates:
            errors.append(f"Duplicate required section: '## {heading}'.")
        if heading in found:
            section_errors: list[str] = []
            validate_assessment_tables(found[heading], heading, section_errors)
            if heading in contract.get("tables", {}):
                parsed[heading] = table(found[heading], contract["tables"][heading], heading, section_errors)
            if not substantive(found[heading]) and not section_errors:
                section_errors.append(f"Section '{heading}' needs substantive content.")
            errors.extend(dict.fromkeys(section_errors))
    scope = found.get("Evidence Scope", "")
    for field in METADATA:
        match = re.search(rf"^\*\*{re.escape(field)}(?::\*\*|\*\*:)[ \t]*(.*)$", scope, re.M)
        if not match or not meaningful(match.group(1)):
            errors.append(f"Evidence Scope: missing or placeholder '{field}'.")
    if "Evidence Ledger" in parsed:
        validate_ledger(parsed["Evidence Ledger"], errors)
    if "Surface Autonomy" in parsed:
        validate_autonomy(parsed["Surface Autonomy"], parsed.get("Autonomy Prerequisites", []), errors)
    if path.name == "readiness-report.md":
        validate_summary(found.get("Recommended Autonomy Level", ""), parsed.get("Surface Autonomy", []), errors)
    return errors


def main() -> int:
    cli = len(sys.argv) == 3 and sys.argv[1] == "--check"
    try:
        contracts = json.loads(CONTRACTS.read_text(encoding="utf-8"))
        if cli:
            path = Path(sys.argv[2])
        elif len(sys.argv) == 1:
            event = json.load(sys.stdin)
            raw_path = event.get("tool_input", {}).get("file_path")
            if not isinstance(raw_path, str) or not raw_path:
                return 0
            path = Path(raw_path)
        else:
            print("Usage: check-report.py [--check FILE]", file=sys.stderr)
            return 2
        errors = validate(path, contracts)
        if errors is None:
            if cli:
                print(f"Unsupported report filename: {path.name}", file=sys.stderr)
                return 2
            return 0
        message = (
            "Report validation failed: " + " ".join(errors)
            if errors else
            "Report structure and declared evidence states validated successfully. Semantic truth and authorization are not validated."
        )
    except (OSError, ValueError, AttributeError, TypeError) as exc:
        errors = [str(exc)]
        message = f"WARNING: Report validation could not complete: {exc}"
    if cli:
        print(message)
        return int(bool(errors))
    print(json.dumps({"systemMessage": message}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
