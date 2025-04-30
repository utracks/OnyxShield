import base64
import hashlib
import os
from Crypto.Cipher import AES
from Crypto import Random
from typing import Optional

class AESEncryptor:
    def __init__(self, key: Optional[bytes] = None):
        self.bs = AES.block_size
        self.key = key or hashlib.sha256(os.urandom(32)).digest()

    def encrypt(self, raw: str) -> str:
        """Encrypt string with AES-256-CBC"""
        raw = self._pad(raw)
        iv = Random.new().read(self.bs)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode())).decode()

    def decrypt(self, enc: str) -> Optional[str]:
        """Decrypt AES-256-CBC encrypted string"""
        try:
            enc = base64.b64decode(enc)
            iv = enc[:self.bs]
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            return self._unpad(cipher.decrypt(enc[self.bs:])).decode('utf-8')
        except Exception:
            return None

    @staticmethod
    def _pad(s: str) -> str:
        return s + (AES.block_size - len(s) % AES.block_size) * chr(
            AES.block_size - len(s) % AES.block_size)

    @staticmethod
    def _unpad(s: bytes) -> bytes:
        return s[:-s[-1]]