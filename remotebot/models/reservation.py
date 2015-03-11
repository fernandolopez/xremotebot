from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy import or_, and_
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy.orm
from datetime import datetime, timedelta
from hashlib import sha1
import uuid
from sqlalchemy.ext.hybrid import hybrid_property, Comparator
from .. import configuration
from .user import User
from ..lib.db import Base

class Reservation(Base):
    __tablename__ = 'reservations'
    id          = Column(Integer, primary_key=True)
    date_from   = Column(DateTime)
    date_to     = Column(DateTime)
    robot_model = Column(String)
    robot_id    = Column(String)
    user_id     = Column(Integer, ForeignKey('users.id'))
    user        = sqlalchemy.orm.relation(User, backref='reservations')

    @classmethod
    def reserved(cls, robot_model, date_from, date_to, session):
        reservations = session.query(Reservation).filter(
            Reservation.robot_model == robot_model,
        ).filter(
            or_(
                and_(date_from >= Reservation.date_from,
                     date_from <  Reservation.date_to),

                and_(date_to   <= Reservation.date_to,
                     date_to   >  Reservation.date_from),

                and_(date_from <= Reservation.date_from,
                     date_to   >= Reservation.date_to)
           )
        )

        return reservations.all()

    @classmethod
    def reserve(cls, robot_model, date_from, date_to, session):
        res = cls.reserved(robot_model, date_from, date_to, session)
        if len(res) > 0:
            # If the robot is reserved return None
            return None

        reservation = cls(robot_model=robot_model,
                          date_from=date_from,
                          date_to=date_to)
        session.add(reservation)
        session.commit()
        return reservation
