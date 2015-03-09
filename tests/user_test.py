import unittest
from datetime import datetime, timedelta
from remotebot.models.user import User
from .test_helper import db
import remotebot.models.user


class UserTest(unittest.TestCase):
    def setUp(self):
        (engine, self.session) = db()

        remotebot.models.user.Base.metadata.create_all(engine)

        self.user = User(
            username='test',
            password='magic',
            api_key='random',
            api_key_expiration=datetime.now() + timedelta(5)
        )

        self.session.add(self.user)
        self.session.commit()

    def test_key_valid(self):
        self.assertFalse(self.user.api_key_expired())

    def test_key_expired(self):
        self.user.api_key_expiration = datetime.now() - timedelta(5)
        self.assertTrue(self.user.api_key_expired())

    def test_login_with_invalid_user(self):
        user = User.login(username='tst', password='magic',
                          session=self.session)
        self.assertIsNone(user)

    def test_login_with_invalid_password(self):
        user = User.login(username='test', password='mgic',
                          session=self.session)
        self.assertIsNone(user)

    def test_login_valid(self):
        user = User.login(username='test', password='magic',
                          session=self.session)
        self.assertIsInstance(user, User)

    def test_renewed_api_key_is_different(self):
        previous = self.user.api_key
        self.user.renew_api_key()
        self.assertNotEqual(previous, self.user.api_key)

    def test_renewed_api_key_is_not_expired(self):
        self.user.api_key_expiration = datetime.now() - timedelta(5)
        self.user.renew_api_key()
        self.assertFalse(self.user.api_key_expired())
