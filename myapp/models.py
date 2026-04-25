import base64

from django.contrib.auth.models import AbstractUser
from django.db import models
from typing import Any
from cryptography.fernet import Fernet

from django.conf import settings

class UserModel(AbstractUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    key_pass = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __init__(self,  *args:Any, **kwargs:Any):
        plain_password = kwargs.pop('password', None)
        super().__init__(args, **kwargs)
        if plain_password is not None:
            self.set_password(plain_password)
        print(f"Plain Password {plain_password}")

    def get_password(self) -> str | None:
        """Retrieve decrypted password"""
        if not self.password:
            return None
        return self._decrypt_password(self.password)
    

    def set_password(self, raw_password:str | None):
        """Encrypt and store password"""
        if not raw_password:
            self.password = None
        else:
            self.password = self._encrypt_password(raw_password)

        print(f"set_password {self}")


    def _encrypt_password(self, password:str) -> str:
        key = base64.urlsafe_b64encode(settings.SECRET_KEY.encode()[:32].ljust(32, b'0'))
        cipher = Fernet(key)
        return cipher.encrypt(password.encode()).decode()

    def _decrypt_password(self, encrypted_password:str) -> str:
        key = base64.urlsafe_b64encode(settings.SECRET_KEY.encode()[:32].ljust(32, b'0'))
        cipher = Fernet(key)
        return cipher.decrypt(encrypted_password.encode()).decode()

    def has_password(self):
        return self.password is not None



