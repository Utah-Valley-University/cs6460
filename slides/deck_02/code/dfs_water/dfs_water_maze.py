#!/usr/bin/env python3
"""
DFS Water Maze Simulation

This simulation visualizes Depth-First Search (DFS) using a water maze,
similar to the CS 188 Berkeley videos. Water spreads through the maze
following DFS exploration order.

Author: Generated for CS 6460
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
from collections import deque
import time


class WaterMaze:
    """Represents a maze where water spreads using DFS."""
    
    def __init__(self, width=15, height=15, start=(1, 1), goal=None):
        """
        Initialize the water maze.
        
        Args:
            width: Width of the maze
            height: Height of the maze
            start: Starting position (row, col)
            goal: Goal position (row, col), defaults to bottom-right
        """
        self.width = width
        self.height = height
        self.start = start
        self.goal = goal if goal else (height-2, width-2)
        
        # Create a simple maze (1 = wall, 0 = open)
        self.maze = self._generate_maze()
        
        # Water state: 0 = dry, 1 = wet, 2 = explored
        self.water_state = np.zeros((height, width), dtype=int)
        self.water_state[start[0], start[1]] = 1  # Start is wet
        
        # Time step tracking - when was each cell explored
        self.exploration_time = np.full((height, width), -1, dtype=int)
        self.exploration_time[start[0], start[1]] = 0  # Start at time 0
        self.current_time = 0
        
        # DFS tracking
        self.stack = [start]
        self.visited = {start}
        self.exploration_order = []
        self.found_goal = False
        
    def _generate_maze(self):
        """Generate a simple maze with walls and open paths."""
        maze = np.ones((self.height, self.width), dtype=int)
        
        # Create open paths (simple pattern for visualization)
        for i in range(1, self.height-1):
            for j in range(1, self.width-1):
                # Create a pattern with some walls
                if (i + j) % 3 != 0:
                    maze[i, j] = 0
        
        # Ensure start and goal are open
        maze[self.start[0], self.start[1]] = 0
        maze[self.goal[0], self.goal[1]] = 0
        
        # Ensure there's a path (simple connectivity)
        for i in range(1, self.height-1):
            maze[i, 1] = 0  # Left column open
            maze[i, self.width-2] = 0  # Right column open
        
        for j in range(1, self.width-1):
            maze[1, j] = 0  # Top row open
            maze[self.height-2, j] = 0  # Bottom row open
        
        return maze
    
    def get_neighbors(self, pos):
        """Get valid neighboring positions (up, down, left, right)."""
        row, col = pos
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if (0 <= new_row < self.height and 
                0 <= new_col < self.width and
                self.maze[new_row, new_col] == 0 and
                (new_row, new_col) not in self.visited):
                neighbors.append((new_row, new_col))
        
        return neighbors
    
    def dfs_step(self):
        """Perform one step of DFS exploration."""
        if not self.stack or self.found_goal:
            return False
        
        current = self.stack[-1]  # Top of stack (LIFO)
        
        # Mark as explored at current time step
        if self.water_state[current[0], current[1]] == 1:
            self.water_state[current[0], current[1]] = 2
            self.exploration_time[current[0], current[1]] = self.current_time
            self.exploration_order.append(current)
            self.current_time += 1
        
        # Check if goal reached
        if current == self.goal:
            self.found_goal = True
            return True
        
        # Get unvisited neighbors
        neighbors = self.get_neighbors(current)
        
        if neighbors:
            # DFS: go to first unvisited neighbor (deep first)
            next_pos = neighbors[0]
            self.stack.append(next_pos)
            self.visited.add(next_pos)
            self.water_state[next_pos[0], next_pos[1]] = 1  # Wet
            # Mark when it becomes wet (same time step as current exploration)
            self.exploration_time[next_pos[0], next_pos[1]] = self.current_time
            return True
        else:
            # Backtrack: no unvisited neighbors
            self.stack.pop()
            return True
    
    def get_water_coverage(self):
        """Get current water coverage for visualization."""
        return self.water_state.copy()
    
    def get_max_time(self):
        """Get maximum exploration time for color scaling."""
        return max(self.current_time, 1)


class WaterMazeVisualizer:
    """Visualizes the DFS water maze animation."""
    
    def __init__(self, maze: WaterMaze, speed=50):
        """
        Initialize the visualizer.
        
        Args:
            maze: WaterMaze instance
            speed: Animation speed (milliseconds between frames)
        """
        self.maze = maze
        self.speed = speed
        self.fig, self.ax = plt.subplots(figsize=(12, 12))
        self.ax.set_xlim(-0.5, maze.width - 0.5)
        self.ax.set_ylim(-0.5, maze.height - 0.5)
        self.ax.set_aspect('equal')
        self.ax.invert_yaxis()  # So (0,0) is top-left
        self.ax.set_title('DFS Water Maze Simulation', fontsize=16, fontweight='bold')
        self.ax.axis('off')
        
        # Create initial visualization
        self.im = None
        self.update_display()
        
    def update_display(self):
        """Update the display with current maze state."""
        self.ax.clear()
        self.ax.set_xlim(-0.5, self.maze.width - 0.5)
        self.ax.set_ylim(-0.5, self.maze.height - 0.5)
        self.ax.set_aspect('equal')
        self.ax.invert_yaxis()
        self.ax.set_title('DFS Water Maze Simulation', fontsize=16, fontweight='bold')
        self.ax.axis('off')
        
        # Draw walls
        for i in range(self.maze.height):
            for j in range(self.maze.width):
                if self.maze.maze[i, j] == 1:
                    rect = patches.Rectangle((j-0.5, i-0.5), 1, 1, 
                                           linewidth=1, edgecolor='black',
                                           facecolor='#333333', zorder=1)
                    self.ax.add_patch(rect)
        
        # Draw water states as rectangles with time-based coloring
        water_state = self.maze.get_water_coverage()
        max_time = self.maze.get_max_time()
        
        for i in range(self.maze.height):
            for j in range(self.maze.width):
                if self.maze.maze[i, j] == 0:  # Only draw on open cells
                    state = water_state[i, j]
                    time_step = self.maze.exploration_time[i, j]
                    
                    if state > 0:  # Wet or explored
                        # Calculate color based on time step
                        # Newer = brighter blue, older = darker blue
                        if time_step >= 0:
                            # Normalize time to 0-1 range (0 = newest, 1 = oldest)
                            age_ratio = time_step / max(max_time, 1)
                            # Clamp to reasonable range
                            age_ratio = max(0.0, min(1.0, age_ratio))
                            
                            # Bright blue (#0066ff) for new, darker blue for old
                            # Start with bright blue RGB: (0, 102, 255)
                            # End with dark blue RGB: (0, 20, 80)
                            r = int(0)
                            g = int(102 - 82 * age_ratio)  # 102 -> 20
                            b = int(255 - 175 * age_ratio)  # 255 -> 80
                            
                            color = f'#{r:02x}{g:02x}{b:02x}'
                            # Darker edge for contrast
                            edge_r = max(0, r - 10)
                            edge_g = max(0, g - 20)
                            edge_b = max(0, b - 30)
                            edge_color = f'#{edge_r:02x}{edge_g:02x}{edge_b:02x}'
                        else:
                            # Default bright blue for cells just added
                            color = '#0066ff'
                            edge_color = '#0033cc'
                        
                        # Draw as rectangle (water flow) - fills most of the cell
                        rect = patches.Rectangle((j-0.45, i-0.45), 0.9, 0.9,
                                               facecolor=color,
                                               edgecolor=edge_color,
                                               linewidth=1.5, zorder=3 if state == 1 else 2)
                        self.ax.add_patch(rect)
        
        # Draw start
        start_rect = patches.Rectangle((self.maze.start[1]-0.4, self.maze.start[0]-0.4), 
                                      0.8, 0.8, linewidth=2, edgecolor='green',
                                      facecolor='lightgreen', zorder=4)
        self.ax.add_patch(start_rect)
        self.ax.text(self.maze.start[1], self.maze.start[0], 'S', 
                    ha='center', va='center', fontsize=14, fontweight='bold', zorder=5)
        
        # Draw goal
        goal_rect = patches.Rectangle((self.maze.goal[1]-0.4, self.maze.goal[0]-0.4), 
                                     0.8, 0.8, linewidth=2, edgecolor='red',
                                     facecolor='lightcoral', zorder=4)
        self.ax.add_patch(goal_rect)
        self.ax.text(self.maze.goal[1], self.maze.goal[0], 'G', 
                    ha='center', va='center', fontsize=14, fontweight='bold', zorder=5)
        
        # Draw stack visualization (current path)
        if self.maze.stack:
            path_x = [pos[1] for pos in self.maze.stack]
            path_y = [pos[0] for pos in self.maze.stack]
            self.ax.plot(path_x, path_y, 'g-', linewidth=3, alpha=0.5, zorder=1)
        
        # Add info text
        info = f"Explored: {len(self.maze.visited)} cells | "
        info += f"Stack size: {len(self.maze.stack)}"
        if self.maze.found_goal:
            info += " | GOAL FOUND!"
        self.ax.text(0.5, -0.3, info, transform=self.ax.transAxes,
                    fontsize=10, ha='left', va='top')
        
        plt.tight_layout()
    
    def animate(self, frame):
        """Animation function called for each frame."""
        if self.maze.dfs_step():
            self.update_display()
        return []
    
    def run(self):
        """Run the animation."""
        # Pre-compute some steps for smoother animation
        max_frames = self.maze.width * self.maze.height * 2
        
        anim = FuncAnimation(self.fig, self.animate, frames=max_frames,
                           interval=self.speed, repeat=False, blit=False)
        plt.show()
        return anim


def main():
    """Main function to run the DFS water maze simulation."""
    print("DFS Water Maze Simulation")
    print("=" * 50)
    print("This simulation shows how Depth-First Search explores a maze")
    print("by visualizing water spreading through the maze.")
    print("\nLegend:")
    print("  Green square (S) = Start")
    print("  Red square (G) = Goal")
    print("  Blue circles = Water spreading (DFS exploration)")
    print("  Light blue = Previously explored cells")
    print("  Green line = Current path (DFS stack)")
    print("\nPress Ctrl+C to exit\n")
    
    # Create maze
    maze = WaterMaze(width=15, height=15, start=(1, 1), goal=(13, 13))
    
    # Create visualizer
    visualizer = WaterMazeVisualizer(maze, speed=100)
    
    # Run animation
    try:
        visualizer.run()
    except KeyboardInterrupt:
        print("\n\nSimulation stopped by user.")


if __name__ == "__main__":
    main()
