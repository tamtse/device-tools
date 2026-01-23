import os
from unittest.mock import AsyncMock
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

# Set test environment variables before any imports
# This ensures Settings class can initialize during test collection
# Allows override via environment variable (useful for CI/CD)
os.environ.setdefault(
    "DATABASE_URL",
    "postgresql://test:test@localhost:5432/test_db"
)


@pytest.fixture
def mock_db_session():
    """Create a mock async database session for testing."""
    session = AsyncMock(spec=AsyncSession)
    session.commit = AsyncMock()
    session.add = AsyncMock()
    session.rollback = AsyncMock()
    session.close = AsyncMock()
    return session


@pytest.fixture
def override_get_db(mock_db_session):
    """Override the get_db dependency with a mock session."""
    from app.main import app
    from app.db.session import get_db
    
    async def _get_db():
        yield mock_db_session
    
    app.dependency_overrides[get_db] = _get_db
    yield
    app.dependency_overrides.clear()
