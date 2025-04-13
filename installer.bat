@echo off
:: Batch script to install Python libraries from requirements.txt
:: Checks for Python and pip, then installs dependencies

echo ========================================
echo     START INSTALLING GAMELIB v0.0b
echo ========================================

:: Display Python version if available
echo Checking Python installation...
python --version 2>nul
if %errorlevel% neq 0 (
    echo Python not found. Make sure Python is installed and added to PATH.
    pause
    exit /b 1
)

:: Store Python version for later display
for /f "tokens=*" %%a in ('python --version 2^>^&1') do set "PYTHON_VERSION=%%a"

echo.
echo ========================================
echo %PYTHON_VERSION% detected
echo Beginning dependency installation...
echo ========================================
echo.


echo Checking pip installation...
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo pip not found. Attempting to install pip...
    python -m ensurepip --upgrade
    if %errorlevel% neq 0 (
        echo Failed to install pip.
        pause
        exit /b 1
    )
)

echo Updating pip...
python -m pip install --upgrade pip
if %errorlevel% neq 0 (
    echo Failed to update pip.
    pause
    exit /b 1
)

echo Searching for requirements.txt...
if not exist "requirements.txt" (
    echo requirements.txt not found in the current directory.
    dir /b
    pause
    exit /b 1
)

echo Installing libraries from requirements.txt...
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install some libraries.
    pause
    exit /b 1
)

echo.
echo ========================================
echo All libraries installed successfully!
echo Python version: %PYTHON_VERSION%
echo ========================================
pause