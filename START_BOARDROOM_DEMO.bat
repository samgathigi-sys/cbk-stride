@echo off
title CBK DSWAAP - Boardroom Presentation Master Launcher
color 1F

echo ===========================================================================
echo   CENTRAL BANK OF KENYA - BANKI KUU YA KENYA
echo   DSWAAP: Sports Wellness & Attendance Automation Platform
echo   BOARDROOM DEMO & PRESENTATION LAUNCHER
echo ===========================================================================
echo.
echo [1/3] Checking Streamlit Engine status on port 8501...
netstat -ano | findstr 8501 >nul
if %errorlevel% equ 0 (
    echo       [OK] Streamlit is already running!
) else (
    echo       [+] Starting Streamlit Core in background...
    start /min "CBK DSWAAP App" python -m streamlit run app.py --server.address=0.0.0.0 --server.port=8501 --server.headless=true
    timeout /t 3 /nobreak >nul
)

echo.
echo [2/3] Checking Cloudflare Secure Public Tunnel...
tasklist | findstr /i "cloudflared" >nul
if %errorlevel% equ 0 (
    echo       [OK] Cloudflare Tunnel is already active!
) else (
    echo       [+] Launching Cloudflare Edge Tunnel...
    start /min "CBK Cloudflare Tunnel" .\cloudflared.exe tunnel --url http://localhost:8501
    timeout /t 3 /nobreak >nul
)

echo.
echo [3/3] Launching Live Portals in your Browser...
echo.
echo ===========================================================================
echo   YOUR LIVE PRESENTATION LINKS FOR THE BOARD:
echo   -------------------------------------------------------------------------
echo   * PERMANENT CLOUD PORTAL (GITHUB & STREAMLIT ENTERPRISE CLOUD):
echo     https://cbk-stride.streamlit.app
echo.
echo   * LOCAL DIRECT PORTAL (LAPTOP PROJECTOR / SCREEN):
echo     http://localhost:8501
echo.
echo   * LOCAL WI-FI IP (DEVICES ON SAME CBK / HOME WI-FI):
echo     http://192.168.1.35:8501
echo.
echo   * GOLFER CONFIRMATION DEMO (S. N. GATHIGI - CBK-1008):
echo     https://cbk-stride.streamlit.app?verify_token=a410c713c72358d5^&staff_id=CBK-1008^&email=sam.gathigi@gmail.com^&discipline=Golf^&confirmed=1
echo ===========================================================================
echo.

start "" "http://localhost:8501"

echo Presentation is LIVE! Keep this window open during your boardroom pitch.
echo Press any key when your presentation is complete to close...
pause >nul
