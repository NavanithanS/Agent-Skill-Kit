#!/usr/bin/env python3
import os
import sys
import re
import hashlib
import argparse
import subprocess
from pathlib import Path

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent
DIST_DIR = PROJECT_ROOT / "dist"
PYPROJECT_PATH = PROJECT_ROOT / "pyproject.toml"
DEFAULT_TAP_PATH = Path("/Users/nava/development/homebrew-Agent-Skill-Kit")

def get_version():
    """Extract version from pyproject.toml"""
    with open(PYPROJECT_PATH, "r") as f:
        content = f.read()
    match = re.search(r'version\s*=\s*"([^"]+)"', content)
    if not match:
        print("Error: Could not find version in pyproject.toml")
        sys.exit(1)
    return match.group(1)

def calculate_sha256(file_path):
    """Calculate SHA256 checksum of a file"""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def update_formula(tap_path, version, sha256, dry_run=False):
    """Update the Homebrew formula with new version and checksum"""
    formula_path = tap_path / "Formula" / "agent-skill-kit.rb"
    
    # Fallback to root if Formula dir doesn't exist
    if not formula_path.exists():
        formula_path = tap_path / "agent-skill-kit.rb"
        
    if not formula_path.exists():
        print(f"Error: Could not find agent-skill-kit.rb in {tap_path}")
        sys.exit(1)
        
    print(f"Updating formula at: {formula_path}")
    
    with open(formula_path, "r") as f:
        content = f.read()
        
    # Update URL
    # Assuming standard PyPI URL format
    new_url = f"https://pypi.io/packages/source/a/agent-skill-kit/agent_skill_kit-{version}.tar.gz"
    content = re.sub(r'url\s+"[^"]+"', f'url "{new_url}"', content)
    
    # Update SHA256
    content = re.sub(r'sha256\s+"[^"]+"', f'sha256 "{sha256}"', content)
    
    if dry_run:
        print("\n--- Dry Run: Formula Content ---")
        print(content)
        print("--------------------------------")
    else:
        with open(formula_path, "w") as f:
            f.write(content)
        print("Formula updated successfully.")

def git_commit_push(tap_path, version, dry_run=False):
    """Commit and push changes to the tap repository"""
    if dry_run:
        print(f"Dry Run: git -C {tap_path} commit -am 'Update agent-skill-kit to v{version}'")
        print(f"Dry Run: git -C {tap_path} push")
        return

    try:
        subprocess.run(["git", "-C", str(tap_path), "add", "."], check=True)
        subprocess.run(["git", "-C", str(tap_path), "commit", "-m", f"Update agent-skill-kit to v{version}"], check=True)
        subprocess.run(["git", "-C", str(tap_path), "push"], check=True)
        print("Successfully pushed changes to remote.")
    except subprocess.CalledProcessError as e:
        print(f"Error during git operations: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Update Homebrew Formula for Agent Skill Kit")
    parser.add_argument("--tap", type=Path, default=DEFAULT_TAP_PATH, help="Path to local Homebrew Tap repository")
    parser.add_argument("--dry-run", action="store_true", help="Print changes without modifying files")
    parser.add_argument("--push", action="store_true", help="Commit and push changes to the Tap repository")
    
    args = parser.parse_args()
    
    version = get_version()
    print(f"Detected version: {version}")
    
    tarball_name = f"agent_skill_kit-{version}.tar.gz"
    tarball_path = DIST_DIR / tarball_name
    
    if not tarball_path.exists():
        print(f"Error: Dist file not found at {tarball_path}")
        print("Did you run 'python -m build'?")
        sys.exit(1)
        
    sha256 = calculate_sha256(tarball_path)
    print(f"SHA256: {sha256}")
    
    if not args.tap.exists():
        print(f"Error: Tap repository not found at {args.tap}")
        sys.exit(1)
        
    update_formula(args.tap, version, sha256, dry_run=args.dry_run)
    
    if args.push:
        git_commit_push(args.tap, version, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
