"""Configuration management for logistics agents."""

import os
from pathlib import Path
from typing import Any, Optional

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings using Pydantic BaseSettings.

    This class handles all configuration for the logistics agents system,
    including OpenAI API settings, data paths, logging configuration,
    and optional MCP server settings.

    Settings are loaded from environment variables and .env files.
    """

    def __init__(self, **kwargs: Any) -> None:
        """Initialize settings with fresh .env file reload."""
        # Force reload .env file to get latest values every time
        load_dotenv(override=True)
        super().__init__(**kwargs)

        # OpenAI Configuration

    openai_api_key: str = "sk-placeholder-key"
    openai_model: str = "gpt-4o-mini"

    # Application Configuration
    log_level: str = "INFO"
    debug: bool = False

    # Logging Configuration
    log_truncate_agent_instructions: int = 0  # 0 = no truncation, >0 = max chars
    log_truncate_agent_input: int = 0  # 0 = no truncation, >0 = max chars
    log_truncate_agent_output: int = 0  # 0 = no truncation, >0 = max chars
    log_truncate_tool_output: int = 0  # 0 = no truncation, >0 = max chars
    log_truncate_tool_input: int = 0  # 0 = no truncation, >0 = max chars

    # Data Configuration
    data_path: Path = Path("./data/samples/inventory_sample_data.csv")
    output_path: Path = Path("./data/outputs/")

    # Optional MCP Server Configuration
    mcp_server_url: Optional[str] = None

    # Agent Configuration
    max_iterations: int = 5

    # Performance Configuration
    concurrent_agents: int = 3

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )

    def validate_paths(self) -> None:
        """
        Validate that required paths exist and create output directory if needed.

        Raises:
            FileNotFoundError: If data_path doesn't exist
            PermissionError: If cannot create output directory
        """
        if not self.data_path.exists():
            raise FileNotFoundError(f"Data file not found: {self.data_path}")

        # Create output directory if it doesn't exist
        self.output_path.mkdir(parents=True, exist_ok=True)

    def get_agent_config(self) -> dict:
        """
        Get common configuration for all agents.

        Returns:
            dict: Configuration dictionary for agent initialization
        """
        return {
            "model": self.openai_model,
            "api_key": self.openai_api_key,
            "debug": self.debug,
            "max_iterations": self.max_iterations,
        }

    def truncate_text(self, text: str, max_length: int, label: str = "") -> str:
        """
        Truncate text based on configuration.

        Args:
            text: Text to potentially truncate
            max_length: Maximum length (0 = no truncation)
            label: Label for logging context

        Returns:
            Original or truncated text
        """
        if max_length == 0 or len(text) <= max_length:
            return text
        return f"{text[:max_length]}... [TRUNCATED - {len(text)} total chars]"


def get_settings() -> Settings:
    """
    Get a fresh settings instance that reads from current environment/files.

    This function always returns a fresh settings instance with the latest
    .env file values, ensuring environment changes are picked up automatically.

    Returns:
        Settings: Fresh settings instance with current .env values
    """
    return Settings()


class AutoRefreshSettings:
    """
    A settings proxy that always returns fresh settings with current .env values.

    This ensures that any changes to the .env file are automatically picked up
    without requiring manual reloads or restart.
    """

    def __getattr__(self, name: str) -> Any:
        """Delegate all attribute access to a fresh Settings instance."""
        return getattr(get_settings(), name)

    def __call__(self) -> Settings:
        """Allow calling like settings() to get fresh instance."""
        return get_settings()


def reload_settings() -> None:
    """Reload the global settings instance from current environment/files."""
    # This function is now deprecated since settings auto-refresh
    # but kept for backwards compatibility
    pass


# Global settings instance that auto-refreshes .env values
# This ensures the latest .env file is always loaded automatically
settings = AutoRefreshSettings()

# Validate settings on import
try:
    settings.validate_paths()
except (FileNotFoundError, PermissionError) as e:
    if settings.debug:
        print(f"Settings validation warning: {e}")
    # Don't fail hard during import, let the application handle it
