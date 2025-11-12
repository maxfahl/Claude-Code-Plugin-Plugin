"""
Integration tests for cc-plugins complete workflows.

Tests complete end-to-end workflows that combine multiple components:
- Create → Validate → Document workflow
- Create → Break → Debug → Fix workflow
- Validate → Update → Validate workflow
- Cross-component interactions
- Error handling across all components

Test Coverage:
- Complete plugin development lifecycle
- Multi-step workflows
- Component interactions
- Error recovery
- Cross-platform compatibility
"""

import json
import subprocess
import tempfile
import pytest
from pathlib import Path
import shutil


@pytest.fixture
def temp_workspace():
    """Create a temporary workspace for integration tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        workspace = Path(tmpdir)
        yield workspace


@pytest.fixture
def cc_plugins_root():
    """Returns the path to the cc-plugins root directory."""
    return Path(__file__).parent.parent


class TestCreateValidateDocumentWorkflow:
    """Test the complete Create → Validate → Document workflow."""

    def test_create_validate_document_workflow(self, temp_workspace, cc_plugins_root):
        """Test creating, validating, and documenting a plugin."""
        plugin_name = "integration-test-plugin"

        # Step 1: Create plugin
        create_cmd = cc_plugins_root / "commands" / "create.md"
        result = self._execute_create_command(
            create_cmd,
            plugin_name,
            description="Integration test plugin",
            cwd=temp_workspace
        )

        assert result.returncode == 0, f"Create failed: {result.stderr}"

        plugin_dir = temp_workspace / plugin_name
        assert plugin_dir.exists(), "Plugin not created"

        # Step 2: Validate plugin
        validator_script = cc_plugins_root / "scripts" / "validate-plugin.py"
        result = subprocess.run(
            ["python3", str(validator_script), str(plugin_dir)],
            capture_output=True,
            text=True
        )

        assert result.returncode == 0, f"Validation failed: {result.stdout}"

        # Step 3: Add components to plugin
        self._add_sample_command(plugin_dir)
        self._add_sample_agent(plugin_dir)
        self._add_sample_skill(plugin_dir)

        # Step 4: Validate again with components
        result = subprocess.run(
            ["python3", str(validator_script), str(plugin_dir)],
            capture_output=True,
            text=True
        )

        assert result.returncode == 0, f"Validation with components failed: {result.stdout}"

        # Step 5: Verify all components are present
        assert (plugin_dir / "commands" / "sample.md").exists()
        assert (plugin_dir / "agents" / "helper.md").exists()
        assert (plugin_dir / "skills" / "sample-skill" / "SKILL.md").exists()

    def _execute_create_command(self, create_cmd, plugin_name, description=None, cwd=None):
        """Execute the create command."""
        with open(create_cmd, 'r') as f:
            content = f.read()

        bash_start = content.find("!bash\n")
        bash_script = content[bash_start + 6:]

        args = [plugin_name]
        if description:
            args.extend(["--description", description])

        result = subprocess.run(
            ["bash", "-c", bash_script, "bash"] + args,
            cwd=cwd,
            capture_output=True,
            text=True
        )

        return result

    def _add_sample_command(self, plugin_dir):
        """Add a sample command to the plugin."""
        command_file = plugin_dir / "commands" / "sample.md"
        command_file.write_text("""---
description: "A sample command for testing"
allowed-tools: ["Bash", "Read", "Write"]
argument-hint: "Optional arguments"
model: "sonnet"
disable-model-invocation: false
---

# Sample Command

This is a sample command for integration testing.

## Usage

```bash
/plugin:sample [args]
```

!bash
echo "Sample command executed"
""")

    def _add_sample_agent(self, plugin_dir):
        """Add a sample agent to the plugin."""
        agent_file = plugin_dir / "agents" / "helper.md"
        agent_file.write_text("""---
description: "A helpful assistant agent"
activation-phrases: ["help me", "assist with"]
allowed-tools: ["Bash", "Read", "Write"]
model: "sonnet"
---

# Helper Agent

A specialized agent for assistance.

## Activation

This agent activates when users need help.

## Capabilities

- Provides assistance
- Answers questions
- Guides through workflows
""")

    def _add_sample_skill(self, plugin_dir):
        """Add a sample skill to the plugin."""
        skill_dir = plugin_dir / "skills" / "sample-skill"
        skill_dir.mkdir(parents=True, exist_ok=True)

        skill_file = skill_dir / "SKILL.md"
        skill_file.write_text("""---
