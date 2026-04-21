"""Configuration management for TempIcon application."""

import json
import os
from pathlib import Path


class ConfigManager:
    """Manage application configuration."""

    DEFAULT_CONFIG = {
        "update_interval": 5,  # seconds
        "show_fahrenheit": False,
        "theme": "dark",
        "window_width": 400,
        "window_height": 300,
        "auto_start": True,
        "icon_style": "square",
        "temp_green_max": 50,  # Celsius - green if below this
        "temp_red_min": 80,  # Celsius - red if above this, amber in between
    }

    def __init__(self):
        self.config_dir = Path.home() / ".config" / "tempicon"
        self.config_file = self.config_dir / "config.json"
        self.config = self.load_config()

    def load_config(self):
        """Load configuration from file or create with defaults."""
        self.config_dir.mkdir(parents=True, exist_ok=True)

        if self.config_file.exists():
            try:
                with open(self.config_file, "r") as f:
                    config = json.load(f)
                    # Merge with defaults to handle new keys
                    merged = {**self.DEFAULT_CONFIG, **config}
                    return merged
            except (json.JSONDecodeError, IOError):
                return self.DEFAULT_CONFIG.copy()

        return self.DEFAULT_CONFIG.copy()

    def save_config(self):
        """Save current configuration to file."""
        self.config_dir.mkdir(parents=True, exist_ok=True)

        try:
            with open(self.config_file, "w") as f:
                json.dump(self.config, f, indent=2)
        except IOError as e:
            print(f"Error saving config: {e}")

    def get(self, key, default=None):
        """Get a configuration value."""
        return self.config.get(key, default)

    def set(self, key, value):
        """Set a configuration value."""
        self.config[key] = value
        self.save_config()

    def reset_to_defaults(self):
        """Reset configuration to defaults."""
        self.config = self.DEFAULT_CONFIG.copy()
        self.save_config()
