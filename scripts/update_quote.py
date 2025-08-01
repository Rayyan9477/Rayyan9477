#!/usr/bin/env python3
"""
Daily Quote Update Script
Updates the daily inspirational quote in README.md
"""

import os
import re
import requests
import random
from datetime import datetime

class QuoteUpdater:
    def __init__(self):
        self.quotes_api_url = "https://api.quotable.io/random"
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
            }
        ]
    
    def get_daily_quote(self):
        """Get a random tech quote"""
        try:
            # Try to get quote from API first
            response = requests.get(self.quotes_api_url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return {
                    "content": data.get("content", ""),
                    "author": data.get("author", "Unknown")
                }
        except:
            pass
        
        # Fallback to predefined tech quotes
        return random.choice(self.tech_quotes)
    
    def update_quote_in_readme(self):
        """Update the quote section in README.md"""
        try:
            with open('README.md', 'r', encoding='utf-8') as file:
                content = file.read()
            
            quote = self.get_daily_quote()
            
            # Update the quote in the Daily Developer Wisdom section
            quote_url = f"https://quotes-github-readme.vercel.app/api?type=horizontal&theme=tokyonight&border=true&quote={quote['content'].replace(' ', '%20')}&author={quote['author'].replace(' ', '%20')}"
            
            # Find and replace the quote image URL
            quote_pattern = r'(<img src="https://quotes-github-readme\.vercel\.app/api\?[^"]*")'
            quote_replacement = f'<img src="{quote_url}"'
            
            if re.search(quote_pattern, content):
                content = re.sub(quote_pattern, quote_replacement, content)
                print(f"✅ Updated daily quote: '{quote['content'][:50]}...' by {quote['author']}")
            else:
                print("⚠️ Quote pattern not found in README")
            
            # Update timestamp
            now = datetime.now().strftime("%B %d, %Y at %I:%M %p UTC")
            if "<!-- Quote Updated:" in content:
                content = re.sub(
                    r'<!-- Quote Updated: .* -->',
                    f'<!-- Quote Updated: {now} -->',
                    content
                )
            else:
                content = f"<!-- Quote Updated: {now} -->\n" + content
            
            with open('README.md', 'w', encoding='utf-8') as file:
                file.write(content)
            
            print("✅ Quote updated successfully!")
            
        except Exception as e:
            print(f"❌ Error updating quote: {e}")

if __name__ == "__main__":
    updater = QuoteUpdater()
    updater.update_quote_in_readme()
