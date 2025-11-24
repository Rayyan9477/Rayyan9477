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
import subprocess
import sys
from datetime import datetime
from typing import Dict, Any

class DailyUpdater:
    def __init__(self):
        # Try to load .env file if present
        try:
            from dotenv import load_dotenv
            env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
            if os.path.exists(env_path):
                load_dotenv(env_path)
                self.log("✅ Loaded environment variables from .env file")
        except ImportError:
            self.log("ℹ️ dotenv package not installed, skipping .env loading")
        except Exception as e:
            self.log(f"⚠️ Error loading .env file: {e}")
            
        self.GH_TOKEN = os.getenv('GH_TOKEN')
        self.wakatime_token = os.getenv('WAKATIME_API_KEY')
        self.username = 'Rayyan9477'
        self.quotes_api_url = "https://api.quotable.io/random"
        self.wakatime_api_base = "https://wakatime.com/api/v1"
        
        # Find README.md
        self.readme_file = self._find_readme()
        self.log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'daily_update.log')
        
        # Tech quotes as fallback
        self.tech_quotes = [
            {"content": "The best way to predict the future is to invent it.", "author": "Alan Kay"},
            {"content": "Code is like humor. When you have to explain it, it's bad.", "author": "Cory House"},
            {"content": "First, solve the problem. Then, write the code.", "author": "John Johnson"},
            {"content": "Any fool can write code that a computer can understand. Good programmers write code that humans can understand.", "author": "Martin Fowler"},
            {"content": "Talk is cheap. Show me the code.", "author": "Linus Torvalds"},
            {"content": "Simplicity is the ultimate sophistication.", "author": "Leonardo da Vinci"},
            {"content": "Innovation distinguishes between a leader and a follower.", "author": "Steve Jobs"}
        ]
        
        self.log("🚀 Daily Update Script Started")
    
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
    
    def get_daily_quote(self) -> Dict[str, str]:
        """Get a daily inspirational quote"""
        try:
            response = requests.get(self.quotes_api_url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                content = data.get("content", "").strip()
                author = data.get("author", "Unknown").strip()
                
                if content and author and len(content) < 200:
                    self.log(f"✅ Fetched quote from API: '{content[:50]}...' by {author}")
                    return {"content": content, "author": author}
            else:
                self.log(f"⚠️ Quote API failed with status {response.status_code}", "WARNING")
        except requests.exceptions.Timeout:
            self.log("⚠️ Quote API request timed out", "WARNING")
        except requests.exceptions.RequestException as e:
            self.log(f"⚠️ Quote API request failed: {e}", "WARNING")
        except Exception as e:
            self.log(f"⚠️ Unexpected error fetching quote: {e}", "WARNING")
        
        # Fallback to predefined quotes
        quote = random.choice(self.tech_quotes)
        self.log(f"✅ Using fallback quote: '{quote['content'][:50]}...' by {quote['author']}")
        return quote
    
    def get_github_stats(self) -> Dict[str, Any]:
        """Fetch latest GitHub statistics"""
        if not self.GH_TOKEN:
            self.log("⚠️ GH_TOKEN not set, skipping GitHub stats", "WARNING")
            return {}
            
        headers = {
            'Authorization': f'token {self.GH_TOKEN}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        try:
            user_url = f'https://api.github.com/users/{self.username}'
            response = requests.get(user_url, headers=headers, timeout=10)
            
            if response.status_code == 403:
                self.log("⚠️ GitHub API rate limit exceeded", "WARNING")
                return {}
            elif response.status_code == 401:
                self.log("⚠️ GitHub API authentication failed", "WARNING")
                return {}
            elif response.status_code != 200:
                self.log(f"⚠️ GitHub API request failed with status {response.status_code}", "WARNING")
                return {}
                
            user_data = response.json()
            stats = {
                'followers': user_data.get('followers', 0),
                'following': user_data.get('following', 0),
                'public_repos': user_data.get('public_repos', 0),
                'total_stars': self._get_total_stars(headers),
                'total_forks': self._get_total_forks(headers)
            }
            
            self.log(f"✅ GitHub stats fetched: {stats['public_repos']} repos, {stats['followers']} followers")
            return stats
            
        except requests.exceptions.Timeout:
            self.log("⚠️ GitHub API request timed out", "WARNING")
            return {}
        except requests.exceptions.RequestException as e:
            self.log(f"❌ Error fetching GitHub stats: {e}", "ERROR")
            return {}
        except Exception as e:
            self.log(f"❌ Unexpected error fetching GitHub stats: {e}", "ERROR")
            return {}
    
    def _get_total_stars(self, headers: Dict[str, str]) -> int:
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
                
        except requests.exceptions.Timeout:
            self.log("⚠️ Stars fetch timed out", "WARNING")
        except requests.exceptions.RequestException as e:
            self.log(f"⚠️ Error fetching stars: {e}", "WARNING")
        except Exception as e:
            self.log(f"⚠️ Unexpected error fetching stars: {e}", "WARNING")
            
        return total_stars
    
    def _get_total_forks(self, headers: Dict[str, str]) -> int:
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
                
        except requests.exceptions.Timeout:
            self.log("⚠️ Forks fetch timed out", "WARNING")
        except requests.exceptions.RequestException as e:
            self.log(f"⚠️ Error fetching forks: {e}", "WARNING")
        except Exception as e:
            self.log(f"⚠️ Unexpected error fetching forks: {e}", "WARNING")
            
        return total_forks
    
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
            # Note: Today might not have contributions yet, so we check from yesterday
            from datetime import datetime, timezone
            today_str = datetime.now(timezone.utc).date().isoformat()
            
            current_streak = 0
            skip_today = True  # Flag to skip today if it has no contributions
            
            for i, day in enumerate(days):
                date = day.get('date', '')
                count = day.get('contributionCount', 0)
                
                # If this is today and has no contributions, skip it
                if skip_today and date == today_str and count == 0:
                    self.log(f"ℹ️ Skipping today ({today_str}) with 0 contributions")
                    skip_today = False
                    continue
                
                # Count days with contributions
                if count > 0:
                    current_streak += 1
                else:
                    # Stop at the first day (after today) with no contributions
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
    
    def generate_contribution_snake(self) -> bool:
        """Generate contribution snake using Platane/snk API"""
        try:
            # Create assets directory if it doesn't exist
            assets_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets')
            if not os.path.exists(assets_dir):
                os.makedirs(assets_dir, exist_ok=True)
                self.log(f"✅ Created assets directory: {assets_dir}")
            
            # Check if snake SVG already exists (generated by GitHub Action)
            svg_path = os.path.join(assets_dir, 'github-contribution-grid-snake.svg')
            if os.path.exists(svg_path):
                self.log("✅ Contribution snake SVG already exists")
                return True
                
            # If not exists, try to download it from GitHub
            svg_url = f"https://raw.githubusercontent.com/{self.username}/{self.username}/main/assets/github-contribution-grid-snake.svg"
            response = requests.get(svg_url, timeout=10)
            
            if response.status_code == 200:
                with open(svg_path, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                self.log("✅ Generated contribution snake SVG")
                return True
            else:
                self.log(f"ℹ️ Snake will be generated by GitHub Action: {response.status_code}", "INFO")
                return True  # Return true because the snake is generated by the action
                
        except requests.exceptions.Timeout:
            self.log("⚠️ Contribution snake generation timed out", "WARNING")
            return True  # Continue anyway as the snake is generated by the action
        except requests.exceptions.RequestException as e:
            self.log(f"⚠️ Error generating contribution snake: {e}", "WARNING")
            return True  # Continue anyway as the snake is generated by the action
        except Exception as e:
            self.log(f"❌ Unexpected error generating contribution snake: {e}", "ERROR")
            return True  # Continue anyway as the snake is generated by the action
    
    def _format_minutes(self, total_minutes: int) -> str:
        """Convert minutes to a human readable 'X hrs Y mins' string"""
        hours = total_minutes // 60
        minutes = total_minutes % 60
        if hours and minutes:
            return f"{hours} hrs {minutes} mins"
        if hours:
            return f"{hours} hrs"
        return f"{minutes} mins"

    def get_wakatime_block(self) -> str:
        """Build the markdown block to be injected into the WakaTime section.

        - If `WAKATIME_API_KEY` is not configured, return a helpful setup message
        - If the API returns no data, return a friendly 'No activity' message
        - Otherwise render a compact weekly summary in a fenced text block
        """
        from datetime import timedelta

        if not self.wakatime_token:
            self.log("ℹ️ WAKATIME_API_KEY not set, using setup instructions placeholder")
            placeholder = (
                '<div align="center">\n'
                '  <img src="https://img.shields.io/badge/Status-Pending%20API%20Key%20Configuration-yellow?style=for-the-badge&logo=wakatime&logoColor=white" alt="WakaTime Status"/>\n'
                '</div>\n\n'
                '> 1) Install editor plugin  2) Copy API key  3) Add secret `WAKATIME_API_KEY` in repository settings  4) Re-run workflow\n'
            )
            return placeholder

        headers = {"Authorization": f"Bearer {self.wakatime_token}"}
        from datetime import timezone
        end_date = datetime.now(timezone.utc).date()
        start_date = end_date - timedelta(days=7)
        url = (
            f"{self.wakatime_api_base}/users/current/summaries?start={start_date.isoformat()}&end={end_date.isoformat()}"
        )
        try:
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code in (401, 403):
                self.log("⚠️ WakaTime authentication/permission failed", "WARNING")
                return (
                    '<div align="center">\n'
                    '  <img src="https://img.shields.io/badge/Status-Pending%20API%20Key%20Configuration-yellow?style=for-the-badge&logo=wakatime&logoColor=white"/>\n'
                    '</div>\n\n'
                    '> Add or refresh repo secret `WAKATIME_API_KEY`, then re-run the workflow.'
                )
            if response.status_code != 200:
                self.log(f"⚠️ WakaTime API error: {response.status_code}", "WARNING")
                return (
                    '<div align="center">\n'
                    '  <img src="https://img.shields.io/badge/WakaTime-API%20Unavailable-lightgrey?style=for-the-badge&logo=wakatime&logoColor=white"/>\n'
                    '</div>'
                )

            payload = response.json()
            data = payload.get("data", [])
            if not data:
                self.log("ℹ️ WakaTime returned no data for the selected period")
                return (
                    "```text\n"
                    f"From: {start_date.strftime('%d %B %Y')} - To: {end_date.strftime('%d %B %Y')}\n\n"
                    "Total Time: 0 secs\n\n"
                    "No activity tracked\n"
                    "```"
                )

            # Aggregate totals across the period
            total_seconds = 0
            language_totals: Dict[str, int] = {}
            editor_totals: Dict[str, int] = {}
            for day in data:
                day_total = day.get("grand_total", {}).get("total_seconds", 0) or 0
                total_seconds += int(day_total)
                for lang in day.get("languages", [])[:8]:  # top languages per day
                    name = lang.get("name", "Other")
                    secs = int(lang.get("total_seconds", 0) or 0)
                    language_totals[name] = language_totals.get(name, 0) + secs
                for ed in day.get("editors", [])[:5]:
                    name = ed.get("name", "Editor")
                    secs = int(ed.get("total_seconds", 0) or 0)
                    editor_totals[name] = editor_totals.get(name, 0) + secs

            total_minutes = total_seconds // 60
            total_text = self._format_minutes(total_minutes)

            # Sort languages by time desc, take top 5
            top_languages = sorted(language_totals.items(), key=lambda x: x[1], reverse=True)[:5]
            top_editors = sorted(editor_totals.items(), key=lambda x: x[1], reverse=True)[:3]

            lines = [
                "```text",
                f"From: {start_date.strftime('%d %B %Y')} - To: {end_date.strftime('%d %B %Y')}",
                "",
                f"Total Time: {total_text}",
                "",
            ]

            if top_languages:
                lines.append("Languages:")
                for name, secs in top_languages:
                    lines.append(f"  {name:<18} {self._format_minutes(secs // 60)}")
                lines.append("")

            if top_editors:
                lines.append("Editors:")
                for name, secs in top_editors:
                    lines.append(f"  {name:<18} {self._format_minutes(secs // 60)}")
                lines.append("")

            lines.append("```")
            block = "\n".join(lines)
            self.log("✅ Built WakaTime stats block")
            return block

        except requests.exceptions.Timeout:
            self.log("⚠️ WakaTime API request timed out", "WARNING")
            return (
                '<div align="center">\n'
                '  <img src="https://img.shields.io/badge/WakaTime-Time%20Out-lightgrey?style=for-the-badge&logo=wakatime&logoColor=white"/>\n'
                '</div>'
            )
        except Exception as e:
            self.log(f"❌ Unexpected WakaTime error: {e}", "ERROR")
            return (
                '<div align="center">\n'
                '  <img src="https://img.shields.io/badge/WakaTime-Error-red?style=for-the-badge&logo=wakatime&logoColor=white"/>\n'
                '</div>'
            )

    def update_readme_content(self, quote: Dict[str, str], stats: Dict[str, Any]) -> bool:
        """Update README.md with new content"""
        try:
            # Check if README file exists
            if not os.path.exists(self.readme_file):
                self.log(f"❌ README.md not found at {self.readme_file}", "ERROR")
                return False
            
            with open(self.readme_file, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Update quote section with proper URL encoding
            import urllib.parse
            encoded_quote = urllib.parse.quote(quote['content'])
            encoded_author = urllib.parse.quote(quote['author'])
            quote_url = f"https://quotes-github-readme.vercel.app/api?type=horizontal&theme=tokyonight&border=true&quote={encoded_quote}&author={encoded_author}"
            
            # More robust quote pattern matching
            quote_patterns = [
                r'(<img src="https://quotes-github-readme\.vercel\.app/api\?[^"]*"[^>]*>)',
                r'(<img[^>]*src="https://quotes-github-readme\.vercel\.app/api\?[^"]*"[^>]*>)'
            ]
            
            quote_updated = False
            for pattern in quote_patterns:
                if re.search(pattern, content):
                    content = re.sub(pattern, f'<img src="{quote_url}" alt="Dev Quote"/>', content)
                    quote_updated = True
                    break
            
            if quote_updated:
                self.log("✅ Updated daily quote in README")
            else:
                self.log("⚠️ Quote pattern not found in README", "WARNING")
            
            # Update GitHub stats badges if stats are available
            if stats:
                # Update followers badge
                followers_pattern = r'https://img\.shields\.io/github/followers/Rayyan9477\?[^"]*'
                followers_replacement = f'https://img.shields.io/github/followers/{self.username}?label=Followers&style=flat-square&color=22c55e&logo=github&logoColor=white'
                if re.search(followers_pattern, content):
                    content = re.sub(followers_pattern, followers_replacement, content)
                    self.log("✅ Updated followers badge")
                
                # Update stars badge
                stars_pattern = r'https://img\.shields\.io/github/stars/Rayyan9477\?[^"]*'
                stars_replacement = f'https://img.shields.io/github/stars/{self.username}?label=Total%20Stars&style=flat-square&color=FFC107&logo=github&logoColor=white'
                if re.search(stars_pattern, content):
                    content = re.sub(stars_pattern, stars_replacement, content)
                    self.log("✅ Updated stars badge")
                
                # Update profile views badge (komarev service)
                profile_views_pattern = r'https://komarev\.com/ghpvc/\?username=Rayyan9477[^"]*'
                profile_views_replacement = f'https://komarev.com/ghpvc/?username={self.username}&label=Profile%20Views&color=0e75b6&style=flat-square'
                if re.search(profile_views_pattern, content):
                    content = re.sub(profile_views_pattern, profile_views_replacement, content)
                    self.log("✅ Updated profile views badge")
                
                # Update current streak badge
                current_streak = self._get_current_streak()
                if current_streak:  # Only update if we successfully fetched the streak
                    # Update badge URL
                    current_streak_badge_pattern = r'https://img\.shields\.io/badge/Current_Streak-[\d_]+Days-[^"]*'
                    current_streak_badge_replacement = f'https://img.shields.io/badge/Current_Streak-{current_streak}-F85D7F?style=flat-square&logo=github&logoColor=white'
                    if re.search(current_streak_badge_pattern, content):
                        content = re.sub(current_streak_badge_pattern, current_streak_badge_replacement, content)
                        self.log("✅ Updated current streak badge")
                else:
                    self.log("ℹ️ Preserving existing streak value", "INFO")
                
                # Update hardcoded numbers in the dashboard
                # Get profile views from komarev (extract from badge)
                try:
                    profile_views_response = requests.get(f'https://komarev.com/ghpvc/?username={self.username}', timeout=5)
                    if profile_views_response.status_code == 200:
                        # The service returns an SVG with the count
                        import re as regex_module
                        views_match = regex_module.search(r'>(\d+)<', profile_views_response.text)
                        if views_match:
                            profile_views = views_match.group(1)
                            # Update profile views number
                            content = regex_module.sub(
                                r'(<b style="font-size: 32px; color: #4FC3F7;">)\d+(</b>)',
                                f'\\g<1>{profile_views}\\g<2>',
                                content,
                                count=1
                            )
                            self.log(f"✅ Updated profile views number: {profile_views}")
                except Exception as e:
                    self.log(f"⚠️ Could not fetch profile views count: {e}", "WARNING")
                
                # Update followers number
                if 'followers' in stats:
                    followers_num_pattern = r'(<b style="font-size: 32px; color: #66BB6A;">)\d+(</b>)'
                    content = re.sub(followers_num_pattern, f'\\g<1>{stats["followers"]}\\g<2>', content, count=1)
                    self.log(f"✅ Updated followers number: {stats['followers']}")
                
                # Update stars number
                if 'total_stars' in stats:
                    stars_num_pattern = r'(<b style="font-size: 32px; color: #FFD54F;">)\d+(</b>)'
                    content = re.sub(stars_num_pattern, f'\\g<1>{stats["total_stars"]}\\g<2>', content, count=1)
                    self.log(f"✅ Updated stars number: {stats['total_stars']}")
                
                # Update streak number
                if current_streak:
                    streak_num_pattern = r'(<b style="font-size: 32px; color: #F85D7F;">)\d+(</b>)'
                    content = re.sub(streak_num_pattern, f'\\g<1>{current_streak.replace("_Days", "")}\\g<2>', content, count=1)
                    self.log(f"✅ Updated streak number: {current_streak}")
                
                self.log("✅ All dashboard numbers updated dynamically")
            
            # Update WakaTime section (if tags exist)
            if "<!--START_SECTION:waka-->" in content and "<!--END_SECTION:waka-->" in content:
                waka_block = self.get_wakatime_block()
                content = re.sub(
                    r"<!--START_SECTION:waka-->[\s\S]*?<!--END_SECTION:waka-->",
                    f"<!--START_SECTION:waka-->\n{waka_block}\n\n<!--END_SECTION:waka-->",
                    content,
                    flags=re.MULTILINE,
                )
                self.log("✅ Updated WakaTime section")
            else:
                self.log("ℹ️ WakaTime tags not found in README; skipping WakaTime update")

            # Update timestamps
            now = datetime.now().strftime("%B %d, %Y at %I:%M %p UTC")
            
            # Update quote timestamp
            if "<!-- Quote Updated:" in content:
                content = re.sub(r'<!-- Quote Updated: .* -->', f'<!-- Quote Updated: {now} -->', content)
            else:
                content = f"<!-- Quote Updated: {now} -->\n" + content
            
            # Update last updated timestamp
            if "<!-- Last Updated:" in content:
                content = re.sub(r'<!-- Last Updated: .* -->', f'<!-- Last Updated: {now} -->', content)
            else:
                content += f"\n<!-- Last Updated: {now} -->"
            
            # Write updated content
            with open(self.readme_file, 'w', encoding='utf-8') as file:
                file.write(content)
            
            self.log("✅ README content updated successfully")
            return True
            
        except FileNotFoundError:
            self.log(f"❌ README.md not found at {self.readme_file}", "ERROR")
            return False
        except PermissionError:
            self.log(f"❌ Permission denied accessing {self.readme_file}", "ERROR")
            return False
        except Exception as e:
            self.log(f"❌ Error updating README content: {e}", "ERROR")
            return False
    
    def commit_changes(self) -> bool:
        """Commit all changes"""
        try:
            result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True, check=True)
            
            if not result.stdout.strip():
                self.log("ℹ️ No changes to commit")
                return True
            
            subprocess.run(['git', 'add', '.'], check=True)
            self.log("✅ Added all changes to git")
            
            now = datetime.now().strftime("%Y-%m-%d")
            commit_message = f"🤖 Daily Update - {now}\n\n• Updated daily inspirational quote\n• Refreshed GitHub statistics\n• Generated latest contribution snake\n• Automated daily maintenance"
            
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
                self.log(f"❌ README.md not found at {self.readme_file}", "ERROR")
                # Try to find README in other locations
                alternative_paths = [
                    'README.md',
                    os.path.join('..', 'README.md'),
                    os.path.join(os.getcwd(), 'README.md')
                ]
                
                for path in alternative_paths:
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
            self.generate_contribution_snake()
            
            # Step 4: Update README content
            if not self.update_readme_content(quote, stats):
                self.log("❌ README update failed", "ERROR")
                return False
            
            # Step 5: Commit changes
            if not self.commit_changes():
                self.log("❌ Commit failed", "ERROR")
                return False
            
            # Step 6: Push changes (optional)
            if os.getenv('PUSH_CHANGES', 'true').lower() == 'true':
                self.push_changes()
            
            self.log("🎉 Daily update completed successfully!")
            return True
            
        except Exception as e:
            self.log(f"❌ Daily update failed: {e}", "ERROR")
            return False

def main():
    """Main entry point"""
    updater = DailyUpdater()
    success = updater.run_daily_update()
    
    try:
        if success:
            print("\nDaily update completed successfully!")
            sys.exit(0)
        else:
            print("\nDaily update failed!")
            sys.exit(1)
    except UnicodeEncodeError:
        # Final safety for terminals that cannot render emojis
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 