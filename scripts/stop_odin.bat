@echo off
REM ============================================================
REM  Odin Windows convenience helper — manual local stop
REM  Candidate-only. Local-only. Windows convenience layer.
REM ============================================================
REM  NOT a service. NOT a tray app. NOT a signed installer.
REM  NOT target-host proof. NOT production readiness.
REM  App owns apply/state/external-send.
REM ============================================================
REM  Usage: Run from repo root, or double-click from repo root.
REM  Shortcut target: scripts\stop_odin.bat
REM  Shortcut working directory: <repo root>
REM ============================================================

python -m odin.cli stop --portable %*
if %errorlevel% neq 0 (
    echo ERROR: Odin stop returned errorlevel %errorlevel%
    exit /b %errorlevel%
)
