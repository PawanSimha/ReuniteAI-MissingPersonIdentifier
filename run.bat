@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title ReuniteAI - Missing Person Identifier
set "URL=http://localhost:5000"
cls
echo.
echo  ============================================
echo   ReuniteAI - Missing Person Identifier
echo  ============================================
echo.

:menu
echo  Choose an option:
echo   [1] Start the stack - fast, existing image
echo   [2] Rebuild and start - from source
echo   [3] Stop and tear down the stack
echo   [4] View live logs
echo   [5] Restart the stack
echo   [6] Exit
echo.
set /p "choice=  Enter your choice 1-6 : "
if "%choice%"=="1" goto start
if "%choice%"=="2" goto rebuild
if "%choice%"=="3" goto stop
if "%choice%"=="4" goto logs
if "%choice%"=="5" goto restart
if "%choice%"=="6" goto end
echo  Invalid choice.
goto menu

:check_docker
docker info >nul 2>&1
if errorlevel 1 (
    echo  [X] Docker is not running. Start Docker Desktop first.
    exit /b 1
)
exit /b 0

:ensure_env
if not exist ".env" (
    echo  [!] .env not found - copying from .env.example ...
    copy /Y ".env.example" ".env" >nul
    echo  [!] Edit .env to set SECRET_KEY, ADMIN_EMAIL and ADMIN_PASSWORD.
)
goto :eof

:start
call :check_docker
if errorlevel 1 goto end
call :ensure_env
echo  [*] Starting containers from existing image ...
docker compose up -d < nul
if errorlevel 1 (
    echo  [X] docker compose up failed. Try option 2 to rebuild.
    goto end
)
call :wait_for_app
goto ready

:rebuild
call :check_docker
if errorlevel 1 goto end
call :ensure_env
echo  [*] Building image and starting containers ...
docker compose up --build -d < nul
if errorlevel 1 (
    echo  [X] Build failed. Check output above.
    goto end
)
call :wait_for_app
goto ready

:wait_for_app
echo  [*] Waiting for the app to become ready ...
set /a tries=0
:wait_loop
set /a tries+=1
if %tries% gtr 60 (
    echo  [X] App did not become ready. Run: docker compose logs web
    goto end
)
curl -s -o nul "%URL%/health" < nul 2>&1 && goto :eof
timeout /t 2 /nobreak >nul
goto wait_loop

:ready
echo.
echo  [OK] ReuniteAI is running!
echo   Application : %URL%
echo   Health check: %URL%/health
start "" "%URL%"
echo.
echo   Useful commands:
echo     View logs : docker compose logs -f web
echo     Stop all  : docker compose stop
echo.
goto end

:stop
call :check_docker
if errorlevel 1 goto end
echo  [*] Stopping the stack ...
docker compose down < nul
echo  [OK] Stack stopped. Data kept - run option 1 to start again.
goto end

:restart
call :check_docker
if errorlevel 1 goto end
echo  [*] Restarting containers ...
docker compose restart < nul
echo  [OK] Containers restarted: %URL%
goto end

:logs
call :check_docker
if errorlevel 1 goto end
docker compose logs -f < nul
goto end

:end
echo.
pause
endlocal
