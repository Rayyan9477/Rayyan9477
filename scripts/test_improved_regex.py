#!/usr/bin/env python3
"""Test the streak parsing with the improved regex"""

import re
import requests

# Fetch the SVG
response = requests.get('https://github-readme-streak-stats.herokuapp.com/?user=Rayyan9477', timeout=30)
svg_content = response.text

print("Testing improved regex patterns...")
print("=" * 60)

patterns = [
    (r'Current Streak.*?<text[^>]*>(\d+)</text>', 'Pattern 1: Current Streak...text'),
    (r'animation: currstreak[^>]*>\s*(\d+)\s*</text>', 'Pattern 2: animation currstreak'),
    (r'<text[^>]*>Current Streak</text>.*?<text[^>]*>(\d+)</text>', 'Pattern 3: Current Streak text...text'),
    (r'Current Streak</text><text[^>]*>(\d+)</text>', 'Pattern 4: Current Streak directly'),
]

for pattern, name in patterns:
    match = re.search(pattern, svg_content, re.IGNORECASE | re.DOTALL)
    if match:
        print(f"✅ {name}")
        print(f"   Matched: {match.group(1)} days")
    else:
        print(f"❌ {name} - No match")

print("=" * 60)
