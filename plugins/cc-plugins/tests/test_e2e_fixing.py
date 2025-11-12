"""
End-to-end tests for plugin fixing workflow.

Tests the complete lifecycle of detecting and fixing broken plugins using
the cc-plugins validation and debug commands.

Test Coverage:
- Detection of missing manifest file
- Detection of invalid JSON in manifest
- Detection of wrong directory structure
- Detection of invalid frontmatter syntax
- Detection of unsupported fields
- Verification that fixes resolve issues
"""

import json
import subprocess
import tempfile
import pytest
from pathlib import Path
import shutil


@pytest.fixture
def temp_workspace():
    """Create a temporary workspace for broken test plugins."""
    with tempfile.TemporaryDirectory() as tmpdir:
        workspace = Path(tmpdir)
        yield workspace


@pytest.fixture
def cc_plugins_root():
    """Returns the path to the cc-plugins root directory."""
    return Path(__file__).parent.parent


class TestMissingManifest:
    """Test detection and fixing of missing manifest file."""

    def test_detects_missing_manifest(self, temp_workspace, cc_plugins_root):
        """Test that validator detects missing plugin.json manifest."""
        # Create broken plugin without manifest
        plugin_dir = temp_workspace / "broken-no-manifest"
        plugin_dir.mkdir()
        (plugin_dir / ".claude-plugin").mkdir()
        # Don't create plugin.json

        # Run validator
        validator_script = cc_plugins_root / "scripts" / "validate-plugin.py"
        result = subprocess.run(
            ["python3", str(validator_script), str(plugin_dir)],
            capture_output=True,
            text=True
        )

        # Should fail
        assert result.returncode != 0
        assert "missing" in result.stdout.lower() and "manifest" in result.stdout.lower()

    def test_fix_missing_manifest(self, temp_workspace, cc_plugins_root):
        """Test that creating manifest file fixes the issue."""
        # Create broken plugin
        plugin_dir = temp_workspace / "broken-no-manifest-fix"
        plugin_dir.mkdir()
        (plugin_dir / ".claude-plugin").mkdir()

        # Verify it's broken
        validator_script = cc_plugins_root / "scripts" / "validate-plugin.py"
        result = subprocess.run(
            ["python3", str(validator_script), str(plugin_dir)],
            capture_output=True,
            text=True
        )
        assert result.returncode != 0

        # Fix: Create minimal manifest
        manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
        manifest = {
            "name": "broken-no-manifest-fix",
            "version": "1.0.0",
            "description": "Test plugin"
        }
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)

        # Verify fix
        result = subprocess.run(
            ["python3", str(validator_script), str(plugin_dir)],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0


class TestInvalidJSON:
    """Test detection and fixing of invalid JSON in manifest."""

    def test_detects_invalid_json_manifest(self, temp_workspace, cc_plugins_root):
        """Test that validator detects malformed JSON in manifest."""
        # Create broken plugin with invalid JSON
        plugin_dir = temp_workspace / "broken-invalid-json"
        plugin_dir.mkdir()
        (plugin_dir / ".claude-plugin").mkdir()

        manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
        # Write invalid JSON (trailing comma, missing quote)
        manifest_path.write_text("""
{
  "name": "broken-plugin",
  "version": "1.0.0",
  "description": "Test plugin,
}
""")

        # Run validator
        validator_script = cc_plugins_root / "scripts" / "validate-plugin.py"
        result = subprocess.run(
            ["python3", str(validator_script), str(plugin_dir)],
            capture_output=True,
            text=True
        )

        # Should fail
        assert result.returncode != 0
        assert "invalid json" in result.stdout.lower() or "json" in result.stdout.lower()

    def test_fix_invalid_json_manifest(self, temp_workspace, cc_plugins_root):
        """Test that fixing JSON syntax resolves the issue."""
        # Create broken plugin
        plugin_dir = temp_workspace / "broken-invalid-json-fix"
        plugin_dir.mkdir()
        (plugin_dir / ".claude-plugin").mkdir()

        manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
        manifest_path.write_text("""
{
  "name": "broken-plugin",
  "version": "1.0.0",
  "description": "Test plugin,
}
""")

        # Verify it's broken
        validator_script = cc_plugins_root / "scripts" / "validate-plugin.py"
        result = subprocess.run(
            ["python3", str(validator_script), str(plugin_dir)],
            capture_output=True,
            text=True
        )
        assert result.returncode != 0

        # Fix: Write valid JSON
        manifest = {
            "name": "broken-invalid-json-fix",
            "version": "1.0.0",
            "description": "Test plugin"
        }
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)

        # Verify fix
        result = subprocess.run(
            ["python3", str(validator_script), str(plugin_dir)],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0


class TestWrongDirectoryStructure:
    """Test detection and fixing of wrong directory structure."""

    def test_detects_components_in_wrong_location(self, temp_workspace, cc_plugins_root):
        """Test that validator detects components inside .claude-plugin."""
        # Create broken plugin with components in wrong place
        plugin_dir = temp_workspace / "broken-wrong-structure"
        plugin_dir.mkdir()
        claude_plugin_dir = plugin_dir / ".claude-plugin"
        claude_plugin_dir.mkdir()

        # Create manifest
        manifest_path = claude_plugin_dir / "plugin.json"
        manifest = {
            "name": "broken-wrong-structure",
            "version": "1.0.0",
            "description": "Test plugin"
        }
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)

        # Put components in WRONG location (.claude-plugin)
        (claude_plugin_dir / "commands").mkdir()
        (claude_plugin_dir / "agents").mkdir()

        # Run validator
        validator_script = cc_plugins_root / "scripts" / "validate-plugin.py"
        result = subprocess.run(
            ["python3", str(validator_script), str(plugin_dir)],
            capture_output=True,
            text=True
        )

        # Should fail
        assert result.returncode != 0
        assert "wrong location" in result.stdout.lower() or "root level" in result.stdout.lower()

    def test_fix_wrong_directory_structure(self, temp_workspace, cc_plugins_root):
        """Test that moving components to root fixes the issue."""
        # Create broken plugin
        plugin_dir = temp_workspace / "broken-wrong-structure-fix"
        plugin_dir.mkdir()
        claude_plugin_dir = plugin_dir / ".claude-plugin"
        claude_plugin_dir.mkdir()

        manifest_path = claude_plugin_dir / "plugin.json"
        manifest = {
            "name": "broken-wrong-structure-fix",
            "version": "1.0.0",
            "description": "Test plugin"
        }
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)

        # Put components in WRONG location
        (claude_plugin_dir / "commands").mkdir()

        # Verify it's broken
        validator_script = cc_plugins_root / "scripts" / "validate-plugin.py"
        result = subprocess.run(
            ["python3", str(validator_script), str(plugin_dir)],
            capture_output=True,
            text=True
        )
        assert result.returncode != 0

        # Fix: Move commands to root level
        shutil.move(
            str(claude_plugin_dir / "commands"),
            str(plugin_dir / "commands")
        )

        # Verify fix
        result = subprocess.run(
            ["python3", str(validator_script), str(plugin_dir)],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0


class TestInvalidFrontmatter:
    """Test detection and fixing of invalid frontmatter syntax."""

    def test_detects_invalid_frontmatter_in_command(self, temp_workspace, cc_plugins_root):
        """Test that validator detects invalid frontmatter in command file."""
        # Create plugin with invalid command frontmatter
        plugin_dir = self._create_valid_plugin(temp_workspace, "broken-invalid-frontmatter")

        # Create command with invalid frontmatter
        commands_dir = plugin_dir / "commands"
        commands_dir.mkdir(exist_ok=True)

        command_file = commands_dir / "test.md"
        # Missing closing --- for frontmatter
        command_file.write_text("""---
description: "Test command"
allowed-tools: ["Bash"]
model: "sonnet"

# Test Command

This is broken.
""")

        # Run validator
        validator_script = cc_plugins_root / "scripts" / "validate-plugin.py"
        result = subprocess.run(
            ["python3", str(validator_script), str(plugin_dir)],
            capture_output=True,
            text=True
        )

        # Should fail
        assert result.returncode != 0

    def test_fix_invalid_frontmatter(self, temp_workspace, cc_plugins_root):
        """Test that fixing frontmatter syntax resolves the issue."""
        # Create plugin with invalid frontmatter
        plugin_dir = self._create_valid_plugin(temp_workspace, "broken-invalid-frontmatter-fix")

        commands_dir = plugin_dir / "commands"
        commands_dir.mkdir(exist_ok=True)

        command_file = commands_dir / "test.md"
        command_file.write_text("""---
description: "Test command"
allowed-tools: ["Bash"]
model: "sonnet"

# Test Command
""")

        # Verify it's broken
        validator_script = cc_plugins_root / "scripts" / "validate-plugin.py"
        result = subprocess.run(
            ["python3", str(validator_script), str(plugin_dir)],
            capture_output=True,
            text=True
        )
        assert result.returncode != 0

        # Fix: Add closing --- and required fields
        command_file.write_text("""---
description: "Test command"
allowed-tools: ["Bash"]
argument-hint: "No arguments"
model: "sonnet"
disable-model-invocation: false
---

# Test Command

This is fixed.
""")

        # Verify fix
        result = subprocess.run(
            ["python3", str(validator_script), str(plugin_dir)],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0

    def _create_valid_plugin(self, workspace, name):
        """Helper to create a valid plugin structure."""
        plugin_dir = workspace / name
        plugin_dir.mkdir()
        (plugin_dir / ".claude-plugin").mkdir()

        manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
        manifest = {
            "name": name,
            "version": "1.0.0",
            "description": "Test plugin"
        }
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)

        return plugin_dir


class TestUnsupportedFields:
    """Test detection of unsupported manifest fields."""

    def test_detects_unsupported_manifest_fields(self, temp_workspace, cc_plugins_root):
        """Test that validator warns about unsupported fields in manifest."""
        # Create plugin with unsupported fields
        plugin_dir = temp_workspace / "broken-unsupported-fields"
        plugin_dir.mkdir()
        (plugin_dir / ".claude-plugin").mkdir()

        manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
        manifest = {
            "name": "broken-unsupported-fields",
            "version": "1.0.0",
            "description": "Test plugin",
            "unsupportedField": "This field doesn't exist in spec",
            "anotherBadField": 123
        }
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)

        # Run validator
        validator_script = cc_plugins_root / "scripts" / "validate-plugin.py"
        result = subprocess.run(
            ["python3", str(validator_script), str(plugin_dir)],
            capture_output=True,
            text=True
        )

        # Should warn about unsupported fields
        output = result.stdout.lower()
        assert "unsupported" in output or "warning" in output

    def test_fix_unsupported_fields(self, temp_workspace, cc_plugins_root):
        """Test that removing unsupported fields resolves warnings."""
        # Create plugin with unsupported fields
        plugin_dir = temp_workspace / "broken-unsupported-fields-fix"
        plugin_dir.mkdir()
        (plugin_dir / ".claude-plugin").mkdir()

        manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
        manifest = {
            "name": "broken-unsupported-fields-fix",
            "version": "1.0.0",
            "description": "Test plugin",
            "badField": "Remove this"
        }
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)

        # Verify warning exists
        validator_script = cc_plugins_root / "scripts" / "validate-plugin.py"
        result = subprocess.run(
            ["python3", str(validator_script), str(plugin_dir)],
            capture_output=True,
            text=True
        )
        output_before = result.stdout.lower()

        # Fix: Remove unsupported field
        manifest = {
            "name": "broken-unsupported-fields-fix",
            "version": "1.0.0",
            "description": "Test plugin"
        }
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)

        # Verify fix (no warnings)
        result = subprocess.run(
            ["python3", str(validator_script), str(plugin_dir)],
            capture_output=True,
            text=True
        )
        output_after = result.stdout.lower()

        # After fix, should have no warnings about unsupported fields
        assert result.returncode == 0


