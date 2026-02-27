from cryptography.fernet import Fernet
import base64, hashlib, os
from dotenv import load_dotenv

load_dotenv()

KEY = os.getenv("KEY")
if not KEY:
    raise RuntimeError("Faltou KEY no .env (ex: KEY=duka)")

def _k() -> bytes:
    return base64.urlsafe_b64encode(hashlib.sha256(KEY.encode("utf-8")).digest())

def encrypt(text: str) -> str:
    return Fernet(_k()).encrypt(text.encode("utf-8")).decode("utf-8")

def decrypt(token: str) -> str:
    return Fernet(_k()).decrypt(token.encode("utf-8")).decode("utf-8")