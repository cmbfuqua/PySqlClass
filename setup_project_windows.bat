@echo off
echo Checking Python version...
python --version 2>NUL | findstr /R /C:"3\.[1-9][2-9]" /C:"3\.[2-9][0-9]" >NUL
if errorlevel 1 (
    echo Python 3.12+ is required but not found.
    echo Attempting to install via winget...
    winget install Python.Python.3.12
    if errorlevel 1 (
        echo Winget failed or is missing. Please manually install Python 3.12+ from https://www.python.org/downloads/
        pause
        exit /b 1
    )
)

echo Creating virtual environment...
python -m venv .venv
call .venv\Scripts\activate.bat

echo Upgrading pip and installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo Initial Database Generation...
:: We will implement db initialization here if needed, but per-folder initialization is standard.
:: For now, we just create an empty finance.db to meet the root file requirement, or it will be created by the first week script.

echo Virtual environment setup complete!
