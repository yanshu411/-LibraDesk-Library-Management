@echo off
cd /d "%~dp0"
python "library_management_system.py"
if errorlevel 1 pause
