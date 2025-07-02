#!/bin/bash

echo "=== HST AI Engineer Project Setup (Poetry) ==="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH."
    echo "Please install Python 3.8 or higher from https://www.python.org/downloads/ or use your package manager."
    exit 1
fi

# Run the setup script
echo "Running Poetry setup script..."
python3 setup_poetry.py
if [ $? -ne 0 ]; then
    echo "Setup failed. Please check the error messages above."
    read -p "Press Enter to continue..."
    exit 1
fi

# Ask if the user wants to run the application
echo ""
read -p "Do you want to run the application now? (y/n): " RUN_APP
if [[ $RUN_APP =~ ^[Yy]$ ]]; then
    echo ""
    echo "Starting the application..."
    source venv/bin/activate && python main.py
else
    echo ""
    echo "To run the application later, activate the virtual environment with:"
    echo "  source venv/bin/activate"
    echo "Then run:"
    echo "  python main.py"
fi

read -p "Press Enter to continue..."