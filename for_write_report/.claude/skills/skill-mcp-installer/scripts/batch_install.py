#!/usr/bin/env python3
"""
Batch install Claude Code skills and MCP servers from a list file at project level.

This script reads install-skills.txt and installs all listed skills and MCP servers
in the current project directory.

Expected format:
  - Claude skills: skill <skill-name> <URL>
  - MCP servers: mcp <package-name> <type>
    where type is: npm, git, or python
"""

import argparse
import subprocess
import sys
from pathlib import Path
import os
import shutil
import json


def parse_install_list(file_path):
    """
    Parse the install-skills.txt file.

    Returns: Tuple of (skills_list, mcp_list)
      - skills_list: List of (skill_name, url) tuples
      - mcp_list: List of (package_name, install_type) tuples
    """
    skills = []
    mcps = []

    with open(file_path, 'r') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()

            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue

            # Split into parts
            parts = line.split(None, 2)  # Max 3 parts
            if len(parts) < 2:
                print(f"Warning: Skipping malformed line {line_num}: {line}", file=sys.stderr)
                continue

            item_type = parts[0].lower()

            if item_type == 'skill':
                # Format: skill <name> <URL>
                if len(parts) != 3:
                    print(f"Warning: Skipping malformed skill line {line_num}: {line}", file=sys.stderr)
                    continue
                skill_name, url = parts[1], parts[2]
                skills.append((skill_name, url))

            elif item_type == 'mcp':
                # Format: mcp <package> <type>
                if len(parts) != 3:
                    print(f"Warning: Skipping malformed MCP line {line_num}: {line}", file=sys.stderr)
                    continue
                package_name, install_type = parts[1], parts[2].lower()
                if install_type not in ['npm', 'git', 'python']:
                    print(f"Warning: Unknown MCP type '{install_type}' on line {line_num}", file=sys.stderr)
                    continue
                mcps.append((package_name, install_type))

            else:
                print(f"Warning: Unknown item type '{item_type}' on line {line_num}: {line}", file=sys.stderr)

    return skills, mcps


def install_skill(skill_name, url):
    """Install a single Claude skill to project's skills directory."""
    import tempfile

    # Create skills directory in project (.claude/skills/)
    skills_dir = Path.cwd() / ".claude" / "skills"
    skills_dir.mkdir(parents=True, exist_ok=True)

    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file = Path(temp_dir) / f"{skill_name}.skill"

            # Download the skill
            print(f"Downloading {skill_name} from {url}")
            result = subprocess.run(
                ["curl", "-L", "-o", str(temp_file), url],
                check=True,
                capture_output=True,
                text=True
            )

            # Extract the skill (it's a zip file)
            skill_extract_dir = skills_dir / skill_name
            skill_extract_dir.mkdir(exist_ok=True)

            print(f"Extracting to {skill_extract_dir}")
            result = subprocess.run(
                ["python3", "-m", "zipfile", "-e", str(temp_file), str(skill_extract_dir)],
                check=True,
                capture_output=True,
                text=True
            )

            print(f"✅ Successfully installed skill: {skill_name}")
            print(f"   Location: {skill_extract_dir}")
            return True

    except subprocess.CalledProcessError as e:
        print(f"Error installing {skill_name}: {e.stderr}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Error installing {skill_name}: {e}", file=sys.stderr)
        return False


