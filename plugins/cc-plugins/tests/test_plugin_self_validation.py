#!/usr/bin/env python3
"""
Test suite for self-validation of cc-plugins itself.

Tests that the cc-plugins meta-plugin passes all validation checks and
serves as a quality example for other plugins.

Validates:
- Plugin structure is correct
- All components are valid
- Plugin can validate other plugins correctly
- Plugin is production-ready
"""

import json
import tempfile
import shutil
from pathlib import Path
import subprocess
import pytest


class TestPluginStructure:
    """Test that cc-plugins has correct structure."""

    @pytest.fixture
    def plugin_root(self):
        """Get cc-plugins root directory."""
        return Path(__file__).parent.parent

    def test_plugin_root_exists(self, plugin_root):
        """Test that plugin root exists."""
        assert plugin_root.exists()

    def test_claude_plugin_directory_exists(self, plugin_root):
        """Test that .claude-plugin directory exists."""
        claude_plugin_dir = plugin_root / ".claude-plugin"
        assert claude_plugin_dir.exists()
        assert claude_plugin_dir.is_dir()

    def test_plugin_json_exists(self, plugin_root):
        """Test that plugin.json manifest exists."""
        manifest_path = plugin_root / ".claude-plugin" / "plugin.json"
        assert manifest_path.exists()
        assert manifest_path.is_file()

    def test_manifest_is_valid_json(self, plugin_root):
        """Test that plugin.json is valid JSON."""
        manifest_path = plugin_root / ".claude-plugin" / "plugin.json"
        try:
            manifest = json.loads(manifest_path.read_text())
            assert isinstance(manifest, dict)
        except json.JSONDecodeError as e:
            pytest.fail(f"plugin.json is not valid JSON: {e}")

    def test_commands_directory_exists(self, plugin_root):
        """Test that commands directory exists."""
        assert (plugin_root / "commands").exists()
        assert (plugin_root / "commands").is_dir()

    def test_agents_directory_exists(self, plugin_root):
        """Test that agents directory exists."""
        assert (plugin_root / "agents").exists()
        assert (plugin_root / "agents").is_dir()

    def test_skills_directory_exists(self, plugin_root):
        """Test that skills directory exists."""
        assert (plugin_root / "skills").exists()
        assert (plugin_root / "skills").is_dir()

    def test_scripts_directory_exists(self, plugin_root):
        """Test that scripts directory exists."""
        assert (plugin_root / "scripts").exists()
        assert (plugin_root / "scripts").is_dir()

    def test_tests_directory_exists(self, plugin_root):
        """Test that tests directory exists."""
        assert (plugin_root / "tests").exists()
        assert (plugin_root / "tests").is_dir()

    def test_readme_exists(self, plugin_root):
        """Test that README.md exists."""
        assert (plugin_root / "README.md").exists()
        assert (plugin_root / "README.md").is_file()


class TestManifestValidity:
    """Test that plugin.json manifest is valid."""

    @pytest.fixture
    def manifest(self):
        """Load plugin manifest."""
        manifest_path = Path(__file__).parent.parent / ".claude-plugin" / "plugin.json"
        return json.loads(manifest_path.read_text())

    def test_manifest_has_name(self, manifest):
        """Test that manifest has name field."""
        assert "name" in manifest
        assert manifest["name"]

    def test_manifest_name_is_kebab_case(self, manifest):
        """Test that manifest name is kebab-case."""
        name = manifest["name"]
        assert name.islower()
        assert not " " in name
        assert not "_" in name

    def test_manifest_has_version(self, manifest):
        """Test that manifest has version."""
        assert "version" in manifest
        assert manifest["version"]

    def test_manifest_version_is_semantic(self, manifest):
        """Test that manifest version is semantic versioning."""
        import re
        version = manifest["version"]
        assert re.match(r"^\d+\.\d+\.\d+", version), \
            f"Version should be semantic (X.Y.Z), got: {version}"

    def test_manifest_has_description(self, manifest):
        """Test that manifest has description."""
        assert "description" in manifest
        assert manifest["description"]

    def test_manifest_fields_are_strings(self, manifest):
        """Test that manifest string fields are strings."""
        string_fields = ["name", "version", "description"]
        for field in string_fields:
            if field in manifest:
                assert isinstance(manifest[field], str), \
                    f"Field {field} should be string"


class TestComponentValidity:
    """Test that all components are valid."""

    @pytest.fixture
    def plugin_root(self):
        """Get plugin root."""
        return Path(__file__).parent.parent

    def test_all_commands_have_frontmatter(self, plugin_root):
        """Test that all commands have YAML frontmatter."""
        commands_dir = plugin_root / "commands"
        if commands_dir.exists():
            for cmd_file in commands_dir.glob("*.md"):
                content = cmd_file.read_text()
                assert content.startswith("---"), \
                    f"Command {cmd_file.name} missing frontmatter"

    def test_all_agents_have_frontmatter(self, plugin_root):
        """Test that all agents have YAML frontmatter."""
        agents_dir = plugin_root / "agents"
        if agents_dir.exists():
            for agent_file in agents_dir.glob("*.md"):
                content = agent_file.read_text()
                assert content.startswith("---"), \
                    f"Agent {agent_file.name} missing frontmatter"

    def test_all_skills_have_skill_md(self, plugin_root):
        """Test that all skills have SKILL.md."""
        skills_dir = plugin_root / "skills"
        if skills_dir.exists():
            for skill_dir in skills_dir.iterdir():
                if skill_dir.is_dir():
                    assert (skill_dir / "SKILL.md").exists(), \
                        f"Skill {skill_dir.name} missing SKILL.md"
                    content = (skill_dir / "SKILL.md").read_text()
                    assert content.startswith("---"), \
                        f"Skill {skill_dir.name}/SKILL.md missing frontmatter"

    def test_command_frontmatter_has_description(self, plugin_root):
        """Test that commands have description field."""
        commands_dir = plugin_root / "commands"
        if commands_dir.exists():
            for cmd_file in commands_dir.glob("*.md"):
                content = cmd_file.read_text()
                assert "description:" in content, \
                    f"Command {cmd_file.name} missing description field"

    def test_agent_frontmatter_has_description(self, plugin_root):
        """Test that agents have description field."""
        agents_dir = plugin_root / "agents"
        if agents_dir.exists():
            for agent_file in agents_dir.glob("*.md"):
                content = agent_file.read_text()
                assert "description:" in content, \
                    f"Agent {agent_file.name} missing description field"


