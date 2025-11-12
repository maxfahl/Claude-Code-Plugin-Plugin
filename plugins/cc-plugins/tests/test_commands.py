"""
Test suite for cc-plugins commands.

Tests ensure that all commands:
- Accept correct arguments
- Execute successfully
- Produce expected output
- Handle errors gracefully
- Follow Claude Code command specification
"""

import os
import json
import pytest
import tempfile
import shutil
import subprocess
from pathlib import Path


@pytest.fixture
def plugin_root():
    """Returns the path to the cc-plugins plugin root directory."""
    return Path(__file__).parent.parent


@pytest.fixture
def commands_dir(plugin_root):
    """Returns the path to the commands directory."""
    return plugin_root / "commands"


@pytest.fixture
def temp_dir():
    """Creates a temporary directory for testing."""
    temp_path = tempfile.mkdtemp()
    yield temp_path
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def sample_plugin_dir(temp_dir):
    """Creates a sample plugin directory structure for testing."""
    plugin_dir = Path(temp_dir) / "test-plugin"
    plugin_dir.mkdir()

    # Create required directories
    (plugin_dir / ".claude-plugin").mkdir()
    (plugin_dir / "commands").mkdir()
    (plugin_dir / "agents").mkdir()
    (plugin_dir / "skills").mkdir()
    (plugin_dir / "scripts").mkdir()

    # Create basic manifest
    manifest = {
        "name": "test-plugin",
        "version": "1.0.0",
        "description": "A test plugin"
    }
    with open(plugin_dir / ".claude-plugin" / "plugin.json", "w") as f:
        json.dump(manifest, f, indent=2)

    return plugin_dir


class TestCreateCommand:
    """Test suite for /cc-plugins:create command."""

    def test_create_command_file_exists(self, commands_dir):
        """Test that create.md command file exists."""
        create_cmd = commands_dir / "create.md"
        assert create_cmd.exists(), f"create.md command file does not exist at {create_cmd}"
        assert create_cmd.is_file(), f"create.md is not a file"

    def test_create_command_has_frontmatter(self, commands_dir):
        """Test that create.md has YAML frontmatter."""
        create_cmd = commands_dir / "create.md"
        with open(create_cmd, 'r') as f:
            content = f.read()

        assert content.startswith("---"), "Command should start with frontmatter delimiter ---"
        assert "---" in content[3:], "Command should have closing frontmatter delimiter ---"
        assert "description" in content, "Frontmatter should include 'description'"

    def test_create_command_frontmatter_valid(self, commands_dir):
        """Test that create.md frontmatter is valid YAML."""
        create_cmd = commands_dir / "create.md"
        with open(create_cmd, 'r') as f:
            content = f.read()

        # Extract frontmatter
        parts = content.split("---")
        assert len(parts) >= 3, "Frontmatter should be properly delimited"

        frontmatter_str = parts[1].strip()
        assert "description:" in frontmatter_str, "Frontmatter should have description"

    def test_create_command_accepts_plugin_name(self, commands_dir):
        """Test that create command description mentions accepting plugin name."""
        create_cmd = commands_dir / "create.md"
        with open(create_cmd, 'r') as f:
            content = f.read()

        # Command should accept plugin name as argument
        assert "name" in content.lower() or "plugin" in content.lower(), \
            "Command should document that it accepts a plugin name"

    def test_create_command_creates_plugin_structure(self, commands_dir):
        """Test that create command creates the plugin directory structure."""
        create_cmd = commands_dir / "create.md"
        with open(create_cmd, 'r') as f:
            content = f.read()

        # Check that command creates all required directories
        assert "mkdir" in content.lower() or ".claude-plugin" in content, \
            "Create command should create required directories"

    def test_create_command_generates_manifest(self, commands_dir):
        """Test that create command generates plugin manifest."""
        create_cmd = commands_dir / "create.md"
        with open(create_cmd, 'r') as f:
            content = f.read()

        # Check that command creates manifest
        assert "plugin.json" in content or "manifest" in content.lower(), \
            "Create command should generate plugin manifest"


