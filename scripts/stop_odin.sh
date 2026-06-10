#!/usr/bin/env bash
# Stop the portable local Odin runtime (POSIX)
set -euo pipefail
python -m odin.cli stop --portable "$@"
