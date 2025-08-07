#!/usr/bin/env python3
"""
Test Runner Script for GitHub Profile Components

This script tests all components of the GitHub profile update system:
- WakaTime API configuration
- GitHub token configuration
- SVG asset validation
- README.md structure
- Workflow configuration
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def print_header(title):
    """Print a section header"""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")

def run_test(test_name, command, env=None):
    """Run a test command and return the result"""
    print(f"\n>> Testing: {test_name}")
    print(f"   Command: {command}")
    
    # Prepare environment
    test_env = os.environ.copy()
    if env:
        test_env.update(env)
    
    try:
        result = subprocess.run(
            command, 
            shell=True,
            capture_output=True,
            text=True,
            env=test_env
        )
        
        if result.returncode == 0:
            print(f"\n✅ {test_name} PASSED")
            print(f"Output:\n{result.stdout[:500]}...")
            if len(result.stdout) > 500:
                print("(output truncated...)")
        else:
            print(f"\n❌ {test_name} FAILED (Exit code: {result.returncode})")
            print(f"Error:\n{result.stderr}")
            print(f"Output:\n{result.stdout}")
        
        return result.returncode == 0
    except Exception as e:
        print(f"\n❌ {test_name} ERROR: {str(e)}")
        return False

def main():
    """Main test runner"""
    print_header("GitHub Profile Components Test Runner")
    
    # Find repo root
    current_dir = Path(__file__).parent
    repo_root = current_dir.parent
    scripts_dir = current_dir
    
    # Track test results
    results = {
        "pass": 0,
        "fail": 0,
        "total": 0,
        "tests": {}
    }
    
    # 1. Test WakaTime Configuration
    print_header("1. WakaTime API Configuration Test")
    wakatime_test = run_test(
        "WakaTime API",
        f"python {scripts_dir}/test_wakatime.py"
    )
    results["tests"]["wakatime"] = wakatime_test
    results["total"] += 1
    if wakatime_test:
        results["pass"] += 1
    else:
        results["fail"] += 1
    
    # 2. Test Workflow Configuration
    print_header("2. Workflow Configuration Test")
    workflow_test = run_test(
        "Workflow Configuration",
        f"python {scripts_dir}/validate_workflow.py"
    )
    results["tests"]["workflow"] = workflow_test
    results["total"] += 1
    if workflow_test:
        results["pass"] += 1
    else:
        results["fail"] += 1
    
    # 3. Test README Structure
    print_header("3. README.md Structure Test")
    readme_test = True  # Placeholder for actual test
    
    # Check if README exists
    readme_path = repo_root / "README.md"
    if not readme_path.exists():
        print("❌ README.md not found")
        readme_test = False
    else:
        # Check for important sections
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()
            sections = [
                "WakaTime Stats",
                "GitHub Analytics",
                "Tech",
                "Daily Inspiration",
                "START_SECTION:waka",
                "END_SECTION:waka"
            ]
            
            missing_sections = []
            for section in sections:
                if section not in content:
                    missing_sections.append(section)
            
            if missing_sections:
                print(f"❌ Missing sections in README.md: {', '.join(missing_sections)}")
                readme_test = False
            else:
                print("✅ All required sections found in README.md")
    
    results["tests"]["readme"] = readme_test
    results["total"] += 1
    if readme_test:
        results["pass"] += 1
    else:
        results["fail"] += 1
    
    # 4. Test Daily Update Script
    print_header("4. Daily Update Script Test (Dry Run)")
    daily_update_test = run_test(
        "Daily Update Script",
        f"cd {scripts_dir} && python daily_update.py",
        {"PUSH_CHANGES": "false"}
    )
    results["tests"]["daily_update"] = daily_update_test
    results["total"] += 1
    if daily_update_test:
        results["pass"] += 1
    else:
        results["fail"] += 1
    
    # Print Summary
    print_header("Test Summary")
    print(f"Total Tests: {results['total']}")
    print(f"Passed: {results['pass']}")
    print(f"Failed: {results['fail']}")
    print(f"Success Rate: {results['pass'] / results['total'] * 100:.1f}%")
    
    # Save results to file
    results_path = repo_root / "test_results.json"
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to {results_path}")
    
    # Return appropriate exit code
    return 0 if results["fail"] == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
