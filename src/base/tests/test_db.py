from ..sql_db_manager import *
from ..models import *
from faker import Faker

faker = Faker()

def test_user_registering():
    with SQLiteDBManager('sqlite:///test.db') as db_mgr:
        credits = LoginCredits(
            username=faker.user_name(),
            password=faker.password()
        )
        db_mgr.register_user(credits)
        assert db_mgr.check_credits(credits)

def test_records_add():
    with SQLiteDBManager('sqlite:///test.db') as db_mgr:
        record1 = DecryptedRecord(
            uid=db_mgr.get_user_by_username('spy').id,
            service='Google',
            username='frenchman',
            password='qwerty',
            description=faker.paragraph()
        ).encrypt('qwerty')
        record2 = DecryptedRecord(
            uid=db_mgr.get_user_by_username('lauren60').id,
            service='Yandex',
            username='lauren2004',
            password='1234',
            description=faker.paragraph()
        ).encrypt('1234')
        db_mgr.add_record(record1)
        db_mgr.add_record(record2)
        r1 = db_mgr.get_records(1)[0]
        r2 = db_mgr.get_records(2)[0]
        rd1 = r1.decrypt('qwerty')
        rd2 = r2.decrypt('1234')
        assert rd1.password == 'qwerty'
        assert rd2.password == '1234'