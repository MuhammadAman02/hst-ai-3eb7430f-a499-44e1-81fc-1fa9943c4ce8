#!/usr/bin/env python
"""
Test Script for Poetry Setup

This script verifies that Poetry is set up correctly by checking for the presence of
required files and attempting to import critical dependencies.

Usage:
    python test_poetry_setup.py
"""

import os
import sys
import importlib

# Critical dependencies to verify
CRITICAL_DEPENDENCIES = [
    "fastapi",
    "nicegui",
    "uvicorn",
    "pydantic"
]

def check_poetry_files():
    """Check if Poetry files exist."""
    required_files = ["pyproject.toml", "poetry.lock"]
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("The following required Poetry files are missing:")
        for file in missing_files:
            print(f"  - {file}")
        return False
    
    print("✓ All required Poetry files are present.")
    return True

def check_dependencies():
    """Check if critical dependencies can be imported."""
    missing_deps = []
    
    for dep in CRITICAL_DEPENDENCIES:
        try:
            importlib.import_module(dep)
            print(f"✓ {dep} is installed and can be imported.")
        except ImportError:
            missing_deps.append(dep)
            print(f"✗ {dep} cannot be imported.")
    
    if missing_deps:
        print("\nThe following critical dependencies are missing:")
        for dep in missing_deps:
            print(f"  - {dep}")
        return False
    
    return True

def main():
    """Main function to run the tests."""
    print("=== Testing Poetry Setup ===\n")
    
    files_ok = check_poetry_files()
    deps_ok = check_dependencies()
    
    if files_ok and deps_ok:
        print("\n✓ Poetry setup is correct and all critical dependencies are available.")
        return True
    else:
        print("\n✗ Poetry setup is incomplete or some dependencies are missing.")
        print("Please run setup_poetry.py to fix the issues.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)