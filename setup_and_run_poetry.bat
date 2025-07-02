@echo off
echo === HST AI Engineer Project Setup (Poetry) ===

:: Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: Python is not installed or not in PATH.
    echo Please install Python 3.8 or higher from https://www.python.org/downloads/
    exit /b 1
)

:: Run the setup script
echo Running Poetry setup script...
python "%~dp0setup_poetry.py"
if %ERRORLEVEL% neq 0 (
    echo Setup failed. Please check the error messages above.
    pause
    exit /b 1
)

:: Ask if the user wants to run the application
echo.
set /p RUN_APP=Do you want to run the application now? (y/n): 
if /i "%RUN_APP%"=="y" (
    echo.
    echo Starting the application...
    call venv\Scripts\activate && python main.py
) else (
    echo.
    echo To run the application later, activate the virtual environment with:
    echo   venv\Scripts\activate
    echo Then run:
    echo   python main.py
)

pause