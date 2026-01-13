#!/usr/bin/env python3
"""
BFS Water Maze Simulation with Weighted Edges (Shallow/Deep Water)

This simulation visualizes Breadth-First Search (BFS) on a maze with weighted edges:
- Shallow water (cost 1) - light blue
- Deep water (cost 2) - dark blue

BFS IGNORES the weights and treats all edges as cost 1, spreading level by level
in concentric circles. This contrasts with UCS which would spread by cost contours.

This is for slide 48: "Guess Which One - BFS or UCS?"

Author: Generated for CS 6460
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
from collections import deque
import time


class WeightedWaterMaze:
    """Represents a maze with weighted edges (shallow/deep water) where BFS ignores weights."""
    
    def __init__(self, width=15, height=15, start=(1, 1), goal=None):
        """
        Initialize the weighted water maze.
        
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
        
        # Create maze with weighted edges
        # 0 = open (shallow water, cost 1)
        # 1 = wall
        # 2 = deep water (cost 2)
        self.maze, self.edge_costs = self._generate_weighted_maze()
        
        # Water state: 0 = dry, 1 = wet (in queue), 2 = explored
        self.water_state = np.zeros((height, width), dtype=int)
        self.water_state[start[0], start[1]] = 1  # Start is wet
        
        # Time step tracking - when was each cell explored
        self.exploration_time = np.full((height, width), -1, dtype=int)
        self.exploration_time[start[0], start[1]] = 0  # Start at time 0
        self.current_time = 0
        
        # BFS tracking - use queue (FIFO)
        # BFS IGNORES edge costs - treats all edges as cost 1
        self.queue = deque([start])
        self.visited = {start}
        self.exploration_order = []
        self.found_goal = False
        self.distances = {start: 0}  # Distance in STEPS (not cost) - BFS ignores weights
        
    def _generate_weighted_maze(self):
        """
        Generate a maze with shallow water (cost 1) and deep water (cost 2).
        Creates a pattern where some areas are shallow and some are deep.
        """
        maze = np.ones((self.height, self.width), dtype=int)
        edge_costs = {}  # Dictionary: (from_pos, to_pos) -> cost
        
        # Create open paths with varying water depths
        for i in range(1, self.height-1):
            for j in range(1, self.width-1):
                # Create a pattern with some walls
                if (i + j) % 3 != 0:
                    # Alternate between shallow (1) and deep (2) water
                    # Create interesting pattern: left side shallow, right side deep
                    if j < self.width // 2:
                        maze[i, j] = 0  # Shallow water (cost 1)
                    else:
                        maze[i, j] = 2  # Deep water (cost 2)
        
        # Ensure start and goal are shallow water
        maze[self.start[0], self.start[1]] = 0
        maze[self.goal[0], self.goal[1]] = 0
        
        # Create a clear path with mixed water depths
        # Left side: shallow water
        for i in range(1, self.height-1):
            maze[i, 1] = 0  # Shallow
            maze[i, 2] = 0  # Shallow
            maze[i, 3] = 0  # Shallow
        
        # Middle: mix of shallow and deep
        for i in range(1, self.height-1):
            if i % 2 == 0:
                maze[i, self.width // 2] = 0  # Shallow
            else:
                maze[i, self.width // 2] = 2  # Deep
        
        # Right side: deep water
        for i in range(1, self.height-1):
            maze[i, self.width-2] = 2  # Deep
            maze[i, self.width-3] = 2  # Deep
        
        # Top and bottom rows: mix
        for j in range(1, self.width-1):
            if j < self.width // 2:
                maze[1, j] = 0  # Shallow
                maze[self.height-2, j] = 0  # Shallow
            else:
                maze[1, j] = 2  # Deep
                maze[self.height-2, j] = 2  # Deep
        
        # Build edge cost dictionary
        # For each open cell, determine cost to move to neighbors
        for i in range(self.height):
            for j in range(self.width):
                if maze[i, j] != 1:  # Not a wall
                    pos = (i, j)
                    current_cost = 1 if maze[i, j] == 0 else 2
                    
                    # Check neighbors
                    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                    for dr, dc in directions:
                        ni, nj = i + dr, j + dc
                        if (0 <= ni < self.height and 0 <= nj < self.width and 
                            maze[ni, nj] != 1):
                            neighbor_pos = (ni, nj)
                            # Cost is based on the destination cell's water depth
                            neighbor_cost = 1 if maze[ni, nj] == 0 else 2
                            edge_costs[(pos, neighbor_pos)] = neighbor_cost
        
        return maze, edge_costs
    
    def get_neighbors(self, pos):
        """
        Get valid neighboring positions (up, down, left, right).
        BFS ignores edge costs - just returns all valid neighbors.
        """
        row, col = pos
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if (0 <= new_row < self.height and 
                0 <= new_col < self.width and
                self.maze[new_row, new_col] != 1 and  # Not a wall
                (new_row, new_col) not in self.visited):
                neighbors.append((new_row, new_col))
        
        return neighbors
    
    def get_edge_cost(self, from_pos, to_pos):
        """Get the cost of moving from from_pos to to_pos."""
        return self.edge_costs.get((from_pos, to_pos), 1)
    
    def bfs_step(self):
        """
        Perform one step of BFS exploration - process all nodes at current level.
        BFS IGNORES edge costs - treats all edges as cost 1 (one step).
        """
        if not self.queue or self.found_goal:
            return False
        
        # Get current distance level (in STEPS, not cost)
        if not self.queue:
            return False
        
        current_distance = self.distances[self.queue[0]]
        
        # Process all nodes at the current distance level together
        nodes_at_level = []
        while self.queue and self.distances[self.queue[0]] == current_distance:
            current = self.queue.popleft()
            nodes_at_level.append(current)
        
        # Mark all nodes at this level as explored at the same time step
        for current in nodes_at_level:
            if self.water_state[current[0], current[1]] == 1:
                self.water_state[current[0], current[1]] = 2
                self.exploration_time[current[0], current[1]] = self.current_time
                self.exploration_order.append(current)
            
            # Check if goal reached
            if current == self.goal:
                self.found_goal = True
                self.current_time += 1
                return True
            
            # Get unvisited neighbors
            neighbors = self.get_neighbors(current)
            
            # BFS: add all neighbors to queue (breadth first)
            # IGNORES edge costs - all neighbors are at distance + 1
            for next_pos in neighbors:
                self.queue.append(next_pos)
                self.visited.add(next_pos)
                self.water_state[next_pos[0], next_pos[1]] = 1  # Wet (in queue)
                # Distance is in STEPS, not cost - BFS ignores weights
                self.distances[next_pos] = current_distance + 1
        
        # Increment time after processing entire level
        self.current_time += 1
        return True
    
    def get_water_coverage(self):
        """Get current water coverage for visualization."""
        return self.water_state.copy()
    
    def get_max_time(self):
        """Get maximum exploration time for color scaling."""
        return max(self.current_time, 1)


class WeightedWaterMazeVisualizer:
    """Visualizes the BFS water maze animation with weighted edges."""
    
    def __init__(self, maze: WeightedWaterMaze, speed=100):
        """
        Initialize the visualizer.
        
        Args:
            maze: WeightedWaterMaze instance
            speed: Animation speed (milliseconds between frames)
        """
        self.maze = maze
        self.speed = speed
        self.fig, self.ax = plt.subplots(figsize=(14, 14))
        self.ax.set_xlim(-0.5, maze.width - 0.5)
        self.ax.set_ylim(-0.5, maze.height - 0.5)
        self.ax.set_aspect('equal')
        self.ax.invert_yaxis()  # So (0,0) is top-left
        self.ax.set_title('Water Maze Simulation - Guess: BFS or UCS?', 
                         fontsize=16, fontweight='bold')
        self.ax.axis('off')
        
        # Create initial visualization
        self.update_display()
        
    def update_display(self):
        """Update the display with current maze state."""
        self.ax.clear()
        self.ax.set_xlim(-0.5, self.maze.width - 0.5)
        self.ax.set_ylim(-0.5, self.maze.height - 0.5)
        self.ax.set_aspect('equal')
        self.ax.invert_yaxis()
        self.ax.set_title('Water Maze Simulation - Guess: BFS or UCS?', 
                         fontsize=16, fontweight='bold')
        self.ax.axis('off')
        
        # Draw walls
        for i in range(self.maze.height):
            for j in range(self.maze.width):
                if self.maze.maze[i, j] == 1:
                    rect = patches.Rectangle((j-0.5, i-0.5), 1, 1, 
                                           linewidth=1, edgecolor='black',
                                           facecolor='#333333', zorder=1)
                    self.ax.add_patch(rect)
        
        # Draw water depths (background)
        for i in range(self.maze.height):
            for j in range(self.maze.width):
                if self.maze.maze[i, j] == 0:  # Shallow water
                    # Light blue background for shallow water
                    rect = patches.Rectangle((j-0.5, i-0.5), 1, 1,
                                           linewidth=0.5, edgecolor='#88ccff',
                                           facecolor='#e6f5ff', zorder=0, alpha=0.3)
                    self.ax.add_patch(rect)
                elif self.maze.maze[i, j] == 2:  # Deep water
                    # Dark blue background for deep water
                    rect = patches.Rectangle((j-0.5, i-0.5), 1, 1,
                                           linewidth=0.5, edgecolor='#004488',
                                           facecolor='#cce6ff', zorder=0, alpha=0.3)
                    self.ax.add_patch(rect)
        
        # Draw water states (spreading water)
        water_state = self.maze.get_water_coverage()
        max_time = self.maze.get_max_time()
        
        for i in range(self.maze.height):
            for j in range(self.maze.width):
                if self.maze.maze[i, j] != 1:  # Not a wall
                    state = water_state[i, j]
                    time_step = self.maze.exploration_time[i, j]
                    
                    if state > 0:  # Wet or explored
                        # Calculate color based on time step
                        if time_step >= 0:
                            time_for_color = time_step
                        elif state == 1:  # In queue, use current time (next level)
                            time_for_color = self.maze.current_time
                        else:
                            time_for_color = 0
                        
                        # Normalize time to 0-1 range
                        age_ratio = time_for_color / max(max_time, 1)
                        age_ratio = max(0.0, min(1.0, age_ratio))
                        
                        # Bright blue for new, darker blue for old
                        r = int(0)
                        g = int(102 - 82 * age_ratio)  # 102 -> 20
                        b = int(255 - 175 * age_ratio)  # 255 -> 80
                        
                        color = f'#{r:02x}{g:02x}{b:02x}'
                        edge_r = max(0, r - 10)
                        edge_g = max(0, g - 20)
                        edge_b = max(0, b - 30)
                        edge_color = f'#{edge_r:02x}{edge_g:02x}{edge_b:02x}'
                        
                        # Draw as rectangle (water flow)
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
        
        # Add legend
        legend_y = -0.5
        self.ax.text(0, legend_y, 'Shallow water (cost 1)', 
                    fontsize=10, color='#0066cc', ha='left', va='top')
        self.ax.text(self.maze.width/2, legend_y, 'Deep water (cost 2)', 
                    fontsize=10, color='#004488', ha='left', va='top')
        
        # Add info text
        info = f"Explored: {len(self.maze.visited)} cells | "
        info += f"Queue size: {len(self.maze.queue)} | "
        info += f"Steps from start: {self.maze.current_time}"
        if self.maze.found_goal:
            info += " | GOAL FOUND!"
            if self.maze.goal in self.maze.distances:
                info += f" (Steps: {self.maze.distances[self.maze.goal]})"
        self.ax.text(0.5, -0.3, info, transform=self.ax.transAxes,
                    fontsize=10, ha='left', va='top')
        
        # Add hint
        hint = "Hint: Does water spread by number of steps or by cost?"
        self.ax.text(0.5, 1.02, hint, transform=self.ax.transAxes,
                    fontsize=11, ha='center', va='bottom', 
                    style='italic', color='#666666')
        
        plt.tight_layout()
    
    def animate(self, frame):
        """Animation function called for each frame."""
        if self.maze.bfs_step():
            self.update_display()
        return []
    
    def run(self):
        """Run the animation."""
        max_frames = self.maze.width * self.maze.height * 2
        
        anim = FuncAnimation(self.fig, self.animate, frames=max_frames,
                           interval=self.speed, repeat=False, blit=False)
        plt.show()
        return anim


def main():
    """Main function to run the BFS water maze simulation."""
    print("=" * 60)
    print("Water Maze Simulation - Guess: BFS or UCS?")
    print("=" * 60)
    print("\nThis maze has:")
    print("  - Shallow water (cost 1) - light blue background")
    print("  - Deep water (cost 2) - dark blue background")
    print("\nWatch how the water spreads:")
    print("  - Does it spread in concentric circles (by steps)?")
    print("  - Or does it spread by cost (shallow first, then deep)?")
    print("\nLegend:")
    print("  Green square (S) = Start")
    print("  Red square (G) = Goal")
    print("  Light blue background = Shallow water (cost 1)")
    print("  Dark blue background = Deep water (cost 2)")
    print("  Bright blue spreading = Water exploring the maze")
    print("\nPress Ctrl+C to exit\n")
    
    # Create maze
    maze = WeightedWaterMaze(width=15, height=15, start=(1, 1), goal=(13, 13))
    
    # Create visualizer
    visualizer = WeightedWaterMazeVisualizer(maze, speed=150)
    
    # Run animation
    try:
        visualizer.run()
    except KeyboardInterrupt:
        print("\n\nSimulation stopped by user.")


if __name__ == "__main__":
    main()
