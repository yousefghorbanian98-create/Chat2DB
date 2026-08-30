@echo off
rem Motion Package — one-click launcher (Windows)
cd /d "%~dp0"
where node >nul 2>nul
if errorlevel 1 (
  echo Node.js not found. Install it from https://nodejs.org then run this again.
  pause
  exit /b 1
)
node serve-dist.cjs --open
pause
