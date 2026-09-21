@echo off
setlocal

set "cleaned="
for %%r in ("src" "scripts") do (
    for /f "delims=" %%d in ('dir /s /b /ad "%~dp0..\..\%%~r\__pycache__" 2^>nul') do (
        echo Deleting "%%d"
        rd /s /q "%%d" 2>nul
        set "cleaned=1"
    )
)
if defined cleaned echo.

set "cleaned="
for %%d in ("build" "dist") do (
    if exist "%~dp0..\..\%%~d" (
        echo Deleting "%~dp0..\..\%%~d"
        rd /s /q "%~dp0..\..\%%~d" 2>nul
        set "cleaned=1"
    )
)
if defined cleaned echo.

set "cleaned="
for %%f in (
    "%~dp0version_*.txt"
    "%~dp0*.spec"
    "%~dp0MSPCManagerHelper.manifest.rc"
    "%~dp0MSPCManagerHelper.manifest.res"
    "%~dp0MSPCManagerHelper.version.rc"
    "%~dp0MSPCManagerHelper.version.res"
) do (
    if exist "%%~f" (
        echo Deleting "%%~f"
        del /f /q "%%~f" 2>nul
        set "cleaned=1"
    )
)
if defined cleaned echo.

echo DONE
echo %cmdcmdline% | find.exe /i "%~nx0" >nul && pause
exit /b 0
