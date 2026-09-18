@echo off
setlocal

set "activate=%~dp0..\.venv\Scripts\Activate.ps1"

if not exist "%activate%" (
    echo .venv was not found. Run "scripts\install_requirements_.venv.cmd" first.
    echo %cmdcmdline% | find.exe /i "%~nx0" >nul && if not defined CI pause
    exit /b 1
)

echo Activating .venv in Windows PowerShell
cd /d "%~dp0.."
start "Launch Windows PowerShell in .venv" powershell.exe -NoProfile -ExecutionPolicy Bypass -NoExit -Command "& { . '%activate%' }"
