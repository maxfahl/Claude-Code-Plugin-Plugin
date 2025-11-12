#!/usr/bin/env python3
"""
Claude Code Plugin Scaffolding Script

This script creates a new Claude Code plugin with a proper directory structure,
manifest file, and optional template files for components.

Usage:
    python scaffold-plugin.py --name my-plugin [--author "Name"] [--description "..."] [--version "1.0.0"] [--components command,agent,skill]
"""

import argparse
import json
import sys
from pathlib import Path
import re


def is_kebab_case(name):
    """Check if a string follows kebab-case convention."""
    if not name:
        return False
    # kebab-case: lowercase, can contain hyphens, no spaces or underscores
    if " " in name or "_" in name:
        return False
    # Must be lowercase with optional hyphens
    return name.islower() and all(c.isalnum() or c == '-' for c in name)


def validate_plugin_name(name):
    """
    Validate plugin name format.

    Returns:
        tuple: (is_valid, error_message)
    """
    if not name:
        return False, "Plugin name cannot be empty"

    if not is_kebab_case(name):
        return False, f"Plugin name must be in kebab-case (lowercase with hyphens). Got: {name}"

    return True, None


def load_template(template_name):
    """
    Load a template file.

    Args:
        template_name: Name of template file (without .template extension)

    Returns:
        str: Template content or empty string if not found
    """
    template_dir = Path(__file__).parent / "templates"
    template_path = template_dir / f"{template_name}.template"

    if template_path.exists():
        return template_path.read_text()

    return ""


def substitute_variables(content, variables):
    """
    Substitute template variables with actual values.

    Args:
        content: Template content
        variables: Dictionary of {variable_name: value}

    Returns:
        str: Content with variables substituted
    """
    result = content
    for key, value in variables.items():
        placeholder = f"{{{{{key}}}}}"
        if value is None:
            value = ""
        elif isinstance(value, list):
            value = "\n  - ".join([""] + [str(v) for v in value])
        result = result.replace(placeholder, str(value))
    return result


def create_plugin_directory_structure(plugin_path):
    """
    Create the standard plugin directory structure.

    Args:
        plugin_path: Path to plugin root directory

    Returns:
        dict: Paths to created directories
    """
    paths = {}

    # Create main directories
    plugin_path.mkdir(parents=True, exist_ok=True)

    # Create .claude-plugin directory
    claude_plugin_dir = plugin_path / ".claude-plugin"
    claude_plugin_dir.mkdir(parents=True, exist_ok=True)
    paths[".claude-plugin"] = claude_plugin_dir

    # Create component directories at plugin root
    for component in ["commands", "agents", "skills", "scripts", "docs"]:
        component_path = plugin_path / component
        component_path.mkdir(parents=True, exist_ok=True)
        paths[component] = component_path

    # Create .gitignore in .claude-plugin
    gitignore_path = claude_plugin_dir / ".gitignore"
    gitignore_path.write_text("*\n!.gitignore\n!plugin.json\n")

    return paths


def generate_manifest(plugin_name, author=None, description=None, version=None):
    """
    Generate plugin.json manifest.

    Args:
        plugin_name: Name of the plugin (kebab-case)
        author: Author name or None
        description: Plugin description or None
        version: Semantic version or None

    Returns:
        dict: Manifest data structure
    """
    manifest = {
        "name": plugin_name,
        "version": version or "1.0.0",
    }

    if description:
        manifest["description"] = description

    if author:
        manifest["author"] = {
            "name": author
        }

    return manifest


def create_manifest_file(plugin_path, manifest_data):
    """
    Write manifest file to .claude-plugin/plugin.json.

    Args:
        plugin_path: Path to plugin root
        manifest_data: Manifest dictionary

    Returns:
        Path: Path to created manifest file
    """
    manifest_path = plugin_path / ".claude-plugin" / "plugin.json"
    manifest_path.write_text(json.dumps(manifest_data, indent=2) + "\n")
    return manifest_path


def create_readme(plugin_path, plugin_name, description=None):
    """
    Create README.md for the plugin.

    Args:
        plugin_path: Path to plugin root
        plugin_name: Name of the plugin
        description: Plugin description or None

    Returns:
        Path: Path to created README file
    """
    readme_path = plugin_path / "README.md"

    content = f"# {plugin_name}\n\n"

    if description:
        content += f"{description}\n\n"

    content += """## Installation

To install this plugin in Claude Code:

```bash
claude plugins install ./{{plugin_path}}
```

## Usage

Add usage instructions and examples here.

## Development

This plugin was created using the Claude Code plugin scaffolding system.

### Structure

- `commands/` - Command definitions
- `agents/` - Agent definitions
- `skills/` - Skill implementations
- `scripts/` - Helper scripts
- `docs/` - Documentation
- `.claude-plugin/plugin.json` - Plugin manifest

## License

See LICENSE file for details.
"""

    readme_path.write_text(content)
    return readme_path


