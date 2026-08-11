""""""
Database module for TrainPlex Document Intelligence Platform.
SQLAlchemy models and database manager for the document processing system.
"""

from .manager import DatabaseManager
from .models import Document, DocumentMetadata, ExtractedField, ProcessingLog, User

__all__ = ['DatabaseManager', 'Document', 'DocumentMetadata', 'ExtractedField', 'ProcessingLog', 'User']"""
