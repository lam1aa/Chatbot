#!/bin/bash

# Setup script for BAföG Chatbot

echo "=== BAföG Chatbot Setup ==="
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✓ Created .env file"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your OPENROUTER_API_KEY"
    echo "   Get your free API key at: https://openrouter.ai/"
else
    echo "✓ .env file already exists"
fi

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Next steps:"
echo "1. Edit .env and add your OPENROUTER_API_KEY"
echo "2. Add your BAföG .txt files to the knowledge_base/ directory"
echo "3. Run: python main.py"
echo ""
