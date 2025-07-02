#!/bin/bash
# Cleanup script for removing obsolete files after migrating to Poetry

echo "=== Cleanup After Poetry Migration ==="
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH."
    echo "Please install Python 3 and try again."
    exit 1
fi

# Check if the cleanup script exists
if [ ! -f "cleanup_after_poetry.py" ]; then
    echo "Error: cleanup_after_poetry.py not found."
    echo "Please make sure you're running this script from the correct directory."
    exit 1
fi

# Check if Poetry is set up
if [ ! -f "pyproject.toml" ]; then
    echo "Error: pyproject.toml not found. Poetry setup is incomplete."
    echo "Please run setup_poetry.py first."
    exit 1
fi

# Run the cleanup script
echo "Running cleanup script..."
echo

# Check if --remove flag is provided
if [ "$1" == "--remove" ]; then
    python3 cleanup_after_poetry.py --remove
else
    python3 cleanup_after_poetry.py
    echo
    echo "To remove the obsolete files, run:"
    echo "  ./cleanup_after_poetry.sh --remove"
fi

echo
echo "Done."