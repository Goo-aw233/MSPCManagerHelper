@echo off
setlocal

for /f "tokens=2,*" %%a in ('reg query "HKEY_LOCAL_MACHINE\HARDWARE\DESCRIPTION\System\CentralProcessor\0" /v ProcessorNameString') do set "cpuName=%%b"
for /f "tokens=3" %%a in ('reg query "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v PROCESSOR_ARCHITECTURE') do set "arch=%%a"
for /f "tokens=2,*" %%a in ('reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion" /v BuildLabEx') do set "buildLabEx=%%b"
for /f "tokens=2,*" %%a in ('reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion" /v LCUVer') do set "lcuVer=%%b"
for /f "tokens=2,*" %%a in ('reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion" /v EditionID') do set "editionID=%%b"

echo Environment (.venv)
ver
echo %arch%
echo %cpuName%
echo %buildLabEx%
echo %lcuVer%
echo %editionID%
echo.
echo ####################
echo.

if "%arch%"=="AMD64" (
    "%~dp0..\..\.venv\Scripts\pyinstaller.exe" ^
        --onefile ^
        --windowed ^
        --name "MSPCManagerHelper_Beta_v0.3.1.0_x64" ^
        --add-data "%~dp0..\\..\\src\\assets\\locales;assets\\locales" ^
        --add-data "%~dp0..\\..\\src\\assets\\icons\\MSPCManagerHelper.ico;assets\\icons" ^
        --add-binary "%~dp0..\\..\\src\\assets\\tools\\ProcDump\\procdump64.exe;assets\\tools\\ProcDump" ^
        --add-binary "%~dp0..\\..\\src\\assets\\tools\\NSudo\\NSudoLC_x64.exe;assets\\tools\\NSudo" ^
        --clean ^
        --distpath "%~dp0..\\..\\dist" ^
        --icon "%~dp0..\\..\\src\\assets\\icons\\MSPCManagerHelper.ico" ^
        --version-file="%~dp0version_x64.txt" ^
        --workpath "%~dp0..\\..\\build" ^
        "%~dp0..\\..\\src\\main.py"
) else if "%arch%"=="ARM64" (
    "%~dp0..\..\.venv\Scripts\pyinstaller.exe" ^
        --onefile ^
        --windowed ^
        --name "MSPCManagerHelper_Beta_v0.3.1.0_ARM64" ^
        --add-data "%~dp0..\\..\\src\\assets\\locales;assets\\locales" ^
        --add-data "%~dp0..\\..\\src\\assets\\icons\\MSPCManagerHelper.ico;assets\\icons" ^
        --add-binary "%~dp0..\\..\\src\\assets\\tools\\ProcDump\\procdump64a.exe;assets\\tools\\ProcDump" ^
        --add-binary "%~dp0..\\..\\src\\assets\\tools\\NSudo\\NSudoLC_ARM64.exe;assets\\tools\\NSudo" ^
        --clean ^
        --distpath "%~dp0..\\..\\dist" ^
        --icon "%~dp0..\\..\\src\\assets\\icons\\MSPCManagerHelper.ico" ^
        --version-file="%~dp0version_ARM64.txt" ^
        --workpath "%~dp0..\\..\\build" ^
        "%~dp0..\\..\\src\\main.py"
) else (
    echo UNKNOWN: %arch%
)

pause
endlocal
