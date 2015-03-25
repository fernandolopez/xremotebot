from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy.orm
from datetime import datetime, timedelta
from hashlib import sha1
import uuid
from sqlalchemy.ext.hybrid import hybrid_property, Comparator
from .. import configuration
from ..lib import db


class _PasswordHashedComparator(Comparator):
    def __init__(self, password_hashed):
        self.password_hashed = password_hashed

    def __eq__(self, other):
        return self.password_hashed == sha1(other.encode()).hexdigest()

class UsernameAlreadyTaken(Exception):
    pass


class User(db.Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password_hashed = Column(String)
    api_key = Column(String)
    api_key_expiration = Column(DateTime)

    @hybrid_property
    def password(self):
        raise NotImplementedError("Comparison only supported via the database")

    @password.setter
    def password(self, value):
        self.password_hashed = sha1(value.encode()).hexdigest()

    @password.comparator
    def password(cls):
        return _PasswordHashedComparator(cls.password_hashed)

    @classmethod
    def login(cls, username, password, session=None):
        session = db.get_session(session)
        try:
            user = session.query(User).filter(User.username == username)\
                                      .filter(User.password == password).one()
        except sqlalchemy.orm.exc.NoResultFound:
            return None

        session.commit()
        return user

    @classmethod
    def create(cls, username, password, session=None):
        session = db.get_session(session)
        user = session.query(User).filter(User.username == username).all()
        if len(user) > 0:
            raise UsernameAlreadyTaken(username)
        user = User(username=username, password=password)
        user.renew_api_key()
        session.add(user)
        session.commit()
        return user

    @classmethod
    def with_api_key(cls, api_key, session=None):
        session = db.get_session(session)
        try:
            user = session.query(User).filter(User.api_key == api_key).one()
        except sqlalchemy.orm.exc.NoResultFound:
            user = None
        else:
            if user.api_key_expired():
                user = None
        session.commit()
        return user

    def api_key_expired(self):
        return self.api_key_expiration - datetime.now() < timedelta()

    def renew_api_key(self):
        self.api_key_expiration =\
            datetime.now() + configuration.api_key_expiration
        self.api_key = str(uuid.uuid4())
        return self.api_key

#    def reserve_any(self):

