#!/bin/bash
# Run BFS Water Maze Simulation
# Requires Python 3.13 or later

cd "$(dirname "$0")/bfs_water"

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.13"

if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 13) else 1)"; then
    echo "Error: Python 3.13 or later is required. Found: $python_version"
    exit 1
fi

# Install dependencies if needed
if ! python3 -c "import numpy, matplotlib" 2>/dev/null; then
    echo "Installing required packages..."
    pip3 install -r requirements.txt
fi

# Run the simulation
echo "Starting BFS Water Maze Simulation..."
python3 bfs_water_maze.py
