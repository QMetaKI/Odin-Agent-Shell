@echo off
REM Portable local Odin runtime starter (Windows)
REM Not a service. Not a tray app. Not a signed installer.
REM Binds localhost only by default.
if "%ODIN_HOST%"=="" set ODIN_HOST=127.0.0.1
if "%ODIN_PORT%"=="" set ODIN_PORT=8877
python -m odin.cli start --portable --host %ODIN_HOST% --port %ODIN_PORT% %*
