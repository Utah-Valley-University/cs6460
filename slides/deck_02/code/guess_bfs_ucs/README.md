# Water Maze Simulations - Guess: DFS, BFS, or UCS?

This directory contains two simulations that visualize search algorithms on a maze with weighted edges:
- **Shallow water** (cost 1) - light blue background
- **Deep water** (cost 2) - dark blue background

## Two Simulations

1. **`guess_bfs_water_maze.py`** - BFS simulation (Slide 48)
   - BFS ignores edge costs, spreads by number of steps
   - Answer: **BFS**

2. **`guess_ucs_water_maze.py`** - UCS simulation (Slide 49)
   - UCS considers edge costs, spreads by cost contours
   - Answer: **UCS**

The key question: **Does the water spread by number of steps (BFS), depth-first (DFS), or by cost (UCS)?**

## Features

- Visual representation of search algorithm on weighted graph
- Shallow water (cost 1) and deep water (cost 2) clearly marked
- Water spreading animation showing exploration pattern
- Students can observe whether water spreads:
  - **In concentric circles** (by number of steps) = BFS
  - **By cost contours** (shallow first, then deep) = UCS

## Requirements

```bash
pip install numpy matplotlib
```

Or install from requirements.txt:

```bash
pip install -r requirements.txt
```

## Usage

### BFS Simulation (Slide 48)

Run the BFS simulation:

```bash
python guess_bfs_water_maze.py
```

Or from the code directory:

```bash
cd code
./run_guess_simulation.sh
```

On Windows:

```cmd
cd code
run_guess_simulation.bat
```

### UCS Simulation (Slide 49)

Run the UCS simulation:

```bash
python guess_ucs_water_maze.py
```

Or from the code directory:

```bash
cd code
./run_guess_ucs_simulation.sh
```

On Windows:

```cmd
cd code
run_guess_ucs_simulation.bat
```

## How It Works

1. **Maze Generation**: Creates a maze with:
   - Shallow water cells (cost 1) - light blue
   - Deep water cells (cost 2) - dark blue
   - Walls (impassable)

2. **Search Algorithm**: 
   - **BFS** (`guess_bfs_water_maze.py`): Ignores edge costs, treats all edges as cost 1
   - **UCS** (`guess_ucs_water_maze.py`): Considers costs, explores by cost contours (shallow first)

3. **Water Visualization**: 
   - Background shows water depth (shallow = light blue, deep = dark blue)
   - Spreading water shows exploration order
   - Bright blue = newly explored
   - Darker blue = previously explored

## Legend

- **Green square (S)**: Start position
- **Red square (G)**: Goal position
- **Light blue background**: Shallow water (cost 1)
- **Dark blue background**: Deep water (cost 2)
- **Bright blue spreading**: Water exploring the maze
- **Gray squares**: Walls

## Key Observation

**BFS behavior:**
- Water spreads in concentric circles
- All cells at the same number of steps from start are explored together
- Ignores whether water is shallow or deep
- Spreads uniformly in all directions

**UCS behavior (for comparison):**
- Water would spread by cost contours
- All shallow water (cost 1) would be explored before deep water (cost 2)
- Would prefer paths through shallow water even if they're longer in steps

## Educational Purpose

### Slide 48: "Guess Which One - BFS or UCS?" (BFS Simulation)

Students should observe:
1. Does water spread in concentric circles? → BFS
2. Does water prefer shallow water first? → UCS

**Answer: BFS** - water spreads by number of steps, not by cost!

### Slide 49: "Guess Which of the Three - DFS, BFS, UCS?" (UCS Simulation)

Students should observe:
1. Does water spread in concentric circles (by steps)? → BFS
2. Does it go deep first then backtrack? → DFS
3. Does it spread by cost (shallow first, then deep)? → UCS

**Answer: UCS** - water spreads by cost contours, exploring all shallow water (cost 1) before deep water (cost 2)!
