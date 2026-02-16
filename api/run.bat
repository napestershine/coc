@echo off
REM Start the Flask API on Windows

setlocal enabledelayedexpansion

echo Starting CoC Flask API...

if not exist venv (
    echo Virtual environment not found. Creating...
    python -m venv venv
)

call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt > nul 2>&1

echo Starting Flask server on http://0.0.0.0:5000
python app.py

endlocal
