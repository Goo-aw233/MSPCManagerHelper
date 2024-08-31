@echo off
pyinstaller --onefile --windowed --name "MSPCManagerHelper_Preview_v24831_-_we11B" --add-data "locales;locales" MainWindow.py
pause
