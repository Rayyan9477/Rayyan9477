#!/usr/bin/env python3
"""
Dynamic README Update Script
Updates README.md with latest GitHub stats, quotes, and dynamic content
"""

import os
import re
import requests
from datetime import datetime
import random

class ReadmeUpdater:
    def __init__(self):
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.username = 'Rayyan9477'
        
    def get_github_stats(self):
        """Fetch latest GitHub statistics"""
        headers = {'Authorization': f'token {self.github_token}'}
        
        # Get user info
        user_url = f'https://api.github.com/users/{self.username}'
        response = requests.get(user_url, headers=headers)
        
        if response.status_code == 200:
            user_data = response.json()
            return {
                'followers': user_data.get('followers', 0),
                'following': user_data.get('following', 0),
                'public_repos': user_data.get('public_repos', 0),
                'created_at': user_data.get('created_at', ''),
            }
        return {}
    
    def get_random_tech_quote(self):
        """Get a random tech quote"""
        quotes = [
            {
                "quote": "The best way to predict the future is to invent it.",
                "author": "Alan Kay"
            },
            {
                "quote": "Code is like humor. When you have to explain it, it's bad.",
                "author": "Cory House"
            },
            {
                "quote": "First, solve the problem. Then, write the code.",
                "author": "John Johnson"
            },
            {
                "quote": "Any fool can write code that a computer can understand. Good programmers write code that humans can understand.",
                "author": "Martin Fowler"
            },
            {
                "quote": "The only way to learn a new programming language is by writing programs in it.",
                "author": "Dennis Ritchie"
            },
            {
                "quote": "Talk is cheap. Show me the code.",
                "author": "Linus Torvalds"
            },
            {
                "quote": "Programs must be written for people to read, and only incidentally for machines to execute.",
                "author": "Harold Abelson"
            },
            {
                "quote": "The computer was born to solve problems that did not exist before.",
                "author": "Bill Gates"
            }
        ]
        return random.choice(quotes)
    
    def update_readme(self):
        """Update README.md with latest content"""
        try:
            with open('README.md', 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Update last updated timestamp
            now = datetime.now().strftime("%B %d, %Y at %I:%M %p UTC")
            
            # Add dynamic update marker if not present
            if "<!-- Last Updated:" not in content:
                content = f"<!-- Last Updated: {now} -->\n" + content
            else:
                content = re.sub(
                    r'<!-- Last Updated: .* -->',
                    f'<!-- Last Updated: {now} -->',
                    content
                )
            
            # Get GitHub stats
            stats = self.get_github_stats()
            if stats:
                print(f"✅ Updated stats: {stats['public_repos']} repos, {stats['followers']} followers")
            
            # Update random quote section
            quote = self.get_random_tech_quote()
            quote_pattern = r'(#### 🎯 Personal Philosophy\n)(.*?)(\n\n</div>)'
            quote_replacement = f'#### 🎯 Personal Philosophy\n> *"{quote["quote"]}"* — {quote["author"]}\n\n> *"The only way to do great work is to love what you do."* — Steve Jobs\n\n> *"Innovation distinguishes between a leader and a follower."* — Steve Jobs\n\n</div>'
            
            content = re.sub(quote_pattern, quote_replacement, content, flags=re.DOTALL)
            
            # Write updated content
            with open('README.md', 'w', encoding='utf-8') as file:
                file.write(content)
            
            print("✅ README.md updated successfully!")
            
        except Exception as e:
            print(f"❌ Error updating README: {e}")

if __name__ == "__main__":
    updater = ReadmeUpdater()
    updater.update_readme()
