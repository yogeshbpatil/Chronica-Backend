#!/bin/bash

# Chronica Backend - Setup Script for macOS/Linux

echo "🚀 Chronica Backend Setup Script"
echo "=================================="

# Check Python version
echo "Checking Python version..."
python3 --version

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please update .env with your database credentials"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Update .env with your PostgreSQL credentials"
echo "2. Run: alembic upgrade head"
echo "3. Run: python -m app.main"
echo "4. Visit: http://localhost:8000/api/docs"
