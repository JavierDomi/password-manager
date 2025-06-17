from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64

def derive_fernet_key_b64(user_id, master_password, salt):
    """
    Derives a base64 Fernet key from the user ID, master password, and salt.
    This key is saved in session and used in views to encrypt/decrypt.
    """
    salt_bytes = base64.b64decode(salt)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt_bytes,
        iterations=100_000,
        backend=default_backend()
    )
    key = kdf.derive((str(user_id) + master_password).encode())
    return base64.urlsafe_b64encode(key).decode()
