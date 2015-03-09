from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.ext.declarative import declarative_base as Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    api_key = Column(String)
    api_key_expiration = Column(Date)

    def gen_api_key(self):
        return 'something'
