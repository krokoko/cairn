#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
python3 "$REPO_ROOT/tests/validators/test_report_contracts.py"
python3 "$REPO_ROOT/tests/validators/test_validate_references.py"
