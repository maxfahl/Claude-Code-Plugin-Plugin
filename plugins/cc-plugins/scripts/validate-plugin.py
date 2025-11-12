#!/usr/bin/env python3
"""
Main plugin validator script.

Validates a Claude Code plugin structure and components for compliance with
official specifications.

Usage:
    ./scripts/validate-plugin.py [path]

Exit codes:
    0: Plugin is valid
    1: Plugin has validation errors
    2: Script execution error

Reference: https://code.claude.com/docs/en/plugin-development
"""

import json
import sys
from pathlib import Path
from typing import List

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from validators import (
    validate_command_file,
    validate_agent_file,
    validate_skill_directory,
    validate_hooks_config,
    validate_mcp_config,
)


class PluginValidator:
    """Validates a Claude Code plugin directory structure."""

    def __init__(self, plugin_root: Path):
        """Initialize validator with plugin root directory."""
        self.plugin_root = plugin_root
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate(self) -> bool:
        """
        Validate the entire plugin structure.

        Returns:
            True if plugin is valid (no errors), False otherwise
        """
        # Check basic structure
        self._validate_directory_structure()

        if self.errors:
            # Stop early if basic structure is invalid
            return False

        # Check manifest
        self._validate_manifest()

        # Check component locations
        self._validate_component_locations()

        # Validate component files
        self._validate_components()

        # Validate configuration files
        self._validate_config_files()

        return len(self.errors) == 0

    def _validate_directory_structure(self):
        """Validate basic plugin directory structure."""
        if not self.plugin_root.exists():
            self.errors.append(f"Plugin directory does not exist: {self.plugin_root}")
            return

        if not self.plugin_root.is_dir():
            self.errors.append(f"Plugin path is not a directory: {self.plugin_root}")
            return

        # Check for .claude-plugin directory
        claude_plugin_dir = self.plugin_root / ".claude-plugin"
        if not claude_plugin_dir.exists():
            self.errors.append(
                f"Missing required .claude-plugin directory at: {self.plugin_root}/.claude-plugin"
            )
        elif not claude_plugin_dir.is_dir():
            self.errors.append(
                f".claude-plugin path is not a directory: {claude_plugin_dir}"
            )

    def _validate_manifest(self):
        """Validate plugin.json manifest file."""
        manifest_path = self.plugin_root / ".claude-plugin" / "plugin.json"

        if not manifest_path.exists():
            self.errors.append(
                f"Missing required manifest file at: {manifest_path}\n"
                f"  Create a plugin.json file in the .claude-plugin/ directory"
            )
            return

        # Read and parse manifest
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest = json.load(f)
        except json.JSONDecodeError as e:
            self.errors.append(
                f"Manifest file contains invalid JSON: {manifest_path}\n"
                f"  Error: {e}"
            )
            return
        except Exception as e:
            self.errors.append(f"Error reading manifest file: {manifest_path}: {e}")
            return

        # Validate manifest schema
        manifest_errors = self._validate_manifest_schema(manifest)
        self.errors.extend(manifest_errors)

    def _validate_manifest_schema(self, manifest: dict) -> List[str]:
        """Validate manifest against official schema."""
        errors = []

        # Required fields
        if "name" not in manifest:
            errors.append("Manifest missing required field: 'name'")
        else:
            name = manifest["name"]
            if not isinstance(name, str):
                errors.append(f"Manifest field 'name' must be string, got {type(name).__name__}")
            elif not self._is_kebab_case(name):
                errors.append(
                    f"Manifest field 'name' must be kebab-case, got: {name}\n"
                    f"  Use lowercase letters and hyphens only (e.g., 'my-plugin')"
                )

        # Optional string fields
        string_fields = ["version", "description", "homepage", "repository", "license"]
        for field in string_fields:
            if field in manifest and not isinstance(manifest[field], str):
                errors.append(
                    f"Manifest field '{field}' must be string, got {type(manifest[field]).__name__}"
                )

        # Author object
        if "author" in manifest:
            author = manifest["author"]
            if not isinstance(author, dict):
                errors.append(f"Manifest field 'author' must be object, got {type(author).__name__}")
            else:
                for key in ["name", "email", "url"]:
                    if key in author and not isinstance(author[key], str):
                        errors.append(
                            f"Manifest field 'author.{key}' must be string, got {type(author[key]).__name__}"
                        )

        # Keywords array
        if "keywords" in manifest:
            keywords = manifest["keywords"]
            if not isinstance(keywords, list):
                errors.append(
                    f"Manifest field 'keywords' must be array, got {type(keywords).__name__}"
                )
            else:
                for i, kw in enumerate(keywords):
                    if not isinstance(kw, str):
                        errors.append(
                            f"Manifest field 'keywords[{i}]' must be string, got {type(kw).__name__}"
                        )

        # Check for unsupported fields
        official_fields = {
            "name", "version", "description", "author", "homepage",
            "repository", "license", "keywords", "commands", "agents",
            "hooks", "mcpServers", "skills"
        }
        for field in manifest:
            if field not in official_fields:
                self.warnings.append(
                    f"Manifest contains unsupported field: '{field}'\n"
                    f"  This field is not in the official specification and will be ignored"
                )

        return errors

    def _validate_component_locations(self):
        """Validate that components are in correct locations."""
        claude_plugin_dir = self.plugin_root / ".claude-plugin"
        component_dirs = ["commands", "agents", "skills", "scripts"]

        for component_dir in component_dirs:
            # Check if component is incorrectly placed in .claude-plugin
            wrong_location = claude_plugin_dir / component_dir
            if wrong_location.exists():
                self.errors.append(
                    f"Component directory '{component_dir}' is in wrong location: {wrong_location}\n"
                    f"  Move '{component_dir}' to the plugin root level: {self.plugin_root / component_dir}"
                )

    def _validate_components(self):
        """Validate component files."""
        # Validate commands
        commands_dir = self.plugin_root / "commands"
        if commands_dir.exists():
            for cmd_file in commands_dir.glob("*.md"):
                errors = validate_command_file(cmd_file)
                self.errors.extend(errors)

        # Validate agents
        agents_dir = self.plugin_root / "agents"
        if agents_dir.exists():
            for agent_file in agents_dir.glob("*.md"):
                errors = validate_agent_file(agent_file)
                self.errors.extend(errors)

        # Validate skills
        skills_dir = self.plugin_root / "skills"
        if skills_dir.exists():
            for skill_dir in skills_dir.iterdir():
                if skill_dir.is_dir():
                    errors = validate_skill_directory(skill_dir)
                    self.errors.extend(errors)

    def _validate_config_files(self):
        """Validate configuration files."""
        # Validate hooks.json if present
        hooks_file = self.plugin_root / "hooks" / "hooks.json"
        if hooks_file.exists():
            errors = validate_hooks_config(hooks_file)
            self.errors.extend(errors)

        # Validate .mcp.json if present
        mcp_file = self.plugin_root / ".mcp.json"
        if mcp_file.exists():
            errors = validate_mcp_config(mcp_file)
            self.errors.extend(errors)

    @staticmethod
    def _is_kebab_case(name: str) -> bool:
        """Check if name is in kebab-case."""
        if not name:
            return False
        if not name.islower():
            return False
        if ' ' in name or '_' in name:
            return False
        return True

    def print_report(self):
        """Print validation report."""
        if not self.errors and not self.warnings:
            print("✓ Plugin validation passed")
            return

        if self.errors:
            print(f"\nERRORS ({len(self.errors)}):")
            for i, error in enumerate(self.errors, 1):
                print(f"\n{i}. {error}")

        if self.warnings:
            print(f"\n\nWARNINGS ({len(self.warnings)}):")
            for i, warning in enumerate(self.warnings, 1):
                print(f"\n{i}. {warning}")


def main():
    """Main entry point."""
    # Get plugin directory
    if len(sys.argv) > 1:
        plugin_root = Path(sys.argv[1])
    else:
        # Use current directory
        plugin_root = Path.cwd()

    # Ensure it's absolute
    plugin_root = plugin_root.resolve()

    # Validate
    validator = PluginValidator(plugin_root)

    try:
        is_valid = validator.validate()
    except Exception as e:
        print(f"Fatal error during validation: {e}", file=sys.stderr)
        return 2

    # Print report
    validator.print_report()

    # Return appropriate exit code
    if validator.errors:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
