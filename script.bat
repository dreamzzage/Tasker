@echo off
echo Cleaning __pycache__ folders and .pyc files...
echo.

REM Delete all __pycache__ folders
for /d /r %%d in (__pycache__) do (
    echo Removing folder: "%%d"
    rmdir /s /q "%%d"
)

REM Delete all .pyc files
for /r %%f in (*.pyc) do (
    echo Deleting file: "%%f"
    del /f /q "%%f"
)

echo.
echo Done.
pause