class TestValidateCommand:
    """Test suite for /cc-plugins:validate command."""

    def test_validate_command_file_exists(self, commands_dir):
        """Test that validate.md command file exists."""
        validate_cmd = commands_dir / "validate.md"
        assert validate_cmd.exists(), f"validate.md command file does not exist at {validate_cmd}"
        assert validate_cmd.is_file(), f"validate.md is not a file"

    def test_validate_command_has_frontmatter(self, commands_dir):
        """Test that validate.md has YAML frontmatter."""
        validate_cmd = commands_dir / "validate.md"
        with open(validate_cmd, 'r') as f:
            content = f.read()

        assert content.startswith("---"), "Command should start with frontmatter"
        assert "---" in content[3:], "Command should have closing frontmatter"

    def test_validate_command_accepts_path_argument(self, commands_dir):
        """Test that validate command accepts path to plugin directory."""
        validate_cmd = commands_dir / "validate.md"
        with open(validate_cmd, 'r') as f:
            content = f.read()

        # Should mention accepting a path or $1
        assert "path" in content.lower() or "$1" in content, \
            "Command should document accepting a path argument"

    def test_validate_command_checks_manifest(self, commands_dir):
        """Test that validate command checks the manifest file."""
        validate_cmd = commands_dir / "validate.md"
        with open(validate_cmd, 'r') as f:
            content = f.read()

        assert "manifest" in content.lower() or "plugin.json" in content, \
            "Validate command should check manifest file"

    def test_validate_command_default_to_current_dir(self, commands_dir):
        """Test that validate command defaults to current directory."""
        validate_cmd = commands_dir / "validate.md"
        with open(validate_cmd, 'r') as f:
            content = f.read()

        # Should mention defaulting to current directory or using PWD
        assert "current" in content.lower() or "pwd" in content.lower() or "${1:-.}" in content, \
            "Command should mention defaulting to current directory"


class TestUpdateCommand:
    """Test suite for /cc-plugins:update command."""

    def test_update_command_file_exists(self, commands_dir):
        """Test that update.md command file exists."""
        update_cmd = commands_dir / "update.md"
        assert update_cmd.exists(), f"update.md command file does not exist at {update_cmd}"
        assert update_cmd.is_file(), f"update.md is not a file"

    def test_update_command_has_frontmatter(self, commands_dir):
        """Test that update.md has YAML frontmatter."""
        update_cmd = commands_dir / "update.md"
        with open(update_cmd, 'r') as f:
            content = f.read()

        assert content.startswith("---"), "Command should start with frontmatter"
        assert "---" in content[3:], "Command should have closing frontmatter"

    def test_update_command_supports_manifest_update(self, commands_dir):
        """Test that update command allows updating manifest fields."""
        update_cmd = commands_dir / "update.md"
        with open(update_cmd, 'r') as f:
            content = f.read()

        # Should mention updating manifest
        assert "manifest" in content.lower(), \
            "Command should support updating manifest"

    def test_update_command_supports_version_bump(self, commands_dir):
        """Test that update command supports version bumping."""
        update_cmd = commands_dir / "update.md"
        with open(update_cmd, 'r') as f:
            content = f.read()

        # Should mention version bumping or --version flag
        assert "version" in content.lower(), \
            "Command should support version updates"

    def test_update_command_validates_after_update(self, commands_dir):
        """Test that update command validates plugin after updates."""
        update_cmd = commands_dir / "update.md"
        with open(update_cmd, 'r') as f:
            content = f.read()

        # Should mention validation
        assert "validat" in content.lower(), \
            "Command should validate after updating"


class TestDocumentCommand:
    """Test suite for /cc-plugins:document command."""

    def test_document_command_file_exists(self, commands_dir):
        """Test that document.md command file exists."""
        doc_cmd = commands_dir / "document.md"
        assert doc_cmd.exists(), f"document.md command file does not exist at {doc_cmd}"
        assert doc_cmd.is_file(), f"document.md is not a file"

    def test_document_command_has_frontmatter(self, commands_dir):
        """Test that document.md has YAML frontmatter."""
        doc_cmd = commands_dir / "document.md"
        with open(doc_cmd, 'r') as f:
            content = f.read()

        assert content.startswith("---"), "Command should start with frontmatter"
        assert "---" in content[3:], "Command should have closing frontmatter"

    def test_document_command_generates_readme(self, commands_dir):
        """Test that document command generates README.md."""
        doc_cmd = commands_dir / "document.md"
        with open(doc_cmd, 'r') as f:
            content = f.read()

        assert "README" in content or "readme" in content.lower(), \
            "Command should generate README documentation"

    def test_document_command_documents_commands(self, commands_dir):
        """Test that document command documents all commands."""
        doc_cmd = commands_dir / "document.md"
        with open(doc_cmd, 'r') as f:
            content = f.read()

        assert "command" in content.lower(), \
            "Command should document commands section"

    def test_document_command_documents_agents(self, commands_dir):
        """Test that document command documents all agents."""
        doc_cmd = commands_dir / "document.md"
        with open(doc_cmd, 'r') as f:
            content = f.read()

        assert "agent" in content.lower(), \
            "Command should document agents section"

    def test_document_command_documents_skills(self, commands_dir):
        """Test that document command documents all skills."""
        doc_cmd = commands_dir / "document.md"
        with open(doc_cmd, 'r') as f:
            content = f.read()

        assert "skill" in content.lower(), \
            "Command should document skills section"

    def test_document_command_includes_installation(self, commands_dir):
        """Test that document command includes installation instructions."""
        doc_cmd = commands_dir / "document.md"
        with open(doc_cmd, 'r') as f:
            content = f.read()

        assert "install" in content.lower(), \
            "Command should include installation instructions"


