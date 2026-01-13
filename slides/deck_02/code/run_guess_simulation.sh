#!/bin/bash
# Run the "Guess BFS or UCS" water maze simulation

cd "$(dirname "$0")" || exit 1

echo "Starting Water Maze Simulation - Guess: BFS or UCS?"
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 not found. Please install Python 3."
    exit 1
fi

# Check if required packages are installed
if ! python3 -c "import numpy, matplotlib" 2>/dev/null; then
    echo "Installing required packages..."
    pip3 install -r guess_bfs_ucs/requirements.txt
fi

# Run the simulation
cd guess_bfs_ucs || exit 1
python3 guess_bfs_water_maze.py
