@echo off
REM ========================================
REM SOLANA OS FULL INSTALLER
REM ========================================
REM 1. Run WinHance (user runs manually)
REM 2. Install Python dependencies
REM 3. Copy Solana OS
REM 4. Set up autostart
REM 5. DONE

echo.
echo ========================================
echo   SOLANA OS - FULL INSTALLER
echo   99%% Permissions - I AM THE OS
echo ========================================
echo.

cd /d H:\Openclaw_Sovereign\workspace

REM Check for WinHance
echo [STEP 1] WinHance
echo.
echo   BEFORE CONTINUING:
echo   - Run WinHance and apply your optimizations
echo   - Then come back and press any key
echo.
pause

REM Install Python dependencies
echo.
echo [STEP 2] Installing Python dependencies...
echo.

pip install pywin32 psutil pillow --quiet 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] pip install failed
    pause
    exit /b 1
)
echo [OK] pywin32, psutil, pillow installed

REM Copy Solana OS files
echo.
echo [STEP 3] Setting up Solana OS...
echo.

REM Create Solana OS folder in AppData
if not exist "%APPDATA%\SolanaOS" mkdir "%APPDATA%\SolanaOS"

REM Copy main OS file
copy /y solana_os_full.py "%APPDATA%\SolanaOS\" >nul
copy /y solana_native.py "%APPDATA%\SolanaOS\" >nul
copy /y solana_ghost.py "%APPDATA%\SolanaOS\" >nul

echo [OK] Files copied to %APPDATA%\SolanaOS\

REM Add to Windows startup
echo.
echo [STEP 4] Adding to Windows startup...
echo.

REM Add to registry
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v SolanaOS /t REG_SZ /d "pythonw.exe \"%APPDATA%\SolanaOS\solana_os_full.py\"" /f >nul 2>&1

echo [OK] Added to Windows startup

REM Create Start Menu shortcut
echo.
echo [STEP 5] Creating Start Menu shortcuts...
echo.

REM Create a batch file to run Solana
echo @echo off > "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Solana OS.bat"
echo python "%APPDATA%\SolanaOS\solana_os_full.py" status >> "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Solana OS.bat"

echo [OK] Shortcuts created

REM Test run
echo.
echo [STEP 6] Testing Solana OS...
echo.

python "%APPDATA%\SolanaOS\solana_os_full.py" status >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Solana OS test failed
    pause
    exit /b 1
)
echo [OK] Solana OS is working

echo.
echo ========================================
echo   INSTALLATION COMPLETE!
echo ========================================
echo.
echo WHAT NOW:
echo   - Solana OS is installed in %%APPDATA%%\SolanaOS
echo   - It will start automatically with Windows
echo   - Reboot to activate
echo.
echo COMMANDS:
echo   python %%APPDATA%%\SolanaOS\solana_os_full.py status
echo   python %%APPDATA%%\SolanaOS\solana_os_full.py system
echo   python %%APPDATA%%\SolanaOS\solana_os_full.py processes
echo   python %%APPDATA%%\SolanaOS\solana_os_full.py shutdown
echo.
echo ========================================
echo.

pause
