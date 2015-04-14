from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy import or_, and_
import sqlalchemy.orm
from datetime import datetime
from .. import configuration
from .user import User
from ..lib.db import Base, get_session


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
    def reserved(cls, user, robot_model, robot_id, date_from, date_to, session=None):
        session = get_session(session)
        reservations = session.query(Reservation).filter(
            and_(Reservation.robot_model == robot_model,
                 Reservation.robot_id == robot_id,
                 Reservation.user == user)
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
    def reserved_by_any_user(cls, robot_model, robot_id, date_from, date_to, session=None):
        session = get_session(session)
        reservations = session.query(Reservation).filter(
            and_(Reservation.robot_model == robot_model,
                 Reservation.robot_id == robot_id)
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
    def reserve(cls, user, robot_model, robot_id, date_from=None, date_to=None, session=None):
        session = get_session(session)

        if date_from is None:
            date_from = datetime.now()
        if date_to is None:
            date_to = date_from + configuration.reservation_expiration

        res = cls.reserved(user, robot_model, robot_id, date_from, date_to, session)
        if len(res) > 0:
            # If the robot is reserved by the same user, return it
            return res[0]
        if (robot_model, str(robot_id)) not in cls.available():
            # If the robot is reserved by other user return None
            return None

        reservation = cls(user=user,
                          robot_model=robot_model,
                          robot_id=robot_id,
                          date_from=date_from,
                          date_to=date_to)
        session.add(reservation)

        session.commit()
        return reservation

    @classmethod
    def all_reserved(cls, now=None, session=None):
        session = get_session(session)
        if now is None:
            now = datetime.now()
        res = session.query(Reservation).filter(
            and_(now >= Reservation.date_from,
                 now <  Reservation.date_to),
        )
        return res.all()

    @classmethod
    def available(cls, all_robots=None, now=None, session=None):
        session = get_session(session)
        reserved = set()

        if all_robots is None:
            all_robots = configuration.robots

        for res in cls.all_reserved(now=now, session=session):
            reserved.add((res.robot_model, res.robot_id))
        all_ = {(model, str(id_)) for model, ids in all_robots.items() for id_ in ids}

        return all_ - reserved

    @classmethod
    def reserve_any(cls, user, all_robots=None, session=None):
        session = get_session(session)
        available = Reservation.available(all_robots=all_robots, session=session)
        reservation = None
        if available:
            robot = available.pop()
            reservation = Reservation.reserve(
                user,
                robot[0],
                robot[1],
                date_from=datetime.now(),
                date_to=datetime.now() + configuration.reservation_expiration,
                session=session,
            )

        return reservation

    def cancel(self, session=None):
        session = get_session(session)
        session.delete(self)
