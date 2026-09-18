@echo off
setlocal

for /f "delims=" %%f in ('dir /s /b /a-d "%~dp0..\..\.DS_Store" 2^>nul') do (
    if not defined cleaned echo Deleting .DS_Store Files...
    echo Deleting "%%f"
    del /f /q "%%f" 2>nul
    set "cleaned=1"
)
if defined cleaned echo.

echo DONE
echo %cmdcmdline% | find.exe /i "%~nx0" >nul && if not defined CI pause
exit /b 0
