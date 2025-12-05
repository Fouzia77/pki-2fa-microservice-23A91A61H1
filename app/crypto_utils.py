import base64
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization

# ... your existing load_private_key and decrypt_seed above ...


def load_public_key(path: str = "instructor_public.pem"):
    """
    Load RSA public key from PEM file.
    """
    key_path = Path(path)
    if not key_path.exists():
        raise FileNotFoundError(f"{path} not found in project root")

    public_key = serialization.load_pem_public_key(
        key_path.read_bytes()
    )
    return public_key


def sign_message(message: str, private_key) -> bytes:
    """
    Sign a message using RSA-PSS with SHA-256.

    - Message is treated as ASCII/UTF-8 string
    - Uses PSS padding with MGF1(SHA-256) and maximum salt length
    """
    message_bytes = message.encode("utf-8")  # CRITICAL: ASCII/UTF-8 of hex string

    signature = private_key.sign(
        message_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )
    return signature


def encrypt_with_public_key(data: bytes, public_key) -> bytes:
    """
    Encrypt data using RSA/OAEP with SHA-256 (instructor public key).

    - Padding: OAEP
    - MGF: MGF1(SHA-256)
    - Hash: SHA-256
    - Label: None
    """
    ciphertext = public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return ciphertext