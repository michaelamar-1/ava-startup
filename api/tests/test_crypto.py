from cryptography.fernet import Fernet
import pytest

from api.src.core.crypto import EncryptionError, SymmetricEncryptor


def test_encrypt_decrypt_roundtrip():
    key = Fernet.generate_key()
    encryptor = SymmetricEncryptor(Fernet(key))  # ✅ CORRECTION: Wrap bytes in Fernet
    token = encryptor.encrypt("top-secret")
    assert token and token != "top-secret"
    assert encryptor.decrypt(token) == "top-secret"


def test_encrypt_without_key_raises():
    encryptor = SymmetricEncryptor(None)
    with pytest.raises(EncryptionError):
        encryptor.encrypt("value")


def test_decrypt_with_invalid_token():
    key = Fernet.generate_key()
    encryptor = SymmetricEncryptor(Fernet(key))  # ✅ CORRECTION: Wrap bytes in Fernet
    with pytest.raises(EncryptionError):
        encryptor.decrypt("not-valid-token")