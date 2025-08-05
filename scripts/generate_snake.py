#!/usr/bin/env python3
"""
Script to generate GitHub contribution snake
"""

import requests
import os

def generate_snake():
    """Generate contribution snake using Platane/snk API"""
    
    # Create assets directory if it doesn't exist
    os.makedirs('assets', exist_ok=True)
    
    # Generate snake using Platane/snk API
    username = "Rayyan9477"
    
    # Generate SVG snake
    svg_url = f"https://raw.githubusercontent.com/Platane/snk/output/{username}/github-contribution-grid-snake.svg"
    
    try:
        response = requests.get(svg_url)
        if response.status_code == 200:
            with open('assets/github-contribution-grid-snake.svg', 'w', encoding='utf-8') as f:
                f.write(response.text)
            print("✅ Generated github-contribution-grid-snake.svg")
        else:
            print(f"❌ Failed to generate SVG: {response.status_code}")
    except Exception as e:
        print(f"❌ Error generating SVG: {e}")
    
    # Generate dark theme SVG
    dark_svg_url = f"https://raw.githubusercontent.com/Platane/snk/output/{username}/github-contribution-grid-snake-dark.svg"
    
    try:
        response = requests.get(dark_svg_url)
        if response.status_code == 200:
            with open('assets/github-contribution-grid-snake-dark.svg', 'w', encoding='utf-8') as f:
                f.write(response.text)
            print("✅ Generated github-contribution-grid-snake-dark.svg")
        else:
            print(f"❌ Failed to generate dark SVG: {response.status_code}")
    except Exception as e:
        print(f"❌ Error generating dark SVG: {e}")

if __name__ == "__main__":
    generate_snake() 