from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
import os
import base64

PRIVATE_KEY_PATH = "ledger_private.key"

def load_or_create_private_key():
    if os.path.exists(PRIVATE_KEY_PATH):
        with open(PRIVATE_KEY_PATH, "rb") as f:
            return serialization.load_pem_private_key(f.read(), password=None)

    key = Ed25519PrivateKey.generate()

    with open(PRIVATE_KEY_PATH, "wb") as f:
        f.write(
            key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
        )

    return key

def sign_data(data: str) -> str:
    key = load_or_create_private_key()
    signature = key.sign(data.encode())
    return base64.b64encode(signature).decode()
