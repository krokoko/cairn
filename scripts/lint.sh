#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
EXIT_CODE=0

echo "=== Linting autonomy-rails ==="

# Prerequisite check
if ! command -v python3 &>/dev/null; then
  echo "FAIL: python3 is required but not found on PATH"
  exit 1
fi

# 1. Check all JSON files are valid
echo ""
echo "--- Checking JSON validity ---"
while IFS= read -r -d '' f; do
  error_output=$(python3 -m json.tool "$f" 2>&1 >/dev/null) || {
    echo "FAIL: Invalid JSON: $f"
    echo "      $error_output"
    EXIT_CODE=1
  }
done < <(find "$REPO_ROOT" -name '*.json' -not -path '*/.git/*' -not -path '*/node_modules/*' -print0)
echo "JSON validity check complete."

# 2. Check plugin names are kebab-case
echo ""
echo "--- Checking plugin names ---"
while IFS= read -r -d '' manifest; do
  name=$(python3 -c "
import json, sys
try:
    d = json.load(open(sys.argv[1]))
    if 'name' not in d:
        print('ERROR_MISSING_NAME', file=sys.stderr)
        sys.exit(1)
    print(d['name'])
except Exception as e:
    print(f'ERROR: {e}', file=sys.stderr)
    sys.exit(1)
" "$manifest" 2>&1) || {
    echo "FAIL: Could not extract 'name' from $manifest: $name"
    EXIT_CODE=1
    continue
  }
  if ! echo "$name" | grep -qE '^[a-z][a-z0-9-]*$'; then
    echo "FAIL: Plugin name '$name' is not kebab-case in $manifest"
    EXIT_CODE=1
  fi
done < <(find "$REPO_ROOT/plugins" -path '*/.claude-plugin/plugin.json' -print0)
echo "Plugin name check complete."

# 3. Check SKILL.md files are under 300 lines
echo ""
echo "--- Checking SKILL.md line limits ---"
while IFS= read -r -d '' skill; do
  lines=$(wc -l < "$skill")
  if [ "$lines" -gt 300 ]; then
    echo "FAIL: $skill has $lines lines (max 300)"
    EXIT_CODE=1
  fi
done < <(find "$REPO_ROOT/plugins" -name 'SKILL.md' -print0)
echo "SKILL.md line limit check complete."

# 4. Check reference docs are under 100 lines
echo ""
echo "--- Checking reference doc line limits ---"
while IFS= read -r -d '' ref; do
  lines=$(wc -l < "$ref")
  if [ "$lines" -gt 100 ]; then
    echo "FAIL: $ref has $lines lines (max 100)"
    EXIT_CODE=1
  fi
done < <(find "$REPO_ROOT/plugins" -path '*/references/*.md' -print0)
echo "Reference doc line limit check complete."

# 5. Check SKILL.md files have YAML frontmatter
echo ""
echo "--- Checking SKILL.md frontmatter ---"
while IFS= read -r -d '' skill; do
  if ! head -1 "$skill" | grep -q '^---$'; then
    echo "FAIL: $skill missing YAML frontmatter"
    EXIT_CODE=1
  fi
done < <(find "$REPO_ROOT/plugins" -name 'SKILL.md' -print0)
echo "Frontmatter check complete."

# 6. Check marketplace entries match plugin directories
echo ""
echo "--- Checking marketplace consistency ---"
MARKETPLACE="$REPO_ROOT/.claude-plugin/marketplace.json"
if [ -f "$MARKETPLACE" ]; then
  plugin_paths_output=""
  plugin_paths_output=$(python3 -c "
import json, sys
data = json.load(open(sys.argv[1]))
for p in data.get('plugins', []):
    print(p['path'])
" "$MARKETPLACE" 2>&1) || {
    echo "FAIL: Could not parse marketplace.json: $plugin_paths_output"
    EXIT_CODE=1
    plugin_paths_output=""
  }
  while IFS= read -r path; do
    [ -z "$path" ] && continue
    if [ ! -d "$REPO_ROOT/$path" ]; then
      echo "FAIL: Marketplace references '$path' but directory does not exist"
      EXIT_CODE=1
    fi
    if [ ! -f "$REPO_ROOT/$path/.claude-plugin/plugin.json" ]; then
      echo "FAIL: Marketplace references '$path' but no plugin.json found"
      EXIT_CODE=1
    fi
  done <<< "$plugin_paths_output"
else
  echo "WARN: No marketplace.json found at $MARKETPLACE (skipped)"
fi
echo "Marketplace consistency check complete."

echo ""
if [ "$EXIT_CODE" -eq 0 ]; then
  echo "=== All lint checks passed ==="
else
  echo "=== Lint checks FAILED ==="
fi
exit $EXIT_CODE
