@echo off
REM Cleanup script for removing obsolete files after migrating to Poetry

echo === Cleanup After Poetry Migration ===
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: Python is not installed or not in PATH.
    echo Please install Python and try again.
    exit /b 1
)

REM Check if the cleanup script exists
if not exist cleanup_after_poetry.py (
    echo Error: cleanup_after_poetry.py not found.
    echo Please make sure you're running this script from the correct directory.
    exit /b 1
)

REM Check if Poetry is set up
if not exist pyproject.toml (
    echo Error: pyproject.toml not found. Poetry setup is incomplete.
    echo Please run setup_poetry.py first.
    exit /b 1
)

REM Run the cleanup script
echo Running cleanup script...
echo.

REM Check if --remove flag is provided
if "%1"=="--remove" (
    python cleanup_after_poetry.py --remove
) else (
    python cleanup_after_poetry.py
    echo.
    echo To remove the obsolete files, run:
    echo   cleanup_after_poetry.bat --remove
)

echo.
echo Done.
pause