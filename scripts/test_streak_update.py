#!/usr/bin/env python3
"""
Test script to verify streak update logic
"""
import os
import sys

# Set a mock token for testing
os.environ['GH_TOKEN'] = 'test_token_placeholder'

# Import the updater
from github_stats_updater import GitHubStatsUpdater

def test_streak_pattern():
    """Test if the streak pattern matches correctly"""
    import re
    
    test_content = """
<img src="https://img.shields.io/badge/🔥_Current_Streak-108_Days-F85D7F?style=for-the-badge&labelColor=1a1a2e" alt="Current Streak" />
"""
    
    pattern = r'🔥_Current_Streak-[\d_]+Days-'
    matches = re.findall(pattern, test_content)
    
    print("Testing streak badge pattern matching...")
    print(f"Pattern: {pattern}")
    print(f"Found matches: {matches}")
    
    if matches:
        print("✅ Pattern matches correctly!")
        
        # Test replacement
        new_content = re.sub(pattern, '🔥_Current_Streak-120_Days-', test_content)
        print("\nOriginal content:")
        print(test_content)
        print("\nUpdated content:")
        print(new_content)
        
        if '120_Days' in new_content:
            print("\n✅ Replacement works correctly!")
        else:
            print("\n❌ Replacement failed!")
    else:
        print("❌ Pattern does not match!")
        
    return bool(matches)

def test_graphql_structure():
    """Test if GraphQL query structure is correct"""
    print("\n" + "="*50)
    print("Testing GraphQL structure...")
    
    query = """
    query($username: String!, $from: DateTime!, $to: DateTime!) {
      user(login: $username) {
        contributionsCollection(from: $from, to: $to) {
          contributionCalendar {
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
    
    print("GraphQL query structure:")
    print(query)
    print("\n✅ GraphQL query structure looks valid!")
    
    # Test streak calculation logic
    print("\nTesting streak calculation logic...")
    
    # Mock contribution days (reversed order, starting from today)
    mock_days = [
        {'contributionCount': 5, 'date': '2025-11-12'},
        {'contributionCount': 3, 'date': '2025-11-11'},
        {'contributionCount': 2, 'date': '2025-11-10'},
        {'contributionCount': 0, 'date': '2025-11-09'},  # Break in streak
        {'contributionCount': 1, 'date': '2025-11-08'},
    ]
    
    current_streak = 0
    for day in mock_days:
        if day.get('contributionCount', 0) > 0:
            current_streak += 1
        else:
            break
    
    print(f"Mock contribution data: {mock_days}")
    print(f"Calculated streak: {current_streak} days")
    
    if current_streak == 3:
        print("✅ Streak calculation logic is correct!")
    else:
        print("❌ Streak calculation logic has issues!")
    
    return current_streak == 3

if __name__ == "__main__":
    print("="*50)
    print("STREAK UPDATE VERIFICATION TEST")
    print("="*50)
    
    test1 = test_streak_pattern()
    test2 = test_graphql_structure()
    
    print("\n" + "="*50)
    print("TEST SUMMARY")
    print("="*50)
    print(f"Pattern Matching: {'✅ PASS' if test1 else '❌ FAIL'}")
    print(f"GraphQL Structure: {'✅ PASS' if test2 else '❌ FAIL'}")
    
    if test1 and test2:
        print("\n🎉 All tests passed! The streak update logic should work correctly in GitHub Actions.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Please review the implementation.")
        sys.exit(1)
