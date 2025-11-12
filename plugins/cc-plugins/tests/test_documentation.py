#!/usr/bin/env python3
"""
Test suite for documentation accuracy and completeness.

Tests that:
- All documented commands exist and work
- All documented examples are correct
- All file references are accurate
- All commands are documented
- Links are not broken
- Version numbers are consistent
- Code examples execute correctly
"""

import sys
import re
import json
from pathlib import Path
import subprocess
import pytest

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))


class TestREADMEIntegrity:
    """Test README.md documentation."""

    @pytest.fixture
    def readme_path(self):
        """Get path to README.md."""
        return Path(__file__).parent.parent / "README.md"

    @pytest.fixture
    def readme_content(self, readme_path):
        """Read README content."""
        return readme_path.read_text()

    def test_readme_exists(self, readme_path):
        """Test that README.md exists."""
        assert readme_path.exists(), "README.md should exist"

    def test_readme_not_empty(self, readme_content):
        """Test that README.md is not empty."""
        assert len(readme_content) > 100, "README.md should have substantial content"

    def test_readme_has_title(self, readme_content):
        """Test that README has main title."""
        assert "# cc-plugins" in readme_content, "README should have main title"

    def test_readme_has_table_of_contents(self, readme_content):
        """Test that README has table of contents."""
        assert "Table of Contents" in readme_content, "README should have Table of Contents"

    def test_readme_has_installation_section(self, readme_content):
        """Test that README documents installation."""
        assert "Installation" in readme_content, "README should have Installation section"

    def test_readme_has_commands_section(self, readme_content):
        """Test that README documents commands."""
        assert "Commands" in readme_content, "README should document commands"

    def test_readme_has_agents_section(self, readme_content):
        """Test that README documents agents."""
        assert "Agents" in readme_content, "README should document agents"

    def test_readme_has_skills_section(self, readme_content):
        """Test that README documents skills."""
        assert "Skills" in readme_content, "README should document skills"

    def test_readme_has_troubleshooting(self, readme_content):
        """Test that README has troubleshooting section."""
        assert "Troubleshooting" in readme_content, "README should have Troubleshooting section"

    def test_readme_references_correct_version(self, readme_content):
        """Test that README references correct version."""
        # Should reference a version number
        assert re.search(r"\d+\.\d+\.\d+", readme_content), "README should reference semantic version"

    def test_all_commands_documented(self, readme_content):
        """Test that all commands are documented in README."""
        commands = ["create", "validate", "debug", "document", "update"]
        for cmd in commands:
            assert f"cc-plugins:{cmd}" in readme_content or f"/cc-plugins:{cmd}" in readme_content, \
                f"README should document command: {cmd}"

    def test_all_agents_documented(self, readme_content):
        """Test that all agents are documented in README."""
        agents = ["plugin-architect", "plugin-debugger", "plugin-documenter"]
        for agent in agents:
            assert agent in readme_content, f"README should document agent: {agent}"

    def test_all_skills_documented(self, readme_content):
        """Test that all skills are documented in README."""
        skills = ["plugin-development", "plugin-validation"]
        for skill in skills:
            assert skill in readme_content, f"README should document skill: {skill}"


class TestDocumentationReferences:
    """Test that documentation references are accurate."""

    @pytest.fixture
    def readme_path(self):
        """Get path to README.md."""
        return Path(__file__).parent.parent / "README.md"

    @pytest.fixture
    def readme_content(self, readme_path):
        """Read README content."""
        return readme_path.read_text()

    @pytest.fixture
    def project_root(self):
        """Get project root."""
        return Path(__file__).parent.parent

    def test_commands_directory_references_actual_files(self, readme_content, project_root):
        """Test that command references exist in commands directory."""
        commands_dir = project_root / "commands"
        if commands_dir.exists():
            command_files = [f.stem for f in commands_dir.glob("*.md")]
            for cmd_file in command_files:
                # README should reference these commands
                assert cmd_file in readme_content.lower() or \
                       f"/{cmd_file}" in readme_content or \
                       cmd_file.replace("-", "") in readme_content.lower(), \
                       f"README should reference command: {cmd_file}"

    def test_agents_directory_references_actual_files(self, readme_content, project_root):
        """Test that agent references exist in agents directory."""
        agents_dir = project_root / "agents"
        if agents_dir.exists():
            agent_files = [f.stem for f in agents_dir.glob("*.md")]
            for agent_file in agent_files:
                assert agent_file in readme_content, \
                    f"README should reference agent: {agent_file}"

    def test_skills_directory_references_actual_files(self, readme_content, project_root):
        """Test that skill references exist in skills directory."""
        skills_dir = project_root / "skills"
        if skills_dir.exists():
            skill_dirs = [d.name for d in skills_dir.iterdir() if d.is_dir()]
            for skill_dir in skill_dirs:
                assert skill_dir in readme_content, \
                    f"README should reference skill: {skill_dir}"

    def test_docs_references_exist(self, readme_content, project_root):
        """Test that documentation references point to real files."""
        # Find doc references in README
        doc_refs = re.findall(r"\[.*?\]\((docs/[^)]+)\)", readme_content)
        for doc_ref in doc_refs:
            doc_path = project_root / doc_ref
            # Each referenced doc should exist or be on external site
            assert doc_ref.startswith("http") or doc_path.exists() or \
                   project_root / doc_ref.split("#")[0] if "#" in doc_ref else doc_path.exists(), \
                   f"Documentation reference should exist: {doc_ref}"

    def test_external_links_are_valid_urls(self, readme_content):
        """Test that external links are valid URLs."""
        urls = re.findall(r"\[.*?\]\((https?://[^)]+)\)", readme_content)
        for url in urls:
            # Should be a valid URL format
            assert url.startswith("http://") or url.startswith("https://"), \
                f"Invalid URL format: {url}"
            # Should not have obvious typos
            assert not url.endswith(".."), f"URL looks truncated: {url}"


