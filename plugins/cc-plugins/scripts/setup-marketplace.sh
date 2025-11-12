#!/bin/bash

# Claude Code Marketplace Setup Script
# Creates a GitHub-based marketplace repository for publishing plugins

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
MARKETPLACE_DIR="$HOME/code/claude-plugins"
GITHUB_USER="${1:-maxfahl}"
PLUGIN_DEV_DIR="$HOME/.claude/plugins"

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Claude Code Marketplace Setup                            ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Prompt for marketplace directory
echo -e "${YELLOW}Where should the marketplace repository be created?${NC}"
echo -e "Default: ${MARKETPLACE_DIR}"
read -p "Path (or press Enter for default): " input_dir
if [ ! -z "$input_dir" ]; then
    MARKETPLACE_DIR="$input_dir"
fi

# Prompt for GitHub username
echo -e "\n${YELLOW}What is your GitHub username?${NC}"
echo -e "Default: ${GITHUB_USER}"
read -p "Username (or press Enter for default): " input_user
if [ ! -z "$input_user" ]; then
    GITHUB_USER="$input_user"
fi

# Prompt for author info
echo -e "\n${YELLOW}Author information:${NC}"
read -p "Your name: " AUTHOR_NAME
read -p "Your email: " AUTHOR_EMAIL
read -p "Your website (optional): " AUTHOR_URL

# Create directory
echo -e "\n${BLUE}Creating marketplace directory...${NC}"
mkdir -p "$MARKETPLACE_DIR"
cd "$MARKETPLACE_DIR"

# Initialize git if needed
if [ ! -d ".git" ]; then
    echo -e "${BLUE}Initializing git repository...${NC}"
    git init
    git branch -M main
else
    echo -e "${GREEN}Git repository already initialized${NC}"
fi

# Create directory structure
echo -e "${BLUE}Creating directory structure...${NC}"
mkdir -p .claude-plugin plugins

# Create .gitignore
echo -e "${BLUE}Creating .gitignore...${NC}"
cat > .gitignore << 'EOF'
# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Python
__pycache__/
*.py[cod]
*.pyc
.pytest_cache/

# Logs
*.log
logs/

# Temporary files
*.tmp
*.temp
EOF

# Create marketplace.json
echo -e "${BLUE}Creating marketplace.json...${NC}"
cat > .claude-plugin/marketplace.json << EOF
{
  "name": "${GITHUB_USER}",
  "owner": {
    "name": "${AUTHOR_NAME}",
    "email": "${AUTHOR_EMAIL}"
$([ ! -z "$AUTHOR_URL" ] && echo "    ,\"url\": \"${AUTHOR_URL}\"")
  },
  "metadata": {
    "description": "${AUTHOR_NAME}'s curated collection of Claude Code plugins",
    "version": "1.0.0",
    "homepage": "https://github.com/${GITHUB_USER}/claude-plugins"
  },
  "plugins": []
}
EOF

# Add cc-plugins to marketplace
echo -e "\n${BLUE}Adding cc-plugins to marketplace...${NC}"
cd plugins

if [ -d "$PLUGIN_DEV_DIR/cc-plugins" ]; then
    ln -s "$PLUGIN_DEV_DIR/cc-plugins" cc-plugins
    echo -e "${GREEN}✓ Symlinked cc-plugins${NC}"

    # Update marketplace.json with cc-plugins
    cd ..
    python3 << EOF
import json

with open('.claude-plugin/marketplace.json', 'r') as f:
    data = json.load(f)

data['plugins'].append({
    "name": "cc-plugins",
    "source": "./plugins/cc-plugins",
    "description": "Meta-plugin for creating, validating, and maintaining Claude Code plugins",
    "version": "1.0.0",
    "author": {
        "name": "${AUTHOR_NAME}",
        "url": "https://github.com/${GITHUB_USER}"
    },
    "category": "Development Engineering",
    "homepage": "https://github.com/${GITHUB_USER}/claude-plugins/tree/main/plugins/cc-plugins",
    "keywords": ["plugin-development", "validation", "scaffolding", "meta-plugin", "tools"]
})

