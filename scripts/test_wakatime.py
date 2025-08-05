#!/usr/bin/env python3
"""
Test script to verify WakaTime API configuration
"""

import os
import requests
import json
from datetime import datetime, timedelta

def test_wakatime_api():
    """Test WakaTime API connection and configuration"""
    
    # Get API key from environment or secrets
    api_key = os.getenv('WAKATIME_API_KEY')
    
    if not api_key:
        print("❌ WAKATIME_API_KEY not found in environment variables")
        print("Please set the WAKATIME_API_KEY environment variable")
        return False
    
    # Test API endpoint
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    
    # Get current date
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Test summaries endpoint
    url = f'https://wakatime.com/api/v1/users/current/summaries?start={today}&end={today}'
    
    try:
        print(f"🔍 Testing WakaTime API connection...")
        print(f"📅 Date: {today}")
        print(f"🔗 URL: {url}")
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ WakaTime API connection successful!")
            
            # Display summary data
            if 'data' in data and data['data']:
                summary = data['data'][0]
                print(f"📊 Total coding time today: {summary.get('grand_total', {}).get('text', '0 mins')}")
                
                # Show languages
                languages = summary.get('languages', [])
                if languages:
                    print("💬 Languages used today:")
                    for lang in languages[:5]:  # Top 5 languages
                        name = lang.get('name', 'Unknown')
                        time = lang.get('text', '0 mins')
                        print(f"   - {name}: {time}")
                else:
                    print("💬 No coding activity recorded today")
            else:
                print("📊 No data available for today")
                
            return True
            
        elif response.status_code == 401:
            print("❌ Authentication failed - Invalid API key")
            print("Please check your WAKATIME_API_KEY")
            return False
            
        elif response.status_code == 403:
            print("❌ Access forbidden - API key may not have proper permissions")
            print("Please check your WakaTime account settings")
            return False
            
        else:
            print(f"❌ API request failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_github_token():
    """Test GitHub token configuration"""
    
    github_token = os.getenv('GITHUB_TOKEN')
    
    if not github_token:
        print("❌ GITHUB_TOKEN not found in environment variables")
        return False
    
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    try:
        print("🔍 Testing GitHub API connection...")
        
        # Test user endpoint
        response = requests.get('https://api.github.com/user', headers=headers, timeout=10)
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ GitHub API connection successful!")
            print(f"👤 Username: {user_data.get('login', 'Unknown')}")
            print(f"📧 Email: {user_data.get('email', 'Not public')}")
            return True
        else:
            print(f"❌ GitHub API request failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ GitHub API test error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 GitHub Actions Configuration Test")
    print("=" * 50)
    
    # Test WakaTime API
    print("\n1️⃣ Testing WakaTime API Configuration")
    print("-" * 40)
    wakatime_success = test_wakatime_api()
    
    # Test GitHub Token
    print("\n2️⃣ Testing GitHub Token Configuration")
    print("-" * 40)
    github_success = test_github_token()
    
    # Summary
    print("\n📋 Test Summary")
    print("-" * 40)
    print(f"WakaTime API: {'✅ PASS' if wakatime_success else '❌ FAIL'}")
    print(f"GitHub Token: {'✅ PASS' if github_success else '❌ FAIL'}")
    
    if wakatime_success and github_success:
        print("\n🎉 All tests passed! Your GitHub Actions should work correctly.")
        print("💡 You can now run the workflows manually to test them.")
    else:
        print("\n⚠️  Some tests failed. Please check the configuration:")
        if not wakatime_success:
            print("   - Verify WAKATIME_API_KEY is set correctly")
            print("   - Check WakaTime account settings")
        if not github_success:
            print("   - Verify GITHUB_TOKEN has proper permissions")
            print("   - Check repository workflow permissions")

if __name__ == "__main__":
    main() 