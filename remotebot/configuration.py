import os.path
import base64
import uuid


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
}

log_level = 'DEBUG'
log_file = 'remotebot.log'
port = 8000
