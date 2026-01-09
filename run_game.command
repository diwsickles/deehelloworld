#!/bin/bash
# The Rookie: Badge of Honor - macOS Launcher
# Double-click this file to run the game on macOS

# Get the directory of this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to the script directory
cd "$DIR"

# Check if Python 3 is available
if command -v python3 &> /dev/null; then
    echo "Starting The Rookie: Badge of Honor..."
    python3 rookie_puzzle_game.py
else
    echo "Error: Python 3 is not installed."
    echo "Please install Python 3 from https://www.python.org/downloads/"
    echo "or via Homebrew: brew install python3"
    read -p "Press Enter to exit..."
fi
