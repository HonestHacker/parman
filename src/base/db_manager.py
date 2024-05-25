from .models import LoginCredits
from typing_extensions import Self
from .models import *

class UserExists(Exception):
    pass

class DBManager:
    def __init__(self, uri: str) -> None:
        self.uri = uri
    def __enter__(self) -> Self:
        self.connect(self.uri)
        return self
    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        self.close()
    def connect(self, uri: str) -> None:
        pass
    def register_user(self, profile: LoginCredits) -> None:
        raise NotImplemented
    def get_user_by_id(self, id: int) -> EncryptedLoginCredits:
        raise NotImplemented
    def get_user_by_username(self, username: str) -> EncryptedLoginCredits:
        raise NotImplemented
    def check_credits(self, credits: LoginCredits) -> bool:
        raise NotImplemented
    def add_record(self, record: Record) -> None:
        raise NotImplemented
    def get_records(self, username: str) -> list[Record]:
        raise NotImplemented
    def update_record(self, uid: int, new_record: Record) -> None:
        raise NotImplemented
    def delete_record(self, uid: int) -> None:
        raise NotImplemented
    def close(self) -> None:
        pass