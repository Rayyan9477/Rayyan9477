#!/usr/bin/env python3
"""
Debug Streak Script - Fetch and display current GitHub streak
"""

import os
import re
import requests
from datetime import datetime, timedelta

def get_streak_from_api():
    """Fetch current streak from GitHub Streak Stats API"""
    username = 'Rayyan9477'
    
    # Try both streak stats services
    streak_urls = [
        f"https://streak-stats.demolab.com/?user={username}&theme=tokyonight",
        f"https://github-readme-streak-stats.herokuapp.com/?user={username}&theme=tokyonight"
    ]
    
    for url in streak_urls:
        print(f"\nTrying: {url}")
        try:
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                svg_content = response.text
                print(f"✅ Got response from {url}")
                
                # Try multiple patterns to parse the streak
                patterns = [
                    (r'<text[^>]*>Current Streak</text>\s*<text[^>]*>(\d+)</text>', 'Pattern 1'),
                    (r'Current Streak</text><text[^>]*>(\d+)</text>', 'Pattern 2'),
                    (r'current-streak[^>]*>(\d+)<', 'Pattern 3'),
                    (r'<text[^>]*data-testid="current-streak-count"[^>]*>(\d+)</text>', 'Pattern 4'),
                    (r'<text[^>]*id="curr-streak-num"[^>]*>(\d+)</text>', 'Pattern 5')
                ]
                
                for pattern, name in patterns:
                    match = re.search(pattern, svg_content, re.IGNORECASE)
                    if match:
                        streak = match.group(1)
                        print(f"✅ {name} matched: {streak} days")
                        return streak
                
                # If no pattern matched, let's save the SVG for inspection
                print("\n⚠️ No pattern matched. Saving SVG for inspection...")
                with open('streak_debug.svg', 'w', encoding='utf-8') as f:
                    f.write(svg_content)
                print("Saved to streak_debug.svg")
                
                # Let's also print a snippet
                print("\nSVG snippet (first 1000 chars):")
                print(svg_content[:1000])
                
        except Exception as e:
            print(f"❌ Error: {e}")
            continue
    
    return None

def get_streak_from_graphql():
    """Fetch current streak using GitHub GraphQL API"""
    token = os.getenv('GH_TOKEN') or os.getenv('GITHUB_TOKEN')
    if not token:
        print("\n⚠️ No GitHub token found")
        return None
    
    username = 'Rayyan9477'
    headers = {
        'Authorization': f'bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Get contribution calendar for the past year
    today = datetime.now()
    one_year_ago = today - timedelta(days=365)
    
    query = """
    query($username: String!, $from: DateTime!, $to: DateTime!) {
      user(login: $username) {
        contributionsCollection(from: $from, to: $to) {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                contributionCount
                date
              }
            }
          }
        }
      }
    }
    """
    
    variables = {
        'username': username,
        'from': one_year_ago.isoformat(),
        'to': today.isoformat()
    }
    
    try:
        print("\nFetching from GitHub GraphQL API...")
        response = requests.post(
            'https://api.github.com/graphql',
            json={'query': query, 'variables': variables},
            headers=headers,
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if 'errors' in data:
                print(f"❌ GraphQL errors: {data['errors']}")
                return None
            
            calendar = data.get('data', {}).get('user', {}).get('contributionsCollection', {}).get('contributionCalendar', {})
            total_contributions = calendar.get('totalContributions', 0)
            weeks = calendar.get('weeks', [])
            
            print(f"✅ Total contributions this year: {total_contributions}")
            
            # Calculate current streak
            current_streak = 0
            days = []
            for week in weeks:
                days.extend(week.get('contributionDays', []))
            
            # Reverse to start from today and go backwards
            days.reverse()
            
            print(f"\nTotal days to analyze: {len(days)}")
            print("\nLast 10 days of contributions:")
            for i, day in enumerate(days[:10]):
                date = day.get('date')
                count = day.get('contributionCount', 0)
                print(f"  {date}: {count} contributions")
            
            # Count streak
            for day in days:
                if day.get('contributionCount', 0) > 0:
                    current_streak += 1
                else:
                    break
            
            print(f"\n✅ Current streak: {current_streak} days")
            return current_streak
        else:
            print(f"❌ GraphQL API error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    return None

if __name__ == "__main__":
    print("=" * 60)
    print("GitHub Streak Debug Tool")
    print("=" * 60)
    
    print("\n1. Fetching from Streak Stats API...")
    api_streak = get_streak_from_api()
    
    print("\n" + "=" * 60)
    print("\n2. Fetching from GitHub GraphQL API...")
    graphql_streak = get_streak_from_graphql()
    
    print("\n" + "=" * 60)
    print("\nSUMMARY:")
    print(f"  Streak Stats API: {api_streak if api_streak else 'Failed'}")
    print(f"  GitHub GraphQL API: {graphql_streak if graphql_streak else 'Failed'}")
    print("=" * 60)
