@echo off
setlocal

for /f "tokens=3" %%a in ('reg query "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v PROCESSOR_ARCHITECTURE') do set arch=%%a

echo %arch%
echo.

if "%arch%"=="AMD64" (
    pyinstaller.exe ^
        --onefile ^
        --windowed ^
        --name "MSPCManagerHelper_Beta_v0.2.0.15_x64" ^
        --add-data "%~dp0..\\..\\src\\locales;locales" ^
        --add-data "%~dp0..\\..\\src\\assets\\MSPCManagerHelper.ico;assets" ^
        --add-binary "%~dp0..\\..\\src\\tools\\ProcDump\\procdump64.exe;tools\\ProcDump" ^
        --add-binary "%~dp0..\\..\\src\\tools\\NSudo\\NSudoLC_x64.exe;tools\\NSudo" ^
        --clean ^
        --distpath "%~dp0..\\..\\dist" ^
        --workpath "%~dp0..\\..\\build" ^
        --version-file="%~dp0version_x64.txt" ^
        --icon "%~dp0..\\..\\src\\assets\\MSPCManagerHelper.ico" ^
        "%~dp0..\\..\\src\\mainWindow.py"
) else if "%arch%"=="ARM64" (
    pyinstaller.exe ^
        --onefile ^
        --windowed ^
        --name "MSPCManagerHelper_Beta_v0.2.0.15_ARM64" ^
        --add-data "%~dp0..\\..\\src\\locales;locales" ^
        --add-data "%~dp0..\\..\\src\\assets\\MSPCManagerHelper.ico;assets" ^
        --add-binary "%~dp0..\\..\\src\\tools\\ProcDump\\procdump64a.exe;tools\\ProcDump" ^
        --add-binary "%~dp0..\\..\\src\\tools\\NSudo\\NSudoLC_ARM64.exe;tools\\NSudo" ^
        --clean ^
        --distpath "%~dp0..\\..\\dist" ^
        --workpath "%~dp0..\\..\\build" ^
        --version-file="%~dp0version_ARM64.txt" ^
        --icon "%~dp0..\\..\\src\\assets\\MSPCManagerHelper.ico" ^
        "%~dp0..\\..\\src\\mainWindow.py"
) else (
    echo UNKNOWN: %arch%
)

pause
endlocal
