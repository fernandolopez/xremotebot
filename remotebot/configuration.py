import os.path
import base64
import uuid
from datetime import timedelta

def days(d):
    return timedelta(d)

def hours(h):
    return timedelta(hours=h)


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

tls = False
hostname = '163.10.20.221' # 'xremotebot.example'
video_ws = 'ws://{}:8084/'.format(hostname)
log_level = 'DEBUG'
log_file = 'remotebot.log'
port = 8000
public_server = False
api_key_expiration = days(700)
reservation_expiration = hours(1)
robots = {
    'n6': [10],
    'scribbler': ['00:1E:19:01:0B:81'],
}
