@echo off
setlocal EnableDelayedExpansion

for %%p in ("%~dp0..\..\.venv\Scripts\python.exe") do set "venv=%%~fp"

set "arguments=%*"

:options
if not defined arguments goto :interactive
set "padded= !arguments! "
if not "!padded: /? =!"=="!padded!" set "help=1"
if not "!padded: /h =!"=="!padded!" set "help=1"
if not "!padded: /help =!"=="!padded!" set "help=1"
if /i not "%~1"=="/python" goto :trim_spaces
set "remainder=!arguments:*%~1=!"
if not defined remainder goto :trim_spaces
if not "!remainder:~0,1!"=="=" goto :trim_spaces
set "python_given=1"
set "python=%~2"
set "arguments=!remainder:~1!"
if defined arguments set "arguments=!arguments:"=!"
if defined arguments if defined python set "arguments=!arguments:*%python%=!"

:trim_spaces
if not defined arguments goto :interactive
if not "!arguments:~0,1!"==" " goto :interactive
set "arguments=!arguments:~1!"
goto :trim_spaces

:interactive
if not defined arguments if not defined CI set "interactive=1"

if defined arguments goto :resolve_python
if not defined interactive goto :resolve_python

echo No build parameters provided, switching to interactive mode.
echo Use build.cmd /? to open the script help.
echo.
if defined python_given goto :resolve_python

echo Python Interpreter [.venv ^| ^<Path to python.exe^> ^| ^<empty^>]:
echo   .venv                 = %venv%
echo   ^<empty^> (No Input)    = python.exe from PATH
set "python="
set /p "python=Python Path: "

:resolve_python
if not defined python set "python=python.exe"
set "python=%python:"=%"
if /i "%python%"==".venv" set "python=%venv%"

:check
"%python%" --version >nul 2>&1 || (
    echo Python Not Found: %python%
    echo Run "scripts\install_requirements_.venv.cmd" first, or choose another interpreter.
    set "code=1"
    goto :done
)

if defined help goto :help
if not defined interactive goto :build

set /p "builder=Builder [nuitka | pyinstaller]: "
set "arguments=/builder=%builder%"

if /i "%builder%"=="pyinstaller" set "types=onedir | onefile"
if /i "%builder%"=="nuitka" set "types=onefile | standalone"
if not defined types goto :build

set /p "type=Type [%types%]: "
set "arguments=%arguments% /type=%type%"

:build
"%python%" "%~dp0build.py" %arguments%
set "code=%errorlevel%"

:done
if defined interactive pause
exit /b %code%

:help
"%python%" "%~dp0build.py" /?
set "code=%errorlevel%"
echo.
echo Exclusive parameters for build.cmd:
echo   /python=[.venv ^| ^<Path to python.exe^> ^| ^<empty^>]
echo     Interpreter used to run build.py, only recognized as the first argument.
echo     Empty or omitted uses python.exe from PATH.
goto :done
