# Claude Code Custom Marketplace Setup Guide

Complete guide for publishing cc-plugins and future plugins to your own GitHub-based Claude Code marketplace.

## Overview

Claude Code supports custom plugin marketplaces hosted on GitHub (or any Git repository). Users can add your marketplace with:
```bash
/plugin marketplace add maxfahl/claude-plugins
```

---

## Recommended Workflow

### Option 1: GitHub Marketplace with Symlinks (Recommended)

This keeps plugins in their development location while publishing via GitHub.

**Structure:**
```
~/.claude/plugins/           # Your development directory (current)
  ├── cc-plugins/            # This plugin (stays here)
  ├── agent-os/              # Future plugin 1
  └── content-publisher/     # Future plugin 2

~/code/claude-plugins/       # GitHub repository (marketplace)
  ├── .claude-plugin/
  │   └── marketplace.json   # Marketplace manifest
  ├── plugins/               # Symlinked plugins
  │   ├── cc-plugins -> ~/.claude/plugins/cc-plugins
  │   ├── agent-os -> ~/.claude/plugins/agent-os
  │   └── content-publisher -> ~/.claude/plugins/content-publisher
  ├── README.md
  └── LICENSE
```

**Advantages:**
- Plugins stay in development location
- Easy to develop and test locally
- Simple to publish updates
- Git repository only contains marketplace structure
- Your existing local marketplace structure works the same way

---

## Step-by-Step Setup

### 1. Create GitHub Marketplace Repository

```bash
# Create marketplace repo directory
mkdir -p ~/code/claude-plugins
cd ~/code/claude-plugins

# Initialize git
git init
git branch -M main

# Create structure
mkdir -p .claude-plugin plugins

# Create .gitignore
cat > .gitignore << 'EOF'
# OS
.DS_Store
.DS_Store?
._*

# IDE
.vscode/
.idea/

# Python
__pycache__/
*.pyc

# Logs
*.log
EOF
```

### 2. Create Marketplace Manifest

Create `.claude-plugin/marketplace.json`:

```json
{
  "name": "maxfahl",
  "owner": {
    "name": "Max Fahl",
    "email": "max@fahl.io",
    "url": "https://maxfahl.com"
  },
  "metadata": {
    "description": "Max Fahl's curated collection of Claude Code plugins",
    "version": "1.0.0",
    "homepage": "https://github.com/maxfahl/claude-plugins"
  },
  "plugins": [
    {
      "name": "cc-plugins",
      "source": "./plugins/cc-plugins",
      "description": "Meta-plugin for creating, validating, and maintaining Claude Code plugins",
      "version": "1.0.0",
      "author": {
        "name": "Max Fahl",
        "url": "https://github.com/maxfahl"
      },
      "category": "Development Engineering",
      "homepage": "https://github.com/maxfahl/claude-plugins/tree/main/plugins/cc-plugins",
      "keywords": ["plugin-development", "validation", "scaffolding", "meta-plugin", "tools"]
    }
  ]
}
```

### 3. Create Symlinks to Your Plugins

```bash
cd ~/code/claude-plugins/plugins

# Symlink cc-plugins
ln -s ~/.claude/plugins/cc-plugins cc-plugins

# Future plugins (when ready)
# ln -s ~/.claude/plugins/agent-os agent-os
# ln -s ~/.claude/plugins/content-publisher content-publisher
```

### 4. Create README

Create `README.md`:

```markdown
# Max Fahl's Claude Code Plugins

Curated collection of Claude Code plugins by Max Fahl.

## Installation

Add this marketplace to Claude Code:

\`\`\`
/plugin marketplace add maxfahl/claude-plugins
\`\`\`

## Available Plugins

### cc-plugins

Meta-plugin for creating, validating, and maintaining Claude Code plugins.

**Install:**
\`\`\`
/plugin install cc-plugins@maxfahl
\`\`\`

**Features:**
- Plugin scaffolding with official specifications
- Comprehensive validation tools
- Debugging utilities
- Documentation generation
- 5 commands, 3 agents, 2 skills

[Full Documentation](./plugins/cc-plugins/README.md)

## Contributing

These plugins are maintained by Max Fahl. For issues or suggestions, please open an issue in this repository.

## License

MIT License - See individual plugin directories for specific licenses.
\`\`\`
```

