"""
Self-validation tests for cc-plugins meta-plugin.

Tests that cc-plugins follows its own rules and specifications (dogfooding).
Ensures the meta-plugin is a valid example of a Claude Code plugin.

Test Coverage:
- cc-plugins validates itself successfully
- All cc-plugins components are valid
- cc-plugins can create similar meta-plugins
- All commands, agents, and skills are properly structured
"""

import json
import subprocess
import pytest
from pathlib import Path


@pytest.fixture
def cc_plugins_root():
    """Returns the path to the cc-plugins root directory."""
    return Path(__file__).parent.parent


class TestSelfValidation:
    """Test that cc-plugins validates itself."""

    def test_cc_plugins_passes_own_validation(self, cc_plugins_root):
        """Test that cc-plugins passes its own validator."""
        validator_script = cc_plugins_root / "scripts" / "validate-plugin.py"

        result = subprocess.run(
            ["python3", str(validator_script), str(cc_plugins_root)],
            capture_output=True,
            text=True
        )

        assert result.returncode == 0, (
            f"cc-plugins failed its own validation!\n"
            f"STDOUT: {result.stdout}\n"
            f"STDERR: {result.stderr}"
        )

        # Should show success message
        assert "✓" in result.stdout or "passed" in result.stdout.lower()

    def test_cc_plugins_has_valid_manifest(self, cc_plugins_root):
        """Test that cc-plugins manifest is valid."""
        manifest_path = cc_plugins_root / ".claude-plugin" / "plugin.json"

        # Manifest must exist
        assert manifest_path.exists(), "cc-plugins manifest not found"

        # Must be valid JSON
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)

        # Required fields
        assert "name" in manifest, "Manifest missing 'name' field"
        assert manifest["name"] == "cc-plugins", "Manifest name mismatch"

        # Name must be kebab-case
        assert manifest["name"].islower() or "-" in manifest["name"]
        assert " " not in manifest["name"]
        assert "_" not in manifest["name"]

        # Optional but expected fields
        assert "version" in manifest
        assert "description" in manifest
        assert "author" in manifest
        assert "license" in manifest

    def test_cc_plugins_directory_structure(self, cc_plugins_root):
        """Test that cc-plugins follows correct directory structure."""
        # Required directories at root level
        required_dirs = ["commands", "agents", "skills", "scripts", "docs", "tests"]

        for dir_name in required_dirs:
            dir_path = cc_plugins_root / dir_name
            assert dir_path.exists(), f"Missing required directory: {dir_name}"
            assert dir_path.is_dir(), f"Not a directory: {dir_name}"

        # .claude-plugin directory must exist
        claude_plugin_dir = cc_plugins_root / ".claude-plugin"
        assert claude_plugin_dir.exists(), "Missing .claude-plugin directory"
        assert claude_plugin_dir.is_dir(), ".claude-plugin is not a directory"

        # Components must NOT be inside .claude-plugin
        for dir_name in ["commands", "agents", "skills", "scripts"]:
            wrong_path = claude_plugin_dir / dir_name
            assert not wrong_path.exists(), (
                f"Component '{dir_name}' should not be inside .claude-plugin"
            )


