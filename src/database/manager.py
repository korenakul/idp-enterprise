"""
Database manager for TrainPlex Document Intelligence Platform.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from typing import Dict, Any, Optional
from contextlib import contextmanager
import logging

logger = logging.getLogger('trainplex.database.manager')


class DatabaseManager:
    """Manage database connections and operations."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.db_type = config.get('type', 'postgresql')
        self.host = config.get('host', 'localhost')
        self.port = config.get('port', 5432)
        self.name = config.get('name', 'trainplex_dip')
        self._engine = None
        self._session = None
    
    def connect(self):
        """Connect to database."""
        url = f"{self.db_type}://{self.host}:{self.port}/{self.name}"
        self._engine = create_engine(url, pool_size=10)
        self._session = scoped_session(sessionmaker(bind=self._engine))
        return self
    
    @contextmanager
    def session_scope(self):
        """Provide transaction scope."""
        session = self._session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
    
    def get_session(self):
        """Get database session."""
        return self._session()
    
    def close(self):
        """Close database connection."""
        if self._session:
            self._session.remove()
        if self._engine:
            self._engine.dispose()
