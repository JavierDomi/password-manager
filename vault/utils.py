from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64

def derive_fernet_key(user_id, master_password, salt):
    """
    Deriva una clave Fernet a partir de user_id, master_password y salt.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=base64.b64decode(salt),
        iterations=100_000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(
        kdf.derive((str(user_id) + master_password).encode())
    )
    return Fernet(key)
