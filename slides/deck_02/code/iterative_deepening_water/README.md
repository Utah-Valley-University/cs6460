# Iterative Deepening Water Maze Simulation

This simulation visualizes Iterative Deepening Search (IDS) using a water maze, similar to the CS 188 Berkeley videos. Water spreads through the maze using iterative deepening: DFS with depth limit 1, then 2, then 3, etc.

## Features

- Visual representation of Iterative Deepening algorithm
- Water spreading animation showing depth-limited DFS exploration
- Time-based color coding (same time step = same color, older = darker)
- Goal placed in middle of maze (not corner)
- Shows how IDS combines DFS and BFS benefits

## Requirements

```bash
pip install numpy matplotlib
```

## Usage

### Interactive Animation

Run the simulation with an interactive matplotlib window:

```bash
python iterative_deepening_water_maze.py
```

### Generate Video Frames

To generate frames for creating a video:

```bash
python iterative_deepening_water_maze_video.py
```

This will save frames to the `frames/` directory, which can then be compiled into a video using ffmpeg:

```bash
ffmpeg -r 10 -i frames/frame_%04d.png -c:v libx264 -pix_fmt yuv420p iterative_deepening_water_maze.mp4
```

## How It Works

1. **Maze Generation**: Creates a maze with walls and open paths, goal in middle
2. **Iterative Deepening Algorithm**: 
   - Runs DFS with depth limit 1
   - If goal not found, runs DFS with depth limit 2
   - Continues increasing depth limit until goal found
3. **Water Visualization**: 
   - Blue rectangles = Water spreading (current exploration)
   - Darker blue = Previously explored cells
   - Color intensity shows when each cell was explored
4. **Goal Detection**: Highlights when the goal is reached

## Legend

- **Green square (S)**: Start position
- **Red square (G)**: Goal position (in middle of maze)
- **Blue rectangles**: Water spreading (current DFS exploration)
- **Darker blue rectangles**: Previously explored cells (water has been here)
- **Green line**: Current DFS path (shows the stack)
- **Gray squares**: Walls

## Algorithm Details

Iterative Deepening combines the benefits of DFS and BFS:
- **Space efficient**: Like DFS, uses O(d) space where d is depth
- **Complete**: Like BFS, guaranteed to find solution if one exists
- **Optimal**: Finds shortest path (when all edges have equal cost)

The algorithm:
1. Runs DFS with depth limit 1 (explores only immediate neighbors)
2. If goal not found, runs DFS with depth limit 2
3. Continues with depth limit 3, 4, 5, etc.
4. Each iteration explores nodes at that depth level

This creates a pattern where you see:
- First iteration: shallow exploration (depth 1)
- Second iteration: deeper exploration (depth 2), but re-explores depth 1
- Third iteration: even deeper (depth 3), re-exploring previous levels
- And so on...

The visualization shows this by the water restarting and spreading further with each iteration.
