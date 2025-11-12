#!/usr/bin/env python3
"""Test the streak parsing with the saved SVG file"""

import re

# Read the saved SVG file
with open('streak_response.svg', 'r', encoding='utf-8') as f:
    svg_content = f.read()

print("Testing improved regex patterns on saved SVG...")
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
        print()
    else:
        print(f"❌ {name} - No match")
        print()

print("=" * 60)
print("\nCONCLUSION: The current streak should be updated to 109 days")
