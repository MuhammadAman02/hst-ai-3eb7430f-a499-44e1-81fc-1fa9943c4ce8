#!/usr/bin/env python
"""
Compatibility Checker Script

This script checks for known compatibility issues between packages,
particularly focusing on NiceGUI and FastAPI compatibility.

It can be used alongside Poetry to ensure that the resolved dependencies
will work correctly together in practice.

Usage:
    python compatibility_checker.py
"""

import os
import sys
import subprocess
import re
import json
from pathlib import Path
from packaging import version

# Known compatibility issues
KNOWN_ISSUES = [
    {
        "package1": "nicegui",
        "package2": "fastapi",
        "condition": "nicegui>=1.3.0 requires fastapi<0.100.0",
        "check": lambda v1, v2: version.parse(v1) >= version.parse("1.3.0") and version.parse(v2) >= version.parse("0.100.0"),
        "recommendation": "Use nicegui<1.3.0 or downgrade fastapi to <0.100.0"
    },
    # Add more known compatibility issues here as they are discovered
]

def get_python_executable():
    """Get the appropriate Python executable path based on the platform and environment."""
    # If running in a virtual environment, use that Python
    if sys.prefix != sys.base_prefix:
        return sys.executable
    
    # Otherwise, use the system Python that's running this script
    return sys.executable

def get_installed_version(package_name):
    """Get the installed version of a package using Poetry."""
    try:
        # Use Poetry to get the installed version
        result = subprocess.run(
            [get_python_executable(), "-m", "poetry", "show", package_name],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Parse the output to get the version
        match = re.search(r"version\s+:\s+([\d\.]+)", result.stdout)
        if match:
            return match.group(1)
        return None
    except subprocess.CalledProcessError:
        return None

def get_all_installed_packages():
    """Get all installed packages and their versions using Poetry."""
    try:
        # Use Poetry to get all installed packages
        result = subprocess.run(
            [get_python_executable(), "-m", "poetry", "show", "--no-dev", "--format", "json"],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Parse the JSON output
        packages = json.loads(result.stdout)
        return {pkg["name"]: pkg["version"] for pkg in packages}
    except (subprocess.CalledProcessError, json.JSONDecodeError):
        return {}

def check_compatibility():
    """Check for known compatibility issues between installed packages."""
    print("Checking for known compatibility issues...")
    
    # Get all installed packages
    packages = get_all_installed_packages()
    if not packages:
        print("✗ Failed to get installed packages")
        return False
    
    issues_found = False
    
    # Check for known issues
    for issue in KNOWN_ISSUES:
        pkg1 = issue["package1"]
        pkg2 = issue["package2"]
        
        if pkg1 in packages and pkg2 in packages:
            ver1 = packages[pkg1]
            ver2 = packages[pkg2]
            
            if issue["check"](ver1, ver2):
                print(f"\n⚠️ Compatibility issue detected: {issue['condition']}")
                print(f"  - {pkg1} version: {ver1}")
                print(f"  - {pkg2} version: {ver2}")
                print(f"  - Recommendation: {issue['recommendation']}")
                issues_found = True
    
    if not issues_found:
        print("✓ No known compatibility issues found")
        return True
    
    return False

def check_poetry_installed():
    """Check if Poetry is installed."""
    try:
        subprocess.run(
            [get_python_executable(), "-m", "poetry", "--version"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    """Main function to run the script."""
    print("=== Compatibility Checker ===")
    
    if not check_poetry_installed():
        print("✗ Poetry is not installed. Please install Poetry first.")
        return False
    
    return check_compatibility()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)