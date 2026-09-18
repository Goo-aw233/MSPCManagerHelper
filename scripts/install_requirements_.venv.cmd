@echo off
setlocal

set "venv=%~dp0..\.venv"
set "python=%venv%\Scripts\python.exe"

echo Creating .venv
py.exe -3.14 -m venv "%venv%" || exit /b 1
echo.

echo Upgrading pip
"%python%" -m pip install --upgrade pip || exit /b 1
echo.

echo Installing requirements.txt
"%python%" -m pip install -r "%~dp0..\requirements.txt" || exit /b 1
echo.

echo DONE
echo %cmdcmdline% | find.exe /i "%~nx0" >nul && if not defined CI pause
exit /b 0