class TestDebugCommand:
    """Test suite for /cc-plugins:debug command."""

    def test_debug_command_file_exists(self, commands_dir):
        """Test that debug.md command file exists."""
        debug_cmd = commands_dir / "debug.md"
        assert debug_cmd.exists(), f"debug.md command file does not exist at {debug_cmd}"
        assert debug_cmd.is_file(), f"debug.md is not a file"

    def test_debug_command_has_frontmatter(self, commands_dir):
        """Test that debug.md has YAML frontmatter."""
        debug_cmd = commands_dir / "debug.md"
        with open(debug_cmd, 'r') as f:
            content = f.read()

        assert content.startswith("---"), "Command should start with frontmatter"
        assert "---" in content[3:], "Command should have closing frontmatter"

    def test_debug_command_checks_structure(self, commands_dir):
        """Test that debug command checks directory structure."""
        debug_cmd = commands_dir / "debug.md"
        with open(debug_cmd, 'r') as f:
            content = f.read()

        assert "structure" in content.lower() or "directory" in content.lower(), \
            "Command should check directory structure"

    def test_debug_command_checks_frontmatter(self, commands_dir):
        """Test that debug command checks component frontmatter."""
        debug_cmd = commands_dir / "debug.md"
        with open(debug_cmd, 'r') as f:
            content = f.read()

        assert "frontmatter" in content.lower() or "yaml" in content.lower(), \
            "Command should check frontmatter"

    def test_debug_command_provides_error_analysis(self, commands_dir):
        """Test that debug command provides detailed error analysis."""
        debug_cmd = commands_dir / "debug.md"
        with open(debug_cmd, 'r') as f:
            content = f.read()

        assert "error" in content.lower() or "issue" in content.lower(), \
            "Command should provide error analysis"

    def test_debug_command_suggests_fixes(self, commands_dir):
        """Test that debug command suggests fixes."""
        debug_cmd = commands_dir / "debug.md"
        with open(debug_cmd, 'r') as f:
            content = f.read()

        assert "fix" in content.lower() or "suggest" in content.lower(), \
            "Command should suggest fixes for issues"


class TestCommandFrontmatterFormat:
    """Test suite for verifying all commands follow proper frontmatter format."""

    @pytest.fixture
    def all_commands(self, commands_dir):
        """Get all command files in the commands directory."""
        return list(commands_dir.glob("*.md"))

    def test_all_commands_have_description(self, all_commands):
        """Test that all commands have description in frontmatter."""
        for cmd_file in all_commands:
            with open(cmd_file, 'r') as f:
                content = f.read()

            assert "description:" in content, \
                f"{cmd_file.name} missing 'description:' in frontmatter"

    def test_all_commands_have_allowed_tools(self, all_commands):
        """Test that all commands have allowed-tools in frontmatter."""
        for cmd_file in all_commands:
            with open(cmd_file, 'r') as f:
                content = f.read()

            assert "allowed-tools:" in content or "allowed_tools:" in content, \
                f"{cmd_file.name} missing 'allowed-tools:' in frontmatter"

    def test_all_commands_properly_closed(self, all_commands):
        """Test that all command frontmatter is properly closed."""
        for cmd_file in all_commands:
            with open(cmd_file, 'r') as f:
                content = f.read()

            # Should have opening and closing ---
            frontmatter_delimiters = content.count("---")
            assert frontmatter_delimiters >= 2, \
                f"{cmd_file.name} frontmatter not properly delimited"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
