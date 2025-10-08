#!/usr/bin/env python3
"""
Simple Test Workflow Script
Tests the GitHub Actions workflow components without Unicode characters
"""

import os
import sys
from datetime import datetime

def test_environment():
    """Test if the environment is properly configured"""
    print("Testing Environment Configuration...")
    
    # Check if we're in the right directory
    if not os.path.exists('README.md'):
        print("ERROR: README.md not found in current directory")
        return False
    
    # Check if we're in scripts directory or need to look for it
    scripts_dir = 'scripts' if os.path.exists('scripts') else '.'
    
    # Check if required scripts exist
    required_scripts = ['daily_update.py', 'github_stats_updater.py']
    for script in required_scripts:
        script_path = os.path.join(scripts_dir, script)
        if not os.path.exists(script_path):
            print(f"ERROR: {script} not found in {scripts_dir} directory")
            return False
    
    print("SUCCESS: Environment configuration looks good")
    return True

def test_github_token():
    """Test if GitHub token is available"""
    print("Testing GitHub Token...")
    
    gh_token = os.getenv('GH_TOKEN') or os.getenv('GITHUB_TOKEN')
    if not gh_token:
        print("WARNING: GitHub token not found in environment variables")
        print("   This is normal for local testing")
        return False
    
    print("SUCCESS: GitHub token found in environment")
    return True

def test_readme_structure():
    """Test if README.md has the required sections"""
    print("Testing README.md Structure...")
    
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
                print(f"ERROR: Required section not found: {section}")
                return False
        
        print("SUCCESS: README.md structure is correct")
        return True
        
    except Exception as e:
        print(f"ERROR: Error reading README.md: {e}")
        return False

def test_scripts():
    """Test if the scripts can be imported and run basic functions"""
    print("Testing Scripts...")
    
    try:
        # Determine scripts directory
        scripts_dir = 'scripts' if os.path.exists('scripts') else '.'
        
        # Test daily_update.py
        sys.path.insert(0, scripts_dir)
        import daily_update
        print("SUCCESS: daily_update.py imports successfully")
        
        # Test github_stats_updater.py
        import github_stats_updater
        print("SUCCESS: github_stats_updater.py imports successfully")
        
        return True
        
    except Exception as e:
        print(f"ERROR: Error testing scripts: {e}")
        return False

def test_workflow_file():
    """Test if the workflow file exists and has correct structure"""
    print("Testing Workflow File...")
    
    # Check for workflow file in different possible locations
    possible_paths = [
        '.github/workflows/actions.yml',
        '../.github/workflows/actions.yml',
        '../../.github/workflows/actions.yml'
    ]
    
    workflow_path = None
    for path in possible_paths:
        if os.path.exists(path):
            workflow_path = path
            break
    
    if not workflow_path:
        print("ERROR: Workflow file not found in any expected location")
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
                print(f"ERROR: Required workflow component not found: {component}")
                return False
        
        print("SUCCESS: Workflow file structure is correct")
        return True
        
    except Exception as e:
        print(f"ERROR: Error reading workflow file: {e}")
        return False

def main():
    """Run all tests"""
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
        print(f"\nRunning {test_name} Test...")
        if test_func():
            passed += 1
        print("-" * 30)
    
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
