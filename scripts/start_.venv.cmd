@echo off
setlocal

set "activate=%~dp0..\.venv\Scripts\activate.bat"

if not exist "%activate%" (
    echo .venv was not found. Run "scripts\install_requirements_.venv.cmd" first.
    echo %cmdcmdline% | find.exe /i "%~nx0" >nul && if not defined CI pause
    exit /b 1
)

echo Activating .venv
cd /d "%~dp0.."
call "%activate%"

if defined CI exit /b 0
cmd.exe /k
