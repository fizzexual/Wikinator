@echo off
cd /d "%~dp0"
docker info >nul 2>&1
if errorlevel 1 (
  echo Start Docker Desktop, wait until it is ready, then open this file again.
  pause
  exit /b 1
)
if not exist "config\.seeded" (
  python scripts\setup.py
) else (
  docker compose up -d
)
if errorlevel 1 (
  echo Wikinator could not start. The error is shown above.
  pause
  exit /b 1
)
start "" "http://localhost:8087/w/Main_Page"
