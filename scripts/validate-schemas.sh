#!/usr/bin/env bash
# Legacy entrypoint — prefer: mise run lint:manifests
set -euo pipefail
exec mise run lint:manifests