with open('.claude-plugin/marketplace.json', 'w') as f:
    json.dump(data, f, indent=2)
    f.write('\n')

print("✓ Added cc-plugins to marketplace.json")
EOF
else
    echo -e "${YELLOW}⚠ cc-plugins not found at $PLUGIN_DEV_DIR/cc-plugins${NC}"
    echo -e "${YELLOW}  You'll need to add it manually${NC}"
fi

# Create README
echo -e "\n${BLUE}Creating README.md...${NC}"
cd "$MARKETPLACE_DIR"
cat > README.md << EOF
# ${AUTHOR_NAME}'s Claude Code Plugins

Curated collection of Claude Code plugins.

## Installation

Add this marketplace to Claude Code:

\`\`\`bash
/plugin marketplace add ${GITHUB_USER}/claude-plugins
\`\`\`

## Available Plugins

### cc-plugins

Meta-plugin for creating, validating, and maintaining Claude Code plugins.

**Install:**
\`\`\`bash
/plugin install cc-plugins@${GITHUB_USER}
\`\`\`

**Features:**
- Plugin scaffolding with official specifications
- Comprehensive validation tools
- Debugging utilities
- Documentation generation
- 5 commands, 3 agents, 2 skills
- 413 tests with 98% coverage

[Full Documentation](./plugins/cc-plugins/README.md)

## Adding Plugins

To add more plugins to this marketplace:

1. Create symlink: \`cd plugins && ln -s ~/.claude/plugins/my-plugin my-plugin\`
2. Update \`.claude-plugin/marketplace.json\`
3. Commit and push

## License

MIT License - See individual plugin directories for specific licenses.

---

Maintained by ${AUTHOR_NAME}
EOF

# Create LICENSE
echo -e "${BLUE}Creating LICENSE...${NC}"
cat > LICENSE << EOF
MIT License

Copyright (c) $(date +%Y) ${AUTHOR_NAME}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

# Commit
echo -e "\n${BLUE}Committing initial marketplace structure...${NC}"
git add .
git commit -m "Initial marketplace setup with cc-plugins"

# Summary
echo -e "\n${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  Marketplace Setup Complete!                              ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
echo -e "\n${BLUE}Location:${NC} $MARKETPLACE_DIR"
echo -e "${BLUE}Structure:${NC}"
echo -e "  .claude-plugin/marketplace.json"
echo -e "  plugins/cc-plugins → $PLUGIN_DEV_DIR/cc-plugins"
echo -e "  README.md"
echo -e "  LICENSE"
echo -e "  .gitignore"

echo -e "\n${YELLOW}Next Steps:${NC}"
echo -e "1. Create GitHub repository: ${GREEN}${GITHUB_USER}/claude-plugins${NC}"
echo -e "2. Add remote:"
echo -e "   ${BLUE}cd $MARKETPLACE_DIR${NC}"
echo -e "   ${BLUE}git remote add origin https://github.com/${GITHUB_USER}/claude-plugins.git${NC}"
echo -e "   ${BLUE}git push -u origin main${NC}"
echo -e "3. Add marketplace in Claude Code:"
echo -e "   ${BLUE}/plugin marketplace add ${GITHUB_USER}/claude-plugins${NC}"
echo -e "4. Install your plugin:"
echo -e "   ${BLUE}/plugin install cc-plugins@${GITHUB_USER}${NC}"

echo -e "\n${YELLOW}Adding More Plugins:${NC}"
echo -e "1. Create plugin in ${PLUGIN_DEV_DIR}/"
echo -e "2. Run: ${BLUE}cd $MARKETPLACE_DIR/plugins && ln -s ${PLUGIN_DEV_DIR}/new-plugin new-plugin${NC}"
echo -e "3. Update ${BLUE}.claude-plugin/marketplace.json${NC}"
echo -e "4. Commit and push"

echo -e "\n${GREEN}Setup complete! 🎉${NC}"
