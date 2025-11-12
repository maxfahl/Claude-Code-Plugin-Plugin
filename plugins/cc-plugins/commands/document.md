---
description: "Generate comprehensive plugin documentation. Creates or updates README.md with all commands, agents, skills, installation instructions, and usage examples automatically extracted from plugin components."
allowed-tools: ["Bash", "Read", "Write"]
argument-hint: "Optional: path to plugin directory (default: current directory)"
model: "sonnet"
disable-model-invocation: false
---

# Document Plugin

Generates comprehensive documentation for a plugin.

## Usage

```bash
/cc-plugins:document
/cc-plugins:document /path/to/plugin
/cc-plugins:document ./my-plugin
```

## What It Does

1. **Generates README.md** with:
   - Plugin name, version, and description
   - Author information
   - Installation instructions
   - Quick start guide
   - Features overview

2. **Documents Commands** with:
   - Command names and descriptions
   - Usage examples and syntax
   - Parameters and options
   - Output examples

3. **Documents Agents** with:
   - Agent names and descriptions
   - Capabilities and expertise
   - Activation triggers
   - Usage scenarios

4. **Documents Skills** with:
   - Skill names and descriptions
   - When to use each skill
   - Activation conditions
   - Integration examples

5. **Includes Development Info** with:
   - Testing instructions
   - Validation steps
   - Contributing guidelines

## Output

Generates `README.md` with structure:

```markdown
# my-awesome-plugin

A helpful plugin for developers.

## Installation

```bash
# Installation instructions
```

## Features

- Feature 1
- Feature 2
- Feature 3

## Available Commands

### /command-name
Description of command

**Usage:**
```bash
/command-name arg1 arg2
```

## Available Agents

### agent-name
Description of agent

**Capabilities:**
- Capability 1
- Capability 2

## Available Skills

### skill-name
Description of skill

**Use when:** ...
**Activation:** ...

## Development

### Running Tests
...

## Support

...
```

## Parameters

- **Path** ($1): Optional. Path to plugin directory (default: current directory)

## Examples

### Generate Documentation for Current Plugin

```bash
cd my-plugin
/cc-plugins:document
```

### Generate Documentation for Specific Plugin

```bash
/cc-plugins:document /path/to/plugin
```

### View Generated Documentation

```bash
cat README.md
# or
open README.md  # macOS
xdg-open README.md  # Linux
start README.md  # Windows
```

## Generated Documentation Structure

```
README.md
├─ Project Header
│  ├─ Title and version
│  ├─ Description
│  └─ Author info
├─ Installation
├─ Features
├─ Quick Start
├─ Commands Section
│  ├─ Command 1
│  │  ├─ Description
│  │  ├─ Usage
│  │  └─ Examples
│  └─ Command 2
├─ Agents Section
│  ├─ Agent 1
│  ├─ Agent 2
│  └─ Agent 3
├─ Skills Section
│  ├─ Skill 1
│  ├─ Skill 2
│  └─ Skill 3
├─ Development
│  ├─ Testing
│  ├─ Validation
│  └─ Contributing
└─ License & Support
```

---

!bash
# Get plugin directory path (default to current directory)
PLUGIN_DIR="${1:-.}"

# Check if directory exists
if [ ! -d "$PLUGIN_DIR" ]; then
  echo "✗ Error: Directory not found: $PLUGIN_DIR"
  exit 1
fi

# Check if it's a plugin directory
MANIFEST_PATH="$PLUGIN_DIR/.claude-plugin/plugin.json"
if [ ! -f "$MANIFEST_PATH" ]; then
  echo "✗ Error: Not a valid plugin directory"
  echo "   Missing: $MANIFEST_PATH"
  exit 1
fi

# Extract plugin info from manifest
PLUGIN_NAME=$(python3 -c "import json; print(json.load(open('$MANIFEST_PATH')).get('name', 'unknown'))")
PLUGIN_VERSION=$(python3 -c "import json; print(json.load(open('$MANIFEST_PATH')).get('version', '1.0.0'))")
PLUGIN_DESC=$(python3 -c "import json; print(json.load(open('$MANIFEST_PATH')).get('description', 'A Claude Code plugin'))")
PLUGIN_AUTHOR=$(python3 -c "import json; print(json.load(open('$MANIFEST_PATH')).get('author', {}).get('name', 'Developer'))")
PLUGIN_LICENSE=$(python3 -c "import json; print(json.load(open('$MANIFEST_PATH')).get('license', 'MIT'))")

# Start building README
README_FILE="$PLUGIN_DIR/README.md"
cat > "$README_FILE" << 'EOF'
EOF

# Write header
cat >> "$README_FILE" << EOF
# $PLUGIN_NAME

$PLUGIN_DESC

