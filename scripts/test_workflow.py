#!/usr/bin/env python3
"""
Test Workflow Script
Tests the GitHub Actions workflow components to ensure everything is working correctly
"""

import os
import sys
import subprocess
from datetime import datetime

def test_environment():
    """Test if the environment is properly configured"""
    try:
        print("🔍 Testing Environment Configuration...")
    except UnicodeEncodeError:
        print("Testing Environment Configuration...")
    
    # Check if we're in the right directory
    if not os.path.exists('README.md'):
        try:
            print("❌ README.md not found in current directory")
        except UnicodeEncodeError:
            print("ERROR: README.md not found in current directory")
        return False
    
    # Check if scripts directory exists
    if not os.path.exists('scripts'):
        try:
            print("❌ scripts directory not found")
        except UnicodeEncodeError:
            print("ERROR: scripts directory not found")
        return False
    
    # Check if required scripts exist
    required_scripts = ['daily_update.py', 'github_stats_updater.py']
    for script in required_scripts:
        if not os.path.exists(f'scripts/{script}'):
            try:
                print(f"❌ {script} not found in scripts directory")
            except UnicodeEncodeError:
                print(f"ERROR: {script} not found in scripts directory")
            return False
    
    try:
        print("✅ Environment configuration looks good")
    except UnicodeEncodeError:
        print("SUCCESS: Environment configuration looks good")
    return True

def test_github_token():
    """Test if GitHub token is available"""
    print("🔍 Testing GitHub Token...")
    
    gh_token = os.getenv('GH_TOKEN') or os.getenv('GITHUB_TOKEN')
    if not gh_token:
        print("⚠️ GitHub token not found in environment variables")
        print("   This is normal for local testing")
        return False
    
    print("✅ GitHub token found in environment")
    return True

def test_readme_structure():
    """Test if README.md has the required sections"""
    print("🔍 Testing README.md Structure...")
    
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()
        
        required_sections = [
            '<!--START_SECTION:activity-->',
            '<!--END_SECTION:activity-->',
            '<!--START_SECTION:waka-->',
            '<!--END_SECTION:waka-->'
        ]
        
        for section in required_sections:
            if section not in content:
                print(f"❌ Required section not found: {section}")
                return False
        
        print("✅ README.md structure is correct")
        return True
        
    except Exception as e:
        print(f"❌ Error reading README.md: {e}")
        return False

def test_scripts():
    """Test if the scripts can be imported and run basic functions"""
    print("🔍 Testing Scripts...")
    
    try:
        # Test daily_update.py
        sys.path.insert(0, 'scripts')
        import daily_update
        print("✅ daily_update.py imports successfully")
        
        # Test github_stats_updater.py
        import github_stats_updater
        print("✅ github_stats_updater.py imports successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing scripts: {e}")
        return False

def test_workflow_file():
    """Test if the workflow file exists and has correct structure"""
    print("🔍 Testing Workflow File...")
    
    workflow_path = '.github/workflows/actions.yml'
    if not os.path.exists(workflow_path):
        print("❌ Workflow file not found")
        return False
    
    try:
        with open(workflow_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for required workflow components
        required_components = [
            'schedule:',
            'cron:',
            'github-activity-readme',
            'waka-readme',
            'Platane/snk'
        ]
        
        for component in required_components:
            if component not in content:
                print(f"❌ Required workflow component not found: {component}")
                return False
        
        print("✅ Workflow file structure is correct")
        return True
        
    except Exception as e:
        print(f"❌ Error reading workflow file: {e}")
        return False

def main():
    """Run all tests"""
    try:
        print("🚀 Starting Workflow Tests...")
        print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 50)
    except UnicodeEncodeError:
        print("Starting Workflow Tests...")
        print(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 50)
    
    tests = [
        ("Environment", test_environment),
        ("GitHub Token", test_github_token),
        ("README Structure", test_readme_structure),
        ("Scripts", test_scripts),
        ("Workflow File", test_workflow_file)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            print(f"\n🧪 Running {test_name} Test...")
        except UnicodeEncodeError:
            print(f"\nRunning {test_name} Test...")
        
        if test_func():
            passed += 1
        print("-" * 30)
    
    try:
        print(f"\n📊 Test Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! Your workflow should work correctly.")
            return True
        else:
            print("⚠️ Some tests failed. Please check the issues above.")
            return False
    except UnicodeEncodeError:
        print(f"\nTest Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("All tests passed! Your workflow should work correctly.")
            return True
        else:
            print("Some tests failed. Please check the issues above.")
            return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
