from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy.orm
from datetime import datetime, timedelta
from hashlib import sha1
import uuid
from sqlalchemy.ext.hybrid import hybrid_property, Comparator
from .. import configuration
Base = declarative_base()


class Reservation(Base):
    __tablename__ = 'reservation'
    id          = Column(Integer, primary_key=True)
    date_from   = Column(DateTime)
    date_to     = Column(DateTime)
    robot_model = Column(String)
    robot_id    = Column(String)