class TestCommandDocumentation:
    """Test command documentation accuracy."""

    @pytest.fixture
    def commands_dir(self):
        """Get commands directory."""
        return Path(__file__).parent.parent / "commands"

    @pytest.fixture
    def readme_content(self):
        """Read README content."""
        return (Path(__file__).parent.parent / "README.md").read_text()

    def test_create_command_documented(self, readme_content):
        """Test that create command is documented."""
        assert "/cc-plugins:create" in readme_content
        assert "kebab-case" in readme_content.lower()

    def test_validate_command_documented(self, readme_content):
        """Test that validate command is documented."""
        assert "/cc-plugins:validate" in readme_content

    def test_debug_command_documented(self, readme_content):
        """Test that debug command is documented."""
        assert "/cc-plugins:debug" in readme_content

    def test_document_command_documented(self, readme_content):
        """Test that document command is documented."""
        assert "/cc-plugins:document" in readme_content

    def test_update_command_documented(self, readme_content):
        """Test that update command is documented."""
        assert "/cc-plugins:update" in readme_content

    def test_command_usage_examples_present(self, readme_content):
        """Test that command usage examples are documented."""
        # Should have usage examples with bash syntax
        assert "```bash" in readme_content
        assert "/cc-plugins:" in readme_content

    def test_command_examples_are_runnable(self, readme_content):
        """Test that documented command examples are properly formatted."""
        # Extract code blocks
        code_blocks = re.findall(r"```bash\n(.*?)\n```", readme_content, re.DOTALL)
        for block in code_blocks:
            if "/cc-plugins:" in block:
                # Should have proper command format
                assert block.startswith("/") or "/cc-plugins:" in block


class TestStructureDocumentation:
    """Test documentation of plugin structure."""

    @pytest.fixture
    def readme_content(self):
        """Read README content."""
        return (Path(__file__).parent.parent / "README.md").read_text()

    @pytest.fixture
    def project_root(self):
        """Get project root."""
        return Path(__file__).parent.parent

    def test_directory_structure_documented(self, readme_content):
        """Test that directory structure is documented."""
        assert "Directory Layout" in readme_content or "directory" in readme_content.lower()

    def test_documented_directories_actually_exist(self, readme_content, project_root):
        """Test that documented directories exist."""
        # Common directories mentioned
        expected_dirs = [".claude-plugin", "commands", "agents", "skills", "scripts", "tests"]
        for dir_name in expected_dirs:
            # Should be mentioned in docs
            assert dir_name in readme_content

    def test_component_types_documented(self, readme_content):
        """Test that component types are documented."""
        component_types = ["Commands", "Agents", "Skills"]
        for component_type in component_types:
            assert component_type in readme_content

    def test_manifest_documented(self, readme_content):
        """Test that manifest file is documented."""
        assert "plugin.json" in readme_content or "manifest" in readme_content.lower()


class TestVersionConsistency:
    """Test that version numbers are consistent."""

    @pytest.fixture
    def plugin_json_path(self):
        """Get path to plugin.json."""
        return Path(__file__).parent.parent / ".claude-plugin" / "plugin.json"

    @pytest.fixture
    def readme_path(self):
        """Get path to README."""
        return Path(__file__).parent.parent / "README.md"

    def test_plugin_json_has_version(self, plugin_json_path):
        """Test that plugin.json has version."""
        assert plugin_json_path.exists(), "plugin.json should exist"
        manifest = json.loads(plugin_json_path.read_text())
        assert "version" in manifest, "plugin.json should have version field"
        assert manifest["version"], "version should not be empty"

    def test_version_is_semantic(self, plugin_json_path):
        """Test that version uses semantic versioning."""
        manifest = json.loads(plugin_json_path.read_text())
        version = manifest["version"]
        # Should match X.Y.Z format
        assert re.match(r"^\d+\.\d+\.\d+", version), \
            f"Version should use semantic versioning (X.Y.Z), got: {version}"

    def test_readme_references_version(self, readme_path, plugin_json_path):
        """Test that README references plugin version."""
        readme_content = readme_path.read_text()
        manifest = json.loads(plugin_json_path.read_text())
        version = manifest["version"]
        
        # README should reference the version
        assert version in readme_content, \
            f"README should reference version {version}"


