"""
Core utilities for IDP Enterprise Document Intelligence Platform.
"""

from .config import get_config, ConfigManager, safe_json_load, safe_json_save

__all__ = ['get_config', 'ConfigManager', 'safe_json_load', 'safe_json_save']
