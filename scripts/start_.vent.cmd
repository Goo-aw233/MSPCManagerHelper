@echo off
echo Activating .venv
cd "%~dp0.."
call "%~dp0..\.venv\Scripts\activate.bat"
cmd /k
