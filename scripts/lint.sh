#!/usr/bin/env bash
# Legacy entrypoint — prefer: mise run lint
set -euo pipefail
exec mise run lint
