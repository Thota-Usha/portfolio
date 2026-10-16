@echo off
title Usha Sree Portfolio - FastAPI Backend Server
echo ========================================================
echo  Starting Usha Sree Portfolio Backend (FastAPI + SQLite)
echo ========================================================
cd /d "%~dp0backend"
echo Serving API and Frontend on http://127.0.0.1:8000
echo Swagger API Docs available at http://127.0.0.1:8000/docs
echo.
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
pause
