#!/usr/bin/env bash
set -euo pipefail

# PostToolUse feedback is advisory. Use check-report.py --check FILE for CI.
trap 'echo "{\"systemMessage\":\"WARNING: Report validation timed out.\"}"; exit 0' TERM
if ! command -v python3 >/dev/null 2>&1; then
  echo '{"systemMessage":"WARNING: Python 3 is unavailable; report validation did not run."}'
  exit 0
fi
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SCRIPT_DIR/check-report.py" || {
  echo '{"systemMessage":"WARNING: Report validator could not complete."}'
}
exit 0
