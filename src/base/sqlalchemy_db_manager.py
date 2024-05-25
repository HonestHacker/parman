from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, select
from sqlalchemy.orm import declarative_base, Session
from .models import LoginCredits
from .secret_string import *
from db_manager import *

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    def __repr__(self) -> str:
        return f"User(ID{self.id}:{self.username}:{self.password})"

class Record(Base):
    __tablename__ = 'records'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    description = Column(String)
    description_secret = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey('authors.id'))

class SQLAlchemyDBManager(DBManager):
    def connect(self, uri: str) -> None:
        self.engine = create_engine(uri)
        self.session = Session(bind=self.engine)
    def register_user(self, profile: LoginCredits) -> None:
        exists = self.session.execute(
            select(User).where(User.username == profile.username)
        ).first()
        if exists:
            raise UserExists('the username is used.')
        db_profile = User(
            username=profile.username,
            password=SHA256String(profile.password).secret_value
        )
        self.session.add(db_profile)
        self.session.commit()
    def get_user_by_id(self, id: int) -> EncryptedLoginCredits:
        db_profile = self.session.query(User).get(id)
        if db_profile is None:
            return None
        profile = EncryptedLoginCredits(
            username=db_profile.username,
            password=SHA256String.from_hash(db_profile.password)
        )
        return profile
    def get_user_by_username(self, username: str) -> EncryptedLoginCredits:
        db_profile = self.session.execute(
            select(User).where(User.username == profile.username)
        ).first()
        profile = self.session.query()
    def close(self) -> None:
        return super().close()
    