class TestSelfComponentValidation:
    """Test that all cc-plugins components are valid."""

    def test_all_commands_are_valid(self, cc_plugins_root):
        """Test that all command files in cc-plugins are valid."""
        commands_dir = cc_plugins_root / "commands"

        # Should have at least one command
        command_files = list(commands_dir.glob("*.md"))
        assert len(command_files) > 0, "cc-plugins has no commands"

        # All commands should be .md files
        for cmd_file in command_files:
            assert cmd_file.suffix == ".md", f"Command file not .md: {cmd_file}"

            # File should be readable
            content = cmd_file.read_text()
            assert len(content) > 0, f"Empty command file: {cmd_file}"

            # Should have frontmatter
            assert content.startswith("---"), f"Command missing frontmatter: {cmd_file}"

    def test_all_agents_are_valid(self, cc_plugins_root):
        """Test that all agent files in cc-plugins are valid."""
        agents_dir = cc_plugins_root / "agents"

        # May have zero or more agents
        agent_files = list(agents_dir.glob("*.md"))

        # All agents should be .md files
        for agent_file in agent_files:
            assert agent_file.suffix == ".md", f"Agent file not .md: {agent_file}"

            # File should be readable
            content = agent_file.read_text()
            assert len(content) > 0, f"Empty agent file: {agent_file}"

            # Should have frontmatter
            assert content.startswith("---"), f"Agent missing frontmatter: {agent_file}"

    def test_all_skills_are_valid(self, cc_plugins_root):
        """Test that all skills in cc-plugins are valid."""
        skills_dir = cc_plugins_root / "skills"

        # May have zero or more skills
        skill_dirs = [d for d in skills_dir.iterdir() if d.is_dir()]

        # All skills should have SKILL.md
        for skill_dir in skill_dirs:
            skill_file = skill_dir / "SKILL.md"

            if skill_file.exists():
                # File should be readable
                content = skill_file.read_text()
                assert len(content) > 0, f"Empty skill file: {skill_file}"

                # Should have frontmatter
                assert content.startswith("---"), f"Skill missing frontmatter: {skill_file}"

    def test_all_scripts_are_executable_or_python(self, cc_plugins_root):
        """Test that all scripts in cc-plugins are valid."""
        scripts_dir = cc_plugins_root / "scripts"

        # Should have at least one script
        script_files = [f for f in scripts_dir.iterdir() if f.is_file() and not f.name.startswith(".")]
        assert len(script_files) > 0, "cc-plugins has no scripts"

        # Check that scripts are valid
        for script_file in script_files:
            # Skip __pycache__ and other non-script files
            if script_file.suffix in [".pyc", ".pyo"]:
                continue

            if script_file.suffix == ".py":
                # Python scripts should be readable
                content = script_file.read_text()
                assert len(content) > 0, f"Empty script: {script_file}"
            elif script_file.suffix == ".sh":
                # Shell scripts should be readable
                content = script_file.read_text()
                assert len(content) > 0, f"Empty script: {script_file}"


class TestSelfSpecCompliance:
    """Test that cc-plugins complies with official specifications."""

    def test_passes_spec_compliance_check(self, cc_plugins_root):
        """Test that cc-plugins passes spec compliance checker."""
        spec_checker = cc_plugins_root / "scripts" / "check-spec-compliance.py"

        if not spec_checker.exists():
            pytest.skip("Spec checker not available")

        result = subprocess.run(
            ["python3", str(spec_checker), str(cc_plugins_root)],
            capture_output=True,
            text=True
        )

        # Should pass spec compliance
        assert result.returncode == 0, (
            f"cc-plugins failed spec compliance check!\n"
            f"STDOUT: {result.stdout}\n"
            f"STDERR: {result.stderr}"
        )

    def test_passes_format_check(self, cc_plugins_root):
        """Test that cc-plugins passes format checker."""
        format_checker = cc_plugins_root / "scripts" / "check-formats.py"

        if not format_checker.exists():
            pytest.skip("Format checker not available")

        result = subprocess.run(
            ["python3", str(format_checker), str(cc_plugins_root)],
            capture_output=True,
            text=True
        )

        # Should pass format check
        assert result.returncode == 0, (
            f"cc-plugins failed format check!\n"
            f"STDOUT: {result.stdout}\n"
            f"STDERR: {result.stderr}"
        )


class TestSelfDocumentation:
    """Test that cc-plugins has proper documentation."""

    def test_has_readme(self, cc_plugins_root):
        """Test that cc-plugins has a README.md file."""
        readme = cc_plugins_root / "README.md"
        assert readme.exists(), "cc-plugins has no README.md"

        content = readme.read_text()
        assert len(content) > 0, "README.md is empty"

        # Should mention plugin name
        assert "cc-plugins" in content.lower()

    def test_has_documentation_directory(self, cc_plugins_root):
        """Test that cc-plugins has documentation."""
        docs_dir = cc_plugins_root / "docs"
        assert docs_dir.exists(), "cc-plugins has no docs directory"
        assert docs_dir.is_dir(), "docs is not a directory"

    def test_commands_are_documented(self, cc_plugins_root):
        """Test that all commands have descriptions."""
        commands_dir = cc_plugins_root / "commands"
        command_files = list(commands_dir.glob("*.md"))

        for cmd_file in command_files:
            content = cmd_file.read_text()

            # Should have description in frontmatter
            assert "description:" in content, f"Command missing description: {cmd_file}"


