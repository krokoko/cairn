#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
EXIT_CODE=0

echo "=== Validating JSON schemas ==="

# Determine which validation tool is available
USE_PYTHON=0
if command -v check-jsonschema &>/dev/null; then
  USE_PYTHON=0
elif python3 -c "import jsonschema" 2>/dev/null; then
  echo "INFO: check-jsonschema not found, using python3 jsonschema"
  USE_PYTHON=1
else
  echo "FAIL: No schema validation tool available."
  echo "      Install one of: check-jsonschema (npm), jsonschema (pip install jsonschema)"
  exit 1
fi

validate() {
  local schema="$1"
  local instance="$2"

  if [ ! -f "$schema" ]; then
    echo "FAIL: Schema file not found: $schema"
    EXIT_CODE=1
    return
  fi
  if [ ! -f "$instance" ]; then
    echo "FAIL: Instance file not found: $instance"
    EXIT_CODE=1
    return
  fi

  if [ "$USE_PYTHON" -eq 1 ]; then
    local output
    output=$(python3 -c "
import json, sys
from jsonschema import validate, ValidationError
schema = json.load(open(sys.argv[1]))
instance = json.load(open(sys.argv[2]))
validate(instance=instance, schema=schema)
" "$schema" "$instance" 2>&1) || {
      echo "FAIL: $instance"
      echo "      $output"
      EXIT_CODE=1
      return
    }
  else
    local output
    output=$(check-jsonschema --schemafile "$schema" "$instance" 2>&1) || {
      echo "FAIL: $instance"
      echo "      $output"
      EXIT_CODE=1
      return
    }
  fi
}

# 1. Validate marketplace.json
echo ""
echo "--- Validating marketplace.json ---"
MARKETPLACE="$REPO_ROOT/.claude-plugin/marketplace.json"
if [ -f "$MARKETPLACE" ]; then
  validate "$REPO_ROOT/schemas/marketplace.schema.json" "$MARKETPLACE"
  echo "Marketplace validation complete."
else
  echo "WARN: No marketplace.json found"
fi

# 2. Validate all plugin.json manifests
echo ""
echo "--- Validating plugin.json manifests ---"
while IFS= read -r -d '' manifest; do
  echo "Validating: $manifest"
  validate "$REPO_ROOT/schemas/plugin.schema.json" "$manifest"
done < <(find "$REPO_ROOT/plugins" -path '*/.claude-plugin/plugin.json' -print0 2>/dev/null)
echo "Plugin manifest validation complete."

echo ""
if [ "$EXIT_CODE" -eq 0 ]; then
  echo "=== All schema validations passed ==="
else
  echo "=== Schema validations FAILED ==="
fi
exit $EXIT_CODE
