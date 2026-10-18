@echo off
title Minnesota Permit Test Practice
cd /d "%~dp0"

echo Checking for PyQt6...
python -c "import PyQt6" 2>nul
if errorlevel 1 (
    echo PyQt6 not found. Installing...
    python -m pip install PyQt6
    if errorlevel 1 (
        echo.
        echo ERROR: Could not install PyQt6. Make sure Python is installed.
        pause
        exit /b 1
    )
)

echo Starting Minnesota Permit Test Practice...
python minnesota_permit_test.py
if errorlevel 1 pause