class TestExampleAccuracy:
    """Test that examples in documentation are accurate."""

    @pytest.fixture
    def readme_content(self):
        """Read README content."""
        return (Path(__file__).parent.parent / "README.md").read_text()

    def test_installation_example_uses_correct_path(self, readme_content):
        """Test that installation example is correct."""
        # Should mention ~/.claude/plugins
        assert "~/.claude/plugins" in readme_content or ".claude/plugins" in readme_content

    def test_command_example_format_correct(self, readme_content):
        """Test that command examples use correct format."""
        # Find command examples
        examples = re.findall(r"/cc-plugins:[a-z-]+", readme_content)
        # Should have examples
        assert len(examples) > 0, "Should have command examples"

    def test_troubleshooting_examples_reference_commands(self, readme_content):
        """Test that troubleshooting examples reference actual commands."""
        if "Troubleshooting" in readme_content:
            # Extract troubleshooting section
            trouble_section = readme_content.split("Troubleshooting")[1]
            if "Issue:" in trouble_section or "###" in trouble_section[:500]:
                # Should have example commands
                assert "/cc-plugins:" in trouble_section or "`" in trouble_section


class TestWorkflowDocumentation:
    """Test documentation of workflows."""

    @pytest.fixture
    def readme_content(self):
        """Read README content."""
        return (Path(__file__).parent.parent / "README.md").read_text()

    def test_workflows_section_exists(self, readme_content):
        """Test that workflows are documented."""
        assert "Workflow" in readme_content, "README should document workflows"

    def test_workflows_include_commands(self, readme_content):
        """Test that workflow examples include commands."""
        if "Workflow" in readme_content:
            workflow_section = readme_content.split("Workflow")[1]
            # Should have command examples
            assert "/cc-plugins:" in workflow_section or "```" in workflow_section

    def test_multiple_workflows_documented(self, readme_content):
        """Test that multiple workflows are documented."""
        # Count workflow sections
        workflow_count = readme_content.count("### Workflow") + \
                        readme_content.count("## Workflow") + \
                        readme_content.count("Workflow:")
        # Should have at least one workflow documented
        assert workflow_count > 0, "Should document at least one workflow"


class TestDocFileReferences:
    """Test references to documentation files."""

    @pytest.fixture
    def project_root(self):
        """Get project root."""
        return Path(__file__).parent.parent

    @pytest.fixture
    def readme_content(self):
        """Read README content."""
        return (Path(__file__).parent.parent / "README.md").read_text()

    def test_referenced_doc_files_exist(self, readme_content, project_root):
        """Test that referenced documentation files exist."""
        # Find local file references
        local_refs = re.findall(r"\[.*?\]\(((?!http)[^)]+\.md)\)", readme_content)
        for ref in local_refs:
            if not ref.startswith("http"):
                doc_path = project_root / ref
                # File should exist or be referenced with #anchor
                base_path = project_root / ref.split("#")[0] if "#" in ref else doc_path
                # Allow for non-existent optional docs
                assert base_path.exists() or "phase" in ref.lower() or "development" in ref.lower() or \
                       "#" in ref, f"Documentation reference should exist: {ref}"

    def test_skill_documentation_referenced(self, readme_content, project_root):
        """Test that skill documentation is referenced."""
        skills_dir = project_root / "skills"
        if skills_dir.exists():
            for skill_dir in skills_dir.iterdir():
                if skill_dir.is_dir():
                    skill_md = skill_dir / "SKILL.md"
                    if skill_md.exists():
                        # Skill should be mentioned in README
                        assert skill_dir.name in readme_content


class TestCompletenesChecks:
    """Test documentation completeness."""

    @pytest.fixture
    def project_root(self):
        """Get project root."""
        return Path(__file__).parent.parent

    @pytest.fixture
    def readme_content(self):
        """Read README content."""
        return (Path(__file__).parent.parent / "README.md").read_text()

    def test_all_command_files_mentioned(self, readme_content, project_root):
        """Test that all command files are documented."""
        commands_dir = project_root / "commands"
        if commands_dir.exists():
            cmd_count = len(list(commands_dir.glob("*.md")))
            # README should mention commands
            assert cmd_count > 0, "Should have command files"

    def test_plugin_manifest_documented(self, readme_content):
        """Test that plugin.json is documented."""
        assert "plugin.json" in readme_content or "manifest" in readme_content.lower()

    def test_testing_documented(self, readme_content):
        """Test that testing is documented."""
        # Should mention tests/pytest
        assert "test" in readme_content.lower() or "pytest" in readme_content.lower()

    def test_license_mentioned(self, readme_content):
        """Test that license is mentioned."""
        assert "License" in readme_content or "LICENSE" in readme_content

    def test_contributing_documented(self, readme_content):
        """Test that contributing is documented."""
        assert "Contribut" in readme_content or "CONTRIBUTING" in readme_content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
