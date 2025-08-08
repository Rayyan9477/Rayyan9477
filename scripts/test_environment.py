#!/usr/bin/env python3
"""
Environment Test Script - Verify GitHub Actions environment setup
Tests that all required environment variables and dependencies are properly configured
"""

import os
import sys
import requests
from datetime import datetime

def test_environment():
    """Test environment configuration"""
    print("🧪 Testing Environment Configuration...")
    print("=" * 50)
    
    # Test 1: Check Python dependencies
    print("\n📦 Testing Dependencies:")
    try:
        import requests
        print("✅ requests - OK")
        
        import dateutil
        print("✅ python-dateutil - OK")
        
        import pytz
        print("✅ pytz - OK")
        
        try:
            import dotenv
            print("✅ python-dotenv - OK")
        except ImportError:
            print("⚠️ python-dotenv - Not installed (optional)")
            
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False
    
    # Test 2: Check environment variables
    print("\n🔑 Testing Environment Variables:")
    
    gh_token = os.getenv('GH_TOKEN')
    github_token = os.getenv('GITHUB_TOKEN')
    wakatime_key = os.getenv('WAKATIME_API_KEY')
    
    if gh_token:
        print("✅ GH_TOKEN - Set")
        token_to_test = gh_token
    elif github_token:
        print("✅ GITHUB_TOKEN - Set (fallback)")
        token_to_test = github_token
    else:
        print("❌ No GitHub token found (GH_TOKEN or GITHUB_TOKEN)")
        print("   Set one of these environment variables with your Personal Access Token")
        return False
    
    if wakatime_key:
        print("✅ WAKATIME_API_KEY - Set")
    else:
        print("⚠️ WAKATIME_API_KEY - Not set (optional for WakaTime stats)")
    
    # Test 3: Validate GitHub token
    print("\n🔍 Testing GitHub API Access:")
    try:
        headers = {
            'Authorization': f'token {token_to_test}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        # Test basic API access
        response = requests.get('https://api.github.com/user', headers=headers, timeout=10)
        
        if response.status_code == 200:
            user_data = response.json()
            username = user_data.get('login', 'Unknown')
            print(f"✅ GitHub API - OK (User: {username})")
        elif response.status_code == 401:
            print("❌ GitHub API - Authentication failed")
            print("   Check that your token is valid and not expired")
            return False
        elif response.status_code == 403:
            print("❌ GitHub API - Rate limit or insufficient permissions")
            return False
        else:
            print(f"❌ GitHub API - Error {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ GitHub API - Connection error: {e}")
        return False
    
    # Test 4: Check file permissions
    print("\n📁 Testing File System:")
    
    readme_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'README.md')
    if os.path.exists(readme_path):
        print("✅ README.md - Found")
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if len(content) > 0:
                    print("✅ README.md - Readable")
                else:
                    print("❌ README.md - Empty file")
                    return False
        except Exception as e:
            print(f"❌ README.md - Cannot read: {e}")
            return False
    else:
        print(f"❌ README.md - Not found at {readme_path}")
        return False
    
    assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets')
    if os.path.exists(assets_dir):
        print("✅ assets/ - Directory exists")
    else:
        print("⚠️ assets/ - Directory missing (will be created)")
    
    # Test 5: Test basic GitHub operations
    print("\n🔧 Testing GitHub Operations:")
    try:
        # Test repository access
        repo_url = 'https://api.github.com/repos/Rayyan9477/Rayyan9477'
        response = requests.get(repo_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            repo_data = response.json()
            print(f"✅ Repository Access - OK")
            print(f"   Repo: {repo_data.get('full_name')}")
            print(f"   Private: {repo_data.get('private', False)}")
        else:
            print(f"❌ Repository Access - Error {response.status_code}")
            print("   Make sure the token has 'repo' permissions")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Repository Access - Connection error: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 All tests passed! Environment is properly configured.")
    print(f"⏰ Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return True

def main():
    """Main entry point"""
    print("🚀 GitHub Profile Automation - Environment Test")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if test_environment():
        print("\n✅ Ready for automation!")
        sys.exit(0)
    else:
        print("\n❌ Environment setup incomplete. Check the errors above.")
        print("\n📖 See SETUP-GUIDE.md for detailed setup instructions.")
        sys.exit(1)

if __name__ == "__main__":
    main()