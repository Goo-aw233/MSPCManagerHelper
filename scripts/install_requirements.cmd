@echo off

cd %~dp0

echo "Upgrading pip & Installing requirements.txt"
python.exe -m pip install --upgrade pip
pip.exe install -r "%~dp0..\requirements.txt"

pause
exit