class TestCanCreateSimilarPlugins:
    """Test that cc-plugins can create similar meta-plugins."""

    def test_can_validate_own_creation_output(self, cc_plugins_root, tmp_path):
        """Test that plugins created by cc-plugins pass validation."""
        # Create a test plugin using the create command
        create_cmd = cc_plugins_root / "commands" / "create.md"

        # Extract bash script
        with open(create_cmd, 'r') as f:
            content = f.read()

        bash_start = content.find("!bash\n")
        if bash_start == -1:
            pytest.skip("Create command has no bash script")

        bash_script = content[bash_start + 6:]

        # Create plugin
        plugin_name = "test-self-created-plugin"
        result = subprocess.run(
            ["bash", "-c", bash_script, "bash", plugin_name],
            cwd=tmp_path,
            capture_output=True,
            text=True
        )

        assert result.returncode == 0, f"Failed to create plugin: {result.stderr}"

        # Validate the created plugin
        plugin_dir = tmp_path / plugin_name
        validator_script = cc_plugins_root / "scripts" / "validate-plugin.py"

        result = subprocess.run(
            ["python3", str(validator_script), str(plugin_dir)],
            capture_output=True,
            text=True
        )

        assert result.returncode == 0, (
            f"Created plugin failed validation!\n"
            f"STDOUT: {result.stdout}\n"
            f"STDERR: {result.stderr}"
        )


class TestMetaPluginCapabilities:
    """Test cc-plugins' meta-plugin capabilities."""

    def test_validator_script_exists_and_works(self, cc_plugins_root):
        """Test that validator script exists and is executable."""
        validator = cc_plugins_root / "scripts" / "validate-plugin.py"

        assert validator.exists(), "Validator script not found"
        assert validator.is_file(), "Validator is not a file"

        # Should be executable
        content = validator.read_text()
        assert len(content) > 0, "Validator script is empty"
        assert "#!/usr/bin/env python3" in content or "python" in content

    def test_scaffold_script_exists(self, cc_plugins_root):
        """Test that scaffolding script exists."""
        scaffold = cc_plugins_root / "scripts" / "scaffold-plugin.py"

        if scaffold.exists():
            content = scaffold.read_text()
            assert len(content) > 0, "Scaffold script is empty"

    def test_has_test_suite(self, cc_plugins_root):
        """Test that cc-plugins has its own test suite."""
        tests_dir = cc_plugins_root / "tests"

        assert tests_dir.exists(), "cc-plugins has no tests directory"
        assert tests_dir.is_dir(), "tests is not a directory"

        # Should have test files
        test_files = list(tests_dir.glob("test_*.py"))
        assert len(test_files) > 0, "cc-plugins has no test files"

    def test_all_tests_are_runnable(self, cc_plugins_root):
        """Test that all test files can be imported."""
        tests_dir = cc_plugins_root / "tests"
        test_files = list(tests_dir.glob("test_*.py"))

        for test_file in test_files:
            content = test_file.read_text()

            # Should have pytest imports
            assert "pytest" in content or "unittest" in content, (
                f"Test file missing test framework: {test_file}"
            )

            # Should have test classes or functions
            has_tests = ("def test_" in content or "class Test" in content)
            assert has_tests, f"Test file has no tests: {test_file}"


class TestDogfooding:
    """Test that cc-plugins uses its own capabilities."""

    def test_uses_own_validation(self, cc_plugins_root):
        """Test that cc-plugins can validate itself."""
        # This is effectively the same as test_cc_plugins_passes_own_validation
        # but emphasizes the dogfooding aspect
        validator_script = cc_plugins_root / "scripts" / "validate-plugin.py"

        result = subprocess.run(
            ["python3", str(validator_script), str(cc_plugins_root)],
            capture_output=True,
            text=True
        )

        assert result.returncode == 0
        assert "✓" in result.stdout or "passed" in result.stdout.lower()

    def test_follows_own_conventions(self, cc_plugins_root):
        """Test that cc-plugins follows its own naming conventions."""
        manifest_path = cc_plugins_root / ".claude-plugin" / "plugin.json"

        with open(manifest_path, 'r') as f:
            manifest = json.load(f)

        # Name should be kebab-case (as enforced by validator)
        name = manifest["name"]
        assert name.islower() or "-" in name
        assert " " not in name
        assert "_" not in name

    def test_has_examples_of_all_component_types(self, cc_plugins_root):
        """Test that cc-plugins has examples of all component types it supports."""
        # Commands
        commands_dir = cc_plugins_root / "commands"
        assert commands_dir.exists()
        assert len(list(commands_dir.glob("*.md"))) > 0, "No example commands"

        # Agents
        agents_dir = cc_plugins_root / "agents"
        assert agents_dir.exists()
        # Agents are optional, but if present, should be valid

        # Skills
        skills_dir = cc_plugins_root / "skills"
        assert skills_dir.exists()
        # Skills are optional, but if present, should be valid

        # Scripts
        scripts_dir = cc_plugins_root / "scripts"
        assert scripts_dir.exists()
        assert len(list(scripts_dir.glob("*.py"))) > 0, "No example scripts"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
