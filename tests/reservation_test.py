import unittest
from datetime import datetime, timedelta
from remotebot.models.reservation import Reservation
from .test_helper import db
import remotebot.models.reservation


class ReservationTest(unittest.TestCase):
    def setUp(self):
        (engine, self.session) = db()

        remotebot.models.reservation.Base.metadata.create_all(engine)

        self.session.add(Reservation(robot_model='N6',
                                     date_from=datetime(2000, 1, 1),
                                     date_to=datetime(2000, 1, 2)))
        self.session.commit()

    def test_new_reservation_contains_older_one(self):
        reserved = Reservation.reserved('N6', datetime(1999, 12, 31), datetime(2000, 1, 3), self.session)
        self.assertEqual(1, len(reserved))

    def test_new_reservation_is_possible(self):
        reserved = Reservation.reserved('N6', datetime(2000, 1, 2), datetime(2000, 1, 3), self.session)
        self.assertEqual(0, len(reserved))

    def test_new_reservation_overlaps_at_the_end(self):
        reserved = Reservation.reserved('N6', datetime(2000, 1, 1) + timedelta(hours=12),
                                        datetime(2000, 1, 3), self.session)
        self.assertEqual(1, len(reserved))

    def test_new_reservation_overlaps_at_the_begining(self):
        reserved = Reservation.reserved('N6', datetime(2000, 1, 1) - timedelta(hours=12),
                                        datetime(2000, 1, 1) + timedelta(hours=1), self.session)

    def test_reserve_free_robot_returns_an_instance(self):
        reservation = Reservation.reserve('N6',
                                          datetime(2000, 2, 1),
                                          datetime(2000, 2, 2),
                                          self.session)
        self.assertIsInstance(reservation, Reservation)

    def test_reserve_occupied_robot_returns_none(self):
        reservation = Reservation.reserve('N6',
                                          datetime(2000, 1, 1),
                                          datetime(2000, 1, 1) + timedelta(hours=1),
                                          self.session)
        self.assertIsNone(reservation)
