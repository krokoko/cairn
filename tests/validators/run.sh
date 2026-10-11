#!/usr/bin/env bash
# Tests for the PostToolUse report validators in both plugins.
#
# Covers each validator branch (good report passes, report missing a section
# fails and names it, non-report files are ignored, autonomy-level regex) plus
# a template-drift guard: every section a validator requires must exist as a
# heading in the matching report template. The drift guard is what catches a
# validator falling out of sync with its template (the class of bug these
# tests were added for).
#
# Deps: bash, python3 (same as the validators themselves). Exit 0 = all pass.
set -uo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
READINESS="$REPO_ROOT/plugins/codebase-ai-readiness/scripts/validate-report.sh"
VERIFICATION="$REPO_ROOT/plugins/software-verification/scripts/validate-verification-report.sh"

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

PASS=0
FAIL=0

# run_validator <script> <report-filename> <body> -> echoes the validator's stdout
run_validator() {
  local script="$1" fname="$2" body="$3"
  local path="$TMP/$fname"
  printf '%s\n' "$body" >"$path"
  printf '{"tool_input":{"file_path":"%s"}}' "$path" | bash "$script"
}

# expect <description> <actual> <substring-that-must-appear>
expect() {
  local desc="$1" actual="$2" needle="$3"
  if [[ "$actual" == *"$needle"* ]]; then
    PASS=$((PASS + 1))
  else
    FAIL=$((FAIL + 1))
    echo "FAIL: $desc"
    echo "  expected to contain: $needle"
    echo "  actual:              $actual"
  fi
}

# expect_absent <description> <actual> <substring-that-must-not-appear>
expect_absent() {
  local desc="$1" actual="$2" needle="$3"
  if [[ "$actual" != *"$needle"* ]]; then
    PASS=$((PASS + 1))
  else
    FAIL=$((FAIL + 1))
    echo "FAIL: $desc"
    echo "  expected NOT to contain: $needle"
    echo "  actual:                  $actual"
  fi
}

# sections_required_by <script> <filename> -> prints one required section per line.
# Extracts the `for section in "A" "B" ...` list guarded by the matching filename.
sections_required_by() {
  local script="$1" fname="$2"
  python3 - "$script" "$fname" <<'PY'
import re, sys
script, fname = sys.argv[1], sys.argv[2]
text = open(script).read()
# Find the `if [[ "$FILENAME" == "<fname>" ]]; then ... for section in <list>` block.
block = re.search(
    re.escape(f'"$FILENAME" == "{fname}"') + r'.*?for section in (.*?);\s*do',
    text, re.S)
if not block:
    sys.exit(0)
for m in re.finditer(r'"([^"]+)"', block.group(1)):
    print(m.group(1))
PY
}

# ---------------------------------------------------------------------------
# Readiness validator
# ---------------------------------------------------------------------------
READINESS_REPORT_OK=$(cat <<'EOF'
## Overall Score
50/100
## Category Breakdown
## Recommended Autonomy Level
L2
## Workflow artifacts
## Collaboration effectiveness
## Blockers
## Roadmap
## Signal evidence
EOF
)

out=$(run_validator "$READINESS" "readiness-report.md" "$READINESS_REPORT_OK")
expect "readiness-report: complete report validates" "$out" "validated successfully"

# Missing one section
out=$(run_validator "$READINESS" "readiness-report.md" "${READINESS_REPORT_OK/\#\# Blockers/}")
expect "readiness-report: missing Blockers is reported" "$out" "Blockers"
expect "readiness-report: missing section fails" "$out" "validation failed"

# Valid sections but no L0-L5 level
READINESS_BAD_LEVEL="${READINESS_REPORT_OK/L2/high autonomy}"
out=$(run_validator "$READINESS" "readiness-report.md" "$READINESS_BAD_LEVEL")
expect "readiness-report: invalid autonomy level fails" "$out" "L0-L5"

# Roadmap file
ROADMAP_OK=$(cat <<'EOF'
## Critical path (must-do for next level)
## High-impact improvements
EOF
)
out=$(run_validator "$READINESS" "readiness-roadmap.md" "$ROADMAP_OK")
expect "readiness-roadmap: complete roadmap validates" "$out" "validated successfully"

