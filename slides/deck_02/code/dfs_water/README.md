# DFS Water Maze Simulation

This simulation visualizes Depth-First Search (DFS) using a water maze, similar to the CS 188 Berkeley videos. Water spreads through the maze following DFS exploration order.

## Features

- Visual representation of DFS algorithm
- Water spreading animation showing exploration order
- Stack visualization showing current DFS path
- Goal detection and path highlighting

## Requirements

```bash
pip install numpy matplotlib
```

## Usage

### Interactive Animation

Run the simulation with an interactive matplotlib window:

```bash
python dfs_water_maze.py
```

### Generate Video Frames

To generate frames for creating a video:

```bash
python dfs_water_maze_video.py
```

This will save frames to the `frames/` directory, which can then be compiled into a video using ffmpeg:

```bash
ffmpeg -r 10 -i frames/frame_%04d.png -c:v libx264 -pix_fmt yuv420p dfs_water_maze.mp4
```

## How It Works

1. **Maze Generation**: Creates a maze with walls and open paths
2. **DFS Algorithm**: Uses a stack (LIFO) to explore the maze
3. **Water Visualization**: 
   - Dark blue circles = Currently exploring (top of stack)
   - Light blue circles = Previously explored cells
   - Green line = Current DFS path (stack contents)
4. **Goal Detection**: Highlights when the goal is reached

## Legend

- **Green square (S)**: Start position
- **Red square (G)**: Goal position
- **Dark blue circles**: Water currently spreading (active DFS exploration)
- **Light blue circles**: Previously explored cells (water has been here)
- **Green line**: Current DFS path (shows the stack)
- **Gray squares**: Walls

## Algorithm Details

The simulation uses a standard DFS implementation:
- Maintains a stack of positions to explore
- Explores neighbors in order (up, down, left, right)
- Backtracks when no unvisited neighbors exist
- Marks cells as "wet" when first visited, "explored" after processing

This matches the behavior shown in CS 188 Berkeley's DFS water maze videos.