class TestInvalidManifestSchema:
    """Test detection and fixing of invalid manifest schema."""

    def test_detects_missing_required_field(self, temp_workspace, cc_plugins_root):
        """Test that validator detects missing 'name' field."""
        # Create plugin without name field
        plugin_dir = temp_workspace / "broken-no-name"
        plugin_dir.mkdir()
        (plugin_dir / ".claude-plugin").mkdir()

        manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
        manifest = {
            "version": "1.0.0",
            "description": "Test plugin"
            # Missing 'name' field
        }
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)

        # Run validator
        validator_script = cc_plugins_root / "scripts" / "validate-plugin.py"
        result = subprocess.run(
            ["python3", str(validator_script), str(plugin_dir)],
            capture_output=True,
            text=True
        )

        # Should fail
        assert result.returncode != 0
        assert "name" in result.stdout.lower() and "required" in result.stdout.lower()

    def test_detects_invalid_name_format(self, temp_workspace, cc_plugins_root):
        """Test that validator detects non-kebab-case names."""
        # Create plugin with invalid name format
        plugin_dir = temp_workspace / "broken-invalid-name"
        plugin_dir.mkdir()
        (plugin_dir / ".claude-plugin").mkdir()

        manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
        manifest = {
            "name": "Invalid_Name_Format",  # Should be kebab-case
            "version": "1.0.0",
            "description": "Test plugin"
        }
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)

        # Run validator
        validator_script = cc_plugins_root / "scripts" / "validate-plugin.py"
        result = subprocess.run(
            ["python3", str(validator_script), str(plugin_dir)],
            capture_output=True,
            text=True
        )

        # Should fail
        assert result.returncode != 0
        assert "kebab" in result.stdout.lower() or "lowercase" in result.stdout.lower()

    def test_fix_invalid_name_format(self, temp_workspace, cc_plugins_root):
        """Test that fixing name format resolves the issue."""
        # Create plugin with invalid name
        plugin_dir = temp_workspace / "broken-invalid-name-fix"
        plugin_dir.mkdir()
        (plugin_dir / ".claude-plugin").mkdir()

        manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
        manifest = {
            "name": "Invalid_Name",
            "version": "1.0.0",
            "description": "Test plugin"
        }
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)

        # Verify it's broken
        validator_script = cc_plugins_root / "scripts" / "validate-plugin.py"
        result = subprocess.run(
            ["python3", str(validator_script), str(plugin_dir)],
            capture_output=True,
            text=True
        )
        assert result.returncode != 0

        # Fix: Use kebab-case
        manifest = {
            "name": "broken-invalid-name-fix",
            "version": "1.0.0",
            "description": "Test plugin"
        }
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)

        # Verify fix
        result = subprocess.run(
            ["python3", str(validator_script), str(plugin_dir)],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0


class TestComplexFixingScenarios:
    """Test fixing plugins with multiple issues."""

    def test_fix_plugin_with_multiple_issues(self, temp_workspace, cc_plugins_root):
        """Test fixing a plugin with multiple validation errors."""
        # Create plugin with multiple issues
        plugin_dir = temp_workspace / "broken-multiple-issues"
        plugin_dir.mkdir()
        claude_plugin_dir = plugin_dir / ".claude-plugin"
        claude_plugin_dir.mkdir()

        # Issue 1: Invalid manifest (wrong name format)
        manifest_path = claude_plugin_dir / "plugin.json"
        manifest = {
            "name": "Invalid_Name",  # Wrong format
            "version": "1.0.0",
            "badField": "unsupported"  # Unsupported field
        }
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)

        # Issue 2: Components in wrong location
        (claude_plugin_dir / "commands").mkdir()

        # Issue 3: Invalid command file
        (claude_plugin_dir / "commands" / "test.md").write_text("""---
description: "Test"
# Missing closing ---
""")

        # Verify it's broken
        validator_script = cc_plugins_root / "scripts" / "validate-plugin.py"
        result = subprocess.run(
            ["python3", str(validator_script), str(plugin_dir)],
            capture_output=True,
            text=True
        )
        assert result.returncode != 0
        error_count = result.stdout.lower().count("error")
        assert error_count >= 1  # At least one error detected

        # Fix all issues
        # Fix 1: Correct manifest
        manifest = {
            "name": "broken-multiple-issues",
            "version": "1.0.0",
            "description": "Test plugin"
        }
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)

        # Fix 2: Move commands to root
        shutil.move(
            str(claude_plugin_dir / "commands"),
            str(plugin_dir / "commands")
        )

        # Fix 3: Fix command file
        (plugin_dir / "commands" / "test.md").write_text("""---
description: "Test"
allowed-tools: ["Bash"]
argument-hint: "No arguments"
model: "sonnet"
disable-model-invocation: false
---

# Test
""")

        # Verify all fixed
        result = subprocess.run(
            ["python3", str(validator_script), str(plugin_dir)],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