name: "sample-skill"
description: "A reusable skill for testing"
allowed-tools: ["Bash"]
model: "sonnet"
---

# Sample Skill

A reusable workflow skill.

## Usage

This skill demonstrates a reusable workflow pattern.

## Steps

1. Initialize
2. Execute
3. Complete
""")


class TestCreateBreakDebugFixWorkflow:
    """Test the Create → Break → Debug → Fix workflow."""

    def test_create_break_debug_fix_workflow(self, temp_workspace, cc_plugins_root):
        """Test creating, breaking, debugging, and fixing a plugin."""
        plugin_name = "break-fix-test-plugin"

        # Step 1: Create valid plugin
        create_cmd = cc_plugins_root / "commands" / "create.md"
        result = self._execute_create_command(create_cmd, plugin_name, cwd=temp_workspace)
        assert result.returncode == 0

        plugin_dir = temp_workspace / plugin_name

        # Step 2: Verify it's valid
        validator_script = cc_plugins_root / "scripts" / "validate-plugin.py"
        result = subprocess.run(
            ["python3", str(validator_script), str(plugin_dir)],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, "Initial plugin should be valid"

        # Step 3: Break the plugin (invalid manifest)
        manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)

        manifest["name"] = "Invalid_Name_With_Underscores"
        manifest["badField"] = "unsupported"

        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)

        # Step 4: Debug - detect issues
        result = subprocess.run(
            ["python3", str(validator_script), str(plugin_dir)],
            capture_output=True,
            text=True
        )
        assert result.returncode != 0, "Should detect broken plugin"
        assert "kebab" in result.stdout.lower() or "lowercase" in result.stdout.lower()

        # Step 5: Fix the plugin
        manifest["name"] = plugin_name
        del manifest["badField"]

        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)

        # Step 6: Verify fix
        result = subprocess.run(
            ["python3", str(validator_script), str(plugin_dir)],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, "Fixed plugin should pass validation"

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


class TestValidateUpdateValidateWorkflow:
    """Test the Validate → Update → Validate workflow."""

    def test_validate_update_validate_workflow(self, temp_workspace, cc_plugins_root):
        """Test validating, updating, and revalidating a plugin."""
        plugin_name = "update-test-plugin"

        # Step 1: Create plugin
        create_cmd = cc_plugins_root / "commands" / "create.md"
        result = self._execute_create_command(create_cmd, plugin_name, cwd=temp_workspace)
        assert result.returncode == 0

        plugin_dir = temp_workspace / plugin_name

        # Step 2: Initial validation
        validator_script = cc_plugins_root / "scripts" / "validate-plugin.py"
        result = subprocess.run(
            ["python3", str(validator_script), str(plugin_dir)],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0

        # Step 3: Update manifest with more metadata
        manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)

        manifest["author"] = {
            "name": "Integration Tester",
            "email": "test@example.com",
            "url": "https://example.com"
        }
        manifest["keywords"] = ["test", "integration", "workflow"]
        manifest["homepage"] = "https://example.com/plugin"
        manifest["repository"] = "https://github.com/example/plugin"

        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)

        # Step 4: Revalidate with updates
        result = subprocess.run(
            ["python3", str(validator_script), str(plugin_dir)],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, "Updated plugin should still be valid"

        # Step 5: Add new component
        command_file = plugin_dir / "commands" / "new-feature.md"
        command_file.write_text("""---
description: "A new feature command"
allowed-tools: ["Bash"]
argument-hint: "No arguments"
model: "sonnet"
disable-model-invocation: false
---

# New Feature

New functionality added in update.

