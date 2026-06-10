param([int]$Port = 8765)
$ErrorActionPreference = "Stop"
Write-Host "Starting Odin local API candidate on 127.0.0.1:$Port"
python -m odin.cli serve --host 127.0.0.1 --port $Port
