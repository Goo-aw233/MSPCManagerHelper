@echo off
cd %~dp0
pip.exe install -r requirements.txt
pip.exe install requests
python.exe -m pip install --upgrade pip
pause
exit
