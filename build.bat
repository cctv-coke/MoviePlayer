@echo off
title MoviePlayer Build Tool
echo.
echo ========================================
echo    MoviePlayer - Build Tool
echo ========================================
echo.

echo [1/4] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.10+
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)
python --version
echo OK: Python installed
echo.

echo [2/4] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo OK: Dependencies installed
echo.

echo [3/4] Installing PyInstaller...
pip install pyinstaller
echo OK: PyInstaller installed
echo.

echo [4/4] Building EXE...
echo    Please wait, this may take a few minutes...
echo.

pyinstaller --name="MoviePlayer" --onefile --windowed --add-data "core;core" --add-data "ui;ui" --add-data "utils;utils" --hidden-import PyQt6.sip --hidden-import PyQt6.QtCore --hidden-import PyQt6.QtGui --hidden-import PyQt6.QtWidgets --hidden-import PyQt6.QtWebEngineWidgets --hidden-import requests --clean --noconfirm run.py

if errorlevel 1 (
    echo.
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo    BUILD SUCCESS!
echo ========================================
echo.
echo Output file: dist\MoviePlayer.exe
echo.
echo Instructions:
echo    1. Copy the exe file to any location
echo    2. Double-click to run
echo    3. No Python installation needed
echo.
echo Notes:
echo    - File size: ~150MB
echo    - First launch may take a few seconds
echo    - If antivirus warns, add to trusted
echo.
pause
