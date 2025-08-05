#!/usr/bin/env python3
"""
Test Script for Daily Update System
Tests all components without making actual commits
"""

import os
import sys
import json
import tempfile
import shutil
from datetime import datetime
from daily_update import DailyUpdater

class DailyUpdateTester:
    def __init__(self):
        self.test_results = []
        self.backup_readme = None
        
    def log_test(self, test_name: str, success: bool, message: str = ""):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        result = f"[{status}] {test_name}"
        if message:
            result += f" - {message}"
        
        print(result)
        self.test_results.append({
            "test": test_name,
            "success": success,
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
    
    def backup_readme(self):
        """Create backup of README.md"""
        if os.path.exists('README.md'):
            self.backup_readme = 'README.md.backup'
            shutil.copy2('README.md', self.backup_readme)
            print("📋 Created README.md backup")
    
    def restore_readme(self):
        """Restore README.md from backup"""
        if self.backup_readme and os.path.exists(self.backup_readme):
            shutil.copy2(self.backup_readme, 'README.md')
            os.remove(self.backup_readme)
            print("📋 Restored README.md from backup")
    
    def test_quote_fetching(self):
        """Test quote fetching functionality"""
        print("\n🧪 Testing Quote Fetching...")
        
        updater = DailyUpdater()
        
        # Test API quote fetching
        try:
            quote = updater.get_daily_quote()
            if quote and 'content' in quote and 'author' in quote:
                self.log_test("Quote API Fetch", True, f"Got quote: '{quote['content'][:50]}...'")
            else:
                self.log_test("Quote API Fetch", False, "Invalid quote format")
        except Exception as e:
            self.log_test("Quote API Fetch", False, f"Exception: {e}")
        
        # Test fallback quotes
        try:
            fallback_quote = updater.tech_quotes[0]
            if fallback_quote and 'content' in fallback_quote:
                self.log_test("Fallback Quotes", True, f"Available: {len(updater.tech_quotes)} quotes")
            else:
                self.log_test("Fallback Quotes", False, "Invalid fallback quote format")
        except Exception as e:
            self.log_test("Fallback Quotes", False, f"Exception: {e}")
    
    def test_github_stats(self):
        """Test GitHub stats fetching"""
        print("\n🧪 Testing GitHub Stats...")
        
        updater = DailyUpdater()
        
        # Test with token
        if updater.github_token:
            try:
                stats = updater.get_github_stats()
                if stats:
                    self.log_test("GitHub Stats with Token", True, 
                                f"Stats: {stats.get('public_repos', 0)} repos, {stats.get('followers', 0)} followers")
                else:
                    self.log_test("GitHub Stats with Token", False, "No stats returned")
            except Exception as e:
                self.log_test("GitHub Stats with Token", False, f"Exception: {e}")
        else:
            self.log_test("GitHub Stats with Token", False, "No GITHUB_TOKEN available")
        
        # Test without token (should handle gracefully)
        original_token = updater.github_token
        updater.github_token = None
        
        try:
            stats = updater.get_github_stats()
            self.log_test("GitHub Stats without Token", True, "Handled gracefully")
        except Exception as e:
            self.log_test("GitHub Stats without Token", False, f"Exception: {e}")
        
        updater.github_token = original_token
    
    def test_contribution_snake(self):
        """Test contribution snake generation"""
        print("\n🧪 Testing Contribution Snake...")
        
        updater = DailyUpdater()
        
        try:
            success = updater.generate_contribution_snake()
            if success:
                self.log_test("Contribution Snake Generation", True, "SVG generated successfully")
            else:
                self.log_test("Contribution Snake Generation", False, "Failed to generate SVG")
        except Exception as e:
            self.log_test("Contribution Snake Generation", False, f"Exception: {e}")
    
    def test_readme_update(self):
        """Test README update functionality"""
        print("\n🧪 Testing README Update...")
        
        updater = DailyUpdater()
        
        # Create test quote and stats
        test_quote = {
            "content": "This is a test quote for validation purposes.",
            "author": "Test Author"
        }
        
        test_stats = {
            "followers": 25,
            "public_repos": 15,
            "total_stars": 100
        }
        
        try:
            success = updater.update_readme_content(test_quote, test_stats)
            if success:
                self.log_test("README Content Update", True, "Content updated successfully")
                
                # Verify quote was updated
                with open('README.md', 'r', encoding='utf-8') as f:
                    content = f.read()
                    if "This is a test quote for validation purposes" in content:
                        self.log_test("Quote Verification", True, "Quote found in README")
                    else:
                        self.log_test("Quote Verification", False, "Quote not found in README")
            else:
                self.log_test("README Content Update", False, "Failed to update content")
        except Exception as e:
            self.log_test("README Content Update", False, f"Exception: {e}")
    
    def test_config_loading(self):
        """Test configuration loading"""
        print("\n🧪 Testing Configuration...")
        
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
            
            required_keys = ['github', 'daily_update', 'quotes', 'github_stats']
            missing_keys = [key for key in required_keys if key not in config]
            
            if not missing_keys:
                self.log_test("Configuration Loading", True, "All required keys present")
            else:
                self.log_test("Configuration Loading", False, f"Missing keys: {missing_keys}")
        except Exception as e:
            self.log_test("Configuration Loading", False, f"Exception: {e}")
    
    def test_logging(self):
        """Test logging functionality"""
        print("\n🧪 Testing Logging...")
        
        updater = DailyUpdater()
        
        try:
            # Test log writing
            test_message = "Test log message"
            updater.log(test_message)
            
            # Check if log file exists and contains message
            if os.path.exists(updater.log_file):
                with open(updater.log_file, 'r', encoding='utf-8') as f:
                    log_content = f.read()
                    if test_message in log_content:
                        self.log_test("Logging Functionality", True, "Log written and verified")
                    else:
                        self.log_test("Logging Functionality", False, "Log message not found")
            else:
                self.log_test("Logging Functionality", False, "Log file not created")
        except Exception as e:
            self.log_test("Logging Functionality", False, f"Exception: {e}")
    
    def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting Daily Update System Tests...")
        print("=" * 50)
        
        # Backup README before testing
        self.backup_readme()
        
        try:
            # Run all tests
            self.test_config_loading()
            self.test_quote_fetching()
            self.test_github_stats()
            self.test_contribution_snake()
            self.test_readme_update()
            self.test_logging()
            
        finally:
            # Restore README after testing
            self.restore_readme()
        
        # Print summary
        print("\n" + "=" * 50)
        print("📊 Test Summary:")
        
        passed = sum(1 for result in self.test_results if result['success'])
        total = len(self.test_results)
        
        print(f"✅ Passed: {passed}/{total}")
        print(f"❌ Failed: {total - passed}/{total}")
        
        if passed == total:
            print("🎉 All tests passed! Daily update system is ready.")
            return True
        else:
            print("⚠️ Some tests failed. Please check the issues above.")
            return False
    
    def save_test_report(self):
        """Save detailed test report"""
        report = {
            "test_run": datetime.now().isoformat(),
            "summary": {
                "total": len(self.test_results),
                "passed": sum(1 for r in self.test_results if r['success']),
                "failed": sum(1 for r in self.test_results if not r['success'])
            },
            "results": self.test_results
        }
        
        with open('test_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print("📋 Test report saved to test_report.json")

def main():
    """Main test runner"""
    tester = DailyUpdateTester()
    success = tester.run_all_tests()
    tester.save_test_report()
    
    if success:
        print("\n✅ All tests completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 