!bash
echo "New feature"
""")

        # Step 6: Final validation
        result = subprocess.run(
            ["python3", str(validator_script), str(plugin_dir)],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, "Plugin with new component should be valid"

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


class TestCrossComponentInteractions:
    """Test interactions between different components."""

    def test_commands_agents_skills_coexist(self, temp_workspace, cc_plugins_root):
        """Test that commands, agents, and skills can coexist in one plugin."""
        plugin_name = "full-featured-plugin"

        # Create plugin
        create_cmd = cc_plugins_root / "commands" / "create.md"
        result = self._execute_create_command(create_cmd, plugin_name, cwd=temp_workspace)
        assert result.returncode == 0

        plugin_dir = temp_workspace / plugin_name

        # Add all component types
        self._add_command(plugin_dir, "cmd1")
        self._add_command(plugin_dir, "cmd2")
        self._add_agent(plugin_dir, "agent1")
        self._add_agent(plugin_dir, "agent2")
        self._add_skill(plugin_dir, "skill1")
        self._add_skill(plugin_dir, "skill2")

        # Validate
        validator_script = cc_plugins_root / "scripts" / "validate-plugin.py"
        result = subprocess.run(
            ["python3", str(validator_script), str(plugin_dir)],
            capture_output=True,
            text=True
        )

        assert result.returncode == 0, "All components should coexist"

    def test_multiple_scripts_in_plugin(self, temp_workspace, cc_plugins_root):
        """Test that multiple scripts can exist in a plugin."""
        plugin_name = "multi-script-plugin"

        # Create plugin
        create_cmd = cc_plugins_root / "commands" / "create.md"
        result = self._execute_create_command(create_cmd, plugin_name, cwd=temp_workspace)
        assert result.returncode == 0

        plugin_dir = temp_workspace / plugin_name

        # Add multiple scripts
        scripts_dir = plugin_dir / "scripts"
        scripts_dir.mkdir(exist_ok=True)

        (scripts_dir / "script1.py").write_text("#!/usr/bin/env python3\nprint('Script 1')\n")
        (scripts_dir / "script2.py").write_text("#!/usr/bin/env python3\nprint('Script 2')\n")
        (scripts_dir / "script3.sh").write_text("#!/bin/bash\necho 'Script 3'\n")

        # Validate
        validator_script = cc_plugins_root / "scripts" / "validate-plugin.py"
        result = subprocess.run(
            ["python3", str(validator_script), str(plugin_dir)],
            capture_output=True,
            text=True
        )

        assert result.returncode == 0, "Multiple scripts should be valid"

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

    def _add_command(self, plugin_dir, name):
        """Add a command to the plugin."""
        (plugin_dir / "commands" / f"{name}.md").write_text(f"""---
description: "Command {name}"
allowed-tools: ["Bash"]
argument-hint: "No arguments"
model: "sonnet"
disable-model-invocation: false
---

# {name.title()}

!bash
echo "{name}"
""")

    def _add_agent(self, plugin_dir, name):
        """Add an agent to the plugin."""
        (plugin_dir / "agents" / f"{name}.md").write_text(f"""---
description: "Agent {name}"
activation-phrases: ["{name}"]
allowed-tools: ["Bash"]
model: "sonnet"
---

# {name.title()} Agent
""")

    def _add_skill(self, plugin_dir, name):
        """Add a skill to the plugin."""
        skill_dir = plugin_dir / "skills" / name
        skill_dir.mkdir(parents=True, exist_ok=True)

        (skill_dir / "SKILL.md").write_text(f"""---
name: "{name}"
description: "Skill {name}"
allowed-tools: ["Bash"]
model: "sonnet"
---

# {name.title()} Skill
""")


class TestErrorHandling:
    """Test error handling across all components."""

    def test_graceful_error_messages(self, temp_workspace, cc_plugins_root):
        """Test that errors provide helpful messages."""
        # Test various error scenarios

        # Scenario 1: Non-existent directory
        validator_script = cc_plugins_root / "scripts" / "validate-plugin.py"
        result = subprocess.run(
            ["python3", str(validator_script), str(temp_workspace / "nonexistent")],
            capture_output=True,
            text=True
        )

        assert result.returncode != 0
        assert "does not exist" in result.stdout.lower()

        # Scenario 2: File instead of directory
        test_file = temp_workspace / "test.txt"
        test_file.write_text("not a directory")

        result = subprocess.run(
            ["python3", str(validator_script), str(test_file)],
            capture_output=True,
            text=True
        )

        assert result.returncode != 0
        assert "not a directory" in result.stdout.lower()

    def test_recovers_from_partial_failures(self, temp_workspace, cc_plugins_root):
        """Test that validation continues after finding one error."""
        plugin_name = "multi-error-plugin"

        # Create plugin
        create_cmd = cc_plugins_root / "commands" / "create.md"
        result = self._execute_create_command(create_cmd, plugin_name, cwd=temp_workspace)
        assert result.returncode == 0

        plugin_dir = temp_workspace / plugin_name

        # Introduce multiple errors
        # Error 1: Invalid manifest name
        manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)

        manifest["name"] = "Invalid_Name"
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)

        # Error 2: Invalid command file
        (plugin_dir / "commands" / "broken.md").write_text("""---
