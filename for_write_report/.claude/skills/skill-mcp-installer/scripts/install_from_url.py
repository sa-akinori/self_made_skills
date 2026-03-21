#!/usr/bin/env python3
"""
Install a Claude Code skill from a URL.

This script downloads a .skill file from a URL and installs it to the
Claude Code skills directory.
"""

import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlparse


def get_skills_directory():
    """Get the Claude Code skills directory path."""
    home = Path.home()
    skills_dir = home / ".claude" / "skills"
    skills_dir.mkdir(parents=True, exist_ok=True)
    return skills_dir


def download_skill(url, output_path):
    """Download a skill file from a URL using curl."""
    try:
        result = subprocess.run(
            ["curl", "-L", "-o", str(output_path), url],
            check=True,
            capture_output=True,
            text=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error downloading skill: {e.stderr}", file=sys.stderr)
        return False


def install_skill(skill_file):
    """Install a skill file using the claude CLI."""
    try:
        result = subprocess.run(
            ["claude", "skill", "install", str(skill_file)],
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing skill: {e.stderr}", file=sys.stderr)
        return False
    except FileNotFoundError:
        print("Error: 'claude' command not found. Is Claude Code installed?", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Download and install a Claude Code skill from a URL"
    )
    parser.add_argument("url", help="URL of the .skill file to install")
    parser.add_argument(
        "--skill-name",
        help="Name of the skill (optional, extracted from URL if not provided)"
    )

    args = parser.parse_args()

    # Extract skill name from URL if not provided
    skill_name = args.skill_name
    if not skill_name:
        parsed_url = urlparse(args.url)
        filename = os.path.basename(parsed_url.path)
        if filename.endswith(".skill"):
            skill_name = filename[:-6]  # Remove .skill extension
        else:
            skill_name = filename

    print(f"Downloading skill: {skill_name}")
    print(f"URL: {args.url}")

    # Download to temporary file
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_skill_file = Path(temp_dir) / f"{skill_name}.skill"

        print(f"\nDownloading...")
        if not download_skill(args.url, temp_skill_file):
            sys.exit(1)

        print(f"Downloaded to: {temp_skill_file}")

        # Install the skill
        print(f"\nInstalling skill...")
        if not install_skill(temp_skill_file):
            sys.exit(1)

        print(f"\n✅ Successfully installed skill: {skill_name}")


if __name__ == "__main__":
    main()
