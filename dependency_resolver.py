#!/usr/bin/env python
"""
Dependency Resolver Script

This script helps diagnose and resolve dependency conflicts using Poetry.
It can be used to check for conflicts, update dependencies, and export
requirements.txt for compatibility with non-Poetry workflows.

Usage:
    python dependency_resolver.py [--check] [--update] [--export]
"""

import os
import sys
import subprocess
import argparse
import platform
from pathlib import Path

def get_python_executable():
    """Get the appropriate Python executable path based on the platform and environment."""
    # If running in a virtual environment, use that Python
    if sys.prefix != sys.base_prefix:
        return sys.executable
    
    # Otherwise, use the system Python that's running this script
    return sys.executable

def check_poetry_installed():
    """Check if Poetry is installed and install it if not."""
    try:
        # Check if Poetry is installed
        subprocess.run(
            [get_python_executable(), "-m", "poetry", "--version"], 
            check=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        print("✓ Poetry is already installed")
        return True
    except subprocess.CalledProcessError:
        print("Installing Poetry...")
        try:
            subprocess.run(
                [get_python_executable(), "-m", "pip", "install", "poetry"], 
                check=True
            )
            print("✓ Poetry installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install Poetry: {e}")
            return False

def check_dependencies():
    """Check for dependency conflicts using Poetry."""
    print("Checking for dependency conflicts...")
    try:
        result = subprocess.run(
            [get_python_executable(), "-m", "poetry", "check"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("✓ No dependency conflicts found")
            return True
        else:
            print(f"✗ Dependency conflicts found:\n{result.stdout}\n{result.stderr}")
            return False
    except subprocess.CalledProcessError as e:
        print(f"✗ Error checking dependencies: {e}")
        return False

def update_dependencies():
    """Update dependencies using Poetry."""
    print("Updating dependencies...")
    try:
        subprocess.run(
            [get_python_executable(), "-m", "poetry", "update"],
            check=True
        )
        print("✓ Dependencies updated successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error updating dependencies: {e}")
        return False

def export_requirements():
    """Export dependencies to requirements.txt for compatibility with pip."""
    print("Exporting dependencies to requirements.txt...")
    try:
        # Export production dependencies
        subprocess.run(
            [get_python_executable(), "-m", "poetry", "export", "-f", "requirements.txt", "--output", "requirements.txt", "--without-hashes"],
            check=True
        )
        print("✓ requirements.txt generated successfully")
        
        # Export development dependencies if dev group exists
        try:
            subprocess.run(
                [get_python_executable(), "-m", "poetry", "export", "-f", "requirements.txt", "--output", "dev-requirements.txt", "--with", "dev", "--without-hashes"],
                check=True
            )
            print("✓ dev-requirements.txt generated successfully")
        except subprocess.CalledProcessError:
            print("✗ No dev dependencies found or error exporting dev dependencies")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error exporting dependencies: {e}")
        return False

def diagnose_conflicts():
    """Diagnose dependency conflicts in more detail."""
    print("Diagnosing dependency conflicts...")
    try:
        # Show dependency tree
        print("\nDependency tree:")
        subprocess.run(
            [get_python_executable(), "-m", "poetry", "show", "--tree"],
            check=True
        )
        
        # Show outdated dependencies
        print("\nOutdated dependencies:")
        subprocess.run(
            [get_python_executable(), "-m", "poetry", "show", "--outdated"],
            check=True
        )
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error diagnosing conflicts: {e}")
        return False

def main():
    """Main function to run the script."""
    parser = argparse.ArgumentParser(description="Dependency Resolver Script")
    parser.add_argument("--check", action="store_true", help="Check for dependency conflicts")
    parser.add_argument("--update", action="store_true", help="Update dependencies")
    parser.add_argument("--export", action="store_true", help="Export dependencies to requirements.txt")
    parser.add_argument("--diagnose", action="store_true", help="Diagnose dependency conflicts in detail")
    args = parser.parse_args()
    
    # If no arguments provided, show help
    if not (args.check or args.update or args.export or args.diagnose):
        parser.print_help()
        return True
    
    print("=== Dependency Resolver ===")
    
    if not check_poetry_installed():
        return False
    
    success = True
    
    if args.check:
        if not check_dependencies():
            success = False
    
    if args.diagnose:
        if not diagnose_conflicts():
            success = False
    
    if args.update:
        if not update_dependencies():
            success = False
    
    if args.export:
        if not export_requirements():
            success = False
    
    if success:
        print("\nAll operations completed successfully.")
    else:
        print("\nSome operations failed. Please check the output above.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)