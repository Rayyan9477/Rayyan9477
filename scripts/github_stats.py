#!/usr/bin/env python3
"""
GitHub Stats Fetcher
Fetches and formats GitHub statistics for the README
"""

import os
import requests
import json
from datetime import datetime, timedelta

class GitHubStatsFetcher:
    def __init__(self):
        self.token = os.getenv('GITHUB_TOKEN')
        if not self.token:
            raise ValueError("GITHUB_TOKEN environment variable is not set")
        self.username = 'Rayyan9477'
        self.headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.timeout = 10  # 10 seconds timeout for requests
    
    def get_user_stats(self):
        """Get basic user statistics"""
        url = f'https://api.github.com/users/{self.username}'
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            
            if response.status_code == 403:
                print("⚠️ Rate limit exceeded. Waiting before retry...")
                return {}
                
            data = response.json()
            return {
                'followers': data.get('followers', 0),
                'following': data.get('following', 0),
                'public_repos': data.get('public_repos', 0),
                'total_stars': self.get_total_stars(),
                'total_forks': self.get_total_forks(),
                'contributions_this_year': self.get_contributions_this_year()
            }
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching user stats: {e}")
            return {}
    
    def get_total_stars(self):
        """Get total stars across all repositories"""
        url = f'https://api.github.com/users/{self.username}/repos'
        total_stars = 0
        page = 1
        
        while True:
            response = requests.get(f'{url}?page={page}&per_page=100', headers=self.headers)
            if response.status_code != 200:
                break
                
            repos = response.json()
            if not repos:
                break
                
            total_stars += sum(repo.get('stargazers_count', 0) for repo in repos)
            page += 1
            
        return total_stars
    
    def get_total_forks(self):
        """Get total forks across all repositories"""
        url = f'https://api.github.com/users/{self.username}/repos'
        total_forks = 0
        page = 1
        
        while True:
            response = requests.get(f'{url}?page={page}&per_page=100', headers=self.headers)
            if response.status_code != 200:
                break
                
            repos = response.json()
            if not repos:
                break
                
            total_forks += sum(repo.get('forks_count', 0) for repo in repos)
            page += 1
            
        return total_forks
    
    def get_contributions_this_year(self):
        """Get contributions for the current year"""
        # This would require GraphQL API for accurate data
        # For now, return a placeholder
        return "1000+"
    
    def get_recent_activity(self, days=30):
        """Get recent activity from the last N days"""
        since = (datetime.now() - timedelta(days=days)).isoformat()
        url = f'https://api.github.com/users/{self.username}/events'
        
        response = requests.get(f'{url}?since={since}', headers=self.headers)
        if response.status_code == 200:
            events = response.json()
            return {
                'commits': len([e for e in events if e['type'] == 'PushEvent']),
                'issues': len([e for e in events if e['type'] == 'IssuesEvent']),
                'prs': len([e for e in events if e['type'] == 'PullRequestEvent']),
                'total_events': len(events)
            }
        return {}
    
    def generate_stats_badge(self):
        """Generate a custom stats badge"""
        stats = self.get_user_stats()
        activity = self.get_recent_activity()
        
        badge_data = {
            'schemaVersion': 1,
            'label': 'GitHub Stats',
            'message': f"{stats.get('public_repos', 0)} repos • {stats.get('total_stars', 0)} stars",
            'color': 'brightgreen',
            'style': 'for-the-badge'
        }
        
        return badge_data

if __name__ == "__main__":
    fetcher = GitHubStatsFetcher()
    stats = fetcher.get_user_stats()
    print(json.dumps(stats, indent=2))
