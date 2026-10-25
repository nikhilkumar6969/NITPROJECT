@echo off
title LabelGuard - Complete System Launcher
color 0B
echo ===================================================================
echo     LABELGUARD AI - STATUTORY COMPLIANCE PLATFORM LAUNCHER
echo ===================================================================
echo.

cd /d "%~dp0"

echo [1/3] Freeing port 8000 for PaddleOCR microservice...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000 ^| findstr LISTENING') do (
    taskkill /F /PID %%a >nul 2>&1
)

echo [2/3] Launching PaddleOCR Backend Microservice on port 8000...
start "LabelGuard - PaddleOCR (Port 8000)" cmd /k "color 0A && paddle-env\Scripts\python.exe backend\ocr_service.py"

timeout /t 2 /nobreak >nul

echo [3/3] Launching Web Interface...
start "LabelGuard - Web Dashboard" cmd /k "color 0B && python run_frontend.py"

timeout /t 1 /nobreak >nul
echo [+] Opening http://localhost:5173/ in default browser...
start http://localhost:5173/

echo.
echo ===================================================================
echo [+] LabelGuard system is active!
echo     - Web Interface : http://localhost:5173/
echo     - OCR Service   : http://127.0.0.1:8000/
echo ===================================================================
pause