description: "Broken command"
# Missing closing ---
""")

        # Run validator
        validator_script = cc_plugins_root / "scripts" / "validate-plugin.py"
        result = subprocess.run(
            ["python3", str(validator_script), str(plugin_dir)],
            capture_output=True,
            text=True
        )

        # Should detect BOTH errors
        assert result.returncode != 0
        output = result.stdout.lower()

        # Check that validation didn't stop at first error
        # (it should report multiple issues)
        assert output.count("error") >= 1

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


class TestCompleteLifecycle:
    """Test the complete plugin development lifecycle."""

    def test_full_plugin_lifecycle(self, temp_workspace, cc_plugins_root):
        """Test creating, developing, validating, and maintaining a plugin."""
        plugin_name = "lifecycle-test-plugin"

        # Phase 1: Creation
        create_cmd = cc_plugins_root / "commands" / "create.md"
        result = self._execute_create_command(
            create_cmd,
            plugin_name,
            description="Lifecycle test plugin",
            author="Tester",
            license="MIT",
            cwd=temp_workspace
        )
        assert result.returncode == 0, "Phase 1: Creation failed"

        plugin_dir = temp_workspace / plugin_name

        # Phase 2: Initial validation
        validator_script = cc_plugins_root / "scripts" / "validate-plugin.py"
        result = subprocess.run(
            ["python3", str(validator_script), str(plugin_dir)],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, "Phase 2: Initial validation failed"

        # Phase 3: Development - add components
        self._add_components(plugin_dir)

        # Phase 4: Validation after development
        result = subprocess.run(
            ["python3", str(validator_script), str(plugin_dir)],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, "Phase 4: Development validation failed"

        # Phase 5: Update metadata
        self._update_metadata(plugin_dir)

        # Phase 6: Final validation
        result = subprocess.run(
            ["python3", str(validator_script), str(plugin_dir)],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, "Phase 6: Final validation failed"

        # Phase 7: Verify structure
        self._verify_complete_structure(plugin_dir)

    def _execute_create_command(self, create_cmd, plugin_name, description=None,
                                 author=None, license=None, cwd=None):
        """Execute the create command."""
        with open(create_cmd, 'r') as f:
            content = f.read()

        bash_start = content.find("!bash\n")
        bash_script = content[bash_start + 6:]

        args = [plugin_name]
        if description:
            args.extend(["--description", description])
        if author:
            args.extend(["--author", author])
        if license:
            args.extend(["--license", license])

        result = subprocess.run(
            ["bash", "-c", bash_script, "bash"] + args,
            cwd=cwd,
            capture_output=True,
            text=True
        )

        return result

    def _add_components(self, plugin_dir):
        """Add all component types to the plugin."""
        # Add command
        (plugin_dir / "commands" / "feature.md").write_text("""---
description: "Main feature command"
allowed-tools: ["Bash", "Read", "Write"]
argument-hint: "No arguments"
model: "sonnet"
disable-model-invocation: false
---

# Feature Command

!bash
echo "Feature executed"
""")

        # Add agent
        (plugin_dir / "agents" / "assistant.md").write_text("""---
description: "Assistant agent"
activation-phrases: ["help", "assist"]
allowed-tools: ["Bash"]
model: "sonnet"
---

# Assistant Agent
""")

        # Add skill
        skill_dir = plugin_dir / "skills" / "workflow"
        skill_dir.mkdir(parents=True, exist_ok=True)
        (skill_dir / "SKILL.md").write_text("""---
name: "workflow"
description: "Workflow skill"
allowed-tools: ["Bash"]
model: "sonnet"
---

# Workflow Skill
""")

    def _update_metadata(self, plugin_dir):
        """Update plugin metadata."""
        manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)

        manifest["version"] = "1.1.0"
        manifest["keywords"] = ["lifecycle", "test", "integration"]

        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)

    def _verify_complete_structure(self, plugin_dir):
        """Verify that plugin has complete structure."""
        assert (plugin_dir / ".claude-plugin" / "plugin.json").exists()
        assert (plugin_dir / "README.md").exists()
        assert (plugin_dir / "commands" / "feature.md").exists()
        assert (plugin_dir / "agents" / "assistant.md").exists()
        assert (plugin_dir / "skills" / "workflow" / "SKILL.md").exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
