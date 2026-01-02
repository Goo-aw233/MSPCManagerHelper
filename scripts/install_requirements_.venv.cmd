@echo off
setlocal

cd %~dp0

echo "Creating .venv"
py.exe -3.14 -m venv "%~dp0..\.venv"

echo "Activating .venv"
call "%~dp0..\.venv\Scripts\activate.bat"

echo "Upgrading pip & Installing requirements.txt"
python.exe -m pip install --upgrade pip
pip.exe install -r "%~dp0..\requirements.txt"

pause
endlocal
exit
