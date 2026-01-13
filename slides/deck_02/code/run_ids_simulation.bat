@echo off
REM Run Iterative Deepening Water Maze Simulation
REM Requires Python 3.13 or later

cd /d "%~dp0iterative_deepening_water"

REM Check Python version
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    exit /b 1
)

python -c "import sys; exit(0 if sys.version_info >= (3, 13) else 1)" 2>nul
if errorlevel 1 (
    echo Error: Python 3.13 or later is required
    python --version
    exit /b 1
)

REM Install dependencies if needed
python -c "import numpy, matplotlib" 2>nul
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements.txt
)

REM Run the simulation
echo Starting Iterative Deepening Water Maze Simulation...
python iterative_deepening_water_maze.py
