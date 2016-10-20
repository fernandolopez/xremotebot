from .test_helper import db
from datetime import datetime, timedelta
from operator import and_, or_
from xremotebot.models.reservation import Reservation, _includes, _overlaps, _conflicts
from xremotebot.models.user import User
import unittest
import xremotebot.models.reservation
from mock import patch


class ReservationTest(unittest.TestCase):
    def setUp(self):
        (engine, self.session) = db()

        xremotebot.models.reservation.Base.metadata.create_all(engine)
        self.all_robots = {'n6': ['42']}
        reservation = Reservation(
            robot_model='N6',
            robot_id='42',
            date_from=datetime(2000, 1, 1),
            date_to=datetime(2000, 1, 2)
        )
        self.user = User(
            username='test',
            password='magic',
            api_key='random',
            api_key_expiration=datetime.now() + timedelta(5)
        )

        reservation.user = self.user
        self.session.add(self.user)
        self.session.commit()

    def test_reserved_disjoint_reservation_returns_empty(self):
        reserved = Reservation.reserved(self.user,
                                        'N6', '42', datetime(2000, 1, 2),
                                        datetime(2000, 1, 3), self.session)
        self.assertEqual(0, len(reserved))

    def test_reserved_overlaping_reservation_in_the_beginning_can_be_found(self):
        reserved = Reservation.reserved(self.user, 'N6', '42',
                                        datetime(1999, 12, 31),
                                        datetime(2000, 1, 3), self.session)
        self.assertEqual(1, len(reserved))

    def test_reserved_overlaping_reservation_at_the_end_can_be_found(self):
        reserved = Reservation.reserved(self.user,
                                        'N6', '42',
                                        datetime(2000, 1, 1) + timedelta(hours=12),
                                        datetime(2000, 1, 3), self.session)
        self.assertEqual(1, len(reserved))

    def test_reserve_free_robot_returns_an_instance(self):
        reservation = Reservation.reserve(self.user,
                                          'N6', '42',
                                          all_robots=self.all_robots,
                                          date_from=datetime(2000, 2, 1),
                                          date_to=datetime(2000, 2, 2),
                                          session=self.session)
        self.assertIsInstance(reservation, Reservation)

    def test_reserve_occupied_robot_returns_none(self):
        reservation = Reservation.reserve(self.user,
                                          'N6', '42',
                                          all_robots=self.all_robots,
                                          date_from=datetime(2000, 1, 1),
                                          date_to=datetime(2000, 1, 1) + timedelta(hours=1),
                                          session=self.session)
        self.assertIsNone(reservation)

    def test_no_free_robots(self):
        now = datetime(2000, 1, 1) + timedelta(minutes=5)
        all_robots = { 'n6': ['1', '2'], 'scribbler': ['asdad'] }
        for model, ids in all_robots.items():
            for id_ in ids:
                Reservation.reserve(self.user,
                                    model,
                                    id_,
                                    all_robots=all_robots,
                                    date_from=datetime(2000, 1, 1),
                                    date_to=datetime(2000, 1, 1) + timedelta(hours=1),
                                    session=self.session)

        self.assertEquals(0, len(Reservation.available(
            all_robots,
            date_from=now,
            date_to=now + timedelta(minutes=5),
            session=self.session)))

    def test_one_free_robot(self):
        now = datetime(2000, 1, 1) + timedelta(minutes=5)
        all_robots = { 'n6': ['1', '2'], 'scribbler': ['asdad']}
        for model, ids in all_robots.items():
            for id_ in ids:
                Reservation.reserve(self.user,
                                    model,
                                    id_,
                                    all_robots=all_robots,
                                    date_from=datetime(2000, 1, 1),
                                    date_to=datetime(2000, 1, 1) + timedelta(hours=1),
                                    session=self.session)
        all_robots['n6'].append('4')
        self.assertEquals(1, len(Reservation.available(all_robots,
            date_from=now,
            date_to=now + timedelta(minutes=5),
            session=self.session)))

    def test_reserve_robot_for_user(self):
        robot = Reservation.reserve_any(self.user, all_robots={'n6': [1]}, session=self.session)
        self.assertIsInstance(robot, Reservation)

    def test_reserve_robot_for_user_should_fail_if_no_robot_available(self):
        robot = Reservation.reserve_any(self.user, all_robots={}, session=self.session)
        self.assertIsNone(robot)


@patch('xremotebot.models.reservation.and_', and_)
@patch('xremotebot.models.reservation.or_', or_)
class ReservationUtilsTest(unittest.TestCase):
    def test_includes_date_is_the_same(self):
        d1_from = datetime(2000, 1, 1, 11)
        d1_to = datetime(2000, 1, 1, 22)
        self.assertTrue(_includes(d1_from, d1_to, d1_from, d1_to))

    def test_includes_returns_true_on_nested_dates(self):
        d1_from = datetime(2000, 1, 1, 11)
        d1_to = datetime(2000, 1, 1, 22)
        d2_from = datetime(2000, 1, 1, 13)
        d2_to = datetime(2000, 1, 1, 20)
        self.assertTrue(_includes(d1_from, d1_to, d2_from, d2_to))

    def test_conflicts_return_false_on_disjoint_dates(self):
        d1_from = datetime(2000, 1, 1, 11)
        d1_to = datetime(2000, 1, 1, 22)
        d2_from = datetime(2000, 1, 1, 8)
        d2_to = datetime(2000, 1, 1, 10)
        self.assertFalse(_conflicts(d1_from, d1_to, d2_from, d2_to))

    def test_overlaps_returns_true_if_one_range_contains_the_beginning_or_the_end_of_the_other(self):
        d1_from = datetime(2000, 1, 1, 11)
        d1_to = datetime(2000, 1, 1, 22)
        d2_from = datetime(2000, 1, 1, 10)
        d2_to = datetime(2000, 1, 1, 12)
        self.assertTrue(_overlaps(d1_from, d1_to, d2_from, d2_to))

        d2_from = datetime(2000, 1, 1, 21)
        d2_to = datetime(2000, 1, 1, 23)
        self.assertTrue(_overlaps(d1_from, d1_to, d2_from, d2_to))
