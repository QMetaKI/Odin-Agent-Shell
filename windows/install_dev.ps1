param([switch]$NoVenv)
$ErrorActionPreference = "Stop"
Write-Host "Odin dev install candidate. No installer/code-signing proof claimed."
if (-not $NoVenv) {
  if (-not (Test-Path ".venv")) { py -3 -m venv .venv }
  . .\.venv\Scripts\Activate.ps1
}
python -m pip install --upgrade pip
python -m pip install -e .
python -m odin.cli validate-all
