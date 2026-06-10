@echo off
REM Stop the portable local Odin runtime (Windows)
python -m odin.cli stop --portable %*
