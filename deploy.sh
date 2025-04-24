#!/bin/bash
# The Measured Mile - Deployment Script
# This script builds the site and deploys it to GitHub Pages

set -e  # Exit immediately if a command exits with a non-zero status

# Color codes for better readability
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Starting deployment process for The Measured Mile...${NC}"

# Ensure we're in the project root directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Step 1: Verify requirements
echo -e "${YELLOW}Checking requirements...${NC}"
if ! command -v python3.11 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is required but not installed.${NC}"
    exit 1
fi

if ! command -v git &> /dev/null; then
    echo -e "${RED}Error: Git is required but not installed.${NC}"
    exit 1
fi

# Verify Python dependencies
python3.11 -c "import markdown, yaml, jinja2, slugify" 2>/dev/null || {
    echo -e "${RED}Error: Missing required Python packages.${NC}"
    echo -e "${YELLOW}Please run: pip install -r requirements.txt${NC}"
    exit 1
}

# Step 2: Build the site
echo -e "${YELLOW}Building the site...${NC}"
python3.11 build.py

# Step 3: Prepare for GitHub Pages
echo -e "${YELLOW}Preparing for GitHub Pages deployment...${NC}"

# Check if the output directory exists
if [ ! -d "output" ]; then
    echo -e "${RED}Error: Output directory not found. Build may have failed.${NC}"
    exit 1
fi

# Create .nojekyll file to prevent Jekyll processing
touch output/.nojekyll

# Create/Update CNAME file for your custom domain
echo "measuredmile.com" > output/CNAME
echo -e "${GREEN}Added CNAME file for measuredmile.com${NC}"

# Create/Update CNAME file if you have a custom domain
if [ -n "$CUSTOM_DOMAIN" ]; then
    echo "$CUSTOM_DOMAIN" > output/CNAME
    echo -e "${GREEN}Added CNAME file for $CUSTOM_DOMAIN${NC}"
fi

# Step 4: Deploy to GitHub Pages
echo -e "${YELLOW}Deploying to GitHub Pages...${NC}"

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo -e "${RED}Error: Not a git repository. Please initialize git first.${NC}"
    echo -e "${YELLOW}Run: git init${NC}"
    exit 1
fi

# Get the current branch name
BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo -e "${YELLOW}Current branch: $BRANCH${NC}"

# Add, commit, and push the changes to the gh-pages branch
echo -e "${YELLOW}Pushing updates to gh-pages branch...${NC}"

# Option 1: Use the gh-pages branch with subtree push
if [ "$1" == "--subtree" ]; then
    git add .
    git commit -m "Update source content"
    git push origin $BRANCH
    git subtree push --prefix output origin gh-pages
    echo -e "${GREEN}Site deployed using git subtree!${NC}"
# Option 2: Use a separate gh-pages branch (recommended for most setups)
else
    # Create a temporary directory
    TEMP_DIR=$(mktemp -d)
    cp -R output/* "$TEMP_DIR"
    
    # Switch to gh-pages branch, creating it if it doesn't exist
    if git show-ref --verify --quiet refs/heads/gh-pages; then
        git checkout gh-pages
    else
        git checkout --orphan gh-pages
        git rm -rf .
    fi
    
    # Copy the built site content
    cp -R "$TEMP_DIR"/* .
    
    # Add all files
    git add -A
    
    # Commit and push changes
    git commit -m "Site updated at $(date)"
    git push origin gh-pages
    
    # Switch back to the original branch
    git checkout $BRANCH
    
    # Clean up
    rm -rf "$TEMP_DIR"
    
    echo -e "${GREEN}Site deployed to GitHub Pages!${NC}"
fi

echo -e "${GREEN}Deployment completed successfully!${NC}"
echo -e "${YELLOW}Your site should be live shortly at: ${NC}"
if [ -n "$CUSTOM_DOMAIN" ]; then
    echo -e "${GREEN}https://$CUSTOM_DOMAIN${NC}"
else
    echo -e "${GREEN}https://$(git config --get remote.origin.url | sed 's/.*github.com[:/]\(.*\)\.git/\1/' | sed 's/\/.*//')$(git config --get remote.origin.url | sed 's/.*github.com[:/]\([^/]*\)\/\([^/.]*\).*/\/\2/' | tr -d '\n' )/index.html${NC}"
fi