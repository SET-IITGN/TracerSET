@echo off
setlocal enabledelayedexpansion
set PYTHONUTF8=1

:: Usage:
::   make.cmd test    - Run pytest with -sv
::   make.cmd clean   - Remove cache and temp files
::   make.cmd all     - Run clean then test

if "%~1"=="" goto usage
if "%~1"=="test" goto test
if "%~1"=="clean" goto clean
if "%~1"=="all" goto all

:usage
echo Usage: make.cmd ^(test^|clean^|all^)
exit /b 1

:test
echo Running tests...
python3 -m pytest -sv
exit /b %ERRORLEVEL%

:clean
echo Cleaning up...

:: Remove all __pycache__ directories
for /d /r . %%d in (__pycache__) do (
    if exist "%%d" rd /s /q "%%d"
)

:: Remove matching files: .tmp, .svg, .dot, .cov*, .htm*, .gv
del /f /q *.tmp 2>nul
del /f /q *.svg 2>nul
del /f /q *.dot 2>nul
del /f /q *.gv 2>nul
del /f /q *.cov* 2>nul
del /f /q *.htm 2>nul
del /f /q *.html 2>nul
del /f /q *.png 2>nul

:: Also search subdirectories for temp files
for /r . %%f in (*.tmp *.svg *.dot *.gv *.cov* *.htm *.html *.png) do (
    if exist "%%f" del /f /q "%%f"
)

echo Cleanup complete.
exit /b 0

:all
call :clean
echo.
call :test
exit /b %ERRORLEVEL%

:end