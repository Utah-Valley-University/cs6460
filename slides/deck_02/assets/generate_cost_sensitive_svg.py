#!/usr/bin/env python3
"""Generate SVG from Graphviz DOT file."""

import subprocess
import sys
import os

dot_file = "cost_sensitive_header.dot"
svg_file = "cost_sensitive_header.svg"

# Get the directory of this script
script_dir = os.path.dirname(os.path.abspath(__file__))
dot_path = os.path.join(script_dir, dot_file)
svg_path = os.path.join(script_dir, svg_file)

try:
    # Try to run graphviz dot command
    result = subprocess.run(
        ["dot", "-Tsvg", dot_path, "-o", svg_path],
        capture_output=True,
        text=True,
        check=True
    )
    print(f"Successfully generated {svg_file}")
    sys.exit(0)
except subprocess.CalledProcessError as e:
    print(f"Error running dot: {e.stderr}", file=sys.stderr)
    sys.exit(1)
except FileNotFoundError:
    print("Error: 'dot' command not found. Please install Graphviz.", file=sys.stderr)
    print("On Ubuntu/Debian: sudo apt-get install graphviz", file=sys.stderr)
    print("On macOS: brew install graphviz", file=sys.stderr)
    print("On Windows: Download from https://graphviz.org/download/", file=sys.stderr)
    sys.exit(1)
