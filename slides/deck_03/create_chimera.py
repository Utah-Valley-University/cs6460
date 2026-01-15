#!/usr/bin/env python3
"""
Script to create a chimera by blending turtle and rabbit images.
Combines slide14_img01.png (UCS/turtle) and slide14_img02.png (Greedy/rabbit)
to create a new image for A* Search.
"""

from PIL import Image, ImageEnhance
import os

def create_chimera(turtle_path, rabbit_path, output_path, blend_ratio=0.5):
    """
    Create a chimera by blending turtle and rabbit images.
    
    Args:
        turtle_path: Path to turtle image (UCS)
        rabbit_path: Path to rabbit image (Greedy)
        output_path: Path to save the chimera
        blend_ratio: How much of each image (0.0 = all turtle, 1.0 = all rabbit)
    """
    # Load images
    turtle_img = Image.open(turtle_path).convert('RGBA')
    rabbit_img = Image.open(rabbit_path).convert('RGBA')
    
    # Resize images to match (use the larger dimensions)
    max_width = max(turtle_img.width, rabbit_img.width)
    max_height = max(turtle_img.height, rabbit_img.height)
    
    turtle_img = turtle_img.resize((max_width, max_height), Image.Resampling.LANCZOS)
    rabbit_img = rabbit_img.resize((max_width, max_height), Image.Resampling.LANCZOS)
    
    # Create a blended image
    # Method 1: Simple alpha blend
    blended = Image.blend(turtle_img, rabbit_img, blend_ratio)
    
    # Method 2: Alternative - overlay with transparency
    # You can experiment with different blend modes
    # blended = Image.composite(rabbit_img, turtle_img, rabbit_img)
    
    # Save the result
    blended.save(output_path, 'PNG')
    print(f"Chimera created and saved to: {output_path}")
    return blended

def create_chimera_advanced(turtle_path, rabbit_path, output_path):
    """
    Create a more sophisticated chimera by combining different parts.
    This version tries to blend the images more creatively.
    """
    turtle_img = Image.open(turtle_path).convert('RGBA')
    rabbit_img = Image.open(rabbit_path).convert('RGBA')
    
    # Resize to match
    max_width = max(turtle_img.width, rabbit_img.width)
    max_height = max(turtle_img.height, rabbit_img.height)
    
    turtle_img = turtle_img.resize((max_width, max_height), Image.Resampling.LANCZOS)
    rabbit_img = rabbit_img.resize((max_width, max_height), Image.Resampling.LANCZOS)
    
    # Create a new image with weighted combination
    # This gives more turtle (slow, steady) but with rabbit features (fast, eager)
    result = Image.new('RGBA', (max_width, max_height))
    
    # Blend: 60% turtle (steady base) + 40% rabbit (speed features)
    turtle_weight = 0.6
    rabbit_weight = 0.4
    
    # Manual pixel blending for more control
    turtle_pixels = turtle_img.load()
    rabbit_pixels = rabbit_img.load()
    result_pixels = result.load()
    
    for y in range(max_height):
        for x in range(max_width):
            t_pixel = turtle_pixels[x, y]
            r_pixel = rabbit_pixels[x, y]
            
            # Blend RGB channels
            r = int(t_pixel[0] * turtle_weight + r_pixel[0] * rabbit_weight)
            g = int(t_pixel[1] * turtle_weight + r_pixel[1] * rabbit_weight)
            b = int(t_pixel[2] * turtle_weight + r_pixel[2] * rabbit_weight)
            a = max(t_pixel[3], r_pixel[3])  # Use max alpha
            
            result_pixels[x, y] = (r, g, b, a)
    
    result.save(output_path, 'PNG')
    print(f"Advanced chimera created and saved to: {output_path}")
    return result

if __name__ == "__main__":
    # Paths relative to script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(script_dir, 'assets')
    
    turtle_path = os.path.join(assets_dir, 'slide14_img01.png')  # UCS (turtle)
    rabbit_path = os.path.join(assets_dir, 'slide14_img02.png')   # Greedy (rabbit)
    
    # Create output path
    output_path = os.path.join(assets_dir, 'slide14_chimera.png')
    
    # Check if images exist
    if not os.path.exists(turtle_path):
        print(f"Error: Turtle image not found at {turtle_path}")
        exit(1)
    if not os.path.exists(rabbit_path):
        print(f"Error: Rabbit image not found at {rabbit_path}")
        exit(1)
    
    print("Creating chimera (turtle + rabbit blend)...")
    print(f"Turtle (UCS): {turtle_path}")
    print(f"Rabbit (Greedy): {rabbit_path}")
    print()
    
    # Try simple blend first
    print("Method 1: Simple 50/50 blend")
    create_chimera(turtle_path, rabbit_path, output_path, blend_ratio=0.5)
    
    # Try advanced blend
    print("\nMethod 2: Advanced 60/40 blend (turtle-heavy)")
    advanced_output = os.path.join(assets_dir, 'slide14_chimera_advanced.png')
    create_chimera_advanced(turtle_path, rabbit_path, advanced_output)
    
    print("\nDone! Check the output images:")
    print(f"  - {output_path}")
    print(f"  - {advanced_output}")
    print("\nYou can adjust the blend_ratio parameter (0.0-1.0) to change the mix.")
