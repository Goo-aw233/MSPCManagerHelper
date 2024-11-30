@echo off
setlocal

for /f "tokens=3" %%a in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v PROCESSOR_ARCHITECTURE') do set arch=%%a

echo %arch%
echo.

if "%arch%"=="AMD64" (
    pyinstaller.exe --onefile --windowed --name "MSPCManagerHelper_Beta_v0.2.0.4_x64" --add-data "locales;locales" --add-data "assets\\MSPCManagerHelper-256.ico;assets" --add-binary "tools\\procdump\\procdump64.exe;tools/procdump" --clean --version-file=version_x64.txt -i "assets\\MSPCManagerHelper-48.ico" mainWindow.py
) else if "%arch%"=="ARM64" (
    pyinstaller.exe --onefile --windowed --name "MSPCManagerHelper_Beta_v0.2.0.4_ARM64" --add-data "locales;locales" --add-data "assets\\MSPCManagerHelper-256.ico;assets" --add-binary "tools\\procdump\\procdump64a.exe;tools/procdump" --clean --version-file=version_ARM64.txt -i "assets\\MSPCManagerHelper-48.ico" mainWindow.py
) else (
    echo UNKNOWN: %arch%
)

pause
endlocal
