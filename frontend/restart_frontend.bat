@echo off
echo RESTARTING FRONTEND...

REM Kill React dev server
taskkill /F /IM node.exe 2>nul

REM Clear browser cache suggestion
echo Please CLEAR BROWSER CACHE:
echo 1. Open Chrome
echo 2. Press Ctrl+Shift+Delete
echo 3. Select "Cached images and files"
echo 4. Click "Clear data"

echo.
echo Starting React...
npm start

pause