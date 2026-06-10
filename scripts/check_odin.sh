#!/usr/bin/env bash
# Check the portable local Odin runtime health (POSIX)
set -euo pipefail
python -m odin.cli check --portable --host "${ODIN_HOST:-127.0.0.1}" --port "${ODIN_PORT:-8877}" "$@"
