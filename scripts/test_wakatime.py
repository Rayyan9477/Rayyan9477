#!/usr/bin/env python3
"""
Test script to verify WakaTime API configuration
"""

import os
import requests
import json
from datetime import datetime, timedelta


def safe_print(message):
    try:
        print(message)
    except UnicodeEncodeError:
        print(message.encode('ascii', 'ignore').decode('ascii'))

def test_wakatime_api():
    """Test WakaTime API connection and configuration"""
    
    # Get API key from environment or secrets
    api_key = os.getenv('WAKATIME_API_KEY')
    
    if not api_key:
        safe_print("❌ WAKATIME_API_KEY not found in environment variables")
        safe_print("Please set the WAKATIME_API_KEY environment variable")
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
        safe_print(f"🔍 Testing WakaTime API connection...")
        safe_print(f"📅 Date: {today}")
        safe_print(f"🔗 URL: {url}")
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            safe_print("✅ WakaTime API connection successful!")
            
            # Display summary data
            if 'data' in data and data['data']:
                summary = data['data'][0]
                safe_print(f"📊 Total coding time today: {summary.get('grand_total', {}).get('text', '0 mins')}")
                
                # Show languages
                languages = summary.get('languages', [])
                if languages:
                    safe_print("💬 Languages used today:")
                    for lang in languages[:5]:  # Top 5 languages
                        name = lang.get('name', 'Unknown')
                        time = lang.get('text', '0 mins')
                        safe_print(f"   - {name}: {time}")
                else:
                    safe_print("💬 No coding activity recorded today")
            else:
                safe_print("📊 No data available for today")
                
            return True
            
        elif response.status_code == 401:
            safe_print("❌ Authentication failed - Invalid API key")
            safe_print("Please check your WAKATIME_API_KEY")
            return False
            
        elif response.status_code == 403:
            safe_print("❌ Access forbidden - API key may not have proper permissions")
            safe_print("Please check your WakaTime account settings")
            return False
            
        else:
            safe_print(f"❌ API request failed with status code: {response.status_code}")
            safe_print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        safe_print(f"❌ Network error: {e}")
        return False
    except json.JSONDecodeError as e:
        safe_print(f"❌ JSON parsing error: {e}")
        return False
    except Exception as e:
        safe_print(f"❌ Unexpected error: {e}")
        return False

def test_GH_TOKEN():
    """Test GitHub token configuration"""
    
    GH_TOKEN = os.getenv('GH_TOKEN')
    
    if not GH_TOKEN:
        safe_print("❌ GH_TOKEN not found in environment variables")
        return False
    
    headers = {
        'Authorization': f'token {GH_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    try:
        safe_print("🔍 Testing GitHub API connection...")
        
        # Test user endpoint
        response = requests.get('https://api.github.com/user', headers=headers, timeout=10)
        
        if response.status_code == 200:
            user_data = response.json()
            safe_print(f"✅ GitHub API connection successful!")
            safe_print(f"👤 Username: {user_data.get('login', 'Unknown')}")
            safe_print(f"📧 Email: {user_data.get('email', 'Not public')}")
            return True
        else:
            safe_print(f"❌ GitHub API request failed: {response.status_code}")
            return False
            
    except Exception as e:
        safe_print(f"❌ GitHub API test error: {e}")
        return False

def main():
    """Main test function"""
    safe_print("🧪 GitHub Actions Configuration Test")
    safe_print("=" * 50)
    
    # Test WakaTime API
    safe_print("\n1️⃣ Testing WakaTime API Configuration")
    safe_print("-" * 40)
    wakatime_success = test_wakatime_api()
    
    # Test GitHub Token
    safe_print("\n2️⃣ Testing GitHub Token Configuration")
    safe_print("-" * 40)
    github_success = test_GH_TOKEN()
    
    # Summary
    safe_print("\n📋 Test Summary")
    safe_print("-" * 40)
    safe_print(f"WakaTime API: {'✅ PASS' if wakatime_success else '❌ FAIL'}")
    safe_print(f"GitHub Token: {'✅ PASS' if github_success else '❌ FAIL'}")
    
    if wakatime_success and github_success:
        safe_print("\n🎉 All tests passed! Your GitHub Actions should work correctly.")
        safe_print("💡 You can now run the workflows manually to test them.")
    else:
        safe_print("\n⚠️  Some tests failed. Please check the configuration:")
        if not wakatime_success:
            safe_print("   - Verify WAKATIME_API_KEY is set correctly")
            safe_print("   - Check WakaTime account settings")
        if not github_success:
            safe_print("   - Verify GH_TOKEN has proper permissions")
            safe_print("   - Check repository workflow permissions")

if __name__ == "__main__":
    main() 