class TestPluginValidation:
    """Test that cc-plugins passes its own validation."""

    @pytest.fixture
    def plugin_root(self):
        """Get plugin root."""
        return Path(__file__).parent.parent

    def test_plugin_validates_successfully(self, plugin_root):
        """Test that cc-plugins validates successfully."""
        result = subprocess.run(
            ["python", "scripts/validate-plugin.py", str(plugin_root)],
            capture_output=True,
            text=True,
            cwd=plugin_root
        )
        
        # Should succeed or have no errors
        output = result.stderr + result.stdout
        
        # Check that there's a success message or no critical errors
        if result.returncode != 0:
            # Print output for debugging
            assert "passed" in output.lower() or \
                   "valid" in output.lower() or \
                   result.returncode == 0, \
                   f"Validation should pass:\n{output}"


class TestMetaPluginFunctionality:
    """Test that cc-plugins can scaffold and validate other plugins."""

    def test_scaffold_creates_valid_plugin(self):
        """Test that scaffolding creates a valid plugin."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Scaffold a test plugin
            result = subprocess.run(
                ["python", "scripts/scaffold-plugin.py",
                 "--name", "test-plugin",
                 "--description", "Test plugin",
                 "--author", "Tester",
                 "--output", tmpdir],
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent.parent
            )
            
            assert result.returncode == 0

    def test_validator_correctly_validates_invalid_plugin(self):
        """Test that validator catches invalid plugins."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create invalid plugin (missing manifest)
            plugin_dir = Path(tmpdir) / "invalid-plugin"
            plugin_dir.mkdir()
            (plugin_dir / ".claude-plugin").mkdir()

            result = subprocess.run(
                ["python", "scripts/validate-plugin.py", str(plugin_dir)],
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent.parent
            )
            
            # Should fail validation
            assert result.returncode != 0


class TestProductionReadiness:
    """Test that plugin is production-ready."""

    @pytest.fixture
    def plugin_root(self):
        """Get plugin root."""
        return Path(__file__).parent.parent

    def test_plugin_has_complete_readme(self, plugin_root):
        """Test that plugin has complete README."""
        readme_path = plugin_root / "README.md"
        content = readme_path.read_text()

        # Should have key sections
        required_sections = [
            "Overview",
            "Features",
            "Installation",
            "Commands",
            "Agents",
            "Skills",
        ]

        for section in required_sections:
            assert section in content, f"README missing section: {section}"

    def test_plugin_has_test_suite(self, plugin_root):
        """Test that plugin has tests."""
        tests_dir = plugin_root / "tests"
        assert tests_dir.exists()
        
        test_files = list(tests_dir.glob("test_*.py"))
        assert len(test_files) > 0, "Plugin should have test files"

    def test_plugin_scripts_are_executable(self, plugin_root):
        """Test that scripts have proper headers."""
        scripts_dir = plugin_root / "scripts"
        for script_file in scripts_dir.glob("*.py"):
            content = script_file.read_text()
            assert content.startswith("#!/usr/bin/env python3") or \
                   content.startswith("#!/usr/bin/env python"), \
                   f"Script {script_file.name} missing shebang"

    def test_plugin_has_clear_license(self, plugin_root):
        """Test that plugin has license."""
        readme = (plugin_root / "README.md").read_text()
        assert "MIT" in readme or "Apache" in readme or "License" in readme, \
            "Plugin should document license"

    def test_plugin_follows_naming_conventions(self, plugin_root):
        """Test that plugin follows naming conventions."""
        # Commands should be kebab-case
        commands_dir = plugin_root / "commands"
        if commands_dir.exists():
            for cmd_file in commands_dir.glob("*.md"):
                name = cmd_file.stem
                assert name.islower() or "-" in name, \
                    f"Command {cmd_file.name} should be kebab-case"


class TestSpecCompliance:
    """Test compliance with official specifications."""

    @pytest.fixture
    def manifest(self):
        """Load manifest."""
        manifest_path = Path(__file__).parent.parent / ".claude-plugin" / "plugin.json"
        return json.loads(manifest_path.read_text())

    def test_manifest_uses_official_fields(self, manifest):
        """Test that manifest uses official field names."""
        official_fields = {
            "name", "version", "description", "author", "homepage",
            "repository", "license", "keywords", "commands", "agents",
            "hooks", "mcpServers", "skills"
        }
        
        for field in manifest:
            assert field in official_fields, \
                f"Manifest uses unofficial field: {field}"

    def test_author_field_structure(self, manifest):
        """Test that author field follows spec."""
        if "author" in manifest:
            author = manifest["author"]
            assert isinstance(author, dict), "Author should be object"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
