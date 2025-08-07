#!/usr/bin/env python3
"""
Workflow Validation Script - Tests the GitHub Actions workflow configuration
"""

import os
import sys
import subprocess
import json
import re
from pathlib import Path

class WorkflowValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.info = []
        self.root_dir = Path(__file__).parent.parent
        self.github_dir = self.root_dir / ".github"
        self.workflows_dir = self.github_dir / "workflows"
        self.assets_dir = self.root_dir / "assets"
        
    def validate_directory_structure(self):
        """Validate the directory structure required for workflows"""
        print("🔍 Checking directory structure...")
        
        directories = [
            (".github", self.github_dir),
            (".github/workflows", self.workflows_dir),
            ("assets", self.assets_dir),
            ("scripts", self.root_dir / "scripts")
        ]
        
        for name, path in directories:
            if path.exists():
                self.info.append(f"✅ {name} directory exists")
            else:
                self.errors.append(f"❌ {name} directory missing")
                
    def validate_workflow_files(self):
        """Validate workflow file syntax and structure"""
        print("🔍 Checking workflow files...")
        
        if not self.workflows_dir.exists():
            self.errors.append("❌ Workflows directory missing, skipping workflow validation")
            return
            
        workflow_files = list(self.workflows_dir.glob("*.yml"))
        if not workflow_files:
            self.errors.append("❌ No workflow files found")
            return
            
        self.info.append(f"✅ Found {len(workflow_files)} workflow file(s)")
        
        for workflow_file in workflow_files:
            self.info.append(f"📄 Checking {workflow_file.name}")
            
            # Check if file is empty
            if workflow_file.stat().st_size == 0:
                self.errors.append(f"❌ {workflow_file.name} is empty")
                continue
                
            # Check for basic YAML syntax (not a full parser)
            content = workflow_file.read_text(encoding='utf-8')
            if not content.strip():
                self.errors.append(f"❌ {workflow_file.name} is effectively empty")
                continue
                
            # Check for common workflow keys
            if not re.search(r"name:", content):
                self.warnings.append(f"⚠️ {workflow_file.name} is missing a name field")
                
            if not re.search(r"on:", content):
                self.errors.append(f"❌ {workflow_file.name} is missing the 'on' trigger")
                
            if not re.search(r"jobs:", content):
                self.errors.append(f"❌ {workflow_file.name} is missing the 'jobs' section")
    
    def validate_python_scripts(self):
        """Validate Python scripts for basic syntax"""
        print("🔍 Checking Python scripts...")
        
        scripts_dir = self.root_dir / "scripts"
        if not scripts_dir.exists():
            self.errors.append("❌ Scripts directory missing, skipping script validation")
            return
            
        python_files = list(scripts_dir.glob("*.py"))
        if not python_files:
            self.warnings.append("⚠️ No Python scripts found")
            return
            
        self.info.append(f"✅ Found {len(python_files)} Python script(s)")
        
        for script_file in python_files:
            self.info.append(f"📄 Checking {script_file.name}")
            
            # Check if file is empty
            if script_file.stat().st_size == 0:
                self.errors.append(f"❌ {script_file.name} is empty")
                continue
                
            # Check for Python syntax errors
            try:
                subprocess.run(
                    [sys.executable, "-m", "py_compile", str(script_file)],
                    check=True,
                    capture_output=True
                )
                self.info.append(f"✅ {script_file.name} syntax is valid")
            except subprocess.CalledProcessError as e:
                self.errors.append(f"❌ {script_file.name} has syntax errors: {e.stderr.decode('utf-8')}")
    
    def validate_asset_files(self):
        """Validate required asset files"""
        print("🔍 Checking asset files...")
        
        if not self.assets_dir.exists():
            self.warnings.append("⚠️ Assets directory missing, skipping asset validation")
            return
            
        # Check for contribution snake SVG
        snake_svg = self.assets_dir / "github-contribution-grid-snake.svg"
        if snake_svg.exists():
            self.info.append("✅ Found contribution snake SVG")
        else:
            self.warnings.append("⚠️ Missing github-contribution-grid-snake.svg")
            
        # Check for required subdirectories
        for subdir in ["banners", "icons"]:
            if (self.assets_dir / subdir).exists():
                self.info.append(f"✅ Found {subdir} directory")
            else:
                self.warnings.append(f"⚠️ Missing {subdir} directory")
    
    def validate_requirements_file(self):
        """Validate requirements.txt file"""
        print("🔍 Checking requirements.txt...")
        
        req_file = self.root_dir / "requirements.txt"
        if not req_file.exists():
            self.errors.append("❌ requirements.txt file missing")
            return
            
        content = req_file.read_text(encoding='utf-8')
        if not content.strip():
            self.errors.append("❌ requirements.txt is empty")
            return
            
        # Check for essential packages
        essential_packages = ["requests"]
        for package in essential_packages:
            if not re.search(fr"{package}[\s=~>]", content):
                self.warnings.append(f"⚠️ requirements.txt might be missing {package}")
                
        self.info.append("✅ requirements.txt appears valid")
    
    def validate_readme(self):
        """Validate README.md file structure"""
        print("🔍 Checking README.md structure...")
        
        readme_file = self.root_dir / "README.md"
        if not readme_file.exists():
            self.errors.append("❌ README.md file missing")
            return
            
        content = readme_file.read_text(encoding='utf-8')
        if not content.strip():
            self.errors.append("❌ README.md is empty")
            return
            
        # Check for WakaTime section
        if "WakaTime Stats" in content and "<!--START_SECTION:waka-->" in content:
            self.info.append("✅ Found WakaTime section in README")
        elif "WakaTime Stats" in content:
            self.warnings.append("⚠️ WakaTime heading exists but missing START/END tags")
        else:
            self.warnings.append("⚠️ README.md doesn't contain WakaTime section")
            
        # Check for GitHub Activity section
        if "Recent GitHub Activity" in content and "<!--START_SECTION:activity-->" in content:
            self.info.append("✅ Found GitHub Activity section in README")
        elif "Recent GitHub Activity" in content:
            self.warnings.append("⚠️ GitHub Activity heading exists but missing START/END tags")
            
        self.info.append("✅ README.md structure appears valid")
    
    def check_all(self):
        """Run all validation checks"""
        self.validate_directory_structure()
        self.validate_workflow_files()
        self.validate_python_scripts()
        self.validate_asset_files()
        self.validate_requirements_file()
        self.validate_readme()
        
        return self.format_results()
        
    def format_results(self):
        """Format validation results"""
        total_errors = len(self.errors)
        total_warnings = len(self.warnings)
        
        result = {
            "status": "success" if total_errors == 0 else "failed",
            "summary": {
                "errors": total_errors,
                "warnings": total_warnings,
                "info": len(self.info)
            },
            "details": {
                "errors": self.errors,
                "warnings": self.warnings,
                "info": self.info
            }
        }
        
        # Print results to console
        print("\n📋 Validation Results:")
        print(f"Errors: {total_errors}, Warnings: {total_warnings}")
        
        if total_errors > 0:
            print("\n❌ ERRORS:")
            for error in self.errors:
                print(f"  {error}")
                
        if total_warnings > 0:
            print("\n⚠️ WARNINGS:")
            for warning in self.warnings:
                print(f"  {warning}")
                
        print("\n✅ INFO:")
        for info in self.info:
            print(f"  {info}")
            
        print("\n" + ("🎉 All checks passed!" if total_errors == 0 else "❌ Some checks failed!"))
        
        # Return as JSON and as a status code
        if total_errors > 0:
            return result, 1
        else:
            return result, 0

def main():
    validator = WorkflowValidator()
    result, status = validator.check_all()
    
    # Write results to JSON file
    with open('workflow_validation_results.json', 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"\n💾 Results saved to workflow_validation_results.json")
    return status

if __name__ == "__main__":
    sys.exit(main())
