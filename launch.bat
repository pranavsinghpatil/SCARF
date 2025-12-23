@echo off
setlocal EnableDelayedExpansion

title SCARF: Scientific Reasoning Framework

echo ===================================================
echo      SCARF: Scientific Reasoning Framework      
echo      Backend + Frontend Launcher
echo ===================================================

echo [0/5] Clearing Ports...
:: Kill likely conflicting processes
for /f "tokens=5" %%a in ('netstat -aon ^| find ":9999" ^| find "LISTENING"') do taskkill /f /pid %%a >nul 2>&1
for /f "tokens=5" %%a in ('netstat -aon ^| find ":5555" ^| find "LISTENING"') do taskkill /f /pid %%a >nul 2>&1
echo    - Ports cleared.

:: 1. Check Python Environment
echo [1/5] Checking Python Virtual Environment...
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
    echo    - .venv activated.
) else (
    echo    - Checking for 'env' or 'venv'...
    if exist "venv\Scripts\activate.bat" call venv\Scripts\activate.bat
    if exist "env\Scripts\activate.bat" call env\Scripts\activate.bat
)

:: 2. Check Environment Variables
echo [2/5] Checking Configuration...
if not exist ".env" (
    echo    [WARNING] .env file not found!
    echo    Please copy .env.example to .env and set NOVITA_API_KEY.
    echo    Creating .env from example...
    copy .env.example .env >nul
) else (
    findstr "NOVITA_API_KEY" .env >nul
    if !errorlevel! equ 0 (
        echo    - API Key config found.
    ) else (
        echo    [WARNING] NOVITA_API_KEY seems missing in .env
    )
)

:: 3. Check Python Dependencies
echo [3/5] Verifying Backend Dependencies...
python -c "import paddleocr; import fastapi; import pydantic; print('   - Core modules found.')" 2>nul
if !errorlevel! neq 0 (
    echo    [ERROR] Missing dependencies. Installing now...
    pip install -r requirements.txt
)

:: 4. Frontend Setup
echo [4/5] Checking Frontend (NewFrontend)...
if exist "NewFrontend\package.json" (
    cd NewFrontend
    if not exist "node_modules" (
        echo    - Installing Frontend Dependencies...
        call npm install
    )
    echo    - Cleaning Vite Cache...
    if exist "node_modules\.vite" rmdir /s /q "node_modules\.vite"
    echo    - Starting Frontend in Background...
    :: FORCE PORT 5555
    start "SCARF Frontend" cmd /k "npm run dev -- --port 5555"
    cd ..
) else (
    echo    [WARNING] NewFrontend folder not found. Skipping UI launch.
)

:: 5. Launch Backend
echo [5/5] Starting SCARF Backend Server...
echo.
echo    -------------------------------------------
echo    Backend:  http://127.0.0.1:9999/docs
echo    Frontend: http://localhost:5555
echo    -------------------------------------------
echo.

uvicorn backend.api.main:app --host 127.0.0.1 --port 9999 --reload

pause
