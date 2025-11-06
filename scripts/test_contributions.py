#!/usr/bin/env python3
"""
Test script to verify GitHub contributions fetcher
"""

import os
import sys

# Set a test token if available
if len(sys.argv) > 1:
    os.environ['GITHUB_TOKEN'] = sys.argv[1]

from fetch_github_contributions import GitHubContributionsFetcher

def main():
    print("=" * 60)
    print("GitHub Contributions Fetcher - Test Script")
    print("=" * 60)
    print()
    
    # Check for token
    token = os.getenv('GH_TOKEN') or os.getenv('GITHUB_TOKEN')
    if not token:
        print("⚠️  No GitHub token found!")
        print()
        print("To test with a token, run:")
        print("  python test_contributions.py YOUR_GITHUB_TOKEN")
        print()
        print("Or set environment variable:")
        print("  $env:GITHUB_TOKEN='your_token_here'")
        print("  python test_contributions.py")
        print()
    else:
        print(f"✅ Token found: {token[:4]}...{token[-4:]}")
        print()
    
    # Test the fetcher
    print("Testing contributions fetcher...")
    print("-" * 60)
    
    fetcher = GitHubContributionsFetcher()
    data = fetcher.fetch_contributions()
    
    print()
    print("=" * 60)
    print("Results:")
    print("=" * 60)
    
    if data.get('fallback', False):
        print("⚠️  Using fallback data (API call failed or no token)")
    else:
        print("✅ Successfully fetched data from GitHub API")
    
    print()
    print(f"  Total Contributions: {data.get('total_contributions', 0):,}")
    print(f"  This Year:          {data.get('this_year_contributions', 0):,}")
    print(f"  Total Commits:      {data.get('total_commits', 0):,}")
    print(f"  Total Issues:       {data.get('total_issues', 0):,}")
    print(f"  Total PRs:          {data.get('total_prs', 0):,}")
    print(f"  Total Reviews:      {data.get('total_reviews', 0):,}")
    print()
    print(f"  Followers:          {data.get('followers', 0):,}")
    print(f"  Public Repos:       {data.get('public_repos', 0):,}")
    print(f"  Total Stars:        {data.get('total_stars', 0):,}")
    print(f"  Total Forks:        {data.get('total_forks', 0):,}")
    print()
    print(f"  Updated:            {data.get('updated_at', 'N/A')}")
    print()
    print("=" * 60)

if __name__ == "__main__":
    main()