def create_component_template(plugin_path, component_type, component_name, description=None):
    """
    Create a template file for a component.

    Args:
        plugin_path: Path to plugin root
        component_type: Type of component (command, agent, skill)
        component_name: Name of the component
        description: Component description

    Returns:
        Path: Path to created template file
    """
    description = description or f"A {component_type} component"

    if component_type == "skill":
        # Skills go in subdirectories with SKILL.md
        skill_dir = plugin_path / "skills" / component_name
        skill_dir.mkdir(parents=True, exist_ok=True)
        template_path = skill_dir / "SKILL.md"

        template = load_template("skill.md")
        variables = {
            "name": component_name,
            "description": description,
            "allowed_tools": ["tool1", "tool2"]
        }
        content = substitute_variables(template, variables)
        template_path.write_text(content)
        return template_path

    else:
        # Commands and agents are files
        component_dir = plugin_path / f"{component_type}s"
        component_dir.mkdir(parents=True, exist_ok=True)

        # Convert component name to filename
        filename = component_name.replace(" ", "-").lower() + ".md"
        template_path = component_dir / filename

        template = load_template(f"{component_type}.md")
        variables = {
            "name": component_name,
            "description": description,
            "allowed_tools": ["tool1", "tool2"] if component_type == "command" else [],
            "tools": ["tool1", "tool2"] if component_type == "agent" else []
        }
        content = substitute_variables(template, variables)
        template_path.write_text(content)
        return template_path


def scaffold_plugin(plugin_name, plugin_path=None, author=None, description=None, version=None, components=None):
    """
    Main scaffolding function.

    Args:
        plugin_name: Name of the plugin (kebab-case)
        plugin_path: Base directory for plugin creation (defaults to current directory)
        author: Author name or None
        description: Plugin description or None
        version: Semantic version or None
        components: List of component types to create templates for

    Returns:
        dict: Information about created plugin structure
    """
    # Validate plugin name
    is_valid, error_msg = validate_plugin_name(plugin_name)
    if not is_valid:
        raise ValueError(error_msg)

    # Determine plugin root path
    if plugin_path is None:
        plugin_path = Path.cwd()
    else:
        plugin_path = Path(plugin_path)

    plugin_root = plugin_path / plugin_name

    # Check if directory exists with content
    if plugin_root.exists() and list(plugin_root.iterdir()):
        raise FileExistsError(f"Plugin directory already exists with content: {plugin_root}")

    # Create directory structure
    print(f"Creating plugin structure at {plugin_root}...")
    dirs = create_plugin_directory_structure(plugin_root)

    # Generate and write manifest
    print(f"Generating plugin.json manifest...")
    manifest = generate_manifest(plugin_name, author=author, description=description, version=version)
    manifest_path = create_manifest_file(plugin_root, manifest)

    # Create README
    print(f"Creating README.md...")
    readme_path = create_readme(plugin_root, plugin_name, description=description)

    # Create component templates if requested
    created_components = []
    if components:
        for component in components:
            component_type = component.strip().lower()
            if component_type in ["command", "agent", "skill"]:
                print(f"Creating {component_type} template...")
                template_path = create_component_template(
                    plugin_root,
                    component_type,
                    f"example-{component_type}",
                    f"Example {component_type}"
                )
                created_components.append((component_type, template_path))

    return {
        "plugin_name": plugin_name,
        "plugin_path": plugin_root,
        "manifest_path": manifest_path,
        "readme_path": readme_path,
        "component_paths": dirs,
        "component_templates": created_components
    }


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Create a new Claude Code plugin with proper structure and templates.",
        epilog="Example: python scaffold-plugin.py --name my-awesome-plugin --author 'John Doe' --description 'My awesome plugin' --version 1.0.0 --components command,agent,skill"
    )

    parser.add_argument(
        "--name",
        required=True,
        help="Plugin name (required, must be kebab-case like 'my-plugin')"
    )

    parser.add_argument(
        "--author",
        help="Plugin author name"
    )

    parser.add_argument(
        "--description",
        help="Plugin description"
    )

    parser.add_argument(
        "--version",
        default="1.0.0",
        help="Plugin version in semver format (default: 1.0.0)"
    )

    parser.add_argument(
        "--components",
        help="Comma-separated list of components to create templates for (command,agent,skill)"
    )

    parser.add_argument(
        "--output",
        help="Output directory for plugin (default: current directory)"
    )

    return parser.parse_args()


def main():
    """Main entry point."""
    try:
        args = parse_arguments()

        # Parse components
        components = None
        if args.components:
            components = [c.strip() for c in args.components.split(",")]

        # Scaffold the plugin
        result = scaffold_plugin(
            plugin_name=args.name,
            plugin_path=args.output,
            author=args.author,
            description=args.description,
            version=args.version,
            components=components
        )

        # Print success message
        print(f"\n✓ Plugin '{args.name}' scaffolded successfully!")
        print(f"\nPlugin location: {result['plugin_path']}")
        print(f"Manifest: {result['manifest_path']}")
        print(f"README: {result['readme_path']}")

        if result['component_templates']:
            print(f"\nComponent templates created:")
            for comp_type, comp_path in result['component_templates']:
                print(f"  - {comp_type.capitalize()}: {comp_path}")

        print(f"\nNext steps:")
        print(f"1. Edit .claude-plugin/plugin.json to add more details")
        print(f"2. Create your components in commands/, agents/, skills/")
        print(f"3. Add documentation to docs/")
        print(f"4. Test with: claude plugins validate ./{args.name}")
        print(f"5. Install with: claude plugins install ./{args.name}")

        return 0

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except FileExistsError as e:
        print(f"Error: {e}", file=sys.stderr)
        print(f"Use a different plugin name or delete the existing directory.", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