### 5. Configure Git to Follow Symlinks

**Option A: Commit Symlinks (Recommended for Public Repos)**

Symlinks work on Unix systems (macOS, Linux) but not Windows. For cross-platform support, consider copying plugin directories instead.

```bash
# Add symlinks (works on Unix)
git add .
git commit -m "Add marketplace structure with cc-plugins"
```

**Option B: Copy Plugin Directories (Cross-Platform)**

```bash
# Instead of symlinks, copy the plugin
cd ~/code/claude-plugins/plugins
cp -r ~/.claude/plugins/cc-plugins .

# Update after changes
rsync -av --delete ~/.claude/plugins/cc-plugins/ ./cc-plugins/
```

### 6. Push to GitHub

```bash
# Create repo on GitHub first, then:
git remote add origin https://github.com/maxfahl/claude-plugins.git
git push -u origin main
```

### 7. Add Marketplace to Claude Code

```bash
# In Claude Code:
/plugin marketplace add maxfahl/claude-plugins

# Install your plugin:
/plugin install cc-plugins@maxfahl
```

---

## Updating Plugins

### With Symlinks (Development Workflow)

```bash
# 1. Make changes in development directory
cd ~/.claude/plugins/cc-plugins
# ... make changes ...
git commit -m "Update: feature description"

# 2. Update marketplace (optional: only if marketplace.json changed)
cd ~/code/claude-plugins
git add .
git commit -m "Update cc-plugins to v1.1.0"
git push

# 3. Users update with:
# /plugin update cc-plugins@maxfahl
```

### With Copied Directories

```bash
# 1. Make changes in development directory
cd ~/.claude/plugins/cc-plugins
# ... make changes ...
git commit -m "Update: feature description"

# 2. Sync to marketplace
cd ~/code/claude-plugins/plugins
rsync -av --delete ~/.claude/plugins/cc-plugins/ ./cc-plugins/

# 3. Commit and push marketplace
cd ~/code/claude-plugins
git add .
git commit -m "Update cc-plugins to v1.1.0"
git push

# 4. Users update with:
# /plugin update cc-plugins@maxfahl
```

---

## Adding More Plugins

When you create new plugins:

```bash
# 1. Create plugin in development directory
cd ~/.claude/plugins
# Create your plugin: my-new-plugin/

# 2. Add to marketplace
cd ~/code/claude-plugins/plugins
ln -s ~/.claude/plugins/my-new-plugin my-new-plugin
# OR: cp -r ~/.claude/plugins/my-new-plugin .

# 3. Update marketplace.json
cd ~/code/claude-plugins
# Edit .claude-plugin/marketplace.json, add:
{
  "name": "my-new-plugin",
  "source": "./plugins/my-new-plugin",
  "description": "Description of your plugin",
  "version": "1.0.0",
  "author": {
    "name": "Max Fahl",
    "url": "https://github.com/maxfahl"
  },
  "category": "Development Engineering",
  "homepage": "https://github.com/maxfahl/claude-plugins/tree/main/plugins/my-new-plugin",
  "keywords": ["keyword1", "keyword2"]
}

# 4. Commit and push
git add .
git commit -m "Add my-new-plugin"
git push
```

---

## Marketplace Categories

Choose from these official categories:

- **Development Engineering** - Developer tools, code quality, testing
- **Workflow Orchestration** - Automation, task management
- **Git Workflow** - Git helpers, version control
- **Security, Compliance, & Legal** - Security scanning, compliance
- **Code Quality Testing** - Testing frameworks, quality tools
- **Documentation** - Documentation generators, API docs
- **Automation DevOps** - CI/CD, deployment, infrastructure
- **Project & Product Management** - Planning, tracking
- **Data Analytics** - Data processing, analysis
- **Design UX** - Design tools, prototyping
- **Marketing Growth** - Marketing automation
- **Business Sales** - Sales tools, CRM

