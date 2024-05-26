from .models import LoginCredits, EncryptedLoginCredits
from .secret_string import *
from .db_manager import *
from urllib.parse import urlparse
from . import db_api
import sqlite3

class SQLDBManager(DBManager):
    def __init__(self, uri: str) -> None:
        self.marker = '?'
        self.queries = {
            'get_user_by_id' : '''SELECT * FROM users WHERE id = {m}''',
            'get_user_by_username' : '''SELECT * FROM users WHERE username = {m}''',
            'registering' : '''INSERT INTO users (username, password) VALUES ({m}, {m})''',
            'add_record' : '''INSERT INTO records (uid, service, username, password, description) VALUES ({m}, {m}, {m}, {m}, {m})''',
            'get_records' : '''SELECT * FROM records WHERE uid = {m}''',
            'update_record' : '''UPDATE records SET service = {m}, username = {m}, password = {m}, description = {m} WHERE id = {m}''',
            'delete_record' : '''DELETE FROM records WHERE id = {m}'''
        }
        super().__init__(uri)
    def connect(self, uri: str) -> None:
        self.connection = db_api.Connection()
        self.cursor = self.connection.cursor()
    def get_query(self, q: str) -> str:
        return self.queries[q].format(m=self.marker)
    def register_user(self, profile: LoginCredits) -> None:
        exists = self.get_user_by_username(profile.username)
        if exists:
            raise UserExists(f"the user with username '{profile.username}' exists!") 
        encrypted_profile = EncryptedLoginCredits(
            username=profile.username,
            password=SHA256String(profile.password)
        )
        self.cursor.execute(self.get_query('registering'), (encrypted_profile.username, str(encrypted_profile.password)))
    def get_user_by_id(self, id: int) -> EncryptedLoginCredits:
        self.cursor.execute(self.get_query('get_user_by_id'), (id,))
        db_profile = self.cursor.fetchone()
        if db_profile is None:
            return None
        profile = EncryptedLoginCredits(
            username=db_profile[1],
            password=SHA256String.from_hash(db_profile[2])
        )
        return profile
    def get_user_by_username(self, username: str) -> EncryptedLoginCredits:
        # TODO: delete copy-paste from get_user_by_id
        self.cursor.execute(self.get_query('get_user_by_username'), (username,))
        db_profile = self.cursor.fetchone()
        if db_profile is None:
            return None
        profile = EncryptedLoginCredits(
            username=db_profile[1],
            password=SHA256String.from_hash(db_profile[2]),
            id=db_profile[0]
        )
        return profile
    def check_credits(self, credits: LoginCredits) -> bool:
        encrypted_credits = EncryptedLoginCredits(
            username=credits.username,
            password=SHA256String(credits.password)
        )
        return self.get_user_by_username(credits.username) == encrypted_credits
    def add_record(self, record: Record) -> None:
        self.cursor.execute(
            self.get_query('add_record'),
            (
                record.uid,
                record.service,
                record.username,
                str(record.password),
                record.description,
            )
        )
    def get_records(self, uid: int) -> list[Record]:
        self.cursor.execute(self.get_query('get_records'), (uid,))
        db_records = self.cursor.fetchall()
        # Lisp-style :)
        records = list(
            map(
                lambda r: Record(
                    uid=r[1],
                    service=r[2],
                    username=r[3],
                    password=TwoFishEncryptedString.from_secret(r[4]),
                    description=r[5],
                    id=r[0]
                ), 
                db_records
            )
        )
        return records
    def update_record(self, record: Record) -> None:
        self.cursor.execute(
            self.get_query('update_record'),
            (
                record.service,
                record.username,
                str(record.password),
                record.description,
                record.id
            )
        )
    def delete_record(self, id: int) -> None:
        self.cursor.execute(self.get_query('delete_record'), (id,))
    def close(self) -> None:
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

class SQLiteDBManager(SQLDBManager):
    def connect(self, uri: str) -> None:
        path = urlparse(uri).path[1:]
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()

