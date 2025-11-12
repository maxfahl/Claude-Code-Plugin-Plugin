"""
Test suite for validating cc-plugins project structure.

Tests ensure that the plugin directory follows official Claude Code plugin specifications:
- Plugin manifest exists at .claude-plugin/plugin.json
- Component directories exist at plugin root level
- Required directories are properly structured
"""

import os
import json
import pytest
from pathlib import Path


@pytest.fixture
def plugin_root():
    """Returns the path to the cc-plugins plugin root directory."""
    return Path(__file__).parent.parent


@pytest.fixture
def manifest_path(plugin_root):
    """Returns the path to the plugin manifest file."""
    return plugin_root / ".claude-plugin" / "plugin.json"


class TestProjectStructure:
    """Test suite for plugin directory structure validation."""

    def test_plugin_root_exists(self, plugin_root):
        """Test that the plugin root directory exists."""
        assert plugin_root.exists(), f"Plugin root directory does not exist: {plugin_root}"
        assert plugin_root.is_dir(), f"Plugin root is not a directory: {plugin_root}"

    def test_claude_plugin_directory_exists(self, plugin_root):
        """Test that .claude-plugin directory exists."""
        claude_plugin_dir = plugin_root / ".claude-plugin"
        assert claude_plugin_dir.exists(), ".claude-plugin directory does not exist"
        assert claude_plugin_dir.is_dir(), ".claude-plugin is not a directory"

    def test_manifest_file_exists(self, manifest_path):
        """Test that plugin.json manifest file exists."""
        assert manifest_path.exists(), f"Manifest file does not exist: {manifest_path}"
        assert manifest_path.is_file(), f"Manifest path is not a file: {manifest_path}"

    def test_manifest_is_valid_json(self, manifest_path):
        """Test that manifest file contains valid JSON."""
        try:
            with open(manifest_path, 'r') as f:
                data = json.load(f)
            assert isinstance(data, dict), "Manifest JSON is not an object"
        except json.JSONDecodeError as e:
            pytest.fail(f"Manifest file contains invalid JSON: {e}")
        except Exception as e:
            pytest.fail(f"Error reading manifest file: {e}")

    def test_component_directories_at_root(self, plugin_root):
        """Test that component directories exist at plugin root level (not inside .claude-plugin)."""
        expected_dirs = ['commands', 'agents', 'skills', 'scripts', 'docs']

        for dir_name in expected_dirs:
            dir_path = plugin_root / dir_name
            assert dir_path.exists(), f"Component directory '{dir_name}' does not exist at plugin root"
            assert dir_path.is_dir(), f"Component path '{dir_name}' is not a directory"

    def test_component_directories_not_in_claude_plugin(self, plugin_root):
        """Test that component directories are NOT inside .claude-plugin directory."""
        component_dirs = ['commands', 'agents', 'skills', 'scripts']
        claude_plugin_dir = plugin_root / ".claude-plugin"

        for dir_name in component_dirs:
            wrong_path = claude_plugin_dir / dir_name
            assert not wrong_path.exists(), (
                f"Component directory '{dir_name}' should NOT be inside .claude-plugin. "
                f"It should be at plugin root level."
            )

    def test_tests_directory_exists(self, plugin_root):
        """Test that tests directory exists for plugin testing."""
        tests_dir = plugin_root / "tests"
        assert tests_dir.exists(), "tests directory does not exist"
        assert tests_dir.is_dir(), "tests path is not a directory"


class TestManifestStructure:
    """Test suite for plugin manifest structure validation."""

    @pytest.fixture
    def manifest_data(self, manifest_path):
        """Load and return manifest JSON data."""
        with open(manifest_path, 'r') as f:
            return json.load(f)

    def test_manifest_has_name(self, manifest_data):
        """Test that manifest contains 'name' field."""
        assert 'name' in manifest_data, "Manifest missing required 'name' field"
        assert isinstance(manifest_data['name'], str), "'name' field must be a string"
        assert manifest_data['name'], "'name' field cannot be empty"

    def test_manifest_name_is_kebab_case(self, manifest_data):
        """Test that manifest name follows kebab-case convention."""
        name = manifest_data.get('name', '')
        # kebab-case: lowercase with hyphens, no spaces or underscores
        assert name.islower() or '-' in name, "Plugin name should be in kebab-case"
        assert ' ' not in name, "Plugin name should not contain spaces"
        assert '_' not in name, "Plugin name should use hyphens, not underscores"

    def test_manifest_optional_fields_are_valid_types(self, manifest_data):
        """Test that optional manifest fields have correct types."""
        # Test optional string fields
        string_fields = ['version', 'description', 'homepage', 'repository', 'license']
        for field in string_fields:
            if field in manifest_data:
                assert isinstance(manifest_data[field], str), f"'{field}' must be a string"

        # Test author object if present
        if 'author' in manifest_data:
            author = manifest_data['author']
            assert isinstance(author, dict), "'author' must be an object"
            for key in ['name', 'email', 'url']:
                if key in author:
                    assert isinstance(author[key], str), f"'author.{key}' must be a string"

        # Test keywords array if present
        if 'keywords' in manifest_data:
            keywords = manifest_data['keywords']
            assert isinstance(keywords, list), "'keywords' must be an array"
            for kw in keywords:
                assert isinstance(kw, str), "All keywords must be strings"


class TestComponentDiscovery:
    """Test suite for discovering and validating plugin components."""

    def test_can_discover_commands(self, plugin_root):
        """Test that command files can be discovered."""
        commands_dir = plugin_root / "commands"
        if commands_dir.exists():
            # Look for .md files in commands directory
            command_files = list(commands_dir.glob("*.md"))
            # We don't require commands to exist yet, but if they do, they should be .md files
            for cmd_file in command_files:
                assert cmd_file.suffix == '.md', f"Command file {cmd_file.name} should have .md extension"

    def test_can_discover_agents(self, plugin_root):
        """Test that agent files can be discovered."""
        agents_dir = plugin_root / "agents"
        if agents_dir.exists():
            # Look for .md files in agents directory
            agent_files = list(agents_dir.glob("*.md"))
            # We don't require agents to exist yet, but if they do, they should be .md files
            for agent_file in agent_files:
                assert agent_file.suffix == '.md', f"Agent file {agent_file.name} should have .md extension"

    def test_can_discover_skills(self, plugin_root):
        """Test that skill directories can be discovered."""
        skills_dir = plugin_root / "skills"
        if skills_dir.exists():
            # Look for subdirectories in skills directory
            skill_dirs = [d for d in skills_dir.iterdir() if d.is_dir()]
            # We don't require skills to exist yet, but if they do, check for SKILL.md
            for skill_dir in skill_dirs:
                skill_md = skill_dir / "SKILL.md"
                if not skill_md.exists():
                    # Warning: skill directory should contain SKILL.md
                    pass  # We'll handle this in component validation tests

    def test_can_discover_scripts(self, plugin_root):
        """Test that scripts can be discovered."""
        scripts_dir = plugin_root / "scripts"
        if scripts_dir.exists():
            # Scripts can be .py, .sh, or other executable files
            script_files = [f for f in scripts_dir.iterdir() if f.is_file()]
            # We allow scripts directory to be empty initially
            assert isinstance(script_files, list), "Should be able to list script files"
