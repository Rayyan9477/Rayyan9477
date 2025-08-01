#!/usr/bin/env python3
"""
Badge Generator
Generates custom badges for the README
"""

import urllib.parse

class BadgeGenerator:
    def __init__(self):
        self.base_url = "https://img.shields.io/badge"
        self.custom_base = "https://img.shields.io/static/v1"
    
    def create_badge(self, label, message, color="blue", style="for-the-badge", logo=None):
        """Create a custom badge URL"""
        params = {
            'label': label,
            'message': message,
            'color': color,
            'style': style
        }
        
        if logo:
            params['logo'] = logo
            params['logoColor'] = 'white'
        
        # URL encode the parameters
        encoded_params = '&'.join([f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items()])
        return f"{self.custom_base}?{encoded_params}"
    
    def ai_badges(self):
        """Generate AI/ML related badges"""
        badges = [
            self.create_badge("AI", "Engineer", "667eea", logo="robot"),
            self.create_badge("ML", "Expert", "f093fb", logo="tensorflow"),
            self.create_badge("NLP", "Specialist", "43cea2", logo="huggingface"),
            self.create_badge("Computer", "Vision", "f5576c", logo="opencv"),
            self.create_badge("RAG", "Systems", "764ba2", logo="elasticsearch"),
            self.create_badge("LLMs", "Development", "185a9d", logo="openai")
        ]
        return badges
    
    def tech_badges(self):
        """Generate technology badges"""
        badges = [
            self.create_badge("Python", "Expert", "3776AB", logo="python"),
            self.create_badge("TensorFlow", "Advanced", "FF6F00", logo="tensorflow"),
            self.create_badge("PyTorch", "Advanced", "EE4C2C", logo="pytorch"),
            self.create_badge("AWS", "Certified", "FF9900", logo="amazon-aws"),
            self.create_badge("Docker", "Proficient", "2496ED", logo="docker"),
            self.create_badge("Kubernetes", "Intermediate", "326CE5", logo="kubernetes")
        ]
        return badges
    
    def stats_badges(self, followers=0, repos=0, stars=0):
        """Generate dynamic stats badges"""
        badges = [
            self.create_badge("Followers", str(followers), "4c1", logo="github"),
            self.create_badge("Repositories", str(repos), "blue", logo="github"),
            self.create_badge("Total", f"{stars} Stars", "yellow", logo="star"),
            self.create_badge("Available", "for Work", "brightgreen", logo="handshake"),
            self.create_badge("Open", "to Collaborate", "blue", logo="github")
        ]
        return badges
    
    def social_badges(self):
        """Generate social media badges"""
        badges = [
            self.create_badge("Email", "rayyanahmed265@yahoo.com", "D14836", logo="gmail"),
            self.create_badge("LinkedIn", "Rayyan Ahmed", "0077B5", logo="linkedin"),
            self.create_badge("Twitter", "@rayyan9477", "1DA1F2", logo="twitter"),
            self.create_badge("Portfolio", "Visit", "4285F4", logo="google-chrome")
        ]
        return badges

if __name__ == "__main__":
    generator = BadgeGenerator()
    
    print("AI/ML Badges:")
    for badge in generator.ai_badges():
        print(f"![Badge]({badge})")
    
    print("\nTech Badges:")
    for badge in generator.tech_badges():
        print(f"![Badge]({badge})")
    
    print("\nSocial Badges:")
    for badge in generator.social_badges():
        print(f"![Badge]({badge})")
