---
description: "Create a new Claude Code plugin with correct structure and official specifications. Accepts a plugin name and optional parameters, scaffolds the plugin structure, and provides next steps."
allowed-tools: ["Bash", "Read", "Write"]
argument-hint: "Plugin name in kebab-case (e.g., my-awesome-plugin) and optional parameters"
model: "sonnet"
disable-model-invocation: false
---

# Create New Plugin

Creates a new Claude Code plugin with the correct directory structure and official specification compliance.

## Usage

```bash
/cc-plugins:create my-awesome-plugin
/cc-plugins:create my-plugin --description "My plugin description"
/cc-plugins:create my-plugin --author "John Doe" --license "MIT"
```

## What It Does

1. Validates the plugin name (kebab-case format)
2. Creates the plugin directory structure:
   - `.claude-plugin/plugin.json` - Plugin manifest
   - `commands/` - Slash commands directory
   - `agents/` - Specialized agents directory
   - `skills/` - Development skills directory
   - `scripts/` - Scripts directory
   - `docs/` - Documentation directory
   - `tests/` - Test suite directory
3. Generates a basic plugin manifest with provided metadata
4. Creates a README.md with installation instructions
5. Validates the created plugin structure
6. Provides next steps for development

## Parameters

- **Plugin Name** ($1): Required. Name in kebab-case (e.g., `my-plugin`)
- **--description**: Optional. Brief description of the plugin
- **--author**: Optional. Plugin author name
- **--license**: Optional. License type (default: MIT)

## Examples

### Basic Plugin Creation

```bash
/cc-plugins:create my-tool
```

Creates a plugin named `my-tool` with default settings.

### With Custom Metadata

```bash
/cc-plugins:create awesome-helper \
  --description "A helper plugin for developers" \
  --author "Jane Developer" \
  --license "Apache-2.0"
```

Creates `awesome-helper` with custom metadata.

## Output

On success, displays:

```
✓ Plugin 'my-awesome-plugin' created successfully!

Location: /path/to/my-awesome-plugin

Next steps:
1. cd my-awesome-plugin
2. Create your first command: add a .md file in commands/
3. Add agents in agents/ directory for specialized functionality
4. Create skills in skills/ directory for reusable workflows
5. Run tests: pytest tests/
6. Validate structure: /cc-plugins:validate

For documentation: /cc-plugins:document
```

---

!bash
# Parse arguments
PLUGIN_NAME="${1:?Plugin name required. Usage: /cc-plugins:create my-plugin}"
shift || true

# Default values
DESCRIPTION="A new Claude Code plugin"
AUTHOR="Developer"
LICENSE="MIT"

# Parse optional parameters
while [[ $# -gt 0 ]]; do
  case $1 in
    --description)
      DESCRIPTION="$2"
      shift 2
      ;;
    --author)
      AUTHOR="$2"
      shift 2
      ;;
    --license)
      LICENSE="$2"
      shift 2
      ;;
    *)
      echo "Unknown parameter: $1"
      exit 1
      ;;
  esac
done

# Validate plugin name (kebab-case)
if [[ ! "$PLUGIN_NAME" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
  echo "Error: Plugin name must be in kebab-case (lowercase with hyphens)"
  echo "Example: my-awesome-plugin"
  exit 1
fi

# Check if directory already exists
if [ -d "$PLUGIN_NAME" ]; then
  echo "Error: Directory '$PLUGIN_NAME' already exists"
  exit 1
fi

# Create plugin directory structure
mkdir -p "$PLUGIN_NAME"/{.claude-plugin,commands,agents,skills,scripts,docs,tests}

# Create plugin manifest
cat > "$PLUGIN_NAME/.claude-plugin/plugin.json" << EOF
{
  "name": "$PLUGIN_NAME",
  "version": "1.0.0",
  "description": "$DESCRIPTION",
  "author": {
    "name": "$AUTHOR"
  },
  "license": "$LICENSE",
  "keywords": ["plugin", "claude-code"]
}
EOF

# Create basic README
cat > "$PLUGIN_NAME/README.md" << EOF
# $PLUGIN_NAME

$DESCRIPTION

## Installation

1. Clone or download this plugin to your Claude Code plugins directory:
   \`\`\`bash
   cd ~/.claude/plugins
   # Place this plugin directory here
   \`\`\`

2. Restart Claude Code to load the plugin

## Usage

### Commands

This plugin provides the following commands:

- Add your commands here

### Agents

This plugin includes specialized agents:

- Add your agents here

### Skills

This plugin offers reusable skills:

- Add your skills here

## Development

### Running Tests

\`\`\`bash
pytest tests/ -v
\`\`\`

### Validation

\`\`\`bash
/cc-plugins:validate
\`\`\`

### Documentation

\`\`\`bash
/cc-plugins:document
\`\`\`

## License

$LICENSE

---

Created with [cc-plugins](https://github.com/maxfahl/cc-plugins)
EOF

# Create empty test file
cat > "$PLUGIN_NAME/tests/test_plugin.py" << 'EOF'
"""
Test suite for this plugin.

Add your tests here.
"""

import pytest


class TestPlugin:
    """Basic plugin test class."""

    def test_plugin_loads(self):
        """Test that plugin can be imported."""
        assert True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
EOF

# Create basic .gitignore
cat > "$PLUGIN_NAME/.gitignore" << EOF
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
.pytest_cache/
.coverage
htmlcov/
.venv/
venv/
ENV/
env/
.idea/
.vscode/
*.swp
*.swo
*~
.DS_Store
EOF

echo "✓ Plugin '$PLUGIN_NAME' created successfully!"
echo ""
echo "Location: $(pwd)/$PLUGIN_NAME"
echo ""
echo "Next steps:"
echo "1. cd $PLUGIN_NAME"
echo "2. Create your first command: add a .md file in commands/"
echo "3. Add agents in agents/ directory for specialized functionality"
echo "4. Create skills in skills/ directory for reusable workflows"
echo "5. Run tests: pytest tests/"
echo "6. Validate structure: /cc-plugins:validate $PLUGIN_NAME"
echo ""
echo "For documentation: /cc-plugins:document"
