#!/usr/bin/env bash
set -euo pipefail

# PostToolUse hook: validates structure of verification-report.md or verification-strategy.md
# Receives JSON on stdin with tool_input.file_path
# Always exits 0 (hook framework requirement) -- communicates via JSON systemMessage

trap 'echo "{\"systemMessage\": \"WARNING: Report validation timed out.\"}"; exit 0' TERM

INPUT=$(cat)
PARSE_ERROR=""
FILE_PATH=$(echo "$INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('file_path',''))" 2>&1) || PARSE_ERROR="$FILE_PATH"

if [ -n "$PARSE_ERROR" ]; then
  SAFE_ERR=$(echo "$PARSE_ERROR" | head -1 | tr '"' "'")
  echo "{\"systemMessage\": \"WARNING: validate-verification-report.sh could not parse hook input: ${SAFE_ERR}. Validation skipped.\"}"
  exit 0
fi

FILENAME=$(basename "$FILE_PATH")

# Only validate known report files
if [[ "$FILENAME" != "verification-report.md" ]] && [[ "$FILENAME" != "verification-strategy.md" ]]; then
  exit 0
fi

if [ ! -f "$FILE_PATH" ]; then
  exit 0
fi

ERRORS=""

# Check for verification-report.md sections
if [[ "$FILENAME" == "verification-report.md" ]]; then
  for section in "Verification Maturity" "Component Breakdown" "Missing Oracles" "Exactness Analysis" "Human Review Requirements" "Autonomy Candidates"; do
    if ! grep -q "## $section" "$FILE_PATH"; then
      ERRORS="${ERRORS}Missing required section: '## ${section}'. "
    fi
  done
fi

# Check for verification-strategy.md sections
if [[ "$FILENAME" == "verification-strategy.md" ]]; then
  for section in "Component Strategies" "Oracle Strategy" "Evidence Pipeline" "Implementation Roadmap"; do
    if ! grep -q "## $section" "$FILE_PATH"; then
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
