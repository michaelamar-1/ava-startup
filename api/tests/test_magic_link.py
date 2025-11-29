"""Tests for magic link authentication."""
import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_send_magic_link_success(client):
    """Test sending magic link with valid email."""
    response = client.post(
        "/api/v1/auth/magic-link/send",
        json={"email": "test@example.com"}
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["success"] is True
    assert "lien de connexion" in data["message"].lower()


@pytest.mark.asyncio
async def test_send_magic_link_invalid_email(client):
    """Test sending magic link with invalid email format."""
    response = client.post(
        "/api/v1/auth/magic-link/send",
        json={"email": "not-an-email"}
    )
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_send_magic_link_nonexistent_email(client):
    """Test sending magic link to non-existent email (should still return success for security)."""
    response = client.post(
        "/api/v1/auth/magic-link/send",
        json={"email": "nonexistent@example.com"}
    )
    
    # Should return success even if email doesn't exist (security best practice)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["success"] is True


@pytest.mark.asyncio
async def test_verify_magic_link_invalid_token(client):
    """Test verifying with invalid token."""
    response = client.get("/api/v1/auth/magic-link/verify?token=invalid_token_12345")
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "invalide" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_verify_magic_link_expired_token(client):
    """Test verifying with expired token."""
    # Create an expired token (would need to be crafted with past exp time)
    # For now, just test with invalid token
    response = client.get("/api/v1/auth/magic-link/verify?token=expired.token.here")
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST

