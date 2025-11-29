"""
Test configuration and fixtures - DIVINE Testing
"""
import os
import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

# Set test environment variables BEFORE any imports
os.environ["AVA_API_DATABASE_URL"] = "postgresql+asyncpg://michaelamar@localhost:5432/avaai_test"
os.environ["AVA_API_ENVIRONMENT"] = "test"
os.environ["AVA_API_LOG_LEVEL"] = "DEBUG"
os.environ["AVA_API_JWT_SECRET_KEY"] = "test_secret_key_for_testing_only"
os.environ["AVA_API_VAPI_API_KEY"] = "test_vapi_key"
os.environ["INTEGRATIONS_STUB_MODE"] = "true"  # Enable stubs for testing
os.environ["CIRCUIT_BREAKER_ENABLED"] = "true"
os.environ["RATE_LIMIT_PER_MINUTE"] = "60"  # Higher limit for tests

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from api.src.core.app import create_app


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    # Mock database to avoid DB connection during tests that don't need it
    from unittest.mock import patch, MagicMock, AsyncMock
    from api.src.infrastructure.database.session import get_session
    
    # Create a mock engine with async context manager support
    mock_engine = MagicMock()
    mock_conn = AsyncMock()
    mock_engine.connect.return_value.__aenter__.return_value = mock_conn
    mock_engine.connect.return_value.__aexit__.return_value = None
    
    # Create a mock session
    async def mock_get_session():
        mock_session = AsyncMock()
        yield mock_session
    
    with patch("api.src.infrastructure.database.session.engine", mock_engine):
        app = create_app()
        # Override get_session dependency to avoid DB queries
        app.dependency_overrides[get_session] = mock_get_session
        
        with TestClient(app) as test_client:
            yield test_client
        
        app.dependency_overrides.clear()


@pytest.fixture
def mock_user():
    """Mock authenticated user for testing."""
    from unittest.mock import MagicMock
    user = MagicMock()
    user.id = "test_user_id"
    user.email = "test@example.com"
    user.vapi_api_key = "test-vapi-key"
    user.twilio_account_sid = "ACtest123456789"
    user.twilio_auth_token = "test-token-123"
    user.twilio_phone_number = "+15551234567"  # Set real value instead of MagicMock
    return user


def create_async_mock_dependency(return_value):
    """Helper to create an async dependency mock that works with FastAPI."""
    async def mock_dependency():
        return return_value
    return mock_dependency


@pytest.fixture
def client_with_mock_user(mock_user):
    """Create a test client with mocked authentication."""
    from unittest.mock import patch, MagicMock, AsyncMock
    from api.src.infrastructure.database.session import get_session
    from api.src.presentation.dependencies.auth import get_current_user
    
    # Create a mock engine with async context manager support
    mock_engine = MagicMock()
    mock_conn = AsyncMock()
    mock_engine.connect.return_value.__aenter__.return_value = mock_conn
    mock_engine.connect.return_value.__aexit__.return_value = None
    
    # Create a mock session
    async def mock_get_session():
        mock_session = AsyncMock()
        yield mock_session
    
    # Create async dependency for current user
    async def mock_get_current_user():
        return mock_user
    
    with patch("api.src.infrastructure.database.session.engine", mock_engine):
        app = create_app()
        # Override dependencies to avoid DB queries and auth
        app.dependency_overrides[get_session] = mock_get_session
        app.dependency_overrides[get_current_user] = mock_get_current_user
        
        with TestClient(app) as test_client:
            yield test_client
        
        app.dependency_overrides.clear()


# Register custom marks
def pytest_configure(config):
    config.addinivalue_line("markers", "integration: mark test as integration test")
    config.addinivalue_line("markers", "unit: mark test as unit test")
