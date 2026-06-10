$ErrorActionPreference = "Stop"
python -m odin.cli build-hub --out .odin_runtime\hub\index.html
Start-Process .odin_runtime\hub\index.html
