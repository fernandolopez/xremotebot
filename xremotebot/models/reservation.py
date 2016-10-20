from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy import or_, and_
import sqlalchemy.orm
from datetime import datetime
from .. import configuration
from .user import User
from ..lib.db import Base, get_session


def _includes(r1_from, r1_to, r2_from, r2_to):
    return or_(
        and_(
            r1_from >= r2_from,
            r1_to <= r2_to,
        ),
        and_(
            r1_from <= r2_from,
            r1_to >= r2_to,
        ),
    )


def _overlaps(r1_from, r1_to, r2_from, r2_to):
    return or_(
        and_(r1_from <= r2_from, r2_from <= r1_to),
        and_(r1_from <= r2_to, r2_to <= r1_to),
    )


def _conflicts(r1_from, r1_to, r2_from, r2_to):
    return or_(
        _includes(r1_from, r1_to, r2_from, r2_to),
        _overlaps(r1_from, r1_to, r2_from, r2_to),
    )


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
            _conflicts(
                date_from,
                date_to,
                Reservation.date_from,
                Reservation.date_to,
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
            _conflicts(
                date_from,
                date_to,
                Reservation.date_from,
                Reservation.date_to,
            )
        )
        return reservations.all()

    @classmethod
    def reserve(cls, user, robot_model, robot_id, all_robots=None, date_from=None, date_to=None, session=None):
        session = get_session(session)

        if date_from is None:
            date_from = datetime.now()
        if date_to is None:
            date_to = date_from + configuration.reservation_expiration

        res = cls.reserved(user, robot_model, robot_id, date_from, date_to, session)
        if len(res) > 0:
            # If the robot is reserved by the same user, return it
            return res[0]
        if (robot_model, str(robot_id)) not in cls.available(all_robots=all_robots,
                                                             date_from=date_from,
                                                             date_to=date_to,
                                                             session=session):
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
    def all_reserved(cls, date_from, date_to, session=None):
        session = get_session(session)
        reservations = session.query(Reservation).filter(
            _conflicts(
                date_from,
                date_to,
                Reservation.date_from,
                Reservation.date_to,
            )
        )
        return reservations.all()

    @classmethod
    def available(cls, all_robots=None, date_from=None, date_to=None, session=None):
        session = get_session(session)
        reserved = set()

        if date_from is None or date_to is None:
            date_from = datetime.now()
            date_to = date_from + configuration.reservation_expiration

        if all_robots is None:
            all_robots = configuration.robots

        for res in cls.all_reserved(date_from, date_to, session=session):
            reserved.add((res.robot_model, res.robot_id))
        all_ = {(model, str(id_)) for model, ids in all_robots.items() for id_ in ids}

        return all_ - reserved

    @classmethod
    def reserve_any(cls, user, all_robots=None, date_from=None, date_to=None,
                    session=None):
        session = get_session(session)
        available = Reservation.available(all_robots=all_robots,
                                          date_from=date_from,
                                          date_to=date_to,
                                          session=session)
        reservation = None
        if available:
            robot = available.pop()
            reservation = Reservation.reserve(
                user,
                robot[0],
                robot[1],
                all_robots=all_robots,
                date_from=datetime.now(),
                date_to=datetime.now() + configuration.reservation_expiration,
                session=session,
            )

        return reservation

    def cancel(self, session=None):
        session = get_session(session)
        session.delete(self)
