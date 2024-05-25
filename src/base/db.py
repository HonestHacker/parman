from .db_manager import *
from .sql_db_manager import *
from urllib.parse import urlparse

def connect(uri: str) -> DBManager:
    parsed_uri = urlparse(uri)
    match parsed_uri.scheme:
        case 'sqlite':
            return SQLiteDBManager(uri)
        case _:
            raise TypeError("unknown scheme of database")