#!/bin/bash
# Auto-generated regeneration script for job application
# Created: 2025-06-25T04:13:49.220867
# AI Provider: llama (3-2-latest)

set -e  # Exit on any error

echo "🔄 Regenerating job application with same configuration..."
echo "📊 Original generation: 2025-06-25T04:13:49.220867"
echo "🤖 AI Provider: llama (3-2-latest)"

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "Makefile" ] || [ ! -d "src" ]; then
    echo "${RED}❌ Error: Not in project root directory${NC}"
    echo "Please run this script from the Bewerbung project root"
    exit 1
fi

# Check dependencies
echo "🔍 Checking dependencies..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "${RED}❌ Python3 not found${NC}"
    exit 1
fi

# Check virtual environment
if [ ! -d ".venv" ]; then
    echo "${YELLOW}⚠️  Virtual environment not found, creating one...${NC}"
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Set environment variables for exact reproduction
export AI_PROVIDER="llama"
export OUTPUT_STRUCTURE="by_model"
export INCLUDE_GENERATION_METADATA="true"
export LLAMA_MODEL="3-2-latest"

# Check AI provider availability
echo "🤖 Checking AI provider availability..."
make test-providers || echo "${YELLOW}⚠️  Some AI providers may not be available${NC}"

# Run generation
echo "🚀 Starting generation..."
make generate

echo "${GREEN}✅ Regeneration completed successfully!${NC}"
echo "📁 Check output in: Ausgabe/"
echo "🔍 Compare with original using: python tests/test_regeneration.py"
