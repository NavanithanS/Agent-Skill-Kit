"""Git utility functions for remote skill registries."""

import subprocess
from pathlib import Path

def get_cache_dir() -> Path:
    """Get the local cache directory for remote skills."""
    cache_dir = Path.home() / ".agents" / "cache" / "remotes"
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir

def parse_repo_url(source: str) -> str:
    """Parse shorthand 'org/repo' to 'https://github.com/org/repo.git' if needed."""
    if source.startswith("-"):
        raise ValueError("Invalid source URL: cannot start with '-'")
    if source.startswith("http://") or source.startswith("https://") or source.startswith("git@"):
        return source
    if "/" in source and len(source.split("/")) == 2:
        return f"https://github.com/{source}.git"
    return source

def get_repo_dir_name(url: str) -> str:
    """Generate a safe directory name for the cached repo."""
    # Convert https://github.com/org/repo.git to github_com_org_repo
    safe_name = url.replace("https://", "").replace("http://", "").replace("git@", "").replace(":", "_").replace("/", "_")
    if safe_name.endswith(".git"):
        safe_name = safe_name[:-4]
    return safe_name

def fetch_remote_skills(source: str) -> Path:
    """
    Fetch a remote repository and return the path to its directory.
    If it exists, pulls the latest. If not, clones it.
    """
    url = parse_repo_url(source)
    repo_name = get_repo_dir_name(url)
    target_dir = get_cache_dir() / repo_name
    
    if target_dir.exists():
        # Pull latest
        try:
            subprocess.run(["git", "pull"], cwd=str(target_dir), check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to pull latest from {url}: {e.stderr.decode('utf-8')}")
    else:
        # Clone
        try:
            subprocess.run(["git", "clone", url, str(target_dir)], check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to clone {url}: {e.stderr.decode('utf-8')}")
            
    return target_dir
