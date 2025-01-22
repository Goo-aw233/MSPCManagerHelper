@echo off
setlocal

for /f "tokens=3" %%a in ('reg query "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v PROCESSOR_ARCHITECTURE') do set arch=%%a

echo %arch%
echo.

if "%arch%"=="AMD64" (
    pyinstaller.exe ^
        --onefile ^
        --windowed ^
        --name "MSPCManagerHelper_Beta_v0.2.0.10_x64" ^
        --add-data "locales;locales" ^
        --add-data "assets\\MSPCManagerHelper-256.ico;assets" ^
        --add-binary "tools\\procdump\\procdump64.exe;tools/procdump" ^
        --add-binary "tools\\NSudo\\NSudoLC_x64.exe;tools/NSudo" ^
        --clean ^
        --version-file="%~dp0\version_x64.txt" ^
        -i "assets\\MSPCManagerHelper-48.ico" ^
        "%~dp0\mainWindow.py"
) else if "%arch%"=="ARM64" (
    pyinstaller.exe ^
        --onefile ^
        --windowed ^
        --name "MSPCManagerHelper_Beta_v0.2.0.10_ARM64" ^
        --add-data "locales;locales" ^
        --add-data "assets\\MSPCManagerHelper-256.ico;assets" ^
        --add-binary "tools\\procdump\\procdump64a.exe;tools/procdump" ^
        --add-binary "tools\\NSudo\\NSudoLC_ARM64.exe;tools/NSudo" ^
        --clean ^
        --version-file="%~dp0\version_ARM64.txt" ^
        -i "assets\\MSPCManagerHelper-48.ico" ^
        "%~dp0\mainWindow.py"
) else (
    echo UNKNOWN: %arch%
)

pause
endlocal
