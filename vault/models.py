from django.db import models
from django.contrib.auth.models import User
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

class PasswordEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    site_name = models.CharField(max_length=100)
    site_url = models.URLField(blank=True)
    username = models.CharField(max_length=100)
    encrypted_password = models.TextField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_fernet(self, master_password):
        user_salt = self.user.vaultsettings.salt
        salt_bytes = base64.b64decode(user_salt)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt_bytes,
            iterations=100_000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(
            kdf.derive((str(self.user.id) + master_password).encode())
        )
        return Fernet(key)

    def set_password(self, plain_password, master_password):
        fernet = self.generate_fernet(master_password)
        self.encrypted_password = fernet.encrypt(plain_password.encode()).decode()

    def get_password(self, master_password):
        fernet = self.generate_fernet(master_password)
        return fernet.decrypt(self.encrypted_password.encode()).decode()


class VaultSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    salt = models.CharField(max_length=24)

    def save(self, *args, **kwargs):
        if not self.salt:
            self.salt = base64.b64encode(os.urandom(16)).decode()
        super().save(*args, **kwargs)
