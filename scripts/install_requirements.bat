@echo off

cd %~dp0

pip.exe install -r "%~dp0..\requirements.txt"
pip.exe install requests
python.exe -m pip install --upgrade pip

pause
exit
