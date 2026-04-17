#!/bin/bash

echo "============================================"
echo " Collaborative Live Report - Quick Start"
echo "============================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3 from https://www.python.org/"
    exit 1
fi

echo "[1/4] Checking dependencies..."
if ! python3 -c "import flask" &> /dev/null; then
    echo "Flask not found. Installing dependencies..."
    pip3 install -r requirements.txt
else
    echo "Dependencies already installed."
fi

echo ""
echo "[2/4] Running tests..."
python3 test_collaborative.py
if [ $? -ne 0 ]; then
    echo ""
    echo "Tests failed. Starting server anyway..."
fi

echo ""
echo "[3/4] Starting API server..."
echo ""
echo "============================================"
echo "  Server will start at http://localhost:5000"
echo "  Press Ctrl+C to stop the server"
echo "============================================"
echo ""

# Start the server
python3 api_server.py
