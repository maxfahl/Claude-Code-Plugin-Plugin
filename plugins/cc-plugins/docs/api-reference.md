# API Reference: cc-plugins

**Complete API documentation for scripts, validators, and functions in cc-plugins.**

## Table of Contents

- [Scripts](#scripts)
- [Validators Module](#validators-module)
- [Template Functions](#template-functions)
- [Exit Codes & Error Handling](#exit-codes--error-handling)
- [Command Line Usage](#command-line-usage)

## Scripts

### scaffold-plugin.py

**Location:** `scripts/scaffold-plugin.py`

**Purpose:** Creates a new Claude Code plugin with correct directory structure.

**Usage:**

```bash
python3 scripts/scaffold-plugin.py \
    --name plugin-name \
    [--author "Author Name"] \
    [--description "Description"] \
    [--version "1.0.0"] \
    [--components command,agent,skill] \
    [--license "MIT"]
```

**Arguments:**

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `--name` | string | YES | - | Plugin name (kebab-case) |
| `--author` | string | NO | Developer | Plugin author name |
| `--description` | string | NO | A new plugin | Plugin description |
| `--version` | string | NO | 1.0.0 | Initial version |
| `--components` | string | NO | command | Components to create (comma-separated) |
| `--license` | string | NO | MIT | License type |

**Returns:**

- Exit code 0: Success
- Exit code 1: Invalid plugin name or other error

**Output:**

```
✓ Plugin 'my-plugin' created successfully!

Location: /path/to/my-plugin

Next steps:
1. cd my-plugin
2. Create your first command
3. Run tests
```

**Examples:**

```bash
# Basic plugin
python3 scripts/scaffold-plugin.py --name my-plugin

# Plugin with metadata
python3 scripts/scaffold-plugin.py \
    --name awesome-tool \
    --author "Jane Developer" \
    --description "An awesome tool for Claude Code" \
    --version 1.0.0

# Plugin with specific components
python3 scripts/scaffold-plugin.py \
    --name agent-plugin \
    --components command,agent,skill
```

**Generated Structure:**

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json
├── commands/
├── agents/
├── skills/
├── tests/
│   └── test_plugin.py
├── docs/
├── README.md
└── .gitignore
```

---

### validate-plugin.py

**Location:** `scripts/validate-plugin.py`

**Purpose:** Validates a plugin's structure and components for compliance.

**Usage:**

```bash
python3 scripts/validate-plugin.py [plugin_directory]
```

**Arguments:**

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `plugin_directory` | path | NO | . (current) | Path to plugin |

**Returns:**

- Exit code 0: Valid plugin
- Exit code 1: Plugin has validation errors
- Exit code 2: Script execution error

**Output:**

Structured validation report with:
- Directory structure checks
- Manifest validation
- Component validation
- Error summary

**Examples:**

```bash
# Validate current directory
python3 scripts/validate-plugin.py

# Validate specific plugin
python3 scripts/validate-plugin.py /path/to/plugin

# Validate and capture output
python3 scripts/validate-plugin.py . > validation_report.txt
```

**Output Example (Success):**

```
Validating plugin: .

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
✓ Found 1 agent(s)
✓ Found 2 skill(s)

✓ Plugin validation PASSED
Summary: 12 checks passed
```

**Output Example (Failure):**

```
✗ Plugin validation FAILED

Issues found:
1. CRITICAL: Missing 'version' field in manifest
   Fix: Add "version": "1.0.0" to .claude-plugin/plugin.json

2. ERROR: Plugin name 'My_Plugin' must be in kebab-case
   Fix: Rename to 'my-plugin'

Run /cc-plugins:debug for detailed analysis and fixes
```

---

## Validators Module

**Location:** `scripts/validators.py`

**Purpose:** Reusable validation functions for plugin components.

### validate_command_file()

```python
def validate_command_file(file_path: Path) -> List[str]
```

**Purpose:** Validate a command markdown file.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `file_path` | Path | Path to command markdown file |

**Returns:**

List of error messages (empty if valid)

**Validates:**

- File exists and is readable
- Has YAML frontmatter
- Frontmatter is valid YAML
- Required frontmatter fields present
- Field types are correct
- Model name is valid (sonnet, opus, haiku)
- Tools list is valid
- No syntax errors

**Raises:**

- No exceptions; returns error list instead

**Example:**

```python
from pathlib import Path
from validators import validate_command_file

cmd_path = Path("commands/my-command.md")
errors = validate_command_file(cmd_path)

if errors:
    for error in errors:
        print(f"Error: {error}")
    exit(1)
else:
    print("Command is valid!")
```

**Required Frontmatter Fields:**

```yaml
---
description: "Command description"
allowed-tools: ["Bash", "Read"]
argument-hint: "Argument description"
model: "sonnet"
disable-model-invocation: false
---
```

---

### validate_agent_file()

```python
def validate_agent_file(file_path: Path) -> List[str]
```

**Purpose:** Validate an agent markdown file.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `file_path` | Path | Path to agent markdown file |

**Returns:**

List of error messages (empty if valid)

**Validates:**

- File exists and is readable
- Has YAML frontmatter
- Frontmatter is valid YAML
- Required frontmatter fields present
- Field types are correct

**Example:**

```python
from pathlib import Path
from validators import validate_agent_file

agent_path = Path("agents/my-agent.md")
errors = validate_agent_file(agent_path)

if errors:
    print("Agent has errors:", errors)
```

**Required Frontmatter Fields:**

```yaml
---
description: "Agent description"
role: "Agent role"
model: "sonnet"
---
```

---

### validate_skill_directory()

```python
def validate_skill_directory(dir_path: Path) -> List[str]
```

**Purpose:** Validate a skill directory structure.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `dir_path` | Path | Path to skill directory |

**Returns:**

List of error messages (empty if valid)

**Validates:**

- Directory exists
- Contains SKILL.md file
- SKILL.md is readable
- Optional implementation files present
- File permissions allow reading

**Example:**

```python
from pathlib import Path
from validators import validate_skill_directory

skill_path = Path("skills/my-skill")
errors = validate_skill_directory(skill_path)

if not errors:
    print("Skill is valid!")
```

**Required Files:**

- `SKILL.md` - Skill definition (required)
- `implementation.py` - Implementation (optional)

---

### validate_hooks_config()

```python
def validate_hooks_config(file_path: Path) -> List[str]
```

**Purpose:** Validate hooks.json configuration.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `file_path` | Path | Path to hooks.json |

**Returns:**

List of error messages (empty if valid)

**Validates:**

- File exists
- Valid JSON syntax
- Required fields present
- Hook definitions are valid
- Event names are recognized

**Example:**

```python
from pathlib import Path
from validators import validate_hooks_config

hooks_path = Path(".claude-plugin/hooks.json")
errors = validate_hooks_config(hooks_path)

if errors:
    print("Hooks configuration errors:", errors)
```

**Configuration Format:**

```json
{
  "hooks": [
    {
      "event": "plugin.loaded",
      "handler": "commands/init.md"
    }
  ]
}
```

---

### validate_mcp_config()

```python
def validate_mcp_config(file_path: Path) -> List[str]
```

**Purpose:** Validate MCP (Model Context Protocol) configuration.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `file_path` | Path | Path to .mcp.json |

**Returns:**

List of error messages (empty if valid)

**Validates:**

- File exists
- Valid JSON syntax
- Server definitions are valid
- Transport configuration is correct
- Environment variables are accessible

**Example:**

```python
from pathlib import Path
from validators import validate_mcp_config

mcp_path = Path(".mcp.json")
errors = validate_mcp_config(mcp_path)

if errors:
    print("MCP configuration errors:", errors)
```

**Configuration Format:**

```json
{
  "servers": {
    "my-server": {
      "url": "http://localhost:3000",
      "transport": "http"
    }
  }
}
```

---

## Template Functions

### Command Template

**Location:** Generated from scaffolding

**Template Variables:**

```bash
PLUGIN_NAME        # Plugin name (from manifest)
COMMAND_NAME       # Command name (from filename)
DESCRIPTION        # Command description (from frontmatter)
ALLOWED_TOOLS      # Tools the command can use
```

**Example Template:**

```markdown
---
description: "{{ DESCRIPTION }}"
allowed-tools: {{ ALLOWED_TOOLS }}
argument-hint: "Arguments for command"
model: "sonnet"
disable-model-invocation: false
---

# {{ COMMAND_NAME }}

{{ DESCRIPTION }}

## Usage

```bash
/{{ PLUGIN_NAME }}:{{ COMMAND_NAME }} arg1 arg2
```

## Parameters

- `arg1`: Description of arg1
- `arg2`: Description of arg2

---

!bash
# Implementation here
echo "Command executed"
```

---

## Exit Codes & Error Handling

### Exit Codes

Standard exit codes used throughout cc-plugins:

| Code | Meaning | When Used |
|------|---------|-----------|
| 0 | Success | Command completed successfully |
| 1 | General Error | Validation failed, file not found, etc. |
| 2 | Execution Error | Script execution error |
| 3 | Validation Error | Component validation failed |
| 4 | File Error | File read/write error |

### Error Handling Patterns

**Pattern 1: File Validation**

```bash
if [ ! -f "$FILE" ]; then
    echo "Error: File not found: $FILE"
    exit 1
fi
```

**Pattern 2: JSON Validation**

```bash
if ! python3 -c "import json; json.load(open('$FILE'))" 2>/dev/null; then
    echo "Error: Invalid JSON in $FILE"
    exit 1
fi
```

**Pattern 3: Directory Validation**

```bash
if [ ! -d "$DIR" ]; then
    echo "Error: Directory not found: $DIR"
    exit 1
fi
```

**Pattern 4: Permission Checking**

```bash
if [ ! -r "$FILE" ]; then
    echo "Error: Cannot read file: $FILE"
    exit 1
fi

if [ ! -w "$FILE" ]; then
    echo "Error: Cannot write to file: $FILE"
    exit 1
fi
```

---

## Command Line Usage

### Bash Functions Provided

Commands exposed through Claude Code:

**Create Plugin:**
```bash
/cc-plugins:create plugin-name [--options]
```

**Validate Plugin:**
```bash
/cc-plugins:validate [path]
```

**Debug Plugin:**
```bash
/cc-plugins:debug [path]
```

**Document Plugin:**
```bash
/cc-plugins:document [path]
```

**Update Plugin:**
```bash
/cc-plugins:update field value
/cc-plugins:update --version major|minor|patch
```

### Environment Variables

**Optional environment variables:**

```bash
DEBUG=1              # Enable debug output
VERBOSE=1            # Enable verbose output
PLUGIN_DIR=path      # Override plugin directory
LOG_LEVEL=debug      # Set logging level
```

**Example:**

```bash
DEBUG=1 /cc-plugins:validate
VERBOSE=1 /cc-plugins:debug
```

---

### Python API Usage

Use validators programmatically:

```python
from pathlib import Path
from scripts.validators import validate_command_file

# Validate command
errors = validate_command_file(Path("commands/hello.md"))

if errors:
    print(f"Found {len(errors)} errors:")
    for error in errors:
        print(f"  - {error}")
else:
    print("All validations passed!")
```

### Testing API

Run validation tests:

```python
import subprocess
import sys

result = subprocess.run(
    [sys.executable, "scripts/validate-plugin.py", "."],
    capture_output=True,
    text=True
)

if result.returncode == 0:
    print("Plugin is valid!")
else:
    print("Plugin has errors:")
    print(result.stdout)
```

---

## Common Usage Examples

### Example 1: Programmatic Plugin Validation

```python
#!/usr/bin/env python3
"""Validate multiple plugins."""

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent / "scripts"))

from validators import validate_command_file

plugins_dir = Path("plugins")
for plugin in plugins_dir.iterdir():
    if plugin.is_dir():
        print(f"Validating {plugin.name}...")
        for cmd in (plugin / "commands").glob("*.md"):
            errors = validate_command_file(cmd)
            if errors:
                print(f"  {cmd.name}: FAILED")
                for err in errors:
                    print(f"    - {err}")
            else:
                print(f"  {cmd.name}: PASSED")
```

### Example 2: Custom Validation Script

```python
#!/usr/bin/env python3
"""Custom validation for specific requirements."""

from pathlib import Path
import json
import sys

def validate_custom(plugin_dir):
    """Validate plugin against custom rules."""
    errors = []

    # Check 1: Must have at least one command
    commands = list((plugin_dir / "commands").glob("*.md"))
    if not commands:
        errors.append("Plugin must have at least one command")

    # Check 2: Manifest must have keywords
    manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
    with open(manifest_path) as f:
        manifest = json.load(f)

    if "keywords" not in manifest or not manifest["keywords"]:
        errors.append("Manifest must have keywords")

    # Check 3: Must have tests
    tests = list((plugin_dir / "tests").glob("test_*.py"))
    if not tests:
        errors.append("Plugin must have at least one test file")

    return errors

if __name__ == "__main__":
    plugin_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    errors = validate_custom(plugin_dir)

    if errors:
        print("Custom validation failed:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print("Custom validation passed!")
        sys.exit(0)
```

### Example 3: Batch Plugin Processing

```bash
#!/bin/bash
# Process all plugins in a directory

PLUGINS_DIR="./plugins"

for plugin_dir in "$PLUGINS_DIR"/*; do
    if [ -d "$plugin_dir" ]; then
        echo "Processing: $(basename "$plugin_dir")"

        # Validate
        python3 scripts/validate-plugin.py "$plugin_dir"
        if [ $? -ne 0 ]; then
            echo "  Validation: FAILED"
            continue
        fi

        # Run tests
        (cd "$plugin_dir" && pytest tests/ -q)
        if [ $? -ne 0 ]; then
            echo "  Tests: FAILED"
            continue
        fi

        # Generate docs
        /cc-plugins:document "$plugin_dir"

        echo "  Status: OK"
    fi
done
```

---

## Official References

- [Claude Code Plugin Development](https://code.claude.com/docs)
- [Plugin Manifest Specification](https://code.claude.com/docs/en/plugin-development)
- [Component Authoring Guide](https://code.claude.com/docs/en/components)
- [Official Plugin Examples](https://code.claude.com/docs/en/examples)

---

**Version:** 1.0.0
**Last Updated:** 2025-01-12
