import os.path
import base64
import uuid
from datetime import timedelta

def days(d):
    return timedelta(d)


def _random_secret():
    '''Generates a random secret for cookie_secret'''
    return base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)

settings = {
    # Change the cookie secret to a custom fixed value for your application
    'cookie_secret': _random_secret(),
    'xsrf_cookies': True,
    'debug': True,
    'static_path': os.path.join(os.path.dirname(__file__), 'static'),
    'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
    'login_url': '/login',
}

log_level = 'DEBUG'
log_file = 'remotebot.log'
port = 8000
public_server = False
api_key_expiration = days(700)
