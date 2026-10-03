@echo off
setlocal
echo ===================================================
echo   CBK STRIDE - Push Changes to Live GitHub App
echo ===================================================

cd /d "%~dp0"

set "COMMIT_MSG=%~1"
if "%COMMIT_MSG%"=="" set "COMMIT_MSG=Update CBK STRIDE live app"

echo [1/3] Staging local changes...
"C:\Users\user\PortableGit\cmd\git.exe" add .

echo [2/3] Committing changes ("%COMMIT_MSG%")...
"C:\Users\user\PortableGit\cmd\git.exe" commit -m "%COMMIT_MSG%"

echo [3/3] Pushing to GitHub (origin/main)...
"C:\Users\user\PortableGit\cmd\git.exe" push origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo SUCCESS: Changes pushed to GitHub! Streamlit Cloud will update https://cbk-stride.streamlit.app automatically in a few seconds.
) else (
    echo.
    echo ERROR: Failed to push to GitHub. If prompted, please run 'gh auth login' or check your GitHub permissions.
)

pause
