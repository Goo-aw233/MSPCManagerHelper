@echo off

echo Deleting .DS_Store Files...
for /r "%~dp0..\.." %%F in (.DS_Store) do (
    if exist "%%F" (
        echo Deleting "%%F"
        del /q /f "%%F"
    )
)

echo DONE
pause
exit
