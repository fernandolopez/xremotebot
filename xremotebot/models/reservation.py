from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy import or_, and_
import sqlalchemy.orm
from datetime import timedelta
from datetime import datetime
from .. import configuration
from ..lib.db import Base, get_session


class Reservation(Base):
    __tablename__ = 'reservations'
    id          = Column(Integer, primary_key=True)
    date_from   = Column(DateTime)
    date_to     = Column(DateTime)
    robot_model = Column(String)
    robot_id    = Column(String)

    @classmethod
    def reserve(cls, robot_model, robot_id, time=None, session=None):
        '''Creates a reservation for a robot starting in the current time and
        ending in the time given by the time argument'''
        session = get_session(session)
        date_from = datetime.now()
        # FIXME: Use the time parameter
        date_to = datetime.now() + timedelta(seconds=120)
        if date_to is None:
            date_to = date_from + configuration.reservation_expiration

        if (robot_model, str(robot_id)) not in cls.available():
            return None
            print "reservation fail"

        reservation = cls(robot_model=robot_model,
                          robot_id=robot_id,
                          date_from=date_from,
                          date_to=date_to)
        session.add(reservation)

        session.commit()
        return reservation

    @classmethod
    def release(cls, reservation_id, session=None):
        '''Release a reservation for a robot'''
        session = get_session(session)
        session.query(Reservation).filter_by(id=reservation_id).delete()
        session.commit()

    @classmethod
    def available(cls, all_robots=None, now=None, session=None):
        '''Return a list of available robots'''
        session = get_session(session)
        reserved = set()

        # FIXME: Use all_robots for something useful or remove the argument
        if all_robots is None:
            all_robots = configuration.robots

        for res in cls.all_reserved(now=now, session=session):
            reserved.add((res.robot_model, res.robot_id))

        all_ = {(model, str(id_)) for model, ids in all_robots.items() for id_ in ids}

        # Return all configured and free robots
        return all_ - reserved

    @classmethod
    def all_reserved(cls, now=None, session=None):
        '''Return currently reserved robots'''
        session = get_session(session)
        if now is None:
            now = datetime.now()
        res = session.query(Reservation).filter(
            and_(now >= Reservation.date_from,
                 now <  Reservation.date_to)
        )
        return res.all()

    def cancel(self, session=None):
        session = get_session(session)
        session.delete(self)
