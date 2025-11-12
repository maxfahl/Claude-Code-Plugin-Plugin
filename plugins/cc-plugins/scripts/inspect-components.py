#!/usr/bin/env python3
"""
Component inspector script for Claude Code plugins.

Analyzes all components in a plugin and reports:
- Lists all components (commands, agents, skills)
- Shows component metadata from frontmatter
- Identifies component issues
- Generates component summary report
- Supports --json output flag

Usage:
    ./scripts/inspect-components.py [--json] [path]

Exit codes:
    0: All components inspected successfully
    1: Errors found during inspection
    2: Script execution error

Reference: https://code.claude.com/docs/en/plugin-development
"""

import json
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Optional

try:
    import yaml
except ImportError:
    print("Error: PyYAML not installed. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)


class ComponentInspector:
    """Inspects and analyzes plugin components."""

    def __init__(self, root_path: Path):
        """Initialize component inspector."""
        self.root_path = root_path
        self.components: List[Dict] = []
        self.issues: List[Dict] = []

    def inspect_all(self) -> bool:
        """
        Inspect all plugin components.

        Returns:
            True if inspection successful (may have issues), False on error
        """
        if not self.root_path.exists():
            self.issues.append({
                'component': 'N/A',
                'type': 'error',
                'message': f"Plugin path does not exist: {self.root_path}"
            })
            return False

        # Inspect commands
        self._inspect_commands()

        # Inspect agents
        self._inspect_agents()

        # Inspect skills
        self._inspect_skills()

        return True

    def _inspect_commands(self):
        """Inspect all command components."""
        commands_dir = self.root_path / "commands"
        if not commands_dir.exists():
            return

        for cmd_file in sorted(commands_dir.glob("*.md")):
            self._inspect_component(cmd_file, "command")

    def _inspect_agents(self):
        """Inspect all agent components."""
        agents_dir = self.root_path / "agents"
        if not agents_dir.exists():
            return

        for agent_file in sorted(agents_dir.glob("*.md")):
            self._inspect_component(agent_file, "agent")

    def _inspect_skills(self):
        """Inspect all skill components."""
        skills_dir = self.root_path / "skills"
        if not skills_dir.exists():
            return

        for skill_dir in sorted(skills_dir.iterdir()):
            if skill_dir.is_dir():
                self._inspect_skill_directory(skill_dir)

    def _inspect_component(self, file_path: Path, component_type: str):
        """Inspect a single component file."""
        component_name = file_path.stem
        component_info = {
            'name': component_name,
            'path': str(file_path.relative_to(self.root_path)),
            'type': component_type,
            'metadata': {},
            'issues': []
        }

        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            component_info['issues'].append(f"Error reading file: {e}")
            self.components.append(component_info)
            return

        # Extract frontmatter
        frontmatter, body = self._extract_frontmatter(content)

        if frontmatter is None:
            component_info['issues'].append("Missing or invalid YAML frontmatter")
            self.components.append(component_info)
            return

        component_info['metadata'] = frontmatter

        # Validate by component type
        if component_type == "command":
            self._validate_command_metadata(component_info)
        elif component_type == "agent":
            self._validate_agent_metadata(component_info)

        self.components.append(component_info)

    def _inspect_skill_directory(self, skill_dir: Path):
        """Inspect a skill directory."""
        skill_name = skill_dir.name
        skill_info = {
            'name': skill_name,
            'path': str(skill_dir.relative_to(self.root_path)),
            'type': 'skill',
            'metadata': {},
            'issues': []
        }

        skill_md = skill_dir / "SKILL.md"

        if not skill_md.exists():
            skill_info['issues'].append("Missing SKILL.md file")
            self.components.append(skill_info)
            return

        try:
            content = skill_md.read_text(encoding='utf-8')
        except Exception as e:
            skill_info['issues'].append(f"Error reading SKILL.md: {e}")
            self.components.append(skill_info)
            return

        frontmatter, body = self._extract_frontmatter(content)

        if frontmatter is None:
            skill_info['issues'].append("Missing or invalid YAML frontmatter in SKILL.md")
            self.components.append(skill_info)
            return

        skill_info['metadata'] = frontmatter

        # Validate skill metadata
        self._validate_skill_metadata(skill_info)

        self.components.append(skill_info)

    def _validate_command_metadata(self, component_info: Dict):
        """Validate command metadata."""
        required_fields = {
            'description': str,
            'allowed-tools': list,
            'argument-hint': str,
            'model': str,
            'disable-model-invocation': bool,
        }

        metadata = component_info['metadata']

        for field, expected_type in required_fields.items():
            if field not in metadata:
                component_info['issues'].append(
                    f"Missing required field: {field}"
                )
            elif expected_type == list and not isinstance(metadata[field], list):
                component_info['issues'].append(
                    f"Field '{field}' should be array, got {type(metadata[field]).__name__}"
                )
            elif expected_type == bool and not isinstance(metadata[field], bool):
                component_info['issues'].append(
                    f"Field '{field}' should be boolean, got {type(metadata[field]).__name__}"
                )
            elif expected_type == str and not isinstance(metadata[field], str):
                component_info['issues'].append(
                    f"Field '{field}' should be string, got {type(metadata[field]).__name__}"
                )

        # Validate model value
        if 'model' in metadata:
            valid_models = ['sonnet', 'opus', 'haiku']
            if metadata['model'] not in valid_models:
                component_info['issues'].append(
                    f"Field 'model' should be one of {valid_models}, got '{metadata['model']}'"
                )

    def _validate_agent_metadata(self, component_info: Dict):
        """Validate agent metadata."""
        metadata = component_info['metadata']

        # Check required field
        if 'description' not in metadata:
            component_info['issues'].append("Missing required field: description")
        elif not isinstance(metadata['description'], str):
            component_info['issues'].append(
                f"Field 'description' should be string, got {type(metadata['description']).__name__}"
            )
        elif len(metadata['description']) > 1024:
            component_info['issues'].append(
                "Field 'description' exceeds maximum length of 1024 characters"
            )

        # Validate optional model field
        if 'model' in metadata:
            valid_models = ['sonnet', 'opus', 'haiku']
            if metadata['model'] not in valid_models:
                component_info['issues'].append(
                    f"Field 'model' should be one of {valid_models}, got '{metadata['model']}'"
                )

        # Validate optional tools field
        if 'tools' in metadata:
            if not isinstance(metadata['tools'], list):
                component_info['issues'].append(
                    f"Field 'tools' should be array, got {type(metadata['tools']).__name__}"
                )

    def _validate_skill_metadata(self, component_info: Dict):
        """Validate skill metadata."""
        metadata = component_info['metadata']

        # Check required fields
        if 'name' not in metadata:
            component_info['issues'].append("Missing required field: name")
        elif not isinstance(metadata['name'], str):
            component_info['issues'].append(
                f"Field 'name' should be string, got {type(metadata['name']).__name__}"
            )
        elif not self._is_kebab_case(metadata['name']):
            component_info['issues'].append(
                f"Field 'name' must be kebab-case (lowercase with hyphens), got '{metadata['name']}'"
            )

        if 'description' not in metadata:
            component_info['issues'].append("Missing required field: description")
        elif not isinstance(metadata['description'], str):
            component_info['issues'].append(
                f"Field 'description' should be string, got {type(metadata['description']).__name__}"
            )
        elif len(metadata['description']) > 1024:
            component_info['issues'].append(
                "Field 'description' exceeds maximum length of 1024 characters"
            )

    @staticmethod
    def _extract_frontmatter(content: str) -> tuple:
        """Extract YAML frontmatter from markdown content."""
        lines = content.split('\n')

        if len(lines) < 3 or lines[0].strip() != '---':
            return None, content

        # Find closing ---
        end_index = None
        for i in range(1, len(lines)):
            if lines[i].strip() == '---':
                end_index = i
                break

        if end_index is None:
            return None, content

        # Extract frontmatter
        frontmatter_str = '\n'.join(lines[1:end_index])
        body = '\n'.join(lines[end_index + 1:])

        try:
            frontmatter = yaml.safe_load(frontmatter_str)
            if frontmatter is None:
                frontmatter = {}
            if not isinstance(frontmatter, dict):
                return None, content
            return frontmatter, body
        except yaml.YAMLError:
            return None, content

    @staticmethod
    def _is_kebab_case(name: str) -> bool:
        """Check if string is in kebab-case."""
        if not name:
            return False
        if not name.islower():
            return False
        if ' ' in name or '_' in name:
            return False
        return True

    def get_summary(self) -> Dict:
        """Get summary of component inspection."""
        by_type = {}
        for component in self.components:
            component_type = component['type']
            if component_type not in by_type:
                by_type[component_type] = []
            by_type[component_type].append(component)

        issues_by_type = {}
        for component in self.components:
            if component['issues']:
                component_type = component['type']
                if component_type not in issues_by_type:
                    issues_by_type[component_type] = 0
                issues_by_type[component_type] += 1

        return {
            'total_components': len(self.components),
            'by_type': {k: len(v) for k, v in by_type.items()},
            'components_with_issues': sum(len(c['issues']) for c in self.components),
            'issues_by_type': issues_by_type
        }

    def print_report(self, as_json: bool = False):
        """Print component inspection report."""
        if as_json:
            self.print_json_report()
            return

        self.print_text_report()

    def print_text_report(self):
        """Print text format report."""
        summary = self.get_summary()

        print("\n=== Component Inspection Report ===\n")

        # Summary
        print(f"Total Components: {summary['total_components']}")
        for comp_type, count in summary['by_type'].items():
            print(f"  {comp_type.capitalize()}s: {count}")

        if summary['components_with_issues'] > 0:
            print(f"\nComponents with Issues: {summary['components_with_issues']}")

        # Components by type
        for comp_type in ['command', 'agent', 'skill']:
            components = [c for c in self.components if c['type'] == comp_type]
            if not components:
                continue

            print(f"\n--- {comp_type.upper()}S ---")
            for component in components:
                status = "✓" if not component['issues'] else "✗"
                print(f"{status} {component['name']}")
                print(f"  Path: {component['path']}")

                # Show key metadata
                metadata = component['metadata']
                if 'description' in metadata:
                    desc = metadata['description']
                    if len(desc) > 70:
                        desc = desc[:67] + "..."
                    print(f"  Description: {desc}")

                # Show version if present
                if 'version' in metadata:
                    print(f"  Version: {metadata['version']}")

                # Show issues
                if component['issues']:
                    print(f"  Issues:")
                    for issue in component['issues']:
                        print(f"    - {issue}")

                print()

    def print_json_report(self):
        """Print JSON format report."""
        output = {
            'summary': self.get_summary(),
            'components': self.components
        }
        print(json.dumps(output, indent=2))


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Inspect and analyze plugin components",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ./scripts/inspect-components.py                 Inspect components in current directory
  ./scripts/inspect-components.py /path/to/plugin Inspect specific plugin
  ./scripts/inspect-components.py --json .        Output results as JSON
        """
    )

    parser.add_argument(
        'path',
        nargs='?',
        default='.',
        help='Path to plugin directory (default: current directory)'
    )

    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results as JSON'
    )

    args = parser.parse_args()

    plugin_root = Path(args.path).resolve()

    inspector = ComponentInspector(plugin_root)

    try:
        success = inspector.inspect_all()
    except Exception as e:
        print(f"Fatal error during inspection: {e}", file=sys.stderr)
        return 2

    inspector.print_report(as_json=args.json)

    # Return 0 if inspection completed (even with issues), 1 if couldn't inspect
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
