from . import db
from .models import *
import traceback
import sys

bad_request = {
    'status' : 400,
    'msg' : "Bad request."
}

user_exists = {
    'status' : 409,
    'msg' : "The user exists."
}

created = {
    'status' : 201,
    'msg' : 'Created.'
}

forbidden = {
    'status' : 403,
    'msg' : "Forbidden."
}

ok = {
    'status' : 200,
    'msg' : 'OK.'
}

def internal_server_error(msg: str):
    return {
        'status' : 500,
        'msg' : 'Internal Server Error: ' + msg
    }

class MainHandler:
    def __init__(self, db_uri: str) -> None:
        self.db_uri = db_uri
    def register_user(self, q: dict) -> dict:
        try:
            user = LoginCredits(**q)
        except TypeError as e:
            return bad_request
        try:
            with db.connect(self.db_uri) as mgr:
                mgr.register_user(user)
        except db.UserExists:
            return user_exists
        except Exception as e:
            return internal_server_error(traceback.format_exc())
        return user_exists
    def login(self, q: dict) -> dict:
        try:
            user = LoginCredits(**q)
        except TypeError as e:
            return bad_request
        try:
            with db.connect(self.db_uri) as mgr:
                is_valid_credits = mgr.check_credits(user)
        except Exception as e:
            return internal_server_error(traceback.format_exc())
        if not is_valid_credits:
            return forbidden
        return ok
    def add_record(self, q: dict) -> dict:
        try:
            user = LoginCredits(
                username=q['credits']['username'],
                password=q['credits']['password']
            )
            with db.connect(self.db_uri) as mgr:
                is_valid_credits = mgr.check_credits(user)
                if not is_valid_credits:
                    return forbidden
                record = DecryptedRecord(
                    uid=mgr.get_user_by_username(user.username).id,
                    service=q['record']['service'],
                    username=q['record']['username'],
                    password=q['record']['password'],
                    description=q['record']['description']
                ).encrypt(user.password)
                mgr.add_record(record)
        except (TypeError, KeyError) as e:
            return bad_request
        except Exception as e:
            return internal_server_error(traceback.format_exc())
        return created
    def get_records(self, q: dict) -> dict:
        try:
            user = LoginCredits(
                username=q['username'],
                password=q['password']
            )
            records = []
            with db.connect(self.db_uri) as mgr:
                is_vaild_credits = mgr.check_credits(user)
                if not is_vaild_credits:
                    return forbidden
                records = mgr.get_records(mgr.get_user_by_username(user.username).id)
                records = map(lambda x: x.decrypt(user.password), records)
        except (TypeError, KeyError) as e:
            return bad_request
        except Exception as e:
            return internal_server_error(traceback.format_exc())
        response = ok.copy()
        response['records'] = records
        return response
    def get_record_by_id(self, q: dict) -> dict:
        try:
            user = LoginCredits(
                username=q['username'],
                password=q['password']
            )
            records = []
            with db.connect(self.db_uri) as mgr:
                is_vaild_credits = mgr.check_credits(user)
                if not is_vaild_credits:
                    return forbidden
                records = mgr.get_records(mgr.get_user_by_username(user.username).id)
                record = list(filter(lambda r: r.id == q['id'], map(lambda x: x.decrypt(user.password), records)))[0]
                print(record, file=sys.stderr)
        except (TypeError, KeyError) as e:
            return bad_request
        except Exception as e:
            return internal_server_error(traceback.format_exc())
        response = ok.copy()
        response['record'] = record
        return response
    def edit_record(self, q: dict):
        try:
            user = LoginCredits(
                username=q['credits']['username'],
                password=q['credits']['password']
            )
            with db.connect(self.db_uri) as mgr:
                is_valid_credits = mgr.check_credits(user)
                if not is_valid_credits:
                    return forbidden
                record = DecryptedRecord(
                    uid=mgr.get_user_by_username(user.username).id,
                    service=q['record']['service'],
                    username=q['record']['username'],
                    password=q['record']['password'],
                    description=q['record']['description'],
                    id=q['record']['id']
                ).encrypt(user.password)
                mgr.update_record(record)
        except (TypeError, KeyError) as e:
            return bad_request
        except Exception as e:
            return internal_server_error(traceback.format_exc())
        return ok
    def delete_record(self, q):
        try:
            user = LoginCredits(
                username=q['credits']['username'],
                password=q['credits']['password']
            )
            with db.connect(self.db_uri) as mgr:
                is_valid_credits = mgr.check_credits(user)
                if not is_valid_credits:
                    return forbidden
                mgr.delete_record(q['record']['id'])
        except (TypeError, KeyError) as e:
            return bad_request
        except Exception as e:
            return internal_server_error(traceback.format_exc())
        return ok