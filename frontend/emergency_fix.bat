@echo off
echo EMERGENCY FIX FOR PACKAGE.JSON

REM Backup jika ada
if exist package.json copy package.json package.json.broken

REM Create CORRECT package.json
echo { > package.json
echo   "name": "product-review-analyzer-frontend", >> package.json
echo   "version": "1.0.0", >> package.json
echo   "private": true, >> package.json
echo   "dependencies": { >> package.json
echo     "react": "^18.2.0", >> package.json
echo     "react-dom": "^18.2.0", >> package.json
echo     "axios": "^1.6.0", >> package.json
echo     "react-scripts": "5.0.1" >> package.json
echo   }, >> package.json
echo   "scripts": { >> package.json
echo     "start": "react-scripts start", >> package.json
echo     "build": "react-scripts build", >> package.json
echo     "test": "react-scripts test", >> package.json
echo     "eject": "react-scripts eject" >> package.json
echo   }, >> package.json
echo   "proxy": "http://localhost:5000", >> package.json
echo   "eslintConfig": { >> package.json
echo     "extends": ["react-app"] >> package.json
echo   }, >> package.json
echo   "browserslist": { >> package.json
echo     "production": [ >> package.json
echo       ">0.2%", >> package.json
echo       "not dead", >> package.json
echo       "not op_mini all" >> package.json
echo     ], >> package.json
echo     "development": [ >> package.json
echo       "last 1 chrome version", >> package.json
echo       "last 1 firefox version", >> package.json
echo       "last 1 safari version" >> package.json
echo     ] >> package.json
echo   } >> package.json
echo } >> package.json

echo.
echo Killing all Node processes...
taskkill /F /IM node.exe 2>nul
timeout /t 2 /nobreak >nul

echo Cleaning cache...
rd /s /q node_modules 2>nul
del package-lock.json 2>nul

echo.
echo Installing dependencies...
npm install

if %ERRORLEVEL% EQU 0 (
    echo ✅ FIXED! Starting React...
    npm start
) else (
    echo ❌ Installation failed!
    pause
)