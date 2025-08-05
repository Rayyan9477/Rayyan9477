#!/usr/bin/env python3
"""
Setup Script for Daily README Automation
Helps users configure the automation system quickly
"""

import os
import json
import sys
from pathlib import Path

def print_banner():
    """Print setup banner"""
    print("🤖 Daily README Automation Setup")
    print("=" * 40)
    print("This script will help you configure the daily automation system.")
    print()

def get_user_input(prompt, default=None, required=True):
    """Get user input with validation"""
    while True:
        if default:
            user_input = input(f"{prompt} (default: {default}): ").strip()
            if not user_input:
                user_input = default
        else:
            user_input = input(f"{prompt}: ").strip()
        
        if user_input or not required:
            return user_input
        else:
            print("❌ This field is required. Please try again.")

def validate_github_username(username):
    """Validate GitHub username format"""
    if not username:
        return False, "Username cannot be empty"
    
    if len(username) < 1 or len(username) > 39:
        return False, "Username must be between 1 and 39 characters"
    
    if not username.replace('-', '').replace('_', '').isalnum():
        return False, "Username can only contain alphanumeric characters, hyphens, and underscores"
    
    return True, "Valid username"

def create_config():
    """Create configuration file"""
    print("📝 Configuration Setup")
    print("-" * 20)
    
    # Get GitHub username
    while True:
        username = get_user_input("Enter your GitHub username")
        is_valid, message = validate_github_username(username)
        if is_valid:
            break
        else:
            print(f"❌ {message}")
    
    # Get repository name
    repo_name = get_user_input("Enter your repository name", username)
    
    # Get schedule preference
    print("\n⏰ Schedule Configuration")
    print("Available schedules:")
    print("1. Daily at 8:00 AM UTC (recommended)")
    print("2. Daily at 12:00 PM UTC")
    print("3. Daily at 6:00 PM UTC")
    print("4. Custom schedule")
    
    schedule_choice = get_user_input("Choose schedule (1-4)", "1")
    
    schedules = {
        "1": "0 8 * * *",
        "2": "0 12 * * *", 
        "3": "0 18 * * *",
        "4": "0 8 * * *"  # Default for custom
    }
    
    cron_schedule = schedules.get(schedule_choice, "0 8 * * *")
    
    if schedule_choice == "4":
        print("\n📅 Custom Schedule")
        print("Enter cron schedule (e.g., '0 8 * * *' for daily at 8 AM UTC)")
        custom_schedule = get_user_input("Custom cron schedule", "0 8 * * *")
        cron_schedule = custom_schedule
    
    # Get timezone
    timezone = get_user_input("Enter timezone for scheduling", "UTC")
    
    # Create config
    config = {
        "github": {
            "username": username,
            "repository": repo_name,
            "branch": "main"
        },
        "daily_update": {
            "enabled": True,
            "schedule": cron_schedule,
            "timezone": timezone,
            "auto_push": True,
            "log_level": "INFO",
            "max_retries": 3,
            "timeout": 30
        },
        "quotes": {
            "api_url": "https://api.quotable.io/random",
            "fallback_enabled": True,
            "max_length": 200,
            "categories": ["technology", "programming", "innovation"]
        },
        "github_stats": {
            "enabled": True,
            "include_stars": True,
            "include_forks": True,
            "include_contributions": True,
            "update_badges": True
        },
        "contribution_snake": {
            "enabled": True,
            "theme": "tokyonight",
            "output_format": "svg",
            "include_dark_theme": True
        },
        "readme": {
            "file_path": "README.md",
            "backup_enabled": True,
            "backup_retention_days": 7,
            "update_timestamps": True,
            "preserve_formatting": True
        },
        "notifications": {
            "success_enabled": True,
            "failure_enabled": True,
            "log_upload": True,
            "retention_days": 7
        },
        "security": {
            "token_required": True,
            "rate_limit_handling": True,
            "error_reporting": True,
            "sanitize_output": True
        }
    }
    
    return config

def save_config(config):
    """Save configuration to file"""
    try:
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=2)
        print("✅ Configuration saved to config.json")
        return True
    except Exception as e:
        print(f"❌ Error saving configuration: {e}")
        return False

def check_dependencies():
    """Check if required dependencies are installed"""
    print("\n📦 Checking Dependencies")
    print("-" * 20)
    
    required_packages = ['requests', 'PyGithub']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.lower().replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} (missing)")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ Missing packages: {', '.join(missing_packages)}")
        print("Install them with: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies are installed")
    return True

def check_files():
    """Check if required files exist"""
    print("\n📁 Checking Required Files")
    print("-" * 20)
    
    required_files = [
        'scripts/daily_update.py',
        '.github/workflows/daily-update.yml',
        'requirements.txt'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} (missing)")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️ Missing files: {', '.join(missing_files)}")
        print("Please ensure all automation files are present in your repository.")
        return False
    
    print("✅ All required files are present")
    return True

def create_assets_directory():
    """Create assets directory if it doesn't exist"""
    assets_dir = Path('assets')
    if not assets_dir.exists():
        assets_dir.mkdir()
        print("✅ Created assets directory")
    else:
        print("✅ Assets directory already exists")

def print_next_steps():
    """Print next steps for the user"""
    print("\n🎯 Next Steps")
    print("=" * 40)
    print("1. 🔑 Set up GitHub Token:")
    print("   - Go to GitHub Settings → Developer Settings → Personal Access Tokens")
    print("   - Create a new token with 'repo' and 'read:user' permissions")
    print("   - Add it to your repository secrets as 'GITHUB_TOKEN'")
    print()
    print("2. 🧪 Test the system:")
    print("   cd scripts")
    print("   python test_daily_update.py")
    print()
    print("3. 🚀 Run manually (optional):")
    print("   cd scripts")
    print("   PUSH_CHANGES=false python daily_update.py")
    print()
    print("4. 📅 The automation will run daily at the scheduled time")
    print("   You can also trigger it manually from the GitHub Actions tab")
    print()
    print("📚 For more information, see AUTOMATION_README.md")

def main():
    """Main setup function"""
    print_banner()
    
    # Check if config already exists
    if os.path.exists('config.json'):
        overwrite = get_user_input("config.json already exists. Overwrite? (y/N)", "N", required=False)
        if overwrite.lower() != 'y':
            print("Setup cancelled.")
            return
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Please install missing dependencies before continuing.")
        return
    
    # Check files
    if not check_files():
        print("\n❌ Please ensure all required files are present before continuing.")
        return
    
    # Create assets directory
    create_assets_directory()
    
    # Create configuration
    config = create_config()
    
    # Save configuration
    if save_config(config):
        print("\n🎉 Setup completed successfully!")
        print_next_steps()
    else:
        print("\n❌ Setup failed. Please check the errors above.")

if __name__ == "__main__":
    main() 