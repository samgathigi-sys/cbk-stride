@echo off
title CBK DSWAAP Server
color 1F
echo ===========================================================================
echo   CENTRAL BANK OF KENYA - DSWAAP SERVER LAUNCHER
echo   Sports Wellness ^& Attendance Automation Platform
echo ===========================================================================
echo.
echo Local Machine Browser: http://localhost:8501
echo Mobile Phone / Network: http://192.168.1.35:8501
echo.
echo Starting Streamlit server... Press Ctrl+C in this window to stop.
echo.
python -m streamlit run app.py --server.address=0.0.0.0 --server.port=8501
pause
