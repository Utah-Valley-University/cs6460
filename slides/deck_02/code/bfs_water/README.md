# BFS Water Maze Simulation

This simulation visualizes Breadth-First Search (BFS) using a water maze, similar to the CS 188 Berkeley videos. Water spreads through the maze following BFS exploration order (level by level).

## Features

- Visual representation of BFS algorithm
- Water spreading animation showing level-by-level exploration
- Queue visualization showing current level being explored
- Goal detection with shortest path distance
- Level-by-level spreading pattern (characteristic of BFS)

## Requirements

```bash
pip install numpy matplotlib
```

## Usage

### Interactive Animation

Run the simulation with an interactive matplotlib window:

```bash
python bfs_water_maze.py
```

### Generate Video Frames

To generate frames for creating a video:

```bash
python bfs_water_maze_video.py
```

This will save frames to the `frames/` directory, which can then be compiled into a video using ffmpeg:

```bash
ffmpeg -r 10 -i frames/frame_%04d.png -c:v libx264 -pix_fmt yuv420p bfs_water_maze.mp4
```

## How It Works

1. **Maze Generation**: Creates a maze with walls and open paths
2. **BFS Algorithm**: Uses a queue (FIFO) to explore the maze level by level
3. **Water Visualization**: 
   - Dark blue circles = Currently in queue (waiting to explore)
   - Light blue circles = Previously explored cells
   - Yellow circles = Current level being explored (all nodes at same distance)
4. **Goal Detection**: Highlights when the goal is reached and shows shortest path distance

## Legend

- **Green square (S)**: Start position
- **Red square (G)**: Goal position
- **Dark blue circles**: Water in queue (waiting to be explored)
- **Light blue circles**: Previously explored cells (water has been here)
- **Yellow circles**: Current level being explored (all nodes at same distance from start)
- **Gray squares**: Walls

## Algorithm Details

The simulation uses a standard BFS implementation:
- Maintains a queue of positions to explore (FIFO)
- Explores all neighbors of current node before moving to next level
- Processes nodes level by level (all nodes at distance 1, then distance 2, etc.)
- Marks cells as "wet" when added to queue, "explored" after processing
- Tracks distance from start (shortest path when goal is found)

This matches the behavior shown in CS 188 Berkeley's BFS water maze videos, where water spreads in concentric "waves" or levels from the start.

## Key Difference from DFS

- **DFS**: Goes deep first (follows one path until dead end, then backtracks)
- **BFS**: Goes wide first (explores all nodes at same distance before going deeper)
- **BFS** finds the shortest path (minimum number of steps) when all edges have equal cost
