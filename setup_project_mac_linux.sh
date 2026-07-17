#!/bin/bash
echo "Checking Python version..."
if ! command -v python3 &> /dev/null || ! python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 12) else 1)'; then
    echo "Python 3.12+ is required but not found."
    if command -v brew &> /dev/null; then
        echo "Installing python@3.12 via Homebrew..."
        brew install python@3.12
    else
        echo "Homebrew not found. Please install Python 3.12+ manually from https://www.python.org/downloads/"
        exit 1
    fi
fi

echo "Creating virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

echo "Upgrading pip and installing dependencies..."
python3 -m pip install --upgrade pip
pip install -r requirements.txt

echo "Virtual environment setup complete!"
