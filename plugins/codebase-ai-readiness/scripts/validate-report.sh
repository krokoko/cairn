#!/usr/bin/env bash
set -euo pipefail

# PostToolUse hook: validates structure of readiness-report.md and readiness-roadmap.md
# Receives JSON on stdin with tool_input.file_path
# Always exits 0 (hook framework requirement) -- communicates via JSON systemMessage

trap 'echo "{\"systemMessage\": \"WARNING: Report validation timed out.\"}"; exit 0' TERM

INPUT=$(cat)
PARSE_ERROR=""
FILE_PATH=$(echo "$INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('file_path',''))" 2>&1) || PARSE_ERROR="$FILE_PATH"

if [ -n "$PARSE_ERROR" ]; then
  # Escape quotes for JSON safety
  SAFE_ERR=$(echo "$PARSE_ERROR" | head -1 | tr '"' "'")
  echo "{\"systemMessage\": \"WARNING: validate-report.sh could not parse hook input: ${SAFE_ERR}. Validation skipped.\"}"
  exit 0
fi

FILENAME=$(basename "$FILE_PATH")

# Only validate known report files
if [[ "$FILENAME" != "readiness-report.md" ]] && [[ "$FILENAME" != "readiness-roadmap.md" ]]; then
  exit 0
fi

if [ ! -f "$FILE_PATH" ]; then
  exit 0
fi

ERRORS=""

if [[ "$FILENAME" == "readiness-report.md" ]]; then
  # Check required sections
  for section in "Overall Score" "Category Breakdown" "Recommended Autonomy Level" "Blockers" "Roadmap"; do
    if ! grep -q "## $section" "$FILE_PATH"; then
      ERRORS="${ERRORS}Missing required section: '## ${section}'. "
    fi
  done

  # Check that autonomy level is valid (L0-L5)
  if grep -q "## Recommended Autonomy Level" "$FILE_PATH"; then
    section_content=$(sed -n '/^## Recommended Autonomy Level/,/^## /p' "$FILE_PATH" | head -10)
    if ! echo "$section_content" | grep -qE '\bL[0-5]\b'; then
      ERRORS="${ERRORS}Autonomy level must be L0-L5. "
    fi
  fi
fi

if [[ "$FILENAME" == "readiness-roadmap.md" ]]; then
  for section in "Critical path" "High-impact improvements"; do
    if ! grep -qi "## $section" "$FILE_PATH"; then
      ERRORS="${ERRORS}Missing required section: '## ${section}'. "
    fi
  done
fi

if [ -n "$ERRORS" ]; then
  echo "{\"systemMessage\": \"Report validation failed: ${ERRORS}Please fix the report structure.\"}"
else
  echo "{\"systemMessage\": \"Report structure validated successfully.\"}"
fi

exit 0
