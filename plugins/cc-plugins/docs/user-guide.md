# User Guide: cc-plugins

**A step-by-step guide to creating, validating, and maintaining Claude Code plugins.**

## Table of Contents

- [Getting Started](#getting-started)
- [Tutorial: Creating Your First Plugin](#tutorial-creating-your-first-plugin)
- [Tutorial: Validating Plugins](#tutorial-validating-plugins)
- [Tutorial: Debugging Plugin Issues](#tutorial-debugging-plugin-issues)
- [Common Tasks & Solutions](#common-tasks--solutions)
- [Best Practices](#best-practices)
- [Frequently Asked Questions](#frequently-asked-questions)

## Getting Started

### Prerequisites

Before using cc-plugins, ensure you have:

1. **Claude Code** installed and running (latest version)
2. **Python 3.8+** installed on your system
3. **cc-plugins** installed in your plugins directory

### Installation Verification

Verify that cc-plugins is properly installed:

```bash
# In Claude Code, run:
/cc-plugins:validate
```

Expected output:
```
✓ Plugin validation PASSED
```

If validation fails, check the [Troubleshooting](#frequently-asked-questions) section.

### Understanding Plugin Basics

A Claude Code plugin is a package that extends Claude Code functionality with:

- **Commands** (`/plugin-name:command-name`): Slash commands users can invoke
- **Agents**: Specialized AI agents for specific tasks (optional)
- **Skills**: Reusable workflows and capabilities (optional)
- **Manifest** (`.claude-plugin/plugin.json`): Plugin metadata and configuration

### Plugin Directory Structure

Every plugin follows this structure:

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json              # Plugin metadata
├── commands/                    # Your slash commands
│   └── hello.md                # Example command
├── agents/                      # Specialized agents (optional)
├── skills/                      # Reusable skills (optional)
├── scripts/                     # Utility scripts (optional)
├── tests/                       # Test files
├── docs/                        # Documentation
├── README.md                    # Plugin documentation
└── .gitignore                   # Git ignore patterns
```

## Tutorial: Creating Your First Plugin

### Step 1: Plan Your Plugin

Before creating your plugin, think about:

1. **What problem does it solve?**
   - Example: "Helps users format code in different styles"

2. **What will it provide?**
   - Commands: Yes/No - What commands?
   - Agents: Yes/No - What would they specialize in?
   - Skills: Yes/No - What workflows?

3. **What's a good name?**
   - Use kebab-case: `my-plugin`, `code-formatter`, `ai-assistant`
   - Short and memorable
   - Descriptive of purpose

**Example Plugin Plan:**
```
Name: code-formatter
Purpose: Helps format and style code
Provides:
  - Command: /code-formatter:format - Format code
  - Command: /code-formatter:beautify - Beautify code
Description: "A plugin for formatting code in various styles and languages"
```

### Step 2: Create Plugin Structure

Use cc-plugins to scaffold your plugin:

```bash
/cc-plugins:create code-formatter \
  --description "A plugin for formatting code in various styles and languages" \
  --author "Your Name"
```

Output:
```
✓ Plugin 'code-formatter' created successfully!

Location: /Users/you/code-formatter

Next steps:
1. cd code-formatter
2. Create your first command: add a .md file in commands/
3. Add agents in agents/ directory for specialized functionality
4. Create skills in skills/ directory for reusable workflows
5. Run tests: pytest tests/
6. Validate structure: /cc-plugins:validate
```

### Step 3: Create Your First Command

Navigate to your plugin:
```bash
cd code-formatter
```

Create a command file `commands/format.md`:

```markdown
---
description: "Format code in the specified style"
allowed-tools: ["Read", "Write"]
argument-hint: "language (javascript, python, etc) and optional style"
model: "sonnet"
disable-model-invocation: false
---

# Format Code

Formats code in the specified programming language and style.

## Usage

```bash
/code-formatter:format javascript --style standard
/code-formatter:format python --style black
```

## Supported Languages

- JavaScript / TypeScript
- Python
- Java
- C++
- Go

## Styles

- `standard`: Standard.js (JavaScript)
- `black`: Black (Python)
- `prettier`: Prettier (JavaScript)

---

!bash
# Your command implementation here
LANGUAGE="${1:?Language required (javascript, python, etc)}"
STYLE="${2:?Style required (standard, black, prettier)}"

echo "Formatting $LANGUAGE code with $STYLE style..."
# Add your actual formatting logic here
```

### Step 4: Test Your Command

Run your plugin validation:

```bash
/cc-plugins:validate
```

Output should show:
```
✓ Plugin validation PASSED

Plugin: code-formatter (v1.0.0)
Author: Your Name

Directory Structure: PASSED
├─ .claude-plugin/
├─ commands/ (1 commands found)
├─ agents/
├─ skills/
├─ tests/
└─ docs/

Manifest Validation: PASSED
Component Validation: PASSED

Overall Status: ✓ PASSED
```

### Step 5: Generate Documentation

Create professional documentation automatically:

```bash
/cc-plugins:document
```

This generates an updated `README.md` with:
- Plugin overview
- Installation instructions
- All commands documented
- Usage examples
- Development guidelines

### Step 6: Add Tests

Add test cases to `tests/test_code_formatter.py`:

```python
"""Tests for code-formatter plugin."""

import pytest
from pathlib import Path


class TestCodeFormatterPlugin:
    """Test cases for code formatter plugin."""

    def test_plugin_structure(self):
        """Test that plugin has required structure."""
        assert Path(".claude-plugin/plugin.json").exists()
        assert Path("commands").exists()
        assert Path("README.md").exists()

    def test_format_command_exists(self):
        """Test that format command is defined."""
        cmd_file = Path("commands/format.md")
        assert cmd_file.exists()

        content = cmd_file.read_text()
        assert "description:" in content
        assert "allowed-tools:" in content

    def test_manifest_valid(self):
        """Test that plugin manifest is valid."""
        import json
        manifest = json.loads(Path(".claude-plugin/plugin.json").read_text())

        assert "name" in manifest
        assert manifest["name"] == "code-formatter"
        assert "version" in manifest


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

Run tests:
```bash
pytest tests/ -v
```

### Step 7: Publish Your Plugin

1. **Validate everything:**
   ```bash
   /cc-plugins:validate
   /cc-plugins:debug
   ```

2. **Run full test suite:**
   ```bash
   pytest tests/ -v
   ```

3. **Update documentation:**
   ```bash
   /cc-plugins:document
   ```

4. **Version your plugin:**
   ```bash
   /cc-plugins:update --version minor
   ```

5. **Commit to git (if using version control):**
   ```bash
   git add .
   git commit -m "Release code-formatter v1.0.0"
   git push
   ```

## Tutorial: Validating Plugins

### Basic Validation

Validate your current plugin:

```bash
# From inside your plugin directory
/cc-plugins:validate
```

### Validating External Plugins

Validate a plugin at any path:

```bash
/cc-plugins:validate /path/to/plugin
/cc-plugins:validate ~/plugins/my-plugin
```

### Understanding Validation Results

**Perfect Validation:**
```
✓ Plugin validation PASSED

Summary: 15 checks passed
```

**Validation Warnings:**
```
✗ Plugin validation found 2 issues:

1. WARNING: Missing tests/ directory
   File: tests/
   Suggestion: Add test files

2. WARNING: Missing .gitignore
   File: .gitignore
   Suggestion: Create .gitignore file

Run /cc-plugins:debug for detailed analysis and fixes
```

**Validation Errors:**
```
✗ Plugin validation FAILED

1. CRITICAL: Missing required manifest field
   Location: .claude-plugin/plugin.json
   Issue: Field 'version' is required
   Fix: Add "version": "1.0.0" to manifest

2. ERROR: Invalid plugin name
   Location: .claude-plugin/plugin.json
   Issue: Plugin name 'My_Plugin' must be in kebab-case
   Fix: Rename to 'my-plugin'

Run /cc-plugins:debug for detailed analysis and fixes
```

## Tutorial: Debugging Plugin Issues

### Running Diagnostics

Use the debug command to identify issues:

```bash
/cc-plugins:debug
```

### Understanding Debug Output

Debug output shows:
- **Critical Issues**: Must be fixed before using the plugin
- **Warnings**: Recommended improvements
- **Info**: Optional suggestions

Example output:
```
Debugging plugin: .

Checking manifest...
✓ Manifest JSON is valid
✓ Plugin name is in kebab-case: my-plugin
✓ Version field exists

Checking directory structure...
✓ commands/ directory exists
✓ agents/ directory exists
✓ skills/ directory exists

Checking components...
✓ Found 3 command(s)
✓ Found 0 agent(s)
✓ Found 2 skill(s)

Checking configuration files...
✓ README.md exists
✓ tests/ directory exists
✓ .gitignore exists

Summary:
--------
Critical Issues: 0 (MUST FIX)
Warnings:        0 (RECOMMENDED)
Total Issues:    0

✓ No issues found! Plugin is ready to use.
```

### Fixing Common Issues

See [Troubleshooting](../README.md#troubleshooting) in README for common issues and fixes.

## Common Tasks & Solutions

### Task 1: Add a New Command

**Steps:**

1. Create a new markdown file in `commands/`:
   ```bash
   touch commands/my-new-command.md
   ```

2. Add command template:
   ```markdown
   ---
   description: "What this command does"
   allowed-tools: ["Bash", "Read", "Write"]
   argument-hint: "argument description"
   model: "sonnet"
   disable-model-invocation: false
   ---

   # Command Title

   Command description and usage.

   ## Usage

   ```bash
   /plugin-name:command-name arg1 arg2
   ```

   ---

   !bash
   # Your command code here
   echo "Command executed"
   ```

3. Validate:
   ```bash
   /cc-plugins:validate
   ```

4. Update documentation:
   ```bash
   /cc-plugins:document
   ```

### Task 2: Update Plugin Metadata

**Update description:**
```bash
/cc-plugins:update description "New plugin description"
```

**Update author:**
```bash
/cc-plugins:update author.name "New Author"
/cc-plugins:update author.email "author@example.com"
```

**Add keywords:**
```bash
/cc-plugins:update keywords "development"
/cc-plugins:update keywords "formatting"
```

### Task 3: Version Management

**Bump version (patch):**
```bash
/cc-plugins:update --version patch
# 1.0.0 → 1.0.1
```

**Bump version (minor):**
```bash
/cc-plugins:update --version minor
# 1.0.0 → 1.1.0
```

**Bump version (major):**
```bash
/cc-plugins:update --version major
# 1.0.0 → 2.0.0
```

### Task 4: Testing Your Plugin

**Run all tests:**
```bash
pytest tests/ -v
```

**Run specific test:**
```bash
pytest tests/test_plugin.py::TestClass::test_method -v
```

**Generate coverage report:**
```bash
pytest tests/ --cov=. --cov-report=html
```

**Run quick smoke test:**
```bash
/cc-plugins:validate && /cc-plugins:debug
```

## Best Practices

### 1. Use Clear, Descriptive Names

Good names:
- `code-formatter` - Clear purpose
- `api-client-helper` - What it helps with
- `documentation-generator` - Function

Avoid:
- `tool` - Too generic
- `x` - Not descriptive
- `MyPlugin` - Use kebab-case instead

### 2. Write Complete Frontmatter

Always include all required YAML frontmatter fields:

```yaml
---
description: "Clear, concise description"
allowed-tools: ["Bash", "Read", "Write"]  # Only required tools
argument-hint: "Describe arguments"
model: "sonnet"  # Choose appropriate model
disable-model-invocation: false
---
```

### 3. Create Comprehensive Documentation

- Write clear command descriptions
- Include usage examples
- Document all parameters
- Show example output
- Explain any special requirements

### 4. Write Tests for Your Commands

Test coverage helps ensure reliability:

```python
class TestMyCommand:
    """Test cases for my command."""

    def test_command_exists(self):
        """Test that command file exists."""
        assert Path("commands/my-command.md").exists()

    def test_command_has_frontmatter(self):
        """Test that command has valid frontmatter."""
        content = Path("commands/my-command.md").read_text()
        assert "description:" in content
        assert "allowed-tools:" in content
```

### 5. Keep Plugins Focused

One responsibility per plugin:
- ✓ `markdown-formatter` - Format markdown files
- ✓ `api-client` - Make API calls
- ✗ `everything-plugin` - Does everything (too broad)

### 6. Use Semantic Versioning

Follow semantic versioning (MAJOR.MINOR.PATCH):

- **1.0.0** - First release
- **1.0.1** - Bug fix (patch bump)
- **1.1.0** - New feature (minor bump)
- **2.0.0** - Breaking changes (major bump)

### 7. Validate Before Sharing

Always run validation before sharing or publishing:

```bash
/cc-plugins:validate
/cc-plugins:debug
pytest tests/ -v
```

### 8. Keep README Updated

After making changes, regenerate documentation:

```bash
/cc-plugins:document
```

## Frequently Asked Questions (FAQ)

### Q: What's kebab-case?

**A:** Kebab-case uses lowercase letters, numbers, and hyphens:
- `my-plugin` ✓
- `my-awesome-plugin-v2` ✓
- `MyPlugin` ✗ (not lowercase)
- `my_plugin` ✗ (uses underscore)
- `my plugin` ✗ (uses spaces)

### Q: Can I add agents and skills to my plugin?

**A:** Yes! Agents and skills are optional components that provide:

**Agents:**
- Specialized AI agents for specific tasks
- More sophisticated than commands
- Add to `agents/` directory

**Skills:**
- Reusable workflows and capabilities
- Combine multiple operations
- Add to `skills/` directory with SKILL.md

### Q: How do I choose the right model?

**A:** Consider your use case:
- `sonnet` (default) - Best balance of speed and intelligence
- `opus` - More capable, for complex tasks
- `haiku` - Faster, for simple tasks

### Q: What tools can my commands use?

**A:** Available tools depend on Claude Code version:
- `Bash` - Execute shell commands
- `Read` - Read files
- `Write` - Write files
- `Edit` - Edit file contents
- `Grep` - Search file contents
- `Glob` - Find files by pattern

Specify in frontmatter:
```yaml
allowed-tools: ["Bash", "Read", "Write"]
```

### Q: How do I test my plugin?

**A:** Use pytest:

1. Create test files in `tests/`
2. Write test functions
3. Run: `pytest tests/ -v`

Example:
```python
def test_command_exists():
    """Test that my command exists."""
    assert Path("commands/my-command.md").exists()
```

### Q: Can I publish my plugin?

**A:** Yes! After validation:

1. Validate: `/cc-plugins:validate`
2. Test: `pytest tests/ -v`
3. Document: `/cc-plugins:document`
4. Version: `/cc-plugins:update --version minor`
5. Commit: `git add . && git commit -m "Release v1.0.0"`
6. Share your GitHub repository

### Q: How do I update my plugin?

**A:**

1. Make changes to your commands/agents/skills
2. Validate: `/cc-plugins:validate`
3. Test: `pytest tests/ -v`
4. Update docs: `/cc-plugins:document`
5. Bump version: `/cc-plugins:update --version patch`
6. Commit and push

### Q: What if validation fails?

**A:** Run debug to get specific recommendations:

```bash
/cc-plugins:debug
```

Debug output shows:
- What's wrong
- Where the issue is
- How to fix it

### Q: Can I use existing plugins as templates?

**A:** Yes! Look at other plugins:

1. Check their structure
2. Read their README
3. Study their commands
4. Review their tests

Good public plugins to learn from:
- Official Claude Code plugins
- Community-contributed plugins
- Examples in documentation

### Q: How do I handle errors in my commands?

**A:** Use exit codes in your bash:

```bash
# Exit with error
if [ ! -f "$file" ]; then
    echo "Error: File not found: $file"
    exit 1
fi

# Exit with success
echo "Success!"
exit 0
```

### Q: Can I add dependencies to my plugin?

**A:** Yes, through:

1. **Python dependencies** - Add to `requirements.txt`
2. **System dependencies** - Document in README
3. **External APIs** - Document in README and commands

### Q: How do I share my plugin?

**A:**

1. Push to GitHub
2. Add topic: `claude-code-plugin`
3. Write comprehensive README
4. Include usage examples
5. Share the link

### Q: What's the difference between commands, agents, and skills?

**A:**

- **Commands** (`/plugin:command`): Direct actions users invoke
- **Agents**: AI agents specialized for specific domains
- **Skills**: Reusable workflows activated contextually

Start with commands; add agents/skills if needed.

### Q: How do I get help?

**A:** Resources available:

1. Run `/cc-plugins:debug` for diagnostics
2. Check [README](../README.md) for troubleshooting
3. Review [Developer Guide](developer-guide.md) for technical details
4. Read [API Reference](api-reference.md) for function documentation
5. Check official [Claude Code docs](https://code.claude.com/docs)

---

**Next Steps:**

- Create your first plugin using the tutorial above
- Check [Developer Guide](developer-guide.md) for advanced topics
- Review [API Reference](api-reference.md) for detailed function documentation
- Join the Claude Code community for support and sharing
