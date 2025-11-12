# Developer Guide: cc-plugins

**Technical documentation for developing advanced Claude Code plugins and contributing to cc-plugins.**

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Plugin Development Patterns](#plugin-development-patterns)
- [Component Specifications](#component-specifications)
- [Validation Framework](#validation-framework)
- [Debugging Techniques](#debugging-techniques)
- [Testing Strategies](#testing-strategies)
- [Contributing Guidelines](#contributing-guidelines)
- [Advanced Topics](#advanced-topics)

## Architecture Overview

### System Architecture

```
Claude Code Runtime
    ↓
Plugin Loader
    ├── Manifest Parser (.claude-plugin/plugin.json)
    ├── Command Loader (commands/*.md)
    ├── Agent Loader (agents/*.md)
    └── Skill Loader (skills/*.md)
    ↓
cc-plugins Meta-Plugin
    ├── Scaffolding Engine (scripts/scaffold-plugin.py)
    ├── Validation Engine (scripts/validate-plugin.py)
    ├── Validation Functions (scripts/validators.py)
    └── Test Framework (tests/*.py)
```

### Component Lifecycle

```
1. Plugin Creation
   ↓
2. Component Authoring (Commands/Agents/Skills)
   ↓
3. Validation (Manifest, Frontmatter, Structure)
   ↓
4. Testing (Unit/Integration Tests)
   ↓
5. Documentation (README Generation)
   ↓
6. Publishing (Version Bump, Git Tag)
```

## Plugin Development Patterns

### Pattern 1: Simple Command Plugin

**Use case:** Simple utilities that perform single actions

**Structure:**
```
simple-tool/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── action1.md
│   ├── action2.md
│   └── action3.md
├── README.md
└── tests/
    └── test_plugin.py
```

**Example Plugin:**
```json
{
  "name": "simple-tool",
  "version": "1.0.0",
  "description": "A simple utility plugin",
  "author": { "name": "Developer" },
  "license": "MIT"
}
```

**Example Command** (`commands/action.md`):
```markdown
---
description: "Performs an action"
allowed-tools: ["Bash"]
argument-hint: "file path"
model: "haiku"
disable-model-invocation: true
---

# Perform Action

Does something with the provided file.

---

!bash
FILE="$1"
if [ -f "$FILE" ]; then
  echo "Found: $FILE"
else
  echo "Not found: $FILE"
  exit 1
fi
```

### Pattern 2: Advanced Agent Plugin

**Use case:** Complex domain-specific functionality with AI agents

**Structure:**
```
advanced-tool/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── init.md
│   └── help.md
├── agents/
│   ├── domain-expert.md
│   ├── analyzer.md
│   └── optimizer.md
├── scripts/
│   ├── analyzer.py
│   └── optimizer.py
├── tests/
└── docs/
    ├── architecture.md
    ├── agent-design.md
    └── workflow-examples.md
```

### Pattern 3: Modular Skill Plugin

**Use case:** Reusable workflows and capabilities

**Structure:**
```
modular-plugin/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   └── orchestrate.md
├── skills/
│   ├── workflow-1/
│   │   ├── SKILL.md
│   │   └── implementation.py
│   ├── workflow-2/
│   │   ├── SKILL.md
│   │   └── implementation.py
│   └── workflow-3/
│       ├── SKILL.md
│       └── implementation.py
├── tests/
└── README.md
```

## Component Specifications

### Plugin Manifest (.claude-plugin/plugin.json)

**Required fields:**

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Plugin description"
}
```

**Full specification:**

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "A plugin that does X",
  "author": {
    "name": "Author Name",
    "email": "author@example.com",
    "url": "https://example.com"
  },
  "homepage": "https://github.com/author/my-plugin",
  "repository": "https://github.com/author/my-plugin",
  "license": "MIT",
  "keywords": ["development", "utility"]
}
```

**Validation rules:**

- `name`: Required, must be kebab-case (lowercase with hyphens)
- `version`: Required, must follow semantic versioning (MAJOR.MINOR.PATCH)
- `description`: Optional but recommended, 1-200 characters
- `author`: Optional, can include name, email, url
- `license`: Optional, standard SPDX license identifier

### Command File Format

**File:** `commands/command-name.md`

**YAML Frontmatter (Required):**

```yaml
---
description: "Brief description of what the command does"
allowed-tools: ["Bash", "Read", "Write"]  # Required tools only
argument-hint: "Hint about command arguments"
model: "sonnet"  # sonnet, opus, or haiku
disable-model-invocation: false  # true to disable AI
---
```

**Frontmatter Fields:**

| Field | Type | Required | Values |
|-------|------|----------|--------|
| `description` | string | YES | 1-500 characters |
| `allowed-tools` | array | YES | Bash, Read, Write, Edit, Grep, Glob, etc. |
| `argument-hint` | string | YES | Brief description |
| `model` | string | YES | sonnet, opus, haiku |
| `disable-model-invocation` | boolean | NO | true/false (default: false) |

**Command Structure:**

```markdown
---
description: "Does something"
allowed-tools: ["Bash"]
argument-hint: "file path"
model: "sonnet"
disable-model-invocation: false
---

# Command Title

Markdown documentation of your command.

## Usage

Examples of how to use the command.

## Parameters

Description of parameters.

---

!bash
# Executable code here
PARAM="$1"
echo "Executing with: $PARAM"
```

**Best practices:**

1. Start with clear title and description
2. Include usage examples
3. Document parameters and options
4. Show example output
5. Keep bash code concise and readable
6. Handle errors gracefully with exit codes

### Agent File Format

**File:** `agents/agent-name.md`

**YAML Frontmatter:**

```yaml
---
description: "Agent description"
role: "Agent role and expertise"
model: "sonnet"
---
```

**Agent Structure:**

```markdown
---
description: "Specialized agent for domain"
role: "Domain expert with expertise in X"
model: "sonnet"
---

# Agent Name

## Role

Clear description of agent's role.

## Expertise

- Area 1
- Area 2
- Area 3

## Capabilities

What the agent can do.

## Activation Triggers

When does this agent activate?

## Example Workflows

How would users interact with this agent?
```

### Skill Directory Format

**Directory:** `skills/skill-name/`

**Required files:**

```
skill-name/
├── SKILL.md           # Skill definition
└── implementation.py  # Optional: Implementation code
```

**SKILL.md Format:**

```markdown
# Skill Name

## Description

What this skill does and its purpose.

## Capabilities

- Capability 1
- Capability 2
- Capability 3

## Activation Triggers

When is this skill used?

## Implementation

How does it work internally?

## Example Usage

```bash
# How to use this skill
```

## Integration

How does it integrate with other components?
```

## Validation Framework

### Validation Layers

```
1. Manifest Validation
   ├── JSON Syntax
   ├── Required Fields
   ├── Field Types
   └── Naming Convention (kebab-case)

2. Component Validation
   ├── File Existence
   ├── YAML Frontmatter
   ├── Required Frontmatter Fields
   ├── Field Types
   └── Markdown Syntax

3. Structural Validation
   ├── Directory Structure
   ├── File Organization
   ├── Dependencies
   └── References

4. Semantic Validation
   ├── Tool Availability
   ├── Model Names
   ├── Version Formats
   └── License Identifiers
```

### Validators Module API

**Location:** `scripts/validators.py`

**Key Functions:**

#### `validate_command_file(file_path: Path) -> List[str]`

Validates a command markdown file.

```python
from validators import validate_command_file
from pathlib import Path

errors = validate_command_file(Path("commands/my-command.md"))
if errors:
    for error in errors:
        print(f"Error: {error}")
else:
    print("Command is valid!")
```

**Checks:**
- File exists and is readable
- Has YAML frontmatter
- Frontmatter has required fields
- Field types are correct
- No syntax errors

#### `validate_agent_file(file_path: Path) -> List[str]`

Validates an agent markdown file.

**Checks:**
- File exists
- Has YAML frontmatter
- Frontmatter completeness
- Markdown syntax

#### `validate_skill_directory(dir_path: Path) -> List[str]`

Validates a skill directory structure.

**Checks:**
- Directory exists
- Has SKILL.md file
- Optional implementation files exist
- File permissions

#### `validate_hooks_config(file_path: Path) -> List[str]`

Validates hooks configuration.

**Checks:**
- JSON syntax
- Required fields
- Event definitions
- Handler references

#### `validate_mcp_config(file_path: Path) -> List[str]`

Validates MCP (Model Context Protocol) configuration.

**Checks:**
- JSON syntax
- Server definitions
- Transport configuration
- Environment variables

### Writing Custom Validators

Extend validation with custom validators:

```python
from pathlib import Path
from typing import List

def validate_my_component(file_path: Path) -> List[str]:
    """
    Validate my custom component.

    Args:
        file_path: Path to component file

    Returns:
        List of error messages (empty if valid)
    """
    errors = []

    # Check 1: File exists
    if not file_path.exists():
        errors.append(f"File not found: {file_path}")
        return errors

    # Check 2: File is readable
    try:
        content = file_path.read_text()
    except Exception as e:
        errors.append(f"Cannot read file: {e}")
        return errors

    # Check 3: Custom validation
    if "required_content" not in content:
        errors.append("Missing required content")

    # Check 4: Format validation
    if not content.startswith("# "):
        errors.append("File must start with heading")

    return errors
```

## Debugging Techniques

### Enabling Verbose Output

Run commands with detailed debugging:

```bash
# Enable debug mode
DEBUG=1 /cc-plugins:validate

# View manifest details
python3 -c "import json; print(json.dumps(json.load(open('.claude-plugin/plugin.json')), indent=2))"
```

### Checking Component Files

**Validate JSON manifest:**
```bash
python3 -m json.tool .claude-plugin/plugin.json
```

**Check YAML frontmatter:**
```bash
# Extract frontmatter from command
python3 << 'EOF'
import yaml

with open("commands/my-command.md") as f:
    content = f.read()
    # Extract frontmatter
    _, fm, _ = content.split("---", 2)
    data = yaml.safe_load(fm)
    print(yaml.dump(data, default_flow_style=False))
EOF
```

**Inspect command code:**
```bash
# Extract executable code from command
grep -A 100 "^!bash$" commands/my-command.md
```

### Debugging Validation Issues

**Step 1: Run validator directly**
```bash
python3 scripts/validate-plugin.py .
```

**Step 2: Check individual components**
```bash
python3 << 'EOF'
from validators import validate_command_file
from pathlib import Path

# Check specific command
errors = validate_command_file(Path("commands/my-command.md"))
print("Errors:", errors if errors else "None")
EOF
```

**Step 3: Trace issue source**
```bash
# Check manifest
cat .claude-plugin/plugin.json

# Check command frontmatter
head -20 commands/my-command.md

# Check directory structure
tree -L 2
```

### Common Debug Patterns

**Pattern: Manifest Issues**
```bash
# Verify manifest exists
[ -f .claude-plugin/plugin.json ] && echo "Exists" || echo "Missing"

# Validate JSON
python3 -m json.tool .claude-plugin/plugin.json > /dev/null && echo "Valid JSON" || echo "Invalid JSON"

# Check required fields
python3 -c "import json; m = json.load(open('.claude-plugin/plugin.json')); print('name:', m.get('name'), 'version:', m.get('version'))"
```

**Pattern: Component Issues**
```bash
# Check all commands exist
find commands -name "*.md" -exec echo "Found: {}" \;

# Validate frontmatter presence
find commands -name "*.md" -exec grep -l "^---$" {} \;

# Check for missing descriptions
find commands -name "*.md" -exec grep -L "^description:" {} \;
```

**Pattern: Structure Issues**
```bash
# List plugin structure
ls -la

# Check directory permissions
find . -type d -exec ls -ld {} \;

# Find all markdown files
find . -name "*.md" -type f
```

## Testing Strategies

### Test Structure

```
tests/
├── test_plugin_structure.py    # Plugin structure tests
├── test_manifest.py            # Manifest validation tests
├── test_commands.py            # Command tests
├── test_agents.py              # Agent tests
├── test_skills.py              # Skill tests
├── test_integration.py         # Integration tests
└── requirements.txt            # Test dependencies
```

### Writing Plugin Tests

**Basic test template:**

```python
"""Test suite for my-plugin."""

import pytest
from pathlib import Path
import json


class TestPluginStructure:
    """Test plugin directory structure."""

    def test_manifest_exists(self):
        """Test that plugin manifest exists."""
        manifest_path = Path(".claude-plugin/plugin.json")
        assert manifest_path.exists(), "Plugin manifest not found"

    def test_manifest_valid_json(self):
        """Test that manifest is valid JSON."""
        manifest_path = Path(".claude-plugin/plugin.json")
        with open(manifest_path) as f:
            data = json.load(f)  # Raises JSONDecodeError if invalid
        assert isinstance(data, dict)

    def test_required_directories(self):
        """Test that required directories exist."""
        required_dirs = ["commands", "agents", "skills"]
        for dir_name in required_dirs:
            assert Path(dir_name).exists(), f"Missing directory: {dir_name}"

    def test_manifest_fields(self):
        """Test that manifest has required fields."""
        manifest_path = Path(".claude-plugin/plugin.json")
        with open(manifest_path) as f:
            manifest = json.load(f)

        # Check required fields
        assert "name" in manifest, "Missing 'name' field"
        assert "version" in manifest, "Missing 'version' field"

        # Check field types
        assert isinstance(manifest["name"], str)
        assert isinstance(manifest["version"], str)


class TestCommands:
    """Test plugin commands."""

    def test_commands_directory(self):
        """Test that commands directory has files."""
        commands_dir = Path("commands")
        commands = list(commands_dir.glob("*.md"))
        assert len(commands) > 0, "No commands found"

    def test_command_frontmatter(self):
        """Test that all commands have valid frontmatter."""
        commands_dir = Path("commands")
        for cmd_file in commands_dir.glob("*.md"):
            content = cmd_file.read_text()

            # Check frontmatter exists
            assert content.startswith("---"), f"{cmd_file}: Missing frontmatter start"

            # Check required fields
            assert "description:" in content, f"{cmd_file}: Missing description"
            assert "allowed-tools:" in content, f"{cmd_file}: Missing allowed-tools"

    def test_specific_command(self):
        """Test specific command functionality."""
        cmd_file = Path("commands/my-command.md")
        assert cmd_file.exists(), "Command not found"

        content = cmd_file.read_text()
        assert "Usage:" in content, "Missing usage documentation"


class TestIntegration:
    """Integration tests for plugin."""

    def test_plugin_validation(self):
        """Test that plugin passes validation."""
        # Run validation script
        import subprocess
        result = subprocess.run(
            ["python3", "scripts/validate-plugin.py", "."],
            capture_output=True
        )
        assert result.returncode == 0, "Plugin validation failed"

    def test_plugin_debug(self):
        """Test that plugin passes debug check."""
        from validators import validate_command_file

        # Check all commands
        for cmd in Path("commands").glob("*.md"):
            errors = validate_command_file(cmd)
            assert not errors, f"Validation errors in {cmd}: {errors}"
```

### Running Tests

**Run all tests:**
```bash
pytest tests/ -v
```

**Run specific test file:**
```bash
pytest tests/test_manifest.py -v
```

**Run specific test:**
```bash
pytest tests/test_manifest.py::TestPluginStructure::test_manifest_exists -v
```

**Run with coverage:**
```bash
pytest tests/ --cov=. --cov-report=html
```

**Run with detailed output:**
```bash
pytest tests/ -vv -s
```

### Test Coverage

Aim for high test coverage:

```bash
# Generate coverage report
pytest tests/ --cov=. --cov-report=html

# View coverage
open htmlcov/index.html
```

Good coverage targets:
- **Manifest validation**: 90%+
- **Component validation**: 85%+
- **Integration tests**: 70%+

## Contributing Guidelines

### Setting Up Development Environment

```bash
# Clone repository
git clone https://github.com/maxfahl/cc-plugins.git
cd cc-plugins

# Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r tests/requirements.txt

# Verify installation
pytest tests/ -v
```

### Development Workflow

1. **Create feature branch:**
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Make changes:**
   - Add/modify code in commands/, scripts/, etc.
   - Add tests in tests/
   - Update documentation

3. **Run tests:**
   ```bash
   pytest tests/ -v
   ```

4. **Validate plugin:**
   ```bash
   /cc-plugins:validate
   /cc-plugins:debug
   ```

5. **Commit changes:**
   ```bash
   git add .
   git commit -m "Add feature: description"
   ```

6. **Push and create PR:**
   ```bash
   git push origin feature/my-feature
   ```

### Code Style Guidelines

**Python Code:**
- Follow PEP 8 style guide
- Use type hints where possible
- Include docstrings for functions
- Keep functions focused and testable

**Bash Scripts:**
- Use `set -e` for error handling
- Quote variables: `"$VAR"`
- Use meaningful variable names
- Include comments for complex logic

**Markdown Documentation:**
- Use clear headings and structure
- Include code examples
- Use consistent formatting
- Include cross-references

### Commit Message Format

```
<type>: <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `test`: Test additions/changes
- `refactor`: Code refactoring
- `style`: Code style changes
- `ci`: CI/CD changes

**Example:**
```
feat: Add validation for skill directories

Add new validator for SKILL.md files and directory structure.
Includes comprehensive error messages and recovery suggestions.

Fixes #42
```

### Pull Request Guidelines

1. **Clear title and description**
2. **Link related issues**
3. **Ensure all tests pass**
4. **Update documentation**
5. **Request review from maintainers**

## Advanced Topics

### Custom Validation Rules

Create custom validators for your use case:

```python
# custom_validators.py
from pathlib import Path
from typing import List

def validate_plugin_licensing(plugin_dir: Path) -> List[str]:
    """Validate plugin has appropriate license."""
    errors = []

    # Check LICENSE file exists
    license_file = plugin_dir / "LICENSE"
    if not license_file.exists():
        errors.append("Missing LICENSE file")

    # Check manifest has license field
    import json
    manifest = json.loads((plugin_dir / ".claude-plugin" / "plugin.json").read_text())
    if "license" not in manifest:
        errors.append("Manifest missing 'license' field")

    return errors
```

### Extending Scaffolding

Customize plugin creation with templates:

```bash
# Use custom template
python3 scripts/scaffold-plugin.py \
    --name my-plugin \
    --template custom-template \
    --components command,agent,skill
```

### Advanced Component Patterns

**Multi-file Commands:**
```
commands/
├── main.md
├── helpers/
│   ├── util1.sh
│   └── util2.sh
└── templates/
    └── template.txt
```

**Dynamic Skill Loading:**
```python
# Load skills dynamically based on availability
import os
from pathlib import Path

for skill_dir in Path("skills").iterdir():
    if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
        # Load skill dynamically
        pass
```

### Performance Optimization

**Lazy Loading:**
```python
# Load heavy dependencies only when needed
def get_validators():
    global validators
    if validators is None:
        from . import validators as v
        validators = v
    return validators
```

**Caching:**
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def validate_manifest(manifest_path):
    """Cache validation results."""
    # Validation logic
    pass
```

### Integration with External Tools

**GitHub Actions Integration:**
```yaml
name: Validate Plugin

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r tests/requirements.txt
      - run: pytest tests/ -v
      - run: python3 scripts/validate-plugin.py .
```

---

**Resources:**

- [Official Plugin Development Guide](https://code.claude.com/docs)
- [Component Authoring Guide](https://code.claude.com/docs/en/components)
- [Python Testing Guide](https://docs.pytest.org/)
- [YAML Specification](https://yaml.org/spec/)
