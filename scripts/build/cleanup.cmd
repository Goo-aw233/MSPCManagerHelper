@echo off

if exist "%~dp0..\..\src\__pycache__" (
    echo del __pycache__
    rmdir /s /q "%~dp0..\..\src\__pycache__"
)

if exist "%~dp0..\..\build" (
    echo del build
    rmdir /s /q "%~dp0..\..\build"
)

if exist "%~dp0..\..\dist" (
    echo del dist
    rmdir /s /q "%~dp0..\..\dist"
)

for %%f in (*.spec) do (
    echo del %%f
    del /f /q "%~dp0%%f"
)

echo DONE
pause
exit
