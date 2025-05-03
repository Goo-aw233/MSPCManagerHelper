@echo off

cd %~dp0

python.exe -m pip install --upgrade pip
pip.exe install -r "%~dp0..\requirements.txt"
pip.exe install requests

pause
exit
