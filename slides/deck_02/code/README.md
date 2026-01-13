# Search Algorithm Simulations

This directory contains interactive simulations for visualizing Depth-First Search (DFS), Breadth-First Search (BFS), and Iterative Deepening Search (IDS) algorithms using water maze visualizations, similar to CS 188 Berkeley videos.

## Quick Start

### Requirements
- Python 3.13 or later
- numpy and matplotlib (will be installed automatically)

### Running Simulations

#### Option 1: Use the provided scripts (easiest)

**Linux/Mac:**
```bash
./run_dfs_simulation.sh    # Run DFS simulation
./run_bfs_simulation.sh    # Run BFS simulation
./run_ids_simulation.sh    # Run Iterative Deepening simulation
```

**Windows:**
```cmd
run_dfs_simulation.bat    # Run DFS simulation
run_bfs_simulation.bat    # Run BFS simulation
run_ids_simulation.bat    # Run Iterative Deepening simulation
```

#### Option 2: Run manually

**DFS:**
```bash
cd dfs_water
pip install -r requirements.txt
python3 dfs_water_maze.py
```

**BFS:**
```bash
cd bfs_water
pip install -r requirements.txt
python3 bfs_water_maze.py
```

**Iterative Deepening:**
```bash
cd iterative_deepening_water
pip install -r requirements.txt
python3 iterative_deepening_water_maze.py
```

## What You'll See

- **DFS**: Water spreads by going deep first (follows one path until dead end, then backtracks)
- **BFS**: Water spreads level by level (all nodes at distance 1, then distance 2, etc.)
- **Iterative Deepening**: Water spreads using DFS with increasing depth limits (1, then 2, then 3, etc.), restarting each time. Goal is in the middle of the maze.

## Generating Videos

To create video files from the simulations:

**DFS:**
```bash
cd dfs_water
python3 dfs_water_maze_video.py
ffmpeg -r 10 -i frames/frame_%04d.png -c:v libx264 -pix_fmt yuv420p dfs_water_maze.mp4
```

**BFS:**
```bash
cd bfs_water
python3 bfs_water_maze_video.py
ffmpeg -r 10 -i frames/frame_%04d.png -c:v libx264 -pix_fmt yuv420p bfs_water_maze.mp4
```

**Iterative Deepening:**
```bash
cd iterative_deepening_water
python3 iterative_deepening_water_maze_video.py
ffmpeg -r 10 -i frames/frame_%04d.png -c:v libx264 -pix_fmt yuv420p iterative_deepening_water_maze.mp4
```

## Troubleshooting

- **Python version error**: Make sure you have Python 3.13 or later installed
- **Module not found**: Run `pip install -r requirements.txt` in the simulation directory
- **Display issues**: If running on a remote server, you may need X11 forwarding or use the video generation scripts instead
