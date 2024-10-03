@echo off
python -m venv .venv
.venv\Scripts\activate
pip.exe install -r requirements.txt
pip.exe install requests
python.exe -m pip install --upgrade pip
pause
