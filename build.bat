@echo off
title Building Tasker with PyInstaller...
echo -----------------------------------------
echo   TASKER BUILD SCRIPT (PyInstaller)
echo -----------------------------------------

REM Move to script directory
cd /d "%~dp0"

REM Clean previous builds
echo Cleaning old build folders...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__

echo.
echo Building executable...

REM Build with PyInstaller
pyinstaller ^
    --noconfirm ^
    --clean ^
    --windowed ^
    --icon=icon.ico ^
    --add-data "pomodoro.py;." ^
    --add-data "habit_tracker.py;." ^
    --add-data "deadline_utils.py;." ^
    --add-data "icon.ico;." ^
    main.py

echo.
echo -----------------------------------------
echo   BUILD COMPLETE
echo   Output folder: dist\main
echo -----------------------------------------

pause