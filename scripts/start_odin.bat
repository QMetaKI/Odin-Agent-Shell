@echo off
REM ============================================================
REM  Odin Windows convenience helper — manual local start
REM  Candidate-only. Local-only. Windows convenience layer.
REM ============================================================
REM  NOT a service. NOT a tray app. NOT a signed installer.
REM  NOT target-host proof. NOT production readiness.
REM  Binds localhost only by default.
REM  App owns apply/state/external-send.
REM ============================================================
REM  Usage: Run from repo root, or double-click from repo root.
REM  Shortcut target: scripts\start_odin.bat
REM  Shortcut working directory: <repo root>
REM ============================================================

if "%ODIN_HOST%"=="" set ODIN_HOST=127.0.0.1
if "%ODIN_PORT%"=="" set ODIN_PORT=8877

python -m odin.cli start --portable --host %ODIN_HOST% --port %ODIN_PORT% %*
if %errorlevel% neq 0 (
    echo ERROR: Odin start returned errorlevel %errorlevel%
    exit /b %errorlevel%
)
