#!/usr/bin/env python3
"""
Daily Update Script - Unified Automation
Updates README.md with daily quote, GitHub stats, and contribution snake
All updates are performed in a single operation for one commit per day
"""

import os
import re
import requests
import random
import json
import subprocess
import sys
from datetime import datetime
from typing import Dict, Any, Optional

class DailyUpdater:
    def __init__(self):
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.username = 'Rayyan9477'
        self.quotes_api_url = "https://api.quotable.io/random"
        
        # Check multiple locations for README.md
        possible_readme_paths = [
            os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'README.md'),  # Two dirs up
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'README.md'),  # Same dir as script
            os.path.join(os.getcwd(), 'README.md'),  # Current working directory
            'README.md'  # Relative path
        ]
        
        # Use the first README.md that exists
        self.readme_file = next((path for path in possible_readme_paths if os.path.exists(path)), 
                               possible_readme_paths[0])  # Default to first path if none exist
                               
        self.log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'daily_update.log')
        
        # Tech quotes as fallback
        self.tech_quotes = [
            {
                "content": "The best way to predict the future is to invent it.",
                "author": "Alan Kay"
            },
            {
                "content": "Code is like humor. When you have to explain it, it's bad.",
                "author": "Cory House"
            },
            {
                "content": "First, solve the problem. Then, write the code.",
                "author": "John Johnson"
            },
            {
                "content": "Any fool can write code that a computer can understand. Good programmers write code that humans can understand.",
                "author": "Martin Fowler"
            },
            {
                "content": "The only way to learn a new programming language is by writing programs in it.",
                "author": "Dennis Ritchie"
            },
            {
                "content": "Talk is cheap. Show me the code.",
                "author": "Linus Torvalds"
            },
            {
                "content": "Programs must be written for people to read, and only incidentally for machines to execute.",
                "author": "Harold Abelson"
            },
            {
                "content": "Simplicity is the ultimate sophistication.",
                "author": "Leonardo da Vinci"
            },
            {
                "content": "It's not a bug – it's an undocumented feature.",
                "author": "Anonymous"
            },
            {
                "content": "The computer was born to solve problems that did not exist before.",
                "author": "Bill Gates"
            },
            {
                "content": "Innovation distinguishes between a leader and a follower.",
                "author": "Steve Jobs"
            },
            {
                "content": "The only way to do great work is to love what you do.",
                "author": "Steve Jobs"
            }
        ]
        
        self.log("🚀 Daily Update Script Started")
    
    def log(self, message: str, level: str = "INFO"):
        """Log messages with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {level}: {message}"
        print(log_message)
        
        # Write to log file
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_message + '\n')
    
    def get_daily_quote(self) -> Dict[str, str]:
        """Get a daily inspirational quote"""
        try:
            # Try external API first
            response = requests.get(self.quotes_api_url, timeout=5)
            response.raise_for_status()
            
            if response.status_code == 200:
                data = response.json()
                content = data.get("content", "").strip()
                author = data.get("author", "Unknown").strip()
                
                if content and author and len(content) < 200:  # Reasonable length
                    self.log(f"✅ Fetched quote from API: '{content[:50]}...' by {author}")
                    return {"content": content, "author": author}
        except Exception as e:
            self.log(f"⚠️ API quote fetch failed: {e}", "WARNING")
        
        # Fallback to predefined tech quotes
        quote = random.choice(self.tech_quotes)
        self.log(f"✅ Using fallback quote: '{quote['content'][:50]}...' by {quote['author']}")
        return quote
    
    def get_github_stats(self) -> Dict[str, Any]:
        """Fetch latest GitHub statistics"""
        if not self.github_token:
            self.log("⚠️ GITHUB_TOKEN not set, skipping GitHub stats", "WARNING")
            return {}
            
        headers = {
            'Authorization': f'token {self.github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        try:
            # Get user info
            user_url = f'https://api.github.com/users/{self.username}'
            response = requests.get(user_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            if response.status_code == 403:
                self.log("⚠️ GitHub API rate limit exceeded", "WARNING")
                return {}
                
            user_data = response.json()
            stats = {
                'followers': user_data.get('followers', 0),
                'following': user_data.get('following', 0),
                'public_repos': user_data.get('public_repos', 0),
                'total_stars': self.get_total_stars(headers),
                'total_forks': self.get_total_forks(headers)
            }
            
            self.log(f"✅ GitHub stats fetched: {stats['public_repos']} repos, {stats['followers']} followers, {stats['total_stars']} stars")
            return stats
            
        except Exception as e:
            self.log(f"❌ Error fetching GitHub stats: {e}", "ERROR")
            return {}
    
    def get_total_stars(self, headers: Dict[str, str]) -> int:
        """Get total stars across all repositories"""
        url = f'https://api.github.com/users/{self.username}/repos'
        total_stars = 0
        page = 1
        
        try:
            while True:
                response = requests.get(f'{url}?page={page}&per_page=100', headers=headers, timeout=10)
                if response.status_code != 200:
                    break
                    
                repos = response.json()
                if not repos:
                    break
                    
                total_stars += sum(repo.get('stargazers_count', 0) for repo in repos)
                page += 1
                
        except Exception as e:
            self.log(f"⚠️ Error fetching stars: {e}", "WARNING")
            
        return total_stars
    
    def get_total_forks(self, headers: Dict[str, str]) -> int:
        """Get total forks across all repositories"""
        url = f'https://api.github.com/users/{self.username}/repos'
        total_forks = 0
        page = 1
        
        try:
            while True:
                response = requests.get(f'{url}?page={page}&per_page=100', headers=headers, timeout=10)
                if response.status_code != 200:
                    break
                    
                repos = response.json()
                if not repos:
                    break
                    
                total_forks += sum(repo.get('forks_count', 0) for repo in repos)
                page += 1
                
        except Exception as e:
            self.log(f"⚠️ Error fetching forks: {e}", "WARNING")
            
        return total_forks
    
    def generate_contribution_snake(self) -> bool:
        """Generate contribution snake using Platane/snk API"""
        try:
            # Create assets directory if it doesn't exist
            os.makedirs('assets', exist_ok=True)
            
            # Generate SVG snake
            svg_url = f"https://raw.githubusercontent.com/Platane/snk/output/{self.username}/github-contribution-grid-snake.svg"
            
            response = requests.get(svg_url, timeout=10)
            if response.status_code == 200:
                with open('assets/github-contribution-grid-snake.svg', 'w', encoding='utf-8') as f:
                    f.write(response.text)
                self.log("✅ Generated contribution snake SVG")
                return True
            else:
                self.log(f"⚠️ Failed to generate snake: {response.status_code}", "WARNING")
                return False
                
        except Exception as e:
            self.log(f"❌ Error generating contribution snake: {e}", "ERROR")
            return False
    
    def update_readme_content(self, quote: Dict[str, str], stats: Dict[str, Any]) -> bool:
        """Update README.md with all new content"""
        try:
            with open(self.readme_file, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Update quote section
            quote_url = f"https://quotes-github-readme.vercel.app/api?type=horizontal&theme=tokyonight&border=true&quote={quote['content'].replace(' ', '%20')}&author={quote['author'].replace(' ', '%20')}"
            
            quote_pattern = r'(<img src="https://quotes-github-readme\.vercel\.app/api\?[^"]*")'
            quote_replacement = f'<img src="{quote_url}"'
            
            if re.search(quote_pattern, content):
                content = re.sub(quote_pattern, quote_replacement, content)
                self.log("✅ Updated daily quote in README")
            else:
                self.log("⚠️ Quote pattern not found in README", "WARNING")
            
            # Update GitHub stats badges if stats are available
            if stats:
                # Update followers badge
                followers_pattern = r'(https://img\.shields\.io/github/followers/Rayyan9477\?[^"]*)'
                followers_replacement = f'https://img.shields.io/github/followers/{self.username}?label=Followers&style=for-the-badge&color=4c1&logo=github'
                content = re.sub(followers_pattern, followers_replacement, content)
                
                # Update stars badge
                stars_pattern = r'(https://img\.shields\.io/github/stars/Rayyan9477\?[^"]*)'
                stars_replacement = f'https://img.shields.io/github/stars/{self.username}?label=Total%20Stars&style=for-the-badge&color=yellow&logo=github'
                content = re.sub(stars_pattern, stars_replacement, content)
                
                self.log("✅ Updated GitHub stats badges")
            
            # Update timestamps
            now = datetime.now().strftime("%B %d, %Y at %I:%M %p UTC")
            
            # Update quote timestamp
            if "<!-- Quote Updated:" in content:
                content = re.sub(
                    r'<!-- Quote Updated: .* -->',
                    f'<!-- Quote Updated: {now} -->',
                    content
                )
            else:
                content = f"<!-- Quote Updated: {now} -->\n" + content
            
            # Update last updated timestamp
            if "<!-- Last Updated:" in content:
                content = re.sub(
                    r'<!-- Last Updated: .* -->',
                    f'<!-- Last Updated: {now} -->',
                    content
                )
            else:
                # Add at the end if not present
                content += f"\n<!-- Last Updated: {now} -->"
            
            # Write updated content
            with open(self.readme_file, 'w', encoding='utf-8') as file:
                file.write(content)
            
            self.log("✅ README content updated successfully")
            return True
            
        except Exception as e:
            self.log(f"❌ Error updating README content: {e}", "ERROR")
            return False
    
    def commit_changes(self) -> bool:
        """Commit all changes with a descriptive message"""
        try:
            # Check if there are any changes to commit
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True, check=True)
            
            if not result.stdout.strip():
                self.log("ℹ️ No changes to commit")
                return True
            
            # Add all changes
            subprocess.run(['git', 'add', '.'], check=True)
            self.log("✅ Added all changes to git")
            
            # Create commit message
            now = datetime.now().strftime("%Y-%m-%d")
            commit_message = f"🤖 Daily Update - {now}\n\n" \
                           f"• Updated daily inspirational quote\n" \
                           f"• Refreshed GitHub statistics and badges\n" \
                           f"• Generated latest contribution snake\n" \
                           f"• Automated daily maintenance\n\n" \
                           f"Updated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}"
            
            # Commit changes
            subprocess.run(['git', 'commit', '-m', commit_message], check=True)
            self.log("✅ Changes committed successfully")
            
            return True
            
        except subprocess.CalledProcessError as e:
            self.log(f"❌ Git operation failed: {e}", "ERROR")
            return False
        except Exception as e:
            self.log(f"❌ Error during commit: {e}", "ERROR")
            return False
    
    def push_changes(self) -> bool:
        """Push changes to remote repository"""
        try:
            subprocess.run(['git', 'push'], check=True)
            self.log("✅ Changes pushed to remote repository")
            return True
        except subprocess.CalledProcessError as e:
            self.log(f"❌ Push failed: {e}", "ERROR")
            return False
        except Exception as e:
            self.log(f"❌ Error during push: {e}", "ERROR")
            return False
    
    def run_daily_update(self) -> bool:
        """Execute complete daily update process"""
        try:
            self.log("🔄 Starting daily update process...")
            
            # Check if README.md exists
            if not os.path.exists(self.readme_file):
                self.log(f"⚠️ README.md not found at {self.readme_file}", "WARNING")
                
                # Try alternative locations
                possible_paths = [
                    'README.md',  # Current directory
                    os.path.join('..', 'README.md'),  # Parent directory
                    os.path.join(os.getcwd(), 'README.md'),  # Full path to current dir
                    os.path.join(os.path.dirname(os.getcwd()), 'README.md')  # Full path to parent dir
                ]
                
                for path in possible_paths:
                    if os.path.exists(path):
                        self.log(f"✅ Found README.md at {path}")
                        self.readme_file = path
                        break
                else:
                    self.log("❌ README.md not found in any expected location", "ERROR")
                    return False
            
            # Step 1: Get daily quote
            quote = self.get_daily_quote()
            
            # Step 2: Get GitHub stats
            stats = self.get_github_stats()
            
            # Step 3: Generate contribution snake
            snake_success = self.generate_contribution_snake()
            
            # Step 4: Update README content
            readme_success = self.update_readme_content(quote, stats)
            
            if not readme_success:
                self.log("❌ README update failed, aborting commit", "ERROR")
                return False
            
            # Step 5: Commit changes
            commit_success = self.commit_changes()
            
            if not commit_success:
                self.log("❌ Commit failed", "ERROR")
                return False
            
            # Step 6: Push changes (optional, can be disabled for testing)
            if os.getenv('PUSH_CHANGES', 'true').lower() == 'true':
                push_success = self.push_changes()
                if not push_success:
                    self.log("⚠️ Push failed, but changes are committed locally", "WARNING")
            
            self.log("🎉 Daily update completed successfully!")
            return True
            
        except Exception as e:
            self.log(f"❌ Daily update failed: {e}", "ERROR")
            return False

def main():
    """Main entry point"""
    updater = DailyUpdater()
    success = updater.run_daily_update()
    
    if success:
        print("\n✅ Daily update completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Daily update failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 