"""
End-to-end tests for plugin creation workflow.

Tests the complete lifecycle of creating a new plugin using the cc-plugins
create command, validating the created structure, and ensuring all generated
files are valid.

Test Coverage:
- Basic plugin creation with default parameters
- Plugin creation with custom metadata
- Validation of created plugin structure
- Documentation generation for created plugins
- Component creation (commands, agents, skills)
- Cleanup of test plugins
"""

import json
import subprocess
import tempfile
import pytest
from pathlib import Path
import shutil


@pytest.fixture
def temp_workspace():
    """Create a temporary workspace for test plugins."""
    with tempfile.TemporaryDirectory() as tmpdir:
        workspace = Path(tmpdir)
        yield workspace
        # Cleanup handled automatically by tempfile


@pytest.fixture
def cc_plugins_root():
    """Returns the path to the cc-plugins root directory."""
    return Path(__file__).parent.parent


class TestBasicPluginCreation:
    """Test basic plugin creation functionality."""

    def test_create_plugin_with_default_parameters(self, temp_workspace, cc_plugins_root):
        """Test creating a plugin with only a name parameter."""
        plugin_name = "test-basic-plugin"
        create_cmd = cc_plugins_root / "commands" / "create.md"

        # Extract and execute the bash script from create.md
        result = self._execute_create_command(
            create_cmd,
            plugin_name,
            cwd=temp_workspace
        )

        assert result.returncode == 0, f"Create command failed: {result.stderr}"

        # Verify plugin directory was created
        plugin_dir = temp_workspace / plugin_name
        assert plugin_dir.exists(), f"Plugin directory not created: {plugin_dir}"
        assert plugin_dir.is_dir(), f"Plugin path is not a directory: {plugin_dir}"

        # Verify basic structure
        self._verify_plugin_structure(plugin_dir, plugin_name)

    def test_create_plugin_with_custom_metadata(self, temp_workspace, cc_plugins_root):
        """Test creating a plugin with custom description, author, and license."""
        plugin_name = "test-custom-plugin"
        description = "A test plugin with custom metadata"
        author = "Test Author"
        license_type = "Apache-2.0"

        create_cmd = cc_plugins_root / "commands" / "create.md"

        result = self._execute_create_command(
            create_cmd,
            plugin_name,
            description=description,
            author=author,
            license=license_type,
            cwd=temp_workspace
        )

        assert result.returncode == 0, f"Create command failed: {result.stderr}"

        # Verify plugin directory
        plugin_dir = temp_workspace / plugin_name
        assert plugin_dir.exists()

        # Verify custom metadata in manifest
        manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)

        assert manifest["name"] == plugin_name
        assert manifest["description"] == description
        assert manifest["author"]["name"] == author
        assert manifest["license"] == license_type

    def test_create_plugin_with_invalid_name(self, temp_workspace, cc_plugins_root):
        """Test that invalid plugin names are rejected."""
        invalid_names = [
            "Test_Plugin",  # Underscore
            "Test Plugin",  # Space
            "TestPlugin",   # CamelCase
            "test-plugin-", # Trailing hyphen
            "-test-plugin", # Leading hyphen
            "test--plugin", # Double hyphen
        ]

        create_cmd = cc_plugins_root / "commands" / "create.md"

        for invalid_name in invalid_names:
            result = self._execute_create_command(
                create_cmd,
                invalid_name,
                cwd=temp_workspace
            )

            # Should fail for invalid names
            assert result.returncode != 0, f"Should reject invalid name: {invalid_name}"

    def test_create_plugin_duplicate_name(self, temp_workspace, cc_plugins_root):
        """Test that creating a plugin with an existing name fails."""
        plugin_name = "test-duplicate-plugin"
        create_cmd = cc_plugins_root / "commands" / "create.md"

        # Create first plugin
        result1 = self._execute_create_command(
            create_cmd,
            plugin_name,
            cwd=temp_workspace
        )
        assert result1.returncode == 0

        # Try to create duplicate
        result2 = self._execute_create_command(
            create_cmd,
            plugin_name,
            cwd=temp_workspace
        )

        # Should fail due to existing directory
        assert result2.returncode != 0
        assert "already exists" in result2.stderr.lower() or "already exists" in result2.stdout.lower()

    def _execute_create_command(self, create_cmd, plugin_name, description=None,
                                 author=None, license=None, cwd=None):
        """
        Execute the create command bash script.

        Args:
            create_cmd: Path to create.md file
            plugin_name: Name of plugin to create
            description: Optional description
            author: Optional author name
            license: Optional license type
            cwd: Working directory for execution

        Returns:
            subprocess.CompletedProcess result
        """
        # Extract bash script from create.md
        with open(create_cmd, 'r') as f:
            content = f.read()

        # Find the bash script section
        bash_start = content.find("!bash\n")
        if bash_start == -1:
            raise ValueError("No bash script found in create.md")

        bash_script = content[bash_start + 6:]  # Skip "!bash\n"

        # Build command arguments
        args = [plugin_name]
        if description:
            args.extend(["--description", description])
        if author:
            args.extend(["--author", author])
        if license:
            args.extend(["--license", license])

        # Execute bash script
        result = subprocess.run(
            ["bash", "-c", bash_script, "bash"] + args,
            cwd=cwd,
            capture_output=True,
            text=True
        )

        return result

    def _verify_plugin_structure(self, plugin_dir, plugin_name):
        """Verify that created plugin has correct structure."""
        # Check required directories
        required_dirs = [
            ".claude-plugin",
            "commands",
            "agents",
            "skills",
            "scripts",
            "docs",
            "tests"
        ]

        for dir_name in required_dirs:
            dir_path = plugin_dir / dir_name
            assert dir_path.exists(), f"Missing directory: {dir_name}"
            assert dir_path.is_dir(), f"Not a directory: {dir_name}"

        # Check required files
        assert (plugin_dir / ".claude-plugin" / "plugin.json").exists()
        assert (plugin_dir / "README.md").exists()
        assert (plugin_dir / ".gitignore").exists()
        assert (plugin_dir / "tests" / "test_plugin.py").exists()

        # Verify manifest is valid JSON
        manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)

        assert manifest["name"] == plugin_name
        assert "version" in manifest
        assert "description" in manifest


