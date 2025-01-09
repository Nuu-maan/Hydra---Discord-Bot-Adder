@echo off
title Hydra Discord Bot Adder
echo ==================================================
echo           Hydra Discord Bot Adder v1.0.0
echo ==================================================
echo.

echo [INFO] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed. Please install Python 3.8+ and try again.
    pause
    exit
)

echo [INFO] Installing required dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies. Check your Python/pip setup.
    pause
    exit
)

echo [INFO] Starting Hydra...
python hydra.py
if %errorlevel% neq 0 (
    echo [ERROR] Hydra encountered an issue. Please check your configuration or logs.
    pause
    exit
)

pause
