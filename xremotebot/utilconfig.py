import base64
import uuid
from datetime import timedelta


def days(d):
    return timedelta(d)


def hours(h):
    return timedelta(hours=h)


def random_secret():
    '''Generates a random secret for cookie_secret'''
    return base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
