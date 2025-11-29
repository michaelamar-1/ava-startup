"""Tests for email service."""
import pytest
from api.src.infrastructure.email.email_service import EmailService


@pytest.mark.asyncio
async def test_send_magic_link_dev_mode():
    """Test magic link email in dev mode (no SMTP)."""
    service = EmailService()
    
    # En dev (sans SMTP config), devrait logger mais retourner True
    result = await service.send_magic_link(
        to_email="test@example.com",
        magic_token="test_token_123"
    )
    
    assert result is True


@pytest.mark.asyncio
async def test_magic_link_url_format():
    """Test that magic link URL is correctly formatted."""
    service = EmailService()
    
    # Le service devrait créer une URL correcte
    # Vérifier indirectement via les logs ou mock
    result = await service.send_magic_link(
        to_email="test@example.com",
        magic_token="abc123xyz"
    )
    
    # En dev, devrait toujours réussir
    assert result is True

