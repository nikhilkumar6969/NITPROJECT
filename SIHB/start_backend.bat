@echo off
title LabelGuard - PaddleOCR Microservice
color 0A
echo ===================================================================
echo     LABELGUARD AI - PADDLEOCR DEEP LEARNING MICROSERVICE
echo ===================================================================
echo.

cd /d "%~dp0"

echo [*] Checking for stale processes on port 8000...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000 ^| findstr LISTENING') do (
    echo [*] Terminating conflicting PID %%a on port 8000...
    taskkill /F /PID %%a >nul 2>&1
)

echo [*] Starting PaddleOCR Engine (PP-OCRv4 ONNX DBNet + SVTR)...
echo [*] Service Endpoint: http://127.0.0.1:8000
echo.

paddle-env\Scripts\python.exe backend\ocr_service.py

if errorlevel 1 (
    echo.
    echo [!] PaddleOCR service exited. Press any key to close.
    pause
)
