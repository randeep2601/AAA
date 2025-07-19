#!/bin/bash

echo "🇮🇳 Hinglish Translation Tool - Starting..."
echo "=============================================="

# Activate virtual environment
source venv/bin/activate

# Set Flask environment variables
export FLASK_APP=app.py
export FLASK_ENV=development
export FLASK_DEBUG=1

# Create directories if they don't exist
mkdir -p uploads processed

echo "📁 Directories created"
echo "🔧 Starting Flask development server..."
echo "🌐 Access the tool at: http://localhost:5000"
echo "=============================================="

# Run the Flask application
python app.py