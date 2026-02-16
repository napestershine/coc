#!/bin/bash
# Start the Flask API

echo "Starting CoC Flask API..."
cd "$(dirname "$0")"

if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating..."
    python -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt > /dev/null 2>&1

echo "Starting Flask server on http://0.0.0.0:5000"
python app.py
