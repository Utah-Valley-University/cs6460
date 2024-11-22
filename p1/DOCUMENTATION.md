# Pacman AI Project Documentation

Note: Students should refer to [P1.md for assignment instructions and requirements.](P1.md) This documentation is intended for developers and maintainers of the Pacman AI codebase.

## Core Components

### 1. Search Algorithms (`search.py`)

- Implements fundamental search algorithms:
  - Depth First Search (DFS)
  - Breadth First Search (BFS)
  - Uniform Cost Search (UCS)
  - A* Search
- Uses an abstract `SearchProblem` base class that defines the interface for search problems
- Each algorithm returns a list of actions to reach a goal state

### 2. Search Agents (`searchAgents.py`)

- Contains various Pacman agents that use search algorithms
- Key classes:
  - `SearchAgent`: Base agent that uses search algorithms
  - `PositionSearchProblem`: For finding paths to specific positions
  - `CornersProblem`: For finding paths through all corners
  - `FoodSearchProblem`: For collecting all food dots

### 3. Graphics Display (`graphicsDisplay.py`)

- Handles visualization using Tkinter
- Key components:
  - `PacmanGraphics`: Main display class
  - `InfoPane`: Shows score and game information
  - Color constants for game elements:

    ```python
    GHOST_COLORS = [
        formatColor(.9,0,0),    # Red
        formatColor(0,.3,.9),   # Blue
        formatColor(.98,.41,.07), # Orange
        formatColor(.1,.75,.7),  # Green
        formatColor(1.0,0.6,0.0), # Yellow
        formatColor(.4,0.13,0.91) # Purple
    ]
    ```

  - Shape definitions for game elements (e.g., `GHOST_SHAPE`)

### 4. Game Engine (`pacman.py`)

- Core game logic and execution
- Key features:
  - Command line interface for game configuration
  - Game state management through `GameState` class
  - Rules enforcement via `ClassicGameRules`
  - Movement logic in `PacmanRules` and `GhostRules`

### 5. Utility Functions (`util.py`)

- Data structures and helper functions:
  - `Stack`: LIFO data structure
  - `Queue`: FIFO data structure
  - `PriorityQueue`: For uniform cost and A* search
  - `Counter`: Extended dictionary for counting
  - Distance calculations (`manhattanDistance`)
  - Random number generation with `FixedRandom`

## Key Concepts

### State Space

- Represented by `GameState` class
- Includes:
  - Pacman position and direction
  - Ghost positions and states
  - Food dot locations
  - Wall configurations
  - Score

### Search Problems

Each search problem must implement:

```python
def getStartState()
def isGoalState(state)
def getSuccessors(state)
def getCostOfActions(actions)
```

### Graphics System

- Uses Tkinter for rendering
- Supports:
  - Agent visualization (Pacman and ghosts)
  - Maze layout
  - Food and capsules
  - Score display
  - Animation effects

### Game Rules

- Scoring:
  - Food pellets: +10 points
  - Ghost capture: +200 points
  - Game win: +500 points
  - Death: -500 points
  - Time penalty: -1 point per move
- Ghost behavior:
  - Cannot stop moving
  - Cannot reverse direction unless at dead end
  - Becomes vulnerable when Pacman eats power capsule

## Usage

The game can be run with various command-line options:
```bash
python pacman.py                 # Basic game
python pacman.py --layout small  # Different layout
python pacman.py -p SearchAgent  # Use search agent
python pacman.py -h              # Show all options
```

## Project Structure

### Layout Files

- Located in `layouts/` directory
- `.lay` files define maze configurations
- Examples:
  - `tinyMaze.lay`: Simple test maze
  - `mediumClassic.lay`: Standard game layout
  - `originalClassic.lay`: Original Pacman maze

### Test Cases

- Located in `test_cases/` directory
- Organized by question/task
- Each test includes:
  - `.test` file: Test configuration
  - `.solution` file: Expected output
  - `CONFIG` file: Test parameters

### Key Files

- `game.py`: Core game mechanics
- `ghostAgents.py`: Ghost AI implementations
- `grading.py`: Autograder functionality
- `graphicsUtils.py`: Low-level graphics functions
- `keyboardAgents.py`: Human player controls
- `layout.py`: Maze layout parsing
- `searchTestClasses.py`: Search algorithm tests

## Development Guide (for Instructors)

### Adding New Search Algorithms

1. Implement algorithm in `search.py`
2. Algorithm must return list of actions
3. Use provided data structures from `util.py`
4. Test with: `python pacman.py -l tinyMaze -p SearchAgent -a fn=depth_first_search`

### Creating Custom Agents

1. Subclass `Agent` from `game.py`
2. Implement `getAction(state)` method
3. Register agent in appropriate agents file
4. Test with: `python pacman.py -p YourAgentClass`

### Adding New Layouts
1. Create `.lay` file in `layouts/` directory
2. Use following symbols:
   - `%`: Wall
   - `.`: Food pellet
   - `o`: Capsule
   - `P`: Pacman start
   - `G`: Ghost start
3. Test with: `python pacman.py -l your_layout`

## Common Issues and Solutions

### Performance Optimization
- Use appropriate data structures for state representation
- Implement efficient heuristics for A* search
- Cache computed values when possible
- Consider using `@lru_cache` for memoization

### Debugging Tips
- Use `python pacman.py --frameTime 0.1` for slower visualization
- Enable debug output with `-v` flag
- Check `test_cases` for example inputs/outputs
- Use autograder for validation: `python autograder.py`

### Known Limitations
- Graphics may flicker on some systems
- Large mazes can be computationally intensive
- Some search algorithms may be impractical for complex layouts
- Keyboard input can be delayed in graphics mode

## Additional Resources

### References
- UC Berkeley CS188 Course Materials
- Pacman AI Projects Documentation
- Python Documentation for Tkinter
- Algorithm References for Search Implementations

### Contributing
1. Fork the repository
2. Create feature branch
3. Implement changes
4. Add tests if applicable
5. Submit pull request

### License
This project is licensed under UC Berkeley's academic license. See LICENSE file for details.
