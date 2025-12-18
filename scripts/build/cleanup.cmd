@echo off

for /d /r "%~dp0..\..\src" %%d in (__pycache__) do (
    if exist "%%d" (
        echo Deleting %%d
        rmdir /s /q "%%d"
    )
)

if exist "%~dp0..\..\build" (
    echo Deleting build
    rmdir /s /q "%~dp0..\..\build"
)

if exist "%~dp0..\..\dist" (
    echo Deleting dist
    rmdir /s /q "%~dp0..\..\dist"
)

for %%f in (*.spec) do (
    echo Deleting %%f
    del /f /q "%~dp0%%f"
)

echo DONE
pause
exit
