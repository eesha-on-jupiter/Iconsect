"""
Shared fixtures and path helpers for Iconsect MCP tests.
The sect-icon-generator subfolder has its own conftest.py that adds the server to sys.path.
"""
from pathlib import Path

# Root of the repo: tests/../
REPO_ROOT = Path(__file__).parent.parent

# Convenience paths to each MCP server directory
MCP_ROOT     = REPO_ROOT / "iconsect" / "mcps"
ICON_GEN_DIR = MCP_ROOT / "sect-icon-generator"
