"""
Database Connection Manager
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import QueuePool
from contextlib import contextmanager
import os

# Database URL configuration
DATABASE_URL = os.environ.get(
    'DATABASE_URL',
    'sqlite:///data/monitoring_sts.db'
)

# For PostgreSQL in production, use:
# DATABASE_URL = "postgresql://user:password@localhost:5432/monitoring_sts"


class DatabaseManager:
    """Singleton database connection manager"""
    _instance = None
    _engine = None
    _session_factory = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialize database engine and session factory"""
        connect_args = {}

        # SQLite specific settings
        if 'sqlite' in DATABASE_URL:
            connect_args = {"check_same_thread": False}

        self._engine = create_engine(
            DATABASE_URL,
            connect_args=connect_args,
            poolclass=QueuePool,
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True,
            echo=False
        )

        self._session_factory = sessionmaker(
            bind=self._engine,
            autocommit=False,
            autoflush=False
        )

    @property
    def engine(self):
        return self._engine

    @property
    def session_factory(self):
        return self._session_factory

    def get_session(self):
        """Get a new session"""
        return self._session_factory()

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations"""
        session = self._session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


# Global database manager instance
_db_manager = None


def get_db_manager():
    """Get the database manager instance"""
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager()
    return _db_manager


def get_db_engine():
    """Get database engine"""
    return get_db_manager().engine


def get_db_session():
    """Get a new database session"""
    return get_db_manager().get_session()


def get_scoped_session():
    """Get a scoped session for thread-safe operations"""
    return scoped_session(get_db_manager().session_factory)
