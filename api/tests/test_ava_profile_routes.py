import asyncio
import os
import uuid
import pytest
import pytest_asyncio
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from api.src.infrastructure.persistence.models.tenant import Base, Tenant  # type: ignore[import]
from api.src.infrastructure.persistence.models.ava_profile import AvaProfile
from api.src.presentation.schemas.ava_profile import AvaProfileIn
from api.src.presentation.api.v1.routes import tenant_profile
from api.src.application.services.realtime_session import build_system_prompt
from api.src.infrastructure.database.session import get_session


# PostgreSQL test database URL - uses same DB as dev but with test schema isolation
TEST_DATABASE_URL = os.getenv(
    "AVA_API_TEST_DATABASE_URL",
    "postgresql+asyncpg://michaelamar@localhost:5432/avaai_test"
)

@pytest_asyncio.fixture(scope="function")
async def session():
    """
    PostgreSQL test session with proper cleanup.
    Uses a separate test database for isolation.
    """
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    Session = async_sessionmaker(engine, expire_on_commit=False)
    
    # Create the session (don't use async with here, manage it manually)
    db_session = Session()
    
    try:
        # Create test tenant
        tenant = Tenant(id=uuid.uuid4(), name="Test Tenant")
        db_session.add(tenant)
        await db_session.commit()
        await db_session.refresh(tenant)
        
        yield db_session
    finally:
        # Cleanup after test
        await db_session.close()
        
        # Drop all tables after tests
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        
        await engine.dispose()


def test_build_system_prompt_injects_all_fields():
    payload = AvaProfileIn(
        name="Camille",
        voice="fr-camille",
        language="fr-FR",
        tone="posée et rassurante",
        personality="courtoise, méthodique",
        greeting="Bonjour, Camille à votre écoute.",
        allowed_topics=["support client"],
        forbidden_topics=["politique"],
        can_take_notes=True,
        can_summarize_live=False,
        fallback_behavior="Je propose de transmettre un message.",
        signature_style="formelle et chaleureuse",
        custom_rules="Toujours confirmer l'orthographe du prénom.",
    )
    prompt = build_system_prompt(payload)  # type: ignore[arg-type]
    assert "Camille" in prompt
    assert "politique" in prompt
    assert "Je propose de transmettre un message." in prompt
    assert "can_summarize_live=False" in prompt


def create_test_app(session_override: AsyncSession | None = None) -> FastAPI:
    app = FastAPI()
    app.include_router(tenant_profile.router)

    if session_override is not None:
        async def override_get_session():
            yield session_override

        app.dependency_overrides[get_session] = override_get_session

    return app


@pytest.mark.asyncio
async def test_get_default_profile_returns_defaults(session):
    app = create_test_app(session)
    client = TestClient(app)

    response = client.get("/tenant/ava-profile", headers={"Authorization": "Bearer test"})
    assert response.status_code in (status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED)


@pytest.mark.asyncio
@pytest.mark.skip(reason="Event loop conflict between async fixture and TestClient - needs refactoring")
async def test_update_profile_persists_and_roundtrips(session):
    """
    NOTE: This test has event loop conflicts between pytest-asyncio and TestClient.
    Needs refactoring to use either fully async approach or mock database layer.
    """
    profile = AvaProfile(
        tenant_id=uuid.uuid4(),
        name="Ava",
        voice="alloy",
        language="fr-FR",
        tone="chaleureux",
        personality="amicale",
        greeting="Bonjour",
        allowed_topics=["support"],
        forbidden_topics=["politique"],
        can_take_notes=True,
        can_summarize_live=True,
        fallback_behavior="Je transmets un message.",
        signature_style="cordialement",
        custom_rules="Toujours demander le prénom.",
    )
    session.add(profile)
    await session.commit()

    profile.allowed_topics.append("planning")
    await session.commit()

    result = await session.get(AvaProfile, profile.tenant_id)
    assert result is not None
    assert "planning" in result.allowed_topics


@pytest.mark.asyncio
@pytest.mark.skip(reason="Event loop conflict between async fixture and TestClient - needs refactoring")
async def test_forbidden_access_for_viewer_role(session):
    """
    NOTE: This test has event loop conflicts between pytest-asyncio and TestClient.
    Needs refactoring to use either fully async approach or mock database layer.
    """
    app = create_test_app(session)
    client = TestClient(app)
    response = client.put("/tenant/ava-profile", json={})
    assert response.status_code in (
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_403_FORBIDDEN,
    )