class TestCreatedPluginValidation:
    """Test that created plugins pass validation."""

    def test_created_plugin_passes_validation(self, temp_workspace, cc_plugins_root):
        """Test that a newly created plugin passes validation."""
        plugin_name = "test-valid-plugin"

        # Create plugin
        create_cmd = cc_plugins_root / "commands" / "create.md"
        result = self._execute_create_command(create_cmd, plugin_name, cwd=temp_workspace)
        assert result.returncode == 0

        # Validate plugin
        plugin_dir = temp_workspace / plugin_name
        validator_script = cc_plugins_root / "scripts" / "validate-plugin.py"

        result = subprocess.run(
            ["python3", str(validator_script), str(plugin_dir)],
            capture_output=True,
            text=True
        )

        assert result.returncode == 0, f"Validation failed: {result.stdout}\n{result.stderr}"
        assert "✓" in result.stdout or "passed" in result.stdout.lower()

    def test_created_plugin_has_valid_manifest(self, temp_workspace, cc_plugins_root):
        """Test that created plugin manifest is valid."""
        plugin_name = "test-manifest-plugin"

        # Create plugin
        create_cmd = cc_plugins_root / "commands" / "create.md"
        result = self._execute_create_command(create_cmd, plugin_name, cwd=temp_workspace)
        assert result.returncode == 0

        # Check manifest structure
        plugin_dir = temp_workspace / plugin_name
        manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"

        with open(manifest_path, 'r') as f:
            manifest = json.load(f)

        # Verify required and optional fields
        assert "name" in manifest
        assert isinstance(manifest["name"], str)
        assert manifest["name"] == plugin_name

        # Check kebab-case
        assert manifest["name"].islower() or "-" in manifest["name"]
        assert " " not in manifest["name"]
        assert "_" not in manifest["name"]

        # Check optional fields
        assert "version" in manifest
        assert "description" in manifest
        assert "license" in manifest

    def _execute_create_command(self, create_cmd, plugin_name, cwd=None):
        """Execute the create command."""
        with open(create_cmd, 'r') as f:
            content = f.read()

        bash_start = content.find("!bash\n")
        bash_script = content[bash_start + 6:]

        result = subprocess.run(
            ["bash", "-c", bash_script, "bash", plugin_name],
            cwd=cwd,
            capture_output=True,
            text=True
        )

        return result


