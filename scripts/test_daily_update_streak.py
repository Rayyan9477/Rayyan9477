#!/usr/bin/env python3
"""Test the daily_update script's streak fetching capability"""

import sys
import os

# Add the scripts directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from daily_update import DailyUpdater

# Create updater instance
updater = DailyUpdater()

print("Testing _get_current_streak method...")
print("=" * 60)

# Test the streak fetching
streak = updater._get_current_streak()

if streak:
    print(f"✅ Successfully fetched streak: {streak}")
    print(f"\nThis will update the badge to: 🔥_Current_Streak-{streak}-")
else:
    print("❌ Failed to fetch streak (will preserve existing value)")

print("=" * 60)