---

## Current Setup (Your Existing Structure)

You already have:
```
~/.claude/plugins/cc-plugins/          # ✓ Plugin exists here
~/.claude/local-marketplace/           # ✓ Local marketplace
  ├── .claude-plugin/marketplace.json  # ✓ Marketplace config
  └── [symlinks to plugins]            # ✓ Already using symlinks
```

**Recommended Action:**
Create a GitHub repo that mirrors your local marketplace structure. This allows:
1. Keep developing in `~/.claude/plugins/`
2. Publish via GitHub marketplace
3. Share with others easily
4. Maintain local testing setup

---

## Testing Before Publishing

```bash
# 1. Add your marketplace locally (for testing)
/plugin marketplace add ~/code/claude-plugins

# 2. Install your plugin
/plugin install cc-plugins@local

# 3. Test all functionality

# 4. Once working, push to GitHub and update path
/plugin marketplace remove local
/plugin marketplace add maxfahl/claude-plugins
```

---

## Best Practices

1. **Semantic Versioning**: Use semver (1.0.0, 1.1.0, 2.0.0)
2. **Documentation**: Each plugin needs comprehensive README
3. **Testing**: Test locally before publishing
4. **License**: Include LICENSE file
5. **CHANGELOG**: Track changes in CHANGELOG.md
6. **Git Tags**: Tag releases with version numbers
7. **CI/CD**: Consider GitHub Actions for automated testing

---

## Example: Complete Setup Script

```bash
#!/bin/bash

# Create marketplace repository
mkdir -p ~/code/claude-plugins
cd ~/code/claude-plugins
git init
git branch -M main

# Create structure
mkdir -p .claude-plugin plugins

# Create .gitignore
cat > .gitignore << 'EOF'
.DS_Store
__pycache__/
*.pyc
.vscode/
.idea/
EOF

# Create marketplace.json
cat > .claude-plugin/marketplace.json << 'EOF'
{
  "name": "maxfahl",
  "owner": {
    "name": "Max Fahl",
    "email": "max@fahl.io"
  },
  "metadata": {
    "description": "Max Fahl's Claude Code plugins",
    "version": "1.0.0",
    "homepage": "https://github.com/maxfahl/claude-plugins"
  },
  "plugins": []
}
EOF

# Symlink cc-plugins
cd plugins
ln -s ~/.claude/plugins/cc-plugins cc-plugins

# Create README
cd ..
cat > README.md << 'EOF'
# Max Fahl's Claude Code Plugins

Add this marketplace:
\`\`\`
/plugin marketplace add maxfahl/claude-plugins
\`\`\`
EOF

# Commit
git add .
git commit -m "Initial marketplace setup"

# Push to GitHub (create repo first)
# git remote add origin https://github.com/maxfahl/claude-plugins.git
# git push -u origin main

echo "Marketplace created at ~/code/claude-plugins"
echo "Next steps:"
echo "1. Create GitHub repository: maxfahl/claude-plugins"
echo "2. Add remote and push"
echo "3. Test with: /plugin marketplace add maxfahl/claude-plugins"
```

---

## Resources

- **Official Docs**: https://code.claude.com/docs/en/plugins
- **Example Marketplaces**:
  - https://github.com/ccplugins/marketplace (150+ plugins)
  - https://github.com/ananddtyagi/claude-code-marketplace
  - https://github.com/EveryInc/every-marketplace

---

## Troubleshooting

**Issue**: Symlinks don't work on Windows
**Solution**: Use copied directories with rsync for updates

**Issue**: Plugin not appearing in marketplace
**Solution**: Ensure `source` path in marketplace.json is correct

**Issue**: Users can't install plugin
**Solution**: Verify GitHub repo is public and marketplace.json is in `.claude-plugin/`

**Issue**: Updates not reflected
**Solution**: Users need to run `/plugin update plugin-name@marketplace-name`

---

This guide provides a complete workflow for publishing cc-plugins and future plugins to your own GitHub marketplace while keeping your development workflow intact.