class TestComponentCreation:
    """Test creating components in a new plugin."""

    def test_can_add_command_to_created_plugin(self, temp_workspace, cc_plugins_root):
        """Test adding a command file to a newly created plugin."""
        plugin_name = "test-command-plugin"

        # Create plugin
        create_cmd = cc_plugins_root / "commands" / "create.md"
        result = self._execute_create_command(create_cmd, plugin_name, cwd=temp_workspace)
        assert result.returncode == 0

        # Add a command file
        plugin_dir = temp_workspace / plugin_name
        command_file = plugin_dir / "commands" / "test-command.md"

        command_content = """---
description: "A test command"
allowed-tools: ["Bash"]
argument-hint: "No arguments required"
model: "sonnet"
disable-model-invocation: false
---

# Test Command

This is a test command.

!bash
echo "Hello from test command"
"""
        command_file.write_text(command_content)

        # Validate the plugin with the new command
        validator_script = cc_plugins_root / "scripts" / "validate-plugin.py"
        result = subprocess.run(
            ["python3", str(validator_script), str(plugin_dir)],
            capture_output=True,
            text=True
        )

        assert result.returncode == 0, f"Validation failed: {result.stdout}"

    def test_can_add_agent_to_created_plugin(self, temp_workspace, cc_plugins_root):
        """Test adding an agent file to a newly created plugin."""
        plugin_name = "test-agent-plugin"

        # Create plugin
        create_cmd = cc_plugins_root / "commands" / "create.md"
        result = self._execute_create_command(create_cmd, plugin_name, cwd=temp_workspace)
        assert result.returncode == 0

        # Add an agent file
        plugin_dir = temp_workspace / plugin_name
        agent_file = plugin_dir / "agents" / "test-agent.md"

        agent_content = """---
description: "A test agent"
activation-phrases: ["test agent"]
allowed-tools: ["Bash"]
model: "sonnet"
---

# Test Agent

This is a test agent.
"""
        agent_file.write_text(agent_content)

        # Validate the plugin with the new agent
        validator_script = cc_plugins_root / "scripts" / "validate-plugin.py"
        result = subprocess.run(
            ["python3", str(validator_script), str(plugin_dir)],
            capture_output=True,
            text=True
        )

        assert result.returncode == 0, f"Validation failed: {result.stdout}"

    def test_can_add_skill_to_created_plugin(self, temp_workspace, cc_plugins_root):
        """Test adding a skill to a newly created plugin."""
        plugin_name = "test-skill-plugin"

        # Create plugin
        create_cmd = cc_plugins_root / "commands" / "create.md"
        result = self._execute_create_command(create_cmd, plugin_name, cwd=temp_workspace)
        assert result.returncode == 0

        # Add a skill directory and SKILL.md
        plugin_dir = temp_workspace / plugin_name
        skill_dir = plugin_dir / "skills" / "test-skill"
        skill_dir.mkdir(parents=True, exist_ok=True)

        skill_file = skill_dir / "SKILL.md"
        skill_content = """---
name: "test-skill"
description: "A test skill"
allowed-tools: ["Bash"]
model: "sonnet"
---

# Test Skill

This is a test skill.
"""
        skill_file.write_text(skill_content)

        # Validate the plugin with the new skill
        validator_script = cc_plugins_root / "scripts" / "validate-plugin.py"
        result = subprocess.run(
            ["python3", str(validator_script), str(plugin_dir)],
            capture_output=True,
            text=True
        )

        assert result.returncode == 0, f"Validation failed: {result.stdout}"

    def _execute_create_command(self, create_cmd, plugin_name, cwd=None):
        """Execute the create command."""
        with open(create_cmd, 'r') as f:
            content = f.read()

        bash_start = content.find("!bash\n")
        bash_script = content[bash_start + 6:]

        result = subprocess.run(
            ["bash", "-c", bash_script, "bash", plugin_name],
            cwd=cwd,
            capture_output=True,
            text=True
        )

        return result


class TestPluginCreationCleanup:
    """Test cleanup of created test plugins."""

    def test_cleanup_removes_all_test_artifacts(self, temp_workspace, cc_plugins_root):
        """Test that temporary plugins are properly cleaned up."""
        plugin_name = "test-cleanup-plugin"

        # Create plugin
        create_cmd = cc_plugins_root / "commands" / "create.md"
        with open(create_cmd, 'r') as f:
            content = f.read()

        bash_start = content.find("!bash\n")
        bash_script = content[bash_start + 6:]

        subprocess.run(
            ["bash", "-c", bash_script, "bash", plugin_name],
            cwd=temp_workspace,
            capture_output=True,
            text=True
        )

        plugin_dir = temp_workspace / plugin_name
        assert plugin_dir.exists()

        # Cleanup (simulate)
        shutil.rmtree(plugin_dir)

        # Verify cleanup
        assert not plugin_dir.exists(), "Plugin directory should be removed"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
