#!/usr/bin/env python3
"""
Specification compliance checker for Claude Code plugins.

Validates:
- Unsupported frontmatter fields
- Deprecated features (HTML conditionals: IF, ELSE, MATCH, VALIDATE)
- Specification compliance
- Provides migration guidance for old patterns
- References official documentation

Usage:
    ./scripts/check-spec-compliance.py [--json] [path]

Exit codes:
    0: Plugin is spec compliant
    1: Compliance issues found
    2: Script execution error

Reference: https://code.claude.com/docs/en/plugin-development
"""

import json
import sys
import argparse
import re
from pathlib import Path
from typing import List, Dict, Set

try:
    import yaml
except ImportError:
    print("Error: PyYAML not installed. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)


# Official spec definitions
OFFICIAL_COMMAND_FIELDS = {
    'description', 'allowed-tools', 'argument-hint', 'model', 'disable-model-invocation'
}

OFFICIAL_AGENT_FIELDS = {
    'description', 'tools', 'model'
}

OFFICIAL_SKILL_FIELDS = {
    'name', 'description', 'allowed-tools', 'version', 'author', 'tags'
}

# Known deprecated patterns
DEPRECATED_PATTERNS = {
    r'<IF\s+': {
        'name': 'HTML IF conditional',
        'pattern': '<IF>',
        'migration': 'Remove HTML conditionals. Use environment checks or configuration in your command logic instead.',
        'reference': 'https://code.claude.com/docs/en/plugin-development#deprecated-features'
    },
    r'<ELSE\s*>': {
        'name': 'HTML ELSE conditional',
        'pattern': '<ELSE>',
        'migration': 'Remove HTML conditionals. Handle conditional logic in your implementation.',
        'reference': 'https://code.claude.com/docs/en/plugin-development#deprecated-features'
    },
    r'<MATCH\s+': {
        'name': 'MATCH conditional',
        'pattern': '<MATCH>',
        'migration': 'Replace MATCH with direct pattern matching in your component logic.',
        'reference': 'https://code.claude.com/docs/en/plugin-development#deprecated-features'
    },
    r'<VALIDATE\s+': {
        'name': 'VALIDATE tag',
        'pattern': '<VALIDATE>',
        'migration': 'Move validation logic into your component implementation or frontmatter schema.',
        'reference': 'https://code.claude.com/docs/en/plugin-development#deprecated-features'
    }
}


class SpecChecker:
    """Checks plugin specification compliance."""

    def __init__(self, root_path: Path):
        """Initialize spec checker."""
        self.root_path = root_path
        self.issues: List[Dict] = []
        self.warnings: List[Dict] = []

    def check_all(self) -> bool:
        """
        Check all plugin components for spec compliance.

        Returns:
            True if no errors found, False otherwise
        """
        if not self.root_path.exists():
            self.issues.append({
                'type': 'error',
                'component': 'N/A',
                'message': f"Path does not exist: {self.root_path}"
            })
            return False

        # Check commands
        self._check_commands()

        # Check agents
        self._check_agents()

        # Check skills
        self._check_skills()

        return len(self.issues) == 0

    def _check_commands(self):
        """Check all command components."""
        commands_dir = self.root_path / "commands"
        if not commands_dir.exists():
            return

        for cmd_file in commands_dir.glob("*.md"):
            self._check_component(cmd_file, "command", OFFICIAL_COMMAND_FIELDS)

    def _check_agents(self):
        """Check all agent components."""
        agents_dir = self.root_path / "agents"
        if not agents_dir.exists():
            return

        for agent_file in agents_dir.glob("*.md"):
            self._check_component(agent_file, "agent", OFFICIAL_AGENT_FIELDS)

    def _check_skills(self):
        """Check all skill components."""
        skills_dir = self.root_path / "skills"
        if not skills_dir.exists():
            return

        for skill_dir in skills_dir.iterdir():
            if skill_dir.is_dir():
                skill_md = skill_dir / "SKILL.md"
                if skill_md.exists():
                    self._check_component(skill_md, "skill", OFFICIAL_SKILL_FIELDS, is_skill=True)

    def _check_component(self, file_path: Path, component_type: str, official_fields: Set[str], is_skill: bool = False):
        """Check a single component for spec compliance."""
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            self.issues.append({
                'type': 'error',
                'component': str(file_path.relative_to(self.root_path)),
                'message': f"Error reading file: {e}"
            })
            return

        # Extract frontmatter
        frontmatter, body = self._extract_frontmatter(content)

        if frontmatter is None:
            self.issues.append({
                'type': 'error',
                'component': str(file_path.relative_to(self.root_path)),
                'message': 'Missing or invalid YAML frontmatter'
            })
            return

        # Check for unsupported fields
        self._check_unsupported_fields(
            file_path, component_type, frontmatter, official_fields
        )

        # Check for deprecated patterns
        self._check_deprecated_patterns(file_path, content)

        # Check type-specific compliance
        if component_type == "command":
            self._check_command_compliance(file_path, frontmatter)
        elif component_type == "agent":
            self._check_agent_compliance(file_path, frontmatter)
        elif component_type == "skill":
            self._check_skill_compliance(file_path, frontmatter)

    def _check_unsupported_fields(
        self, file_path: Path, component_type: str,
        frontmatter: dict, official_fields: Set[str]
    ):
        """Check for unsupported fields in frontmatter."""
        component_path = str(file_path.relative_to(self.root_path))

        for field in frontmatter:
            if field not in official_fields:
                self.warnings.append({
                    'type': 'unsupported_field',
                    'component': component_path,
                    'message': f"Unsupported field '{field}' in {component_type} frontmatter. "
                               f"This field is not in the official specification and will be ignored.",
                    'reference': 'https://code.claude.com/docs/en/plugin-development'
                })

    def _check_deprecated_patterns(self, file_path: Path, content: str):
        """Check for deprecated patterns in component."""
        component_path = str(file_path.relative_to(self.root_path))

        for pattern_regex, pattern_info in DEPRECATED_PATTERNS.items():
            if re.search(pattern_regex, content, re.IGNORECASE):
                self.warnings.append({
                    'type': 'deprecated_pattern',
                    'component': component_path,
                    'message': f"Deprecated pattern detected: {pattern_info['name']} ({pattern_info['pattern']}). "
                               f"Migration: {pattern_info['migration']}",
                    'reference': pattern_info['reference']
                })

    def _check_command_compliance(self, file_path: Path, frontmatter: dict):
        """Check command specification compliance."""
        component_path = str(file_path.relative_to(self.root_path))
        required_fields = {'description', 'allowed-tools', 'argument-hint', 'model', 'disable-model-invocation'}

        for field in required_fields:
            if field not in frontmatter:
                self.issues.append({
                    'type': 'missing_required_field',
                    'component': component_path,
                    'message': f"Missing required command field: '{field}'. "
                               f"Commands must have all required fields.",
                    'reference': 'https://code.claude.com/docs/en/plugin-development'
                })

        # Validate model value
        if 'model' in frontmatter:
            if frontmatter['model'] not in ['sonnet', 'opus', 'haiku']:
                self.issues.append({
                    'type': 'invalid_value',
                    'component': component_path,
                    'message': f"Invalid model value: '{frontmatter['model']}'. "
                               f"Must be one of: sonnet, opus, haiku",
                    'reference': 'https://code.claude.com/docs/en/plugin-development'
                })

        # Validate types
        if 'allowed-tools' in frontmatter and not isinstance(frontmatter['allowed-tools'], list):
            self.issues.append({
                'type': 'invalid_type',
                'component': component_path,
                'message': "Field 'allowed-tools' must be an array",
                'reference': 'https://code.claude.com/docs/en/plugin-development'
            })

        if 'disable-model-invocation' in frontmatter and not isinstance(frontmatter['disable-model-invocation'], bool):
            self.issues.append({
                'type': 'invalid_type',
                'component': component_path,
                'message': "Field 'disable-model-invocation' must be boolean",
                'reference': 'https://code.claude.com/docs/en/plugin-development'
            })

    def _check_agent_compliance(self, file_path: Path, frontmatter: dict):
        """Check agent specification compliance."""
        component_path = str(file_path.relative_to(self.root_path))

        # Check required field
        if 'description' not in frontmatter:
            self.issues.append({
                'type': 'missing_required_field',
                'component': component_path,
                'message': "Missing required agent field: 'description'. "
                           "Agents must have a description.",
                'reference': 'https://code.claude.com/docs/en/plugin-development'
            })
        elif len(str(frontmatter.get('description', ''))) > 1024:
            self.issues.append({
                'type': 'invalid_value',
                'component': component_path,
                'message': "Field 'description' exceeds maximum length of 1024 characters",
                'reference': 'https://code.claude.com/docs/en/plugin-development'
            })

        # Validate optional model field
        if 'model' in frontmatter:
            if frontmatter['model'] not in ['sonnet', 'opus', 'haiku']:
                self.issues.append({
                    'type': 'invalid_value',
                    'component': component_path,
                    'message': f"Invalid model value: '{frontmatter['model']}'. "
                               f"Must be one of: sonnet, opus, haiku",
                    'reference': 'https://code.claude.com/docs/en/plugin-development'
                })

        # Validate optional tools field
        if 'tools' in frontmatter and not isinstance(frontmatter['tools'], list):
            self.issues.append({
                'type': 'invalid_type',
                'component': component_path,
                'message': "Field 'tools' must be an array",
                'reference': 'https://code.claude.com/docs/en/plugin-development'
            })

    def _check_skill_compliance(self, file_path: Path, frontmatter: dict):
        """Check skill specification compliance."""
        component_path = str(file_path.relative_to(self.root_path))
        required_fields = {'name', 'description'}

        for field in required_fields:
            if field not in frontmatter:
                self.issues.append({
                    'type': 'missing_required_field',
                    'component': component_path,
                    'message': f"Missing required skill field: '{field}'",
                    'reference': 'https://code.claude.com/docs/en/plugin-development'
                })

        # Validate name is kebab-case
        if 'name' in frontmatter:
            name = frontmatter['name']
            if not self._is_kebab_case(name):
                self.issues.append({
                    'type': 'invalid_value',
                    'component': component_path,
                    'message': f"Skill name must be kebab-case (lowercase with hyphens), got: '{name}'",
                    'reference': 'https://code.claude.com/docs/en/plugin-development'
                })

        # Validate description length
        if 'description' in frontmatter:
            desc = str(frontmatter['description'])
            if len(desc) > 1024:
                self.issues.append({
                    'type': 'invalid_value',
                    'component': component_path,
                    'message': "Skill description exceeds maximum length of 1024 characters",
                    'reference': 'https://code.claude.com/docs/en/plugin-development'
                })

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

    def print_report(self, as_json: bool = False):
        """Print compliance report."""
        if as_json:
            self.print_json_report()
            return

        self.print_text_report()

    def print_text_report(self):
        """Print text format report."""
        print("\n=== Specification Compliance Report ===\n")

        if not self.issues and not self.warnings:
            print("✓ All components are spec compliant\n")
            print("Official Specification Reference:")
            print("  https://code.claude.com/docs/en/plugin-development\n")
            return

        # Issues
        if self.issues:
            print(f"ERRORS ({len(self.issues)}):\n")
            for i, issue in enumerate(self.issues, 1):
                print(f"{i}. {issue['component']}")
                print(f"   Type: {issue['type']}")
                print(f"   {issue['message']}")
                if 'reference' in issue:
                    print(f"   Reference: {issue['reference']}")
                print()

        # Warnings
        if self.warnings:
            print(f"\nWARNINGS ({len(self.warnings)}):\n")
            for i, warning in enumerate(self.warnings, 1):
                print(f"{i}. {warning['component']}")
                print(f"   Type: {warning['type']}")
                print(f"   {warning['message']}")
                if 'reference' in warning:
                    print(f"   Reference: {warning['reference']}")
                print()

        # Documentation reference
        print("\nOfficial Documentation:")
        print("  https://code.claude.com/docs/en/plugin-development\n")

    def print_json_report(self):
        """Print JSON format report."""
        output = {
            'compliant': len(self.issues) == 0,
            'error_count': len(self.issues),
            'warning_count': len(self.warnings),
            'errors': self.issues,
            'warnings': self.warnings,
            'documentation': 'https://code.claude.com/docs/en/plugin-development'
        }
        print(json.dumps(output, indent=2))


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Check plugin specification compliance",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ./scripts/check-spec-compliance.py                 Check current directory
  ./scripts/check-spec-compliance.py /path/to/plugin Check specific plugin
  ./scripts/check-spec-compliance.py --json .        Output results as JSON

Official Reference:
  https://code.claude.com/docs/en/plugin-development
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

    checker = SpecChecker(plugin_root)

    try:
        is_compliant = checker.check_all()
    except Exception as e:
        print(f"Fatal error during compliance check: {e}", file=sys.stderr)
        return 2

    checker.print_report(as_json=args.json)

    return 0 if is_compliant else 1


if __name__ == "__main__":
    sys.exit(main())
