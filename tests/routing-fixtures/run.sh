#!/usr/bin/env bash
# Validate verification routing fixtures: directory layout, profile presence,
# expected-routing.json schema conformance, and that every expected tool is a term the
# plugin references actually contain. This does NOT measure routing accuracy (manual eval).
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
FIXTURES_DIR="$REPO_ROOT/tests/routing-fixtures/fixtures"
REFS_DIR="$REPO_ROOT/plugins/software-verification/skills"
SCHEMA="$REPO_ROOT/schemas/routing-fixture.schema.json"
EVIDENCE_SCHEMA="$REPO_ROOT/schemas/verification-evidence.schema.json"
EVIDENCE_EXAMPLE="$FIXTURES_DIR/evidence-record.example.json"

PASS=0
FAIL=0

pass() { PASS=$((PASS + 1)); }
fail() {
  FAIL=$((FAIL + 1))
  echo "FAIL: $1"
}

EXPECTED_FIXTURES=(
  python-ledger
  python-parser
  rust-counter
  rust-distributed-service
  distributed-protocol
  c-to-rust-migration
  agentic-payment-agent
)

echo "=== Routing fixture validation ==="

for name in "${EXPECTED_FIXTURES[@]}"; do
  dir="$FIXTURES_DIR/$name"
  if [[ ! -d "$dir" ]]; then
    fail "missing fixture directory: $name"
    continue
  fi
  if [[ ! -f "$dir/profile.md" ]]; then
    fail "$name: missing profile.md"
  else
    pass
  fi
  if [[ ! -f "$dir/expected-routing.json" ]]; then
    fail "$name: missing expected-routing.json"
    continue
  fi
  if ! ajv validate -s "$SCHEMA" -d "$dir/expected-routing.json" --errors=text >/dev/null 2>&1; then
    fail "$name: expected-routing.json failed schema validation"
    ajv validate -s "$SCHEMA" -d "$dir/expected-routing.json" --errors=text 2>&1 | sed 's/^/  /'
  else
    pass
  fi
  fixture_id="$(python3 -c "import json; print(json.load(open('$dir/expected-routing.json'))['fixture'])")"
  # every expected tool must exist as a term in the plugin references (guards against catalog drift)
  while IFS= read -r tool; do
    if grep -rqiF -- "$tool" "$REFS_DIR"; then pass; else fail "$name: expected tool '$tool' not found in plugin references"; fi
  done < <(python3 -c "import json; [print(t) for t in json.load(open('$dir/expected-routing.json'))['expected_tools']]")
  if [[ "$fixture_id" != "$name" ]]; then
    fail "$name: fixture id '$fixture_id' does not match directory name"
  else
    pass
  fi
done

# Orphan fixture dirs (not in manifest)
for dir in "$FIXTURES_DIR"/*/; do
  base="$(basename "$dir")"
  [[ "$base" == "fixtures" ]] && continue
  found=0
  for name in "${EXPECTED_FIXTURES[@]}"; do
    [[ "$base" == "$name" ]] && found=1
  done
  if [[ "$found" -eq 0 && -f "$dir/expected-routing.json" ]]; then
    fail "orphan fixture directory not in manifest: $base"
  fi
done

if [[ -f "$EVIDENCE_EXAMPLE" ]]; then
  if ajv validate -s "$EVIDENCE_SCHEMA" -d "$EVIDENCE_EXAMPLE" --errors=text >/dev/null 2>&1; then
    pass
  else
    fail "evidence-record.example.json failed verification-evidence schema"
    ajv validate -s "$EVIDENCE_SCHEMA" -d "$EVIDENCE_EXAMPLE" --errors=text 2>&1 | sed 's/^/  /'
  fi
else
  fail "missing evidence-record.example.json"
fi

echo ""
echo "Routing fixture tests: $PASS passed, $FAIL failed"
[[ "$FAIL" -eq 0 ]]
