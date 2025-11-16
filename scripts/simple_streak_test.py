import requests
import re

try:
    print("Fetching streak stats...")
    r = requests.get('https://github-readme-streak-stats.herokuapp.com/?user=Rayyan9477', timeout=30)
    print(f'Status: {r.status_code}')
    
    if r.status_code == 200:
        # Save to file for inspection
        with open('streak_response.svg', 'w', encoding='utf-8') as f:
            f.write(r.text)
        print("Saved response to streak_response.svg")
        
        # Try to find the current streak number
        patterns = [
            r'<text[^>]*>(\d+)</text>[^<]*<text[^>]*>Current Streak</text>',
            r'<text[^>]*>Current Streak</text>[^<]*<text[^>]*>(\d+)</text>',
            r'current-streak-number[^>]*>(\d+)',
            r'id="curr-streak-num"[^>]*>(\d+)',
        ]
        
        for i, pattern in enumerate(patterns, 1):
            match = re.search(pattern, r.text, re.IGNORECASE | re.DOTALL)
            if match:
                print(f'Pattern {i} found streak: {match.group(1)} days')
            else:
                print(f'Pattern {i}: No match')
        
        # Show a snippet
        print("\nFirst 2000 characters of response:")
        print(r.text[:2000])
    else:
        print(f"Failed with status {r.status_code}")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
