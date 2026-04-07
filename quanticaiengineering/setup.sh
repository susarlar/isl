#!/bin/bash
# Quick Start Setup Script for macOS/Linux
# Run: chmod +x setup.sh && ./setup.sh

echo "================================================"
echo "Policy Corpus RAG - Setup Script"
echo "================================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Step 1: Check Python installation
echo -e "${YELLOW}[1/5] Checking Python installation...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓ Python found: $PYTHON_VERSION${NC}"
else
    echo -e "${RED}✗ Python not found. Please install Python 3.9 or higher.${NC}"
    exit 1
fi

# Step 2: Create virtual environment
echo ""
echo -e "${YELLOW}[2/5] Setting up virtual environment...${NC}"
if [ -d "venv" ]; then
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
else
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Step 3: Activate virtual environment and upgrade pip
echo ""
echo -e "${YELLOW}[3/5] Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

echo "Upgrading pip..."
python -m pip install --upgrade pip --quiet
echo -e "${GREEN}✓ Pip upgraded${NC}"

# Step 4: Install dependencies
echo ""
echo -e "${YELLOW}[4/5] Installing dependencies...${NC}"
echo "This may take a few minutes..."
pip install -r requirements.txt --quiet
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Dependencies installed successfully${NC}"
else
    echo -e "${RED}✗ Failed to install dependencies${NC}"
    exit 1
fi

# Step 5: Create .env file
echo ""
echo -e "${YELLOW}[5/5] Setting up configuration...${NC}"
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${GREEN}✓ Created .env file from template${NC}"
    echo ""
    echo -e "${CYAN}IMPORTANT: Edit .env and add your Groq API key!${NC}"
    echo -e "${CYAN}Get your key from: https://console.groq.com${NC}"
else
    echo -e "${GREEN}✓ .env file already exists${NC}"
fi

# Create necessary directories
mkdir -p data/vector_store logs
echo -e "${GREEN}✓ Created necessary directories${NC}"

# Summary
echo ""
echo "================================================"
echo -e "${GREEN}Setup Complete!${NC}"
echo "================================================"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Edit .env file and add your GROQ_API_KEY"
echo "2. Run: python config.py  (to verify configuration)"
echo "3. Run: python scripts/build_vector_db.py  (to build index)"
echo "4. Run: python app/query.py  (to start querying)"
echo ""
echo "For detailed instructions, see README.md"
echo ""
