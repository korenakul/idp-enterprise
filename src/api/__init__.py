"""
API module for IDP Enterprise Document Intelligence Platform.
"""

from .routes import router
from .server import create_app

__all__ = ['router', 'create_app']
