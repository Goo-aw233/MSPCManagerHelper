@echo off
setlocal EnableDelayedExpansion

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

for /f "tokens=3" %%a in ('reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion" /v CurrentMajorVersionNumber 2^>nul') do set "maj=%%a"
for /f "tokens=3" %%a in ('reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion" /v CurrentMinorVersionNumber 2^>nul') do set "min=%%a"
for /f "tokens=3" %%a in ('reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion" /v CurrentBuildNumber 2^>nul') do set "buildNum=%%a"
for /f "tokens=3" %%a in ('reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion" /v UBR 2^>nul') do set "ubr=%%a"

REM Convert Hexadecimal or Decimal Strings to Decimal (If Conversion Fails, Retain Original String)
if defined maj (
    set /a maj=!maj! 2>nul
)
if defined min (
    set /a min=!min! 2>nul
)
if defined buildNum (
    set /a buildNum=!buildNum! 2>nul
)
if defined ubr (
    set /a ubr=!ubr! 2>nul
) else (
    set "ubr=0"
)

if defined maj if defined min if defined buildNum (
    set "lcuVer=!maj!.!min!.!buildNum!.!ubr!"
    echo !lcuVer!
) else (
    echo (UNKNOWN LCUVer)
)

echo %editionID%
echo.
echo ####################
echo.

if "%arch%"=="AMD64" (
    "%~dp0..\..\.venv\Scripts\python.exe" -m nuitka ^
        --onefile ^
        --windows-console-mode=disable ^
        --output-dir="%~dp0..\..\dist" ^
        --output-filename="MSPCManagerHelper_Beta_v0.3.1.0_x64.exe" ^
        --include-data-dir="%~dp0..\..\src\assets\locales=assets\locales" ^
        --include-data-files="%~dp0..\..\src\assets\icons\MSPCManagerHelper.ico=assets\icons\MSPCManagerHelper.ico" ^
        --include-data-files="%~dp0..\..\src\assets\tools\ProcDump\procdump64.exe=assets\tools\ProcDump\procdump64.exe" ^
        --include-data-files="%~dp0..\..\src\assets\tools\NSudo\NSudoLC_x64.exe=assets\tools\NSudo\NSudoLC_x64.exe" ^
        --include-module=winrt.windows.foundation ^
        --include-module=winrt.windows.foundation.collections ^
        --include-windows-runtime-dlls=yes ^
        --enable-plugin=tk-inter ^
        --windows-icon-from-ico="%~dp0..\..\src\assets\icons\MSPCManagerHelper.ico" ^
        --file-version=0.3.1.0 ^
        --product-version=0.3.1.0 ^
        --file-description="MSPCManagerHelper" ^
        --product-name="MSPCManagerHelper" ^
        --company-name="GuCATs" ^
        --copyright="© 2024 - 2026 GuCATs All rights reserved." ^
        --main="%~dp0..\..\src\main.py"
) else if "%arch%"=="ARM64" (
    "%~dp0..\..\.venv\Scripts\python.exe" -m nuitka ^
        --onefile ^
        --windows-console-mode=disable ^
        --output-dir="%~dp0..\..\dist" ^
        --output-filename="MSPCManagerHelper_Beta_v0.3.1.0_ARM64.exe" ^
        --include-data-dir="%~dp0..\..\src\assets\locales=assets\locales" ^
        --include-data-files="%~dp0..\..\src\assets\icons\MSPCManagerHelper.ico=assets\icons\MSPCManagerHelper.ico" ^
        --include-data-files="%~dp0..\..\src\assets\tools\ProcDump\procdump64.exe=assets\tools\ProcDump\procdump64.exe" ^
        --include-data-files="%~dp0..\..\src\assets\tools\NSudo\NSudoLC_ARM64.exe=assets\tools\NSudo\NSudoLC_ARM64.exe" ^
        --include-module=winrt.windows.foundation ^
        --include-module=winrt.windows.foundation.collections ^
        --include-windows-runtime-dlls=yes ^
        --enable-plugin=tk-inter ^
        --windows-icon-from-ico="%~dp0..\..\src\assets\icons\MSPCManagerHelper.ico" ^
        --file-version=0.3.1.0 ^
        --product-version=0.3.1.0 ^
        --file-description="MSPCManagerHelper" ^
        --product-name="MSPCManagerHelper" ^
        --company-name="GuCATs" ^
        --copyright="© 2024 - 2026 GuCATs All rights reserved." ^
        --main="%~dp0..\..\src\main.py"
) else (
    echo UNKNOWN: %arch%
)

pause
endlocal
