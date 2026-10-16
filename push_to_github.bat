@echo off
title Push Portfolio to GitHub
echo ===========================================
echo  Pushing Portfolio to https://github.com/Thota-Usha/portfolio
echo ===========================================
cd /d "%~dp0"
git push -u origin main
echo.
if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] Code successfully pushed to GitHub!
    echo Now open Vercel and import your portfolio!
) else (
    echo [NOTE] If you saw a login popup, please sign in to complete the push.
)
pause
