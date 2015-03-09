import unittest
from remotebot.models.user import User


class UserTest(unittest.TestCase):
    def setUp(self):
        self.user = User()
