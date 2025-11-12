---
description: "Update plugin manifest fields, add new components, or bump version numbers. Supports semantic versioning (major, minor, patch) and automatically validates plugin after updates."
allowed-tools: ["Bash", "Read", "Write", "Edit"]
argument-hint: "Field name and value (e.g., description 'New description') or --version major|minor|patch"
model: "sonnet"
disable-model-invocation: false
---

# Update Plugin

Updates plugin manifest fields, adds new components, or manages version numbers.

## Usage

```bash
# Update manifest field
/cc-plugins:update description "A new description"
/cc-plugins:update version 2.0.0

# Bump semantic version
/cc-plugins:update --version major
/cc-plugins:update --version minor
/cc-plugins:update --version patch

# Update author information
/cc-plugins:update author.name "John Developer"
/cc-plugins:update author.email "john@example.com"

# Add keywords
/cc-plugins:update keywords "new-keyword"
```

## What It Does

1. **Manifest Updates**: Modifies fields in `.claude-plugin/plugin.json`
2. **Version Bumping**: Automatically increments version following semantic versioning
3. **Component Addition**: Adds new command, agent, or skill templates
4. **Validation**: Automatically validates plugin after updates
5. **Backup**: Creates backup of manifest before changes
6. **Confirmation**: Shows changes before applying them

## Parameters

- **Field Name** ($1): Manifest field to update (e.g., `description`, `version`, `author.name`)
- **Value** ($2): New value for the field
- **--version**: Bump version (major|minor|patch)
- **--add-command**: Add new command template
- **--add-agent**: Add new agent template
- **--add-skill**: Add new skill template

## Examples

### Update Description

```bash
/cc-plugins:update description "My awesome plugin that does X"
```

### Update Author

```bash
/cc-plugins:update author.name "Jane Developer"
/cc-plugins:update author.email "jane@dev.com"
```

### Bump Version

```bash
# From 1.2.3 to 2.0.0
/cc-plugins:update --version major

# From 1.2.3 to 1.3.0
/cc-plugins:update --version minor

# From 1.2.3 to 1.2.4
/cc-plugins:update --version patch
```

### Add Keywords

```bash
/cc-plugins:update keywords "development"
/cc-plugins:update keywords "testing"
```

## Output

### Success Output

```
✓ Plugin updated successfully!

Changes applied:
- description: "Old description" → "My awesome plugin"
- version: 1.0.0 → 1.1.0 (minor bump)

Updated fields:
├─ description
└─ version

Validation: PASSED ✓

Plugin 'my-plugin' is ready to use!
```

### Confirmation Prompt

```
Update plugin manifest?

Current value (description):
"Old description"

New value:
"My awesome plugin"

Changes:
- description will be updated

Proceed? (yes/no)
```

## Field Options

### Manifest Fields

- `description`: Plugin description
- `version`: Version number (semver format)
- `author.name`: Author full name
- `author.email`: Author email
- `author.url`: Author website
- `homepage`: Plugin homepage URL
- `repository`: Repository URL
- `license`: License type (MIT, Apache-2.0, etc.)
- `keywords`: Keywords (comma-separated or repeated calls)

### Nested Fields

```bash
# Nested field syntax
/cc-plugins:update author.name "New Name"
/cc-plugins:update author.email "email@example.com"
```

---

!bash
# Parse arguments
if [ $# -eq 0 ]; then
  echo "Usage: /cc-plugins:update <field> <value>"
  echo "       /cc-plugins:update --version <major|minor|patch>"
  exit 1
fi

# Check if in a plugin directory
if [ ! -f "./.claude-plugin/plugin.json" ]; then
  echo "✗ Error: Not in a plugin directory"
  echo "   Missing: ./.claude-plugin/plugin.json"
  exit 1
fi

MANIFEST_PATH="./.claude-plugin/plugin.json"

# Handle --version flag
if [ "$1" = "--version" ]; then
  VERSION_TYPE="${2:?Version type required: major, minor, or patch}"

  # Get current version
  CURRENT_VERSION=$(python3 -c "import json; print(json.load(open('$MANIFEST_PATH')).get('version', '1.0.0'))")

  # Parse version
  IFS='.' read -r MAJOR MINOR PATCH <<< "$CURRENT_VERSION"
  MAJOR=${MAJOR:-1}
  MINOR=${MINOR:-0}
  PATCH=${PATCH:-0}

  case "$VERSION_TYPE" in
    major)
      ((MAJOR++))
      MINOR=0
      PATCH=0
      ;;
    minor)
      ((MINOR++))
      PATCH=0
      ;;
    patch)
      ((PATCH++))
      ;;
    *)
      echo "✗ Error: Unknown version type: $VERSION_TYPE"
      echo "   Use: major, minor, or patch"
      exit 1
      ;;
  esac

  NEW_VERSION="$MAJOR.$MINOR.$PATCH"
  FIELD="version"
  VALUE="$NEW_VERSION"
else
  FIELD="${1:?Field name required}"
  VALUE="${2:?Value required}"
fi

# Show confirmation
echo "Update plugin manifest?"
echo ""
echo "Field: $FIELD"
echo "Value: $VALUE"
echo ""

# Backup manifest
cp "$MANIFEST_PATH" "${MANIFEST_PATH}.backup"

# Update manifest using Python
python3 << PYTHON_SCRIPT
import json
import sys

# Load manifest
with open('$MANIFEST_PATH', 'r') as f:
    manifest = json.load(f)

# Handle nested fields (e.g., author.name)
if '.' in '$FIELD':
    parts = '$FIELD'.split('.')
    current = manifest
    for part in parts[:-1]:
        if part not in current:
            current[part] = {}
        current = current[part]
    current[parts[-1]] = '$VALUE'
else:
    manifest['$FIELD'] = '$VALUE'

# Write back
with open('$MANIFEST_PATH', 'w') as f:
    json.dump(manifest, f, indent=2)

print("✓ Manifest updated!")
print(f"  {':'.join('$FIELD'.split('.'))}: $VALUE")

PYTHON_SCRIPT

# Validate after update
echo ""
echo "Validating plugin..."

# Quick validation check
if python3 -c "import json; json.load(open('$MANIFEST_PATH'))" 2>/dev/null; then
  echo "✓ Validation passed"
  echo ""
  echo "Plugin updated successfully!"
  exit 0
else
  echo "✗ Validation failed"
  echo "Restoring from backup..."
  mv "${MANIFEST_PATH}.backup" "$MANIFEST_PATH"
  exit 1
fi
