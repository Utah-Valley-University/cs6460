#!/usr/bin/env python3
"""
BFS Water Maze Simulation - Video Frame Generator

This version saves frames for video generation instead of showing interactive animation.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
from bfs_water_maze import WaterMaze


class WaterMazeVideoGenerator:
    """Generates video frames for BFS water maze simulation."""
    
    def __init__(self, maze: WaterMaze, output_dir="frames"):
        """
        Initialize the video generator.
        
        Args:
            maze: WaterMaze instance
            output_dir: Directory to save frames
        """
        self.maze = maze
        self.output_dir = output_dir
        self.frame_count = 0
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Setup figure
        self.fig, self.ax = plt.subplots(figsize=(12, 12))
        self.ax.set_xlim(-0.5, maze.width - 0.5)
        self.ax.set_ylim(-0.5, maze.height - 0.5)
        self.ax.set_aspect('equal')
        self.ax.invert_yaxis()
        self.ax.set_title('BFS Water Maze Simulation', fontsize=16, fontweight='bold')
        self.ax.axis('off')
        
    def draw_frame(self):
        """Draw and save a single frame."""
        self.ax.clear()
        self.ax.set_xlim(-0.5, self.maze.width - 0.5)
        self.ax.set_ylim(-0.5, self.maze.height - 0.5)
        self.ax.set_aspect('equal')
        self.ax.invert_yaxis()
        self.ax.set_title('BFS Water Maze Simulation', fontsize=16, fontweight='bold')
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
                        # For BFS: nodes at same level (distance) should have same color
                        # Use distance if time not set yet (for nodes in queue)
                        if time_step >= 0:
                            time_for_color = time_step
                        elif state == 1:  # In queue, use current time (next level)
                            time_for_color = self.maze.current_time
                        else:
                            time_for_color = 0
                        
                        # Normalize time to 0-1 range (0 = newest, 1 = oldest)
                        age_ratio = time_for_color / max(max_time, 1)
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
        
        # Note: Current level visualization removed - time-based coloring shows this better
        
        # Add info text
        info = f"Explored: {len(self.maze.visited)} cells | "
        info += f"Queue size: {len(self.maze.queue)}"
        if self.maze.found_goal:
            info += " | GOAL FOUND!"
            if self.maze.goal in self.maze.distances:
                info += f" (Distance: {self.maze.distances[self.maze.goal]})"
        self.ax.text(0.5, -0.3, info, transform=self.ax.transAxes,
                    fontsize=10, ha='left', va='top')
        
        plt.tight_layout()
        
        # Save frame
        filename = os.path.join(self.output_dir, f"frame_{self.frame_count:04d}.png")
        plt.savefig(filename, dpi=100, bbox_inches='tight')
        self.frame_count += 1
        
        print(f"Saved frame {self.frame_count}: {filename}")
    
    def generate_video(self, max_steps=None):
        """Generate all frames for the video."""
        if max_steps is None:
            max_steps = self.maze.width * self.maze.height * 2
        
        print(f"Generating video frames (max {max_steps} steps)...")
        
        # Save initial frame
        self.draw_frame()
        
        # Generate frames
        step = 0
        while step < max_steps and (self.maze.queue or not self.maze.found_goal):
            if self.maze.bfs_step():
                self.draw_frame()
                step += 1
            else:
                break
        
        # Save a few extra frames at the end
        for _ in range(10):
            self.draw_frame()
        
        print(f"\nGenerated {self.frame_count} frames in {self.output_dir}/")
        print(f"\nTo create a video, run:")
        print(f"  ffmpeg -r 10 -i {self.output_dir}/frame_%04d.png -c:v libx264 -pix_fmt yuv420p bfs_water_maze.mp4")


def main():
    """Main function to generate video frames."""
    print("BFS Water Maze - Video Frame Generator")
    print("=" * 50)
    
    # Create maze
    maze = WaterMaze(width=15, height=15, start=(1, 1), goal=(13, 13))
    
    # Create video generator
    generator = WaterMazeVideoGenerator(maze, output_dir="frames")
    
    # Generate frames
    generator.generate_video()


if __name__ == "__main__":
    main()
