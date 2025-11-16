#!/usr/bin/env python3
"""
GitHub Stats Updater - Enhanced Version
Updates README.md with real-time GitHub statistics and activity
Designed to work with GitHub Actions for automated updates every 12 hours
"""

import os
import re
import requests
import subprocess
import sys
from datetime import datetime
from typing import Dict, Any, Optional

class GitHubStatsUpdater:
    def __init__(self):
        self.GH_TOKEN = os.getenv('GH_TOKEN') or os.getenv('GITHUB_TOKEN')
        self.username = 'Rayyan9477'
        self.readme_file = self._find_readme()
        self.log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'github_stats.log')
        
        self.log("🚀 GitHub Stats Updater Started")
    
    def _find_readme(self) -> str:
        """Find README.md in common locations"""
        possible_paths = [
            os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'README.md'),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'README.md'),
            os.path.join(os.getcwd(), 'README.md'),
            'README.md'
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                self.log(f"✅ Found README.md at {path}")
                return path
        
        # If no README found, return the most likely path
        self.log(f"⚠️ README.md not found in expected locations, using default: {possible_paths[0]}")
        return possible_paths[0]
    
    def log(self, message: str, level: str = "INFO"):
        """Log messages with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {level}: {message}"
        try:
            print(log_message)
        except UnicodeEncodeError:
            # Fallback for terminals that cannot render emojis
            safe_message = log_message.encode("ascii", "ignore").decode("ascii")
            try:
                print(safe_message)
            except Exception:
                pass
        
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_message + '\n')
        except (PermissionError, OSError):
            pass  # Ignore logging errors
        except Exception:
            pass  # Ignore any other logging errors
    
    def get_github_user_stats(self) -> Dict[str, Any]:
        """Fetch comprehensive GitHub user statistics"""
        if not self.GH_TOKEN:
            self.log("⚠️ GitHub token not available, stats will not update", "WARNING")
            return self._get_fallback_stats()
        
        headers = {
            'Authorization': f'token {self.GH_TOKEN}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        try:
            # Get user information
            user_url = f'https://api.github.com/users/{self.username}'
            response = requests.get(user_url, headers=headers, timeout=15)
            
            if response.status_code == 403:
                self.log("⚠️ GitHub API rate limit exceeded", "WARNING")
                return self._get_fallback_stats()
            elif response.status_code == 401:
                self.log("⚠️ GitHub API authentication failed", "WARNING")
                return self._get_fallback_stats()
            elif response.status_code != 200:
                self.log(f"⚠️ GitHub API request failed with status {response.status_code}", "WARNING")
                return self._get_fallback_stats()
            
            user_data = response.json()
            
            # Get repository statistics
            repos_stats = self._get_repository_stats(headers)
            
            # Get contribution statistics (basic estimate)
            contribution_stats = self._get_contribution_stats(headers)
            
            stats = {
                'followers': user_data.get('followers', 0),
                'following': user_data.get('following', 0),
                'public_repos': user_data.get('public_repos', 0),
                'total_stars': repos_stats.get('total_stars', 0),
                'total_forks': repos_stats.get('total_forks', 0),
                'total_contributions': contribution_stats.get('total_contributions', 0),
                'this_year_contributions': contribution_stats.get('this_year_contributions', 0),
                'updated_at': datetime.now().isoformat()
            }
            
            self.log(f"✅ GitHub stats fetched: {stats['public_repos']} repos, {stats['followers']} followers, {stats['total_stars']} stars")
            return stats
            
        except requests.exceptions.Timeout:
            self.log("⚠️ GitHub API request timed out", "WARNING")
            return self._get_fallback_stats()
        except requests.exceptions.RequestException as e:
            self.log(f"❌ Error fetching GitHub stats: {e}", "ERROR")
            return self._get_fallback_stats()
        except Exception as e:
            self.log(f"❌ Unexpected error fetching GitHub stats: {e}", "ERROR")
            return self._get_fallback_stats()
    
    def _get_repository_stats(self, headers: Dict[str, str]) -> Dict[str, int]:
        """Get total stars and forks across all repositories"""
        url = f'https://api.github.com/users/{self.username}/repos'
        total_stars = 0
        total_forks = 0
        page = 1
        
        try:
            while True:
                response = requests.get(f'{url}?page={page}&per_page=100&sort=updated', headers=headers, timeout=15)
                if response.status_code != 200:
                    break
                
                repos = response.json()
                if not repos:
                    break
                
                for repo in repos:
                    total_stars += repo.get('stargazers_count', 0)
                    total_forks += repo.get('forks_count', 0)
                
                page += 1
                if len(repos) < 100:  # Last page
                    break
                    
        except requests.exceptions.Timeout:
            self.log("⚠️ Repository stats fetch timed out", "WARNING")
        except requests.exceptions.RequestException as e:
            self.log(f"⚠️ Error fetching repository stats: {e}", "WARNING")
        except Exception as e:
            self.log(f"⚠️ Unexpected error fetching repository stats: {e}", "WARNING")
        
        return {'total_stars': total_stars, 'total_forks': total_forks}
    
    def _get_contribution_stats(self, headers: Dict[str, str]) -> Dict[str, int]:
        """Get contribution statistics - preserves existing counts if API fails"""
        # Note: GitHub doesn't provide total contribution counts via REST API
        # We'll preserve existing badge values and only update if we can get better data
        return {
            'total_contributions': 0,  # Will preserve existing value
            'this_year_contributions': 0  # Will preserve existing value
        }
    
    def _get_profile_views(self) -> str:
        """Get profile views badge using komarev service"""
        try:
            # Use komarev profile view counter service for dynamic badge
            return "https://komarev.com/ghpvc/?username=Rayyan9477&label=Profile%20Views&color=0e75b6&style=for-the-badge"
        except Exception as e:
            self.log(f"⚠️ Error setting up profile views badge: {e}", "WARNING")
            return "https://img.shields.io/badge/👀_Profile_Views-650+-0e75b6?style=for-the-badge&labelColor=1a1a2e"  # Fallback
    
    def _get_current_streak(self) -> str:
        """Get current streak from GitHub using GraphQL API or streak stats service"""
        # Try GitHub GraphQL API first if token is available
        if self.GH_TOKEN:
            try:
                streak = self._get_streak_from_github_api()
                if streak is not None and streak >= 0:
                    self.log(f"✅ Fetched current streak from GitHub GraphQL API: {streak} days")
                    return f"{streak}_Days"
            except Exception as e:
                self.log(f"⚠️ GitHub GraphQL API streak fetch failed: {e}", "WARNING")
        
        # Fallback to streak stats service
        try:
            # Try alternative endpoint first (vercel deployment)
            streak_urls = [
                f"https://streak-stats.demolab.com/?user={self.username}&theme=tokyonight&hide_border=true&background=0D1117&stroke=F85D7F&ring=F85D7F&fire=F8D866&currStreakLabel=FFFFFF",
                f"https://github-readme-streak-stats.herokuapp.com/?user={self.username}&theme=tokyonight&hide_border=true&background=0D1117&stroke=F85D7F&ring=F85D7F&fire=F8D866&currStreakLabel=FFFFFF"
            ]
            
            for streak_url in streak_urls:
                try:
                    response = requests.get(streak_url, timeout=15)
                    if response.status_code == 200:
                        svg_content = response.text
                        # Parse current streak from SVG - try multiple patterns
                        # The actual number appears after the "Current Streak" label in a separate text element
                        patterns = [
                            r'Current Streak.*?<text[^>]*>(\d+)</text>',
                            r'animation: currstreak[^>]*>\s*(\d+)\s*</text>',
                            r'<text[^>]*>Current Streak</text>.*?<text[^>]*>(\d+)</text>',
                            r'Current Streak</text><text[^>]*>(\d+)</text>',
                        ]
                        
                        for pattern in patterns:
                            current_streak_match = re.search(pattern, svg_content, re.IGNORECASE | re.DOTALL)
                            if current_streak_match:
                                streak_days = current_streak_match.group(1)
                                self.log(f"✅ Fetched current streak: {streak_days} days")
                                return f"{streak_days}_Days"
                except:
                    continue
                    
        except requests.exceptions.Timeout:
            self.log("⚠️ Streak stats fetch timed out", "WARNING")
        except requests.exceptions.RequestException as e:
            self.log(f"⚠️ Error fetching streak stats: {e}", "WARNING")
        except Exception as e:
            self.log(f"⚠️ Unexpected error fetching streak: {e}", "WARNING")
        
        # If all methods fail, preserve existing value by returning None
        self.log("ℹ️ Unable to fetch streak, preserving existing value", "INFO")
        return None  # Signal to preserve existing value
    
    def _get_streak_from_github_api(self) -> int:
        """Get current contribution streak using GitHub GraphQL API"""
        if not self.GH_TOKEN:
            return None
            
        headers = {
            'Authorization': f'bearer {self.GH_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        # Get contribution calendar for the past year
        from datetime import datetime, timedelta
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
            'username': self.username,
            'from': one_year_ago.isoformat(),
            'to': today.isoformat()
        }
        
        try:
            self.log("🔍 Querying GitHub GraphQL API for contribution data...")
            response = requests.post(
                'https://api.github.com/graphql',
                json={'query': query, 'variables': variables},
                headers=headers,
                timeout=20
            )
            
            if response.status_code != 200:
                self.log(f"⚠️ GraphQL API returned status {response.status_code}", "WARNING")
                return None
            
            data = response.json()
            
            if 'errors' in data:
                self.log(f"⚠️ GraphQL errors: {data['errors']}", "WARNING")
                return None
            
            calendar = data.get('data', {}).get('user', {}).get('contributionsCollection', {}).get('contributionCalendar', {})
            total_contributions = calendar.get('totalContributions', 0)
            weeks = calendar.get('weeks', [])
            
            self.log(f"📊 Total contributions in past year: {total_contributions}")
            
            if not weeks:
                self.log("⚠️ No contribution weeks data available", "WARNING")
                return None
            
            # Flatten all days from weeks
            days = []
            for week in weeks:
                days.extend(week.get('contributionDays', []))
            
            if not days:
                self.log("⚠️ No contribution days data available", "WARNING")
                return None
            
            # Sort by date descending (most recent first)
            days.sort(key=lambda x: x.get('date', ''), reverse=True)
            
            # Log the most recent contributions for debugging
            self.log(f"📅 Analyzing {len(days)} days of contribution history...")
            recent_days = days[:7]  # Last 7 days
            self.log("Recent contributions:")
            for day in recent_days:
                date = day.get('date', 'Unknown')
                count = day.get('contributionCount', 0)
                self.log(f"  {date}: {count} contribution(s)")
            
            # Calculate current streak
            current_streak = 0
            for day in days:
                count = day.get('contributionCount', 0)
                if count > 0:
                    current_streak += 1
                else:
                    # Stop at the first day with no contributions
                    break
            
            self.log(f"🔥 Current streak calculated: {current_streak} days")
            return current_streak
            
        except requests.exceptions.RequestException as e:
            self.log(f"⚠️ Network error accessing GitHub API: {e}", "WARNING")
            return None
        except Exception as e:
            self.log(f"⚠️ Unexpected error in GraphQL API call: {e}", "WARNING")
            import traceback
            self.log(f"Stack trace: {traceback.format_exc()}", "WARNING")
            return None
    
    def _get_fallback_stats(self) -> Dict[str, Any]:
        """Return fallback statistics when API is unavailable"""
        return {
            'followers': 0,
            'following': 0,
            'public_repos': 0,
            'total_stars': 0,
            'total_forks': 0,
            'total_commits': 0,
            'this_year_commits': 0,
            'updated_at': datetime.now().isoformat(),
            'fallback': True
        }
    
    def update_readme_stats(self, stats: Dict[str, Any]) -> bool:
        """Update README.md with new GitHub statistics"""
        try:
            if not os.path.exists(self.readme_file):
                self.log(f"❌ README.md not found at {self.readme_file}", "ERROR")
                return False
            
            with open(self.readme_file, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Update followers badge
            followers_pattern = r'(https://img\.shields\.io/github/followers/Rayyan9477\?[^"]*)'
            followers_replacement = f'https://img.shields.io/github/followers/{self.username}?label=Followers&style=for-the-badge&color=4c1&logo=github'
            if re.search(followers_pattern, content):
                content = re.sub(followers_pattern, followers_replacement, content)
                self.log("✅ Updated followers badge")
            
            # Update stars badge
            stars_pattern = r'(https://img\.shields\.io/github/stars/Rayyan9477\?[^"]*)'
            stars_replacement = f'https://img.shields.io/github/stars/{self.username}?label=Total%20Stars&style=for-the-badge&color=yellow&logo=github'
            if re.search(stars_pattern, content):
                content = re.sub(stars_pattern, stars_replacement, content)
                self.log("✅ Updated stars badge")
            
            # Update profile views badge
            profile_views_badge = self._get_profile_views()
            profile_views_pattern = r'https://img\.shields\.io/badge/👀_Profile_Views-[\d\+]+-[^"]*'
            if re.search(profile_views_pattern, content):
                content = re.sub(profile_views_pattern, profile_views_badge, content)
                self.log("✅ Updated profile views badge")
            
            # Update current streak badge
            current_streak = self._get_current_streak()
            if current_streak:  # Only update if we successfully fetched the streak
                current_streak_pattern = r'🔥_Current_Streak-[\d_]+Days-'
                current_streak_replacement = f'🔥_Current_Streak-{current_streak}-'
                if re.search(current_streak_pattern, content):
                    content = re.sub(current_streak_pattern, current_streak_replacement, content)
                    self.log("✅ Updated current streak badge")
                else:
                    self.log("⚠️ Current streak pattern not found in README", "WARNING")
            else:
                self.log("ℹ️ Preserving existing streak value", "INFO")
            
            # Note: Contribution counts are preserved as-is since GitHub REST API
            # doesn't provide total contribution data. The existing counts remain.
            # Only followers and stars badges are updated automatically.
            self.log("ℹ️ Contribution counts preserved (not available via REST API)")
            
            # Update timestamp
            now = datetime.now().strftime("%B %d, %Y at %I:%M %p UTC")
            if "<!-- Last Updated:" in content:
                content = re.sub(r'<!-- Last Updated: .* -->', f'<!-- Last Updated: {now} -->', content)
            else:
                content += f"\n<!-- Last Updated: {now} -->"
            
            # Write updated content
            with open(self.readme_file, 'w', encoding='utf-8') as file:
                file.write(content)
            
            self.log("✅ README stats updated successfully")
            return True
            
        except FileNotFoundError:
            self.log(f"❌ README.md not found at {self.readme_file}", "ERROR")
            return False
        except PermissionError:
            self.log(f"❌ Permission denied accessing {self.readme_file}", "ERROR")
            return False
        except Exception as e:
            self.log(f"❌ Error updating README stats: {e}", "ERROR")
            return False
    
    def run_stats_update(self) -> bool:
        """Execute complete stats update process"""
        try:
            self.log("🔄 Starting GitHub stats update process...")
            
            # Check if README.md exists
            if not os.path.exists(self.readme_file):
                self.log(f"❌ README.md not found at {self.readme_file}", "ERROR")
                return False
            
            # Get GitHub statistics
            stats = self.get_github_user_stats()
            
            # Update README content
            if not self.update_readme_stats(stats):
                self.log("❌ README stats update failed", "ERROR")
                return False
            
            self.log("🎉 GitHub stats update completed successfully!")
            return True
            
        except Exception as e:
            self.log(f"❌ GitHub stats update failed: {e}", "ERROR")
            return False

def main():
    """Main entry point"""
    updater = GitHubStatsUpdater()
    success = updater.run_stats_update()
    
    try:
        if success:
            print("\nGitHub stats update completed successfully!")
            sys.exit(0)
        else:
            print("\nGitHub stats update failed!")
            sys.exit(1)
    except UnicodeEncodeError:
        # Final safety for terminals that cannot render emojis
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
