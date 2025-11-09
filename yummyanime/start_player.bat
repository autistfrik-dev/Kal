@echo off
echo ============================================================
echo YummyAnime Video Player Server
echo ============================================================
echo.
echo Starting server...
echo.
cd /d "%~dp0"
python simple_server.py
pause