def install_mcp_npm(package_name):
    """Install an MCP server from npm locally to project."""
    mcp_dir = Path.cwd() / "mcp-servers"
    mcp_dir.mkdir(exist_ok=True)

    try:
        # Check if already installed
        if package_name.startswith("@"):
            package_path = mcp_dir / "node_modules" / package_name
        else:
            package_path = mcp_dir / "node_modules" / package_name

        if package_path.exists():
            print(f"Package already installed: {package_name}")
            print(f"✅ Using existing npm package: {package_name}")
            print(f"   Location: {package_path}")
            return True

        print(f"Installing npm package: {package_name}")
        print(f"Target directory: {mcp_dir}")

        result = subprocess.run(
            ["npm", "install", package_name],
            cwd=str(mcp_dir),
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        print(f"✅ Successfully installed npm package: {package_name}")
        print(f"   Location: {mcp_dir / 'node_modules' / package_name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing npm package {package_name}: {e.stderr}", file=sys.stderr)
        return False
    except FileNotFoundError:
        print("Error: 'npm' command not found. Is Node.js installed?", file=sys.stderr)
        return False


def install_mcp_git(repo_url):
    """Install an MCP server from a git repository to project."""
    try:
        # Extract repo name from URL
        repo_name = repo_url.rstrip('/').split('/')[-1]
        if repo_name.endswith('.git'):
            repo_name = repo_name[:-4]

        # Create MCP servers directory in project
        mcp_dir = Path.cwd() / "mcp-servers"
        mcp_dir.mkdir(exist_ok=True)

        target_dir = mcp_dir / repo_name

        # Check if already installed
        if target_dir.exists() and (target_dir / ".git").exists():
            print(f"Repository already exists: {target_dir}")
            print(f"✅ Using existing git MCP server: {repo_name}")
            print(f"   Location: {target_dir}")
            return True

        print(f"Cloning repository: {repo_url}")
        print(f"Target directory: {target_dir}")

        # Clone the repository
        result = subprocess.run(
            ["git", "clone", repo_url, str(target_dir)],
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)

        # Install dependencies
        print(f"Installing dependencies in {target_dir}")
        result = subprocess.run(
            ["npm", "install"],
            cwd=str(target_dir),
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)

        print(f"✅ Successfully installed git MCP server: {repo_name}")
        print(f"   Location: {target_dir}")
        return True

    except subprocess.CalledProcessError as e:
        print(f"Error installing git MCP server {repo_url}: {e.stderr}", file=sys.stderr)
        return False
    except FileNotFoundError as e:
        print(f"Error: Command not found - {e}", file=sys.stderr)
        print("Ensure 'git' and 'npm' are installed.", file=sys.stderr)
        return False


def install_mcp_python(package_name):
    """Install an MCP server from Python package to project."""
    # Create python packages directory in project
    mcp_python_dir = Path.cwd() / "mcp-servers" / "python-packages"
    mcp_python_dir.mkdir(parents=True, exist_ok=True)

    try:
        print(f"Installing Python package: {package_name}")
        print(f"Target directory: {mcp_python_dir}")

        result = subprocess.run(
            ["pip", "install", "--target", str(mcp_python_dir), package_name],
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        print(f"✅ Successfully installed Python package: {package_name}")
        print(f"   Location: {mcp_python_dir}")
        return True

    except subprocess.CalledProcessError as e:
        print(f"Error installing Python package {package_name}: {e.stderr}", file=sys.stderr)
        return False
    except FileNotFoundError:
        print("Error: 'pip' command not found. Is Python installed?", file=sys.stderr)
        return False


def find_entry_point(server_path):
    """Find the entry point (index.js, server.js, etc.) for an MCP server.

    Returns: Tuple of (entry_point, command_type) where command_type is 'node' or 'python'
    """
    server_path = Path(server_path)

    # Check for Python MCP servers first
    python_entries = [
        server_path / f"{server_path.name}_server.py",
        server_path / f"{server_path.name.replace('-', '_')}_server.py",
        server_path / "src" / "server.py",
        server_path / "server.py",
    ]

    for entry in python_entries:
        if entry.exists():
            return (entry, "python")

    # Look for any *_server.py files in root
    for py_file in server_path.glob("*_server.py"):
        return (py_file, "python")

    # Check for Python package with __main__.py
    main_py_locations = [
        server_path / "src" / server_path.name.replace('-', '_') / "__main__.py",
        server_path / server_path.name.replace('-', '_') / "__main__.py",
    ]
    for main_py in main_py_locations:
        if main_py.exists():
            # Return the package directory for python -m execution
            return (main_py.parent, "python-module")

    # Common Node.js entry point locations
    possible_entries = [
        server_path / "dist" / "index.js",
        server_path / "build" / "index.js",
        server_path / "index.js",
        server_path / "src" / "index.js",
        server_path / "dist" / "server.js",
        server_path / "build" / "server.js",
        server_path / "server.js",
    ]

    for entry in possible_entries:
        if entry.exists():
            return (entry, "node")

    # Check for TypeScript source that needs building
    ts_sources = [
        server_path / "src" / "index.ts",
        server_path / "index.ts",
    ]
    for ts_file in ts_sources:
        if ts_file.exists():
            # Needs to be built first
            return (ts_file, "typescript")

    # If none found, check package.json
    package_json = server_path / "package.json"
    if package_json.exists():
        try:
            with open(package_json) as f:
                pkg_data = json.load(f)
                if "main" in pkg_data:
                    main_file = server_path / pkg_data["main"]
                    if main_file.exists():
                        return (main_file, "node")
                # Check bin field
                if "bin" in pkg_data:
                    if isinstance(pkg_data["bin"], str):
                        bin_file = server_path / pkg_data["bin"]
                        if bin_file.exists():
                            return (bin_file, "node")
                    elif isinstance(pkg_data["bin"], dict):
                        # Use first bin entry
                        for bin_path in pkg_data["bin"].values():
                            bin_file = server_path / bin_path
                            if bin_file.exists():
                                return (bin_file, "node")
        except:
            pass

    return (None, None)


def create_mcp_config(installed_mcps, project_dir):
    """Create project-level MCP configuration file."""
    if not installed_mcps:
        return

    # Create .mcp.json in project root (not .claude/mcp_config.json)
    mcp_config_file = project_dir / ".mcp.json"

    # Build configuration
    mcp_servers = {}

    for package, install_type, status in installed_mcps:
        if not status:  # Skip failed installations
            continue

        server_name = None
        entry_point = None
        command_type = None

        if install_type == "npm":
            # Extract package name
            if package.startswith("@"):
                # Scoped package
                server_name = package.split("/")[-1]
                server_path = project_dir / "mcp-servers" / "node_modules" / package
            else:
                server_name = package
                server_path = project_dir / "mcp-servers" / "node_modules" / package

            entry_point, command_type = find_entry_point(server_path)

        elif install_type == "git":
            # Extract repo name from URL
            repo_name = package.rstrip('/').split('/')[-1]
            if repo_name.endswith('.git'):
                repo_name = repo_name[:-4]

            server_name = repo_name
            server_path = project_dir / "mcp-servers" / repo_name
            entry_point, command_type = find_entry_point(server_path)

        elif install_type == "python":
            server_name = package
            # Python MCP servers installed via pip use uvx
            command_type = "python-uvx"
            entry_point = package  # Store package name

        if server_name:
            if install_type == "python" or command_type == "python-uvx":
                # Python package installed via pip - use uvx
                mcp_servers[server_name] = {
                    "command": "uvx",
                    "args": [package]
                }
            elif command_type == "python-module" and entry_point:
                # Python module - use python -m
                # entry_point is the package directory
                package_name = entry_point.name
                mcp_servers[server_name] = {
                    "command": "python",
                    "args": ["-m", package_name],
                    "env": {
                        "PYTHONPATH": str(entry_point.parent.absolute())
                    }
                }
            elif command_type == "python" and entry_point:
                # Python MCP server from git - use python directly
                mcp_servers[server_name] = {
                    "command": "python",
                    "args": [str(entry_point.absolute())]
                }
            elif command_type == "node" and entry_point:
                # Node.js MCP server
                mcp_servers[server_name] = {
                    "command": "node",
                    "args": [str(entry_point.absolute())]
                }
            elif command_type == "typescript":
                # TypeScript source that needs building
                print(f"Warning: {server_name} requires building TypeScript first")
                mcp_servers[server_name] = {
                    "command": "node",
                    "args": [f"<build-required-run-npm-build-first>"],
                    "_note": f"TypeScript project - run 'npm run build' in {server_name} directory first"
                }
            else:
                # Fallback: add with placeholder
                print(f"Warning: Could not find entry point for {server_name}")
                mcp_servers[server_name] = {
                    "command": "node",
                    "args": [f"<path-to-{server_name}/index.js>"],
                    "_note": "Please update the path to the correct entry point"
                }

    # Write configuration
    config = {
        "mcpServers": mcp_servers
    }

    with open(mcp_config_file, 'w') as f:
        json.dump(config, f, indent=2)

    print(f"\n✅ Created MCP configuration file: {mcp_config_file}")
    print(f"   Configuration contains {len(mcp_servers)} server(s)")

    return mcp_config_file


def main():
    parser = argparse.ArgumentParser(
        description="Batch install Claude Code skills and MCP servers at project level from install-skills.txt"
    )
    parser.add_argument(
        "file",
        nargs="?",
        default="install-skills.txt",
        help="Path to the install list file (default: install-skills.txt)"
    )

    args = parser.parse_args()
    file_path = Path(args.file)

    # Check if file exists
    if not file_path.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        print("\nExpected format of install-skills.txt:")
        print("# Claude Skills")
        print("skill skill-name-1 https://url.com/skill1.skill")
        print("skill skill-name-2 https://url.com/skill2.skill")
        print("\n# MCP Servers")
        print("mcp @scope/package-name npm")
        print("mcp https://github.com/user/repo.git git")
        print("mcp package-name python")
        sys.exit(1)

    # Parse the file
    print(f"Reading from: {file_path}\n")
    print(f"Installing to project directory: {Path.cwd()}\n")
    skills, mcps = parse_install_list(file_path)

    if not skills and not mcps:
        print("No skills or MCP servers found in the file.", file=sys.stderr)
        sys.exit(1)

    # Display what will be installed
    if skills:
        print(f"Found {len(skills)} Claude skill(s) to install:")
        for skill_name, url in skills:
            print(f"  - {skill_name}: {url}")
        print()

    if mcps:
        print(f"Found {len(mcps)} MCP server(s) to install:")
        for package, install_type in mcps:
            print(f"  - {package} ({install_type})")
        print()

    # Start installation
    print("=" * 60)
    print("Starting batch installation (PROJECT LEVEL)")
    print("=" * 60 + "\n")

    skill_success = 0
    skill_failed = 0
    mcp_success = 0
    mcp_failed = 0
    installed_mcps = []  # Track installed MCPs for config generation

    # Install Claude skills
    if skills:
        print("\n" + "=" * 60)
        print("Installing Claude Skills to .claude/skills/")
        print("=" * 60 + "\n")

        for idx, (skill_name, url) in enumerate(skills, 1):
            print(f"[{idx}/{len(skills)}] Installing: {skill_name}")
            print("-" * 60)

            if install_skill(skill_name, url):
                skill_success += 1
            else:
                skill_failed += 1
                print(f"❌ Failed to install: {skill_name}")
            print()

    # Install MCP servers
    if mcps:
        print("\n" + "=" * 60)
        print("Installing MCP Servers to ./mcp-servers/")
        print("=" * 60 + "\n")

        for idx, (package, install_type) in enumerate(mcps, 1):
            print(f"[{idx}/{len(mcps)}] Installing: {package} ({install_type})")
            print("-" * 60)

            success = False
            if install_type == 'npm':
                success = install_mcp_npm(package)
            elif install_type == 'git':
                success = install_mcp_git(package)
            elif install_type == 'python':
                success = install_mcp_python(package)

            # Track installation result
            installed_mcps.append((package, install_type, success))

            if success:
                mcp_success += 1
            else:
                mcp_failed += 1
                print(f"❌ Failed to install: {package}")
            print()

    # Summary
    print("\n" + "=" * 60)
    print("Installation Summary")
    print("=" * 60)

    if skills:
        print(f"\nClaude Skills:")
        print(f"  ✅ Successful: {skill_success}")
        print(f"  ❌ Failed: {skill_failed}")
        print(f"  📦 Total: {len(skills)}")
        print(f"  📁 Location: .claude/skills/")

    if mcps:
        print(f"\nMCP Servers:")
        print(f"  ✅ Successful: {mcp_success}")
        print(f"  ❌ Failed: {mcp_failed}")
        print(f"  📦 Total: {len(mcps)}")
        print(f"  📁 Location: ./mcp-servers/")

    print(f"\n📦 Grand Total: {len(skills) + len(mcps)} items")
    print(f"🗂️  Project Directory: {Path.cwd()}")

    # Create project-level MCP configuration
    if mcp_success > 0:
        print("\n" + "=" * 60)
        print("Creating Project-Level MCP Configuration")
        print("=" * 60)

        try:
            config_file = create_mcp_config(installed_mcps, Path.cwd())
            print(f"\n✅ MCP configuration created successfully!")
            print(f"   The MCP servers are now configured at project level.")
            print(f"\n⚠️  IMPORTANT: To use installed tools, you MUST restart the session:")
            print(f"   1. Exit this session: Type /exit")
            print(f"   2. Resume the session: Run 'claude -r' (or 'claude --resume')")
            print(f"   3. Verify installation:")
            print(f"      - Type /mcp to see MCP servers")
            print(f"      - Type /skills to see Claude skills")
            print(f"\n   Note: Tools are only loaded at session startup.")
        except Exception as e:
            print(f"\n⚠️  Warning: Failed to create MCP configuration: {e}")
            print(f"   You may need to manually configure MCP servers in:")
            print(f"   ~/.claude/claude_desktop_config.json")

    if skill_failed > 0 or mcp_failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
