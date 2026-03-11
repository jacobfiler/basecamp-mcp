"""Config file management for Basecamp MCP credentials."""

import json
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

CONFIG_DIR = Path.home() / ".config" / "basecamp-mcp"
CONFIG_FILE = CONFIG_DIR / "config.json"


def load_config() -> dict | None:
    """Load config from ~/.config/basecamp-mcp/config.json."""
    if not CONFIG_FILE.exists():
        return None
    try:
        return json.loads(CONFIG_FILE.read_text())
    except (json.JSONDecodeError, OSError) as e:
        logger.error(f"Failed to read config: {e}")
        return None


def save_config(config: dict) -> None:
    """Save config to ~/.config/basecamp-mcp/config.json."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(config, indent=2) + "\n")
    # Restrict permissions to owner only
    CONFIG_FILE.chmod(0o600)


def update_tokens(access_token: str, refresh_token: str | None = None) -> None:
    """Update tokens in existing config (called after refresh)."""
    config = load_config()
    if not config:
        logger.error("No config file to update tokens in")
        return
    config["access_token"] = access_token
    if refresh_token:
        config["refresh_token"] = refresh_token
    config["token_updated_at"] = datetime.now().isoformat()
    save_config(config)
