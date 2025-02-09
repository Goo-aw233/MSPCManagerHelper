@echo off
setlocal

cd %~dp0

echo "Creating .venv"
python.exe -m venv "%~dp0..\.venv"

echo "Activating .venv"
call "%~dp0..\.venv\Scripts\activate.bat"

echo "Installing requirements.txt & Upgrading pip"
pip.exe install -r "%~dp0..\requirements.txt"
pip.exe install requests
python.exe -m pip install --upgrade pip

pause
endlocal
exit
