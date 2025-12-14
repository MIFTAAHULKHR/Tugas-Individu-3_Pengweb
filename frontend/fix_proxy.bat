@echo off
echo Fixing proxy configuration...

REM Update package.json proxy to port 5000
npm pkg set proxy="http://localhost:5000"

REM Stop current React process
taskkill /F /IM node.exe 2>nul

echo.
echo ✅ Proxy updated to port 5000
echo.
echo Steps:
echo 1. Make sure backend is running: python flask_app.py
echo 2. Restart frontend: npm start
echo.
pause