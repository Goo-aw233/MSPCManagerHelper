@echo off

if exist "__pycache__" (
    echo del __pycache__
    rmdir /s /q "%~dp0\__pycache__"
)

if exist "build" (
    echo del build
    rmdir /s /q "%~dp0\build"
)

if exist "dist" (
    echo del dist
    rmdir /s /q "%~dp0\dist"
)

for %%f in (*.spec) do (
    echo del %%f
    del /f /q "%~dp0\%%f"
)

echo DONE
pause
exit
