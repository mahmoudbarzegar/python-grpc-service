import base64

from django.contrib.auth.models import AbstractUser
from django.db import models
from typing import Optional
from cryptography.fernet import Fernet

from django.conf import settings

def _get_cipher() -> Fernet:
    """Return a Fernet cipher derived from Django SECRET_KEY."""
    
    key = settings.SECRET_KEY.encode()[:32].ljust(32, b"0")
    key = base64.urlsafe_b64encode(key)
    return Fernet(key)

class UserModel(AbstractUser):
    email = models.EmailField(unique=True)


class ExternalCredentialModel(models.Model):
    """
    Stores encrypted credentials for external systems
    (SMTP, APIs, services…)
    """

    service_name = models.CharField(max_length=100)
    username = models.CharField(max_length=255)
    encrypted_password = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # -------------------------------
    # Set encrypted password
    # -------------------------------
    def set_password(self, raw_password: Optional[str]) -> None:
        if not raw_password:
            self.encrypted_password = None
            return
        cipher = _get_cipher()
        self.encrypted_password = cipher.encrypt(raw_password.encode()).decode()

    # -------------------------------
    # Get decrypted password
    # -------------------------------
    def get_password(self) -> Optional[str]:
        if not self.encrypted_password:
            return None
        cipher = _get_cipher()
        return cipher.decrypt(self.encrypted_password.encode()).decode()

    def __str__(self) -> str:
        return f"{self.service_name} ({self.username})"