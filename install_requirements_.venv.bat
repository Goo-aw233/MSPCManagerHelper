@echo off
setlocal

cd %~dp0
echo ".venv"
python.exe -m venv .venv
echo "activate"
call .venv\Scripts\activate

echo "install & upgrade pip"
pip.exe install -r requirements.txt
pip.exe install requests
python.exe -m pip install --upgrade pip

pause
endlocal
exit