out=$(run_validator "$READINESS" "readiness-roadmap.md" "## High-impact improvements")
expect "readiness-roadmap: missing Critical path fails" "$out" "validation failed"

# Non-report file is ignored (no output)
out=$(run_validator "$READINESS" "notes.md" "## Whatever")
expect_absent "readiness: unrelated file is ignored" "$out" "validation"

# ---------------------------------------------------------------------------
# Verification validator
# ---------------------------------------------------------------------------
# Build a complete report body from the validator's own required-section list,
# so this stays correct as sections are added.
build_body() {
  local script="$1" fname="$2"
  sections_required_by "$script" "$fname" | while IFS= read -r s; do
    printf '## %s\n' "$s"
  done
}

for fname in verification-report.md verification-strategy.md ai-smells-gates-report.md; do
  body="$(build_body "$VERIFICATION" "$fname")"
  out=$(run_validator "$VERIFICATION" "$fname" "$body")
  expect "$fname: complete report validates" "$out" "validated successfully"

  # Drop the last required section and confirm it is reported as missing.
  last_section="$(sections_required_by "$VERIFICATION" "$fname" | tail -1)"
  partial="$(printf '%s\n' "$body" | grep -vF "## $last_section")"
  out=$(run_validator "$VERIFICATION" "$fname" "$partial")
  expect "$fname: missing '$last_section' is reported" "$out" "$last_section"
  expect "$fname: missing section fails" "$out" "validation failed"
done

out=$(run_validator "$VERIFICATION" "notes.md" "## Whatever")
expect_absent "verification: unrelated file is ignored" "$out" "validation"

# Regression guard for the specific section whose omission was the original bug.
body="$(build_body "$VERIFICATION" verification-report.md)"
expect "verification-report: validator requires Requirement Traceability" "$body" "## Requirement Traceability"

# ---------------------------------------------------------------------------
# Template-drift guard: every section a validator requires must exist as a
# heading in the matching template. This is what catches validator/template
# drift before it ships.
# ---------------------------------------------------------------------------
check_template_coverage() {
  local script="$1" fname="$2" template="$3"
  if [[ ! -f "$template" ]]; then
    FAIL=$((FAIL + 1))
    echo "FAIL: template not found for $fname: $template"
    return
  fi
  while IFS= read -r section; do
    [[ -z "$section" ]] && continue
    if grep -qF "## $section" "$template"; then
      PASS=$((PASS + 1))
    else
      FAIL=$((FAIL + 1))
      echo "FAIL: drift — '$fname' validator requires '## $section' but it is absent from $(basename "$template")"
    fi
  done < <(sections_required_by "$script" "$fname")
}

SV_REF="$REPO_ROOT/plugins/software-verification/skills"
check_template_coverage "$VERIFICATION" verification-report.md \
  "$SV_REF/assess-verification/references/report-template.md"
check_template_coverage "$VERIFICATION" verification-strategy.md \
  "$SV_REF/design-strategy/references/strategy-report-template.md"
check_template_coverage "$VERIFICATION" ai-smells-gates-report.md \
  "$SV_REF/detect-ai-smells/references/ai-smells-gates-report-template.md"

# Readiness report template lives in a reference; roadmap template is inline in
# the SKILL, so only the report is drift-checked here.
check_template_coverage "$READINESS" readiness-report.md \
  "$REPO_ROOT/plugins/codebase-ai-readiness/skills/assess-readiness/references/report-template.md"

# ---------------------------------------------------------------------------
# Reference path resolution (validate-references.py)
# ---------------------------------------------------------------------------
REF_OUT="$(python3 "$REPO_ROOT/tests/validators/test_validate_references.py")"
REF_EXIT=$?
printf '%s\n' "$REF_OUT"
while IFS= read -r line; do
  case "$line" in
    PASS*) PASS=$((PASS + 1)) ;;
    FAIL*) FAIL=$((FAIL + 1)) ;;
  esac
done <<< "$REF_OUT"
if [[ "$REF_EXIT" -ne 0 ]]; then
  : # failures already counted via FAIL lines
fi

# ---------------------------------------------------------------------------
echo
echo "Validator tests: $PASS passed, $FAIL failed"
[[ "$FAIL" -eq 0 ]]
