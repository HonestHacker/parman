from hashlib import sha256
from twofish import Twofish
from typing_extensions import Self
import base64

class SecretString:
    secret_value: str
    def __repr__(self) -> str:
        return f'SECRET!:{type(self).__name__}({self.secret_value})'
    def __str__(self) -> str:
        return self.secret_value
    def set_secret_value(self, value: str):
        raise NotImplemented
    @classmethod
    def from_secret(cls, secret: str):
        obj = object.__new__(cls)
        obj.secret_value = secret
        return obj

class EncryptedString(SecretString):
    def __init__(self, value: str, key: str):
        self.set_secret_value(value, key)
    def set_secret_value(self, value: str, key: str):
        self.secret_value = self.encrypt(value, key)
    def get_decrypted_value(self, key: str) -> str:
        return self.decrypt(self.secret_value, key)
    @classmethod
    def encrypt(cls, value: str, key: str) -> str:
        raise NotImplemented
    @classmethod
    def decrypt(cls, value: str, key: str) -> str:
        raise NotImplemented

class TwoFishEncryptedString(EncryptedString):
    BLOCK_SIZE = 16
    @classmethod
    def encrypt(cls, value: str, key: str) -> str:
        T = Twofish(key.encode())
        encrypted_value = b''
        value_bytes = value.encode()
        value_bytes += b'\x00' * (cls.BLOCK_SIZE - (len(value_bytes) % cls.BLOCK_SIZE))
        iterations = len(value_bytes) // cls.BLOCK_SIZE
        for i in range(iterations):
            encrypted_value += T.encrypt(value_bytes[cls.BLOCK_SIZE * i:(i + 1) * cls.BLOCK_SIZE])
        return base64.b64encode(encrypted_value).decode()
    @classmethod
    def decrypt(cls, value: str, key: str) -> str:
        T = Twofish(key.encode())
        decrypted_value = b''
        encrypted_value = base64.b64decode(value)
        iterations = len(encrypted_value) // cls.BLOCK_SIZE
        for i in range(iterations):
            decrypted_value += T.decrypt(encrypted_value[cls.BLOCK_SIZE * i:(i + 1) * cls.BLOCK_SIZE])
        return decrypted_value.replace(b'\x00', b'').decode()

class HashedString(SecretString):
    def __init__(self, value: str):
        self.set_secret_value(value)
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, str):
            return self.hash(__value) == self.secret_value
        elif isinstance(__value, type(self)):
            return self.secret_value == __value.secret_value
        return False
    def set_secret_value(self, value: str):
        self.secret_value = self.hash(value)
    @classmethod
    def from_hash(cls, hash: str):
        hashed_string = cls('Nothing')
        hashed_string.secret_value = hash
        return hashed_string
    @classmethod
    def hash(cls, value: str) -> str:
        raise NotImplemented

class SHA256String(HashedString):
    @classmethod
    def hash(cls, value: str) -> str:
        return sha256(value.encode()).hexdigest()