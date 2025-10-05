@echo off
echo ========================================
echo PathPatrol - Pothole Complaint Portal
echo ========================================
echo.

REM Check if venv exists
if not exist "venv\" (
    echo Virtual environment not found!
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created!
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if streamlit is installed
pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    echo Dependencies installed!
    echo.
)

REM Run the application
echo Starting PathPatrol...
echo The app will open in your browser at http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo.

streamlit run app.py