**Version:** $PLUGIN_VERSION
**Author:** $PLUGIN_AUTHOR
**License:** $PLUGIN_LICENSE

---

## Installation

1. Place this plugin in your Claude Code plugins directory:
   \`\`\`bash
   cd ~/.claude/plugins
   \`\`\`

2. Restart Claude Code to load the plugin

3. Verify installation:
   \`\`\`bash
   /cc-plugins:validate
   \`\`\`

## Quick Start

To use this plugin:

\`\`\`bash
# Create a new plugin based on this template
/cc-plugins:create my-plugin

# Validate your plugin
/cc-plugins:validate my-plugin

# Generate documentation
/cc-plugins:document my-plugin
\`\`\`

---

EOF

# Document commands
if [ -d "$PLUGIN_DIR/commands" ]; then
  COMMANDS=$(find "$PLUGIN_DIR/commands" -maxdepth 1 -name "*.md" -type f)
  if [ -n "$COMMANDS" ]; then
    echo "## Available Commands" >> "$README_FILE"
    echo "" >> "$README_FILE"

    while IFS= read -r cmd_file; do
      cmd_name=$(basename "$cmd_file" .md)
      # Extract description from frontmatter if available
      cmd_desc=$(sed -n '/^---$/,/^---$/p' "$cmd_file" | grep "description:" | sed 's/description: //;s/"//g')
      [ -z "$cmd_desc" ] && cmd_desc="Command"

      echo "### \`/$PLUGIN_NAME:$cmd_name\`" >> "$README_FILE"
      echo "" >> "$README_FILE"
      echo "$cmd_desc" >> "$README_FILE"
      echo "" >> "$README_FILE"
    done <<< "$COMMANDS"
  fi
fi

# Document agents
if [ -d "$PLUGIN_DIR/agents" ]; then
  AGENTS=$(find "$PLUGIN_DIR/agents" -maxdepth 1 -name "*.md" -type f)
  if [ -n "$AGENTS" ]; then
    echo "## Available Agents" >> "$README_FILE"
    echo "" >> "$README_FILE"

    while IFS= read -r agent_file; do
      agent_name=$(basename "$agent_file" .md)
      # Extract description from frontmatter if available
      agent_desc=$(sed -n '/^---$/,/^---$/p' "$agent_file" | grep "description:" | sed 's/description: //;s/"//g')
      [ -z "$agent_desc" ] && agent_desc="Specialized agent"

      echo "### $agent_name" >> "$README_FILE"
      echo "" >> "$README_FILE"
      echo "$agent_desc" >> "$README_FILE"
      echo "" >> "$README_FILE"
    done <<< "$AGENTS"
  fi
fi

# Document skills
if [ -d "$PLUGIN_DIR/skills" ]; then
  SKILLS=$(find "$PLUGIN_DIR/skills" -mindepth 1 -maxdepth 1 -type d)
  if [ -n "$SKILLS" ]; then
    echo "## Available Skills" >> "$README_FILE"
    echo "" >> "$README_FILE"

    while IFS= read -r skill_dir; do
      skill_name=$(basename "$skill_dir")
      [ -f "$skill_dir/SKILL.md" ] && skill_desc=$(head -n 3 "$skill_dir/SKILL.md" | tail -n 1) || skill_desc="Development skill"

      echo "### $skill_name" >> "$README_FILE"
      echo "" >> "$README_FILE"
      echo "$skill_desc" >> "$README_FILE"
      echo "" >> "$README_FILE"
    done <<< "$SKILLS"
  fi
fi

# Add development section
cat >> "$README_FILE" << 'EOF'

## Development

### Running Tests

```bash
cd /path/to/plugin
pytest tests/ -v
```

### Validating Plugin

```bash
/cc-plugins:validate /path/to/plugin
```

### Debugging Issues

```bash
/cc-plugins:debug /path/to/plugin
```

### Using in Development

1. Make changes to your plugin
2. Run validation: `/cc-plugins:validate`
3. Run tests: `pytest tests/`
4. Update documentation: `/cc-plugins:document`

## Contributing

1. Fork the plugin repository
2. Create a feature branch
3. Add tests for new features
4. Ensure all tests pass
5. Update documentation
6. Submit a pull request

## Support

For issues and questions:

- Check the documentation
- Run `/cc-plugins:debug` for error analysis
- Review tests for usage examples

## License

EOF

echo "$PLUGIN_LICENSE" >> "$README_FILE"

echo ""
echo "✓ Documentation generated successfully!"
echo ""
echo "Generated: $README_FILE"
echo ""
echo "You can now:"
echo "1. Review the documentation: cat $README_FILE"
echo "2. Share with others"
echo "3. Include in version control"
echo ""
echo "Update this file by running /cc-plugins:document again"
