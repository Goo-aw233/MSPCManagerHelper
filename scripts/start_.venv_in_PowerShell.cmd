@echo off

echo Activating .venv in PowerShell
cd "%~dp0.."
start powershell.exe -NoExit -Command "& { . .\.venv\Scripts\Activate.ps1 }"
