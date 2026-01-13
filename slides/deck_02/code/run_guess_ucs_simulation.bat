@echo off
REM Run the "Guess DFS, BFS, or UCS" water maze simulation (UCS version)

cd /d "%~dp0"

echo Starting Water Maze Simulation - Guess: DFS, BFS, or UCS? (UCS)
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found. Please install Python 3.
    pause
    exit /b 1
)

REM Check if required packages are installed
python -c "import numpy, matplotlib" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -r guess_bfs_ucs\requirements.txt
)

REM Run the simulation
cd guess_bfs_ucs
python guess_ucs_water_maze.py

pause
