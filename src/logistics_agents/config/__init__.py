"""
Configuration package for logistics agents.

This package handles all configuration management including:
- Application settings
- Environment variables
- OpenAI API configuration
- Data paths and output settings
"""

from .settings import settings

__all__ = ["settings"]
