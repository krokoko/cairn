#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
EXIT_CODE=0

echo "--- Checking JSON validity ---"
while IFS= read -r -d '' file; do
  if ! python3 -m json.tool "$file" >/dev/null 2>&1; then
    echo "FAIL: Invalid JSON: $file"
    EXIT_CODE=1
  fi
done < <(find "$REPO_ROOT" -name '*.json' -not -path '*/.git/*' -not -path '*/node_modules/*' -print0)

if [ "$EXIT_CODE" -eq 0 ]; then
  echo "JSON validity check complete."
fi
exit "$EXIT_CODE"
