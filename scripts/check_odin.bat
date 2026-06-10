@echo off
REM Check the portable local Odin runtime health (Windows)
if "%ODIN_HOST%"=="" set ODIN_HOST=127.0.0.1
if "%ODIN_PORT%"=="" set ODIN_PORT=8877
python -m odin.cli check --portable --host %ODIN_HOST% --port %ODIN_PORT% %*
