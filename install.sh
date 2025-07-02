#!/bin/bash
set -e

echo "🚀 Setting up Logistics Agents Project..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source $HOME/.cargo/env
fi

# Create virtual environment
echo "Creating virtual environment..."
uv venv --python 3.11

# Activate virtual environment
echo "Activating virtual environment..."
if [ -f ".venv/Scripts/activate" ]; then
    source .venv/Scripts/activate
elif [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
else
    echo "❌ Could not find virtual environment activation script"
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
uv pip install -e ".[dev,notebooks]"

# Copy environment file
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cat > .env << EOF
# OpenAI Configuration
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_MODEL=gpt-4o-mini

# Application Configuration
LOG_LEVEL=INFO
DEBUG=false

# Data Configuration
DATA_PATH=./data/samples/inventory_sample_data.csv
OUTPUT_PATH=./data/outputs/

# Optional: MCP Server Configuration
MCP_SERVER_URL_SSE=https://your-mcp-server.com/webhook
EOF
    echo "⚠️  Please edit .env file with your OpenAI API key"
fi

# Install pre-commit hooks
echo "Setting up pre-commit hooks..."
pre-commit install

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your OpenAI API key"
if [ -f ".venv/Scripts/activate" ]; then
    echo "2. Run: source .venv/Scripts/activate"
else
    echo "2. Run: source .venv/bin/activate"
fi
echo "3. Run: python run.py --help" 