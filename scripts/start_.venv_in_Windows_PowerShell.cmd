@echo off

echo Activating .venv in Windows PowerShell
cd "%~dp0.."
start powershell.exe -NoProfile -ExecutionPolicy Bypass -NoExit -Command "& { . .\.venv\Scripts\Activate.ps1 }"
