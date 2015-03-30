import unittest
from datetime import datetime, timedelta
from remotebot.models.reservation import Reservation
from remotebot.models.user import User
from .test_helper import db
import remotebot.models.reservation


class ReservationTest(unittest.TestCase):
    def setUp(self):
        (engine, self.session) = db()

        remotebot.models.reservation.Base.metadata.create_all(engine)

        self.session.add(Reservation(robot_model='N6',
                                     robot_id='42',
                                     date_from=datetime(2000, 1, 1),
                                     date_to=datetime(2000, 1, 2)))
        self.user = User(
            username='test',
            password='magic',
            api_key='random',
            api_key_expiration=datetime.now() + timedelta(5)
         )

        self.session.add(self.user)
        self.session.commit()


    def test_new_reservation_contains_older_one(self):
        reserved = Reservation.reserved('N6', '42', datetime(1999, 12, 31),
                                        datetime(2000, 1, 3), self.session)
        self.assertEqual(1, len(reserved))

    def test_new_reservation_is_possible(self):
        reserved = Reservation.reserved('N6', '42', datetime(2000, 1, 2),
                                        datetime(2000, 1, 3), self.session)
        self.assertEqual(0, len(reserved))

    def test_new_reservation_overlaps_at_the_end(self):
        reserved = Reservation.reserved('N6', '42',
                                        datetime(2000, 1, 1) + timedelta(hours=12),
                                        datetime(2000, 1, 3), self.session)
        self.assertEqual(1, len(reserved))

    def test_new_reservation_overlaps_at_the_begining(self):
        reserved = Reservation.reserved('N6', '42',
                                        datetime(2000, 1, 1) - timedelta(hours=12),
                                        datetime(2000, 1, 1) + timedelta(hours=1), self.session)

    def test_reserve_free_robot_returns_an_instance(self):
        reservation = Reservation.reserve(self.user,
                                          'N6', '42',
                                          datetime(2000, 2, 1),
                                          datetime(2000, 2, 2),
                                          self.session)
        self.assertIsInstance(reservation, Reservation)

    def test_reserve_occupied_robot_returns_none(self):
        reservation = Reservation.reserve(self.user,
                                          'N6', '42',
                                          datetime(2000, 1, 1),
                                          datetime(2000, 1, 1) + timedelta(hours=1),
                                          self.session)
        self.assertIsNone(reservation)

    def test_no_free_robots(self):
        now = datetime(2000, 1, 1) + timedelta(minutes=5)
        all_robots = { 'n6': ['1', '2'], 'scribbler': ['asdad'] }
        for model, ids in all_robots.items():
            for id_ in ids:
                Reservation.reserve(self.user,
                                    model,
                                    id_,
                                    datetime(2000, 1, 1),
                                    datetime(2000, 1, 1) + timedelta(hours=1),
                                    self.session)

        self.assertEquals(0, len(Reservation.available(all_robots, now=now, session=self.session)))

    def test_one_free_robot(self):
        now = datetime(2000, 1, 1) + timedelta(minutes=5)
        all_robots = { 'n6': ['1', '2'], 'scribbler': ['asdad']}
        for model, ids in all_robots.items():
            for id_ in ids:
                Reservation.reserve(self.user,
                                    model,
                                    id_,
                                    datetime(2000, 1, 1),
                                    datetime(2000, 1, 1) + timedelta(hours=1),
                                    self.session)
        all_robots['n6'].append('4')
        self.assertEquals(1, len(Reservation.available(all_robots, now=now, session=self.session)))

    def test_reserve_robot_for_user(self):
        robot = Reservation.reserve_any(self.user, all_robots={'n6': [1]}, session=self.session)
        self.assertIsInstance(robot, Reservation)

    def test_reserve_robot_for_user_should_fail_if_no_robot_available(self):
        robot = Reservation.reserve_any(self.user, all_robots={}, session=self.session)
        self.assertIsNone(robot)



