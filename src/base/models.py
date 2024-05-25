from dataclasses import dataclass
from .secret_string import *

@dataclass
class LoginCredits:
    username: str
    password: str
    id: int = -1

@dataclass
class EncryptedLoginCredits:
    username: str
    password: HashedString
    id: int = -1
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, EncryptedLoginCredits):
            return self.username == __value.username and self.password == __value.password
        return False

@dataclass
class Record:
    uid: int
    service: str
    username: str
    password: EncryptedString
    description: str
    id: int = -1
    def decrypt(self, key: str):
        decrypted_password = self.password.get_decrypted_value(key)
        print(decrypted_password)
        return DecryptedRecord(
            id=self.id,
            uid=self.uid,
            service=self.service,
            username=self.username,
            password=decrypted_password,
            description=self.description
        )

@dataclass
class DecryptedRecord:
    uid: int
    service: str
    username: str
    password: str
    description: str
    id: int = -1
    def encrypt(self, key: str):
        return DecryptedRecord(
            id=self.id,
            uid=self.uid,
            service=self.service,
            username=self.username,
            password=TwoFishEncryptedString(self.password, key),
            description=self.description
        )