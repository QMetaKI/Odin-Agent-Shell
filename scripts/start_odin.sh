#!/usr/bin/env bash
# Portable local Odin runtime starter (POSIX)
# Not a service. Not a tray app. Not a signed installer.
# Binds localhost only by default.
set -euo pipefail
python -m odin.cli start --portable --host "${ODIN_HOST:-127.0.0.1}" --port "${ODIN_PORT:-8877}" "$@"
