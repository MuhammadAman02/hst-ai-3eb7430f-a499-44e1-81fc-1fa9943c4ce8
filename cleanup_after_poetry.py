#!/usr/bin/env python
"""
Cleanup Script After Poetry Migration

This script identifies and lists files that are no longer needed after migrating to Poetry
for dependency management. It can optionally remove these files if confirmed by the user.

Usage:
    python cleanup_after_poetry.py [--remove]

Options:
    --remove    Actually remove the files instead of just listing them
"""

import os
import sys
import shutil
from pathlib import Path

# Files that are no longer needed after migrating to Poetry
OBSOLETE_FILES = [
    "requirements.in",
    "requirements.txt",
    "dev-requirements.in",
    "dev-requirements.txt",
    "compile_requirements.py",
]

# Files that should be kept for backward compatibility or reference
KEEP_FILES = [
    "setup.py",  # May still be needed for some tools or deployment scenarios
    "setup_and_run.bat",
    "setup_and_run.sh",
]

# Files that are part of the Poetry setup
POETRY_FILES = [
    "pyproject.toml",
    "poetry.lock",
    "setup_poetry.py",
    "setup_and_run_poetry.bat",
    "setup_and_run_poetry.sh",
]

def check_poetry_setup():
    """Check if Poetry is properly set up in the project."""
    if not os.path.exists("pyproject.toml"):
        print("Error: pyproject.toml not found. Poetry setup is incomplete.")
        return False
    
    if not os.path.exists("poetry.lock"):
        print("Warning: poetry.lock not found. Run 'poetry install' first.")
        return False
    
    return True

def list_obsolete_files():
    """List files that are no longer needed after migrating to Poetry."""
    found_files = []
    
    for file in OBSOLETE_FILES:
        if os.path.exists(file):
            found_files.append(file)
    
    return found_files

def remove_files(files):
    """Remove the specified files."""
    for file in files:
        try:
            os.remove(file)
            print(f"✓ Removed {file}")
        except Exception as e:
            print(f"✗ Failed to remove {file}: {e}")

def main():
    """Main function to run the script."""
    print("=== Cleanup After Poetry Migration ===\n")
    
    # Check if Poetry is properly set up
    if not check_poetry_setup():
        print("\nPlease complete the Poetry setup before running this cleanup script.")
        return False
    
    # List obsolete files
    obsolete_files = list_obsolete_files()
    
    if not obsolete_files:
        print("No obsolete files found. Your project is already clean.")
        return True
    
    print("The following files are no longer needed after migrating to Poetry:")
    for file in obsolete_files:
        print(f"  - {file}")
    
    # Check if --remove flag is provided
    if "--remove" in sys.argv:
        print("\nRemoving obsolete files...")
        remove_files(obsolete_files)
        print("\nCleanup completed successfully!")
    else:
        print("\nTo remove these files, run:")
        print("  python cleanup_after_poetry.py --remove")
        print("\nNote: This will permanently delete the files listed above.")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)