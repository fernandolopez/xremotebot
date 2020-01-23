'''Configuration file (with a bit of logic)'''
import os.path
import base64
import uuid
from datetime import timedelta


def days(d):
    '''Get a timedelta object for `d` days'''
    return timedelta(d)


def hours(h):
    '''Get a timedelta object for `h` days'''
    return timedelta(hours=h)

def seconds(s):
    '''Get a timedelta object for `s` seconds'''
    return timedelta(seconds=s)

def _random_secret():
    '''Generates a random secret for cookie_secret'''
    return base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)

# Tornado settings
settings = {
    # Change the cookie secret to a custom fixed value for your application
    'cookie_secret': _random_secret(),
    'xsrf_cookies': True,
    'debug': True,
    'static_path': os.path.join(os.path.dirname(__file__), 'static'),
    'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
    'login_url': '/login',
}

# DB settings
dburi = 'sqlite:///test.db'


tls = False
log_level = 'INFO'
log_file = 'xremotebot.log'
port = 8000

# If False no authentication is required
public_server = False

# Expiration time for api keys
api_key_expiration = days(700)

# Expiration time for robot reservation
reservation_expiration = seconds(60)

# Dict of models of robots and ids/macs of individual robots
robots = {
    'n6': [1]
}

# STREAMING configuration
disable_streaming = True
camera_device = '/dev/video0'
framerate = '30'
resolution = '352x288'
use_embed_streaming = False
# Set this variable to use an external streaming service
embed_streaming = '''<iframe width="360" height="302"
src="http://www.ustream.tv/embed/20521415?v=3&amp;wmode=direct&autoplay=true&quality=low&showtitle=false"
scrolling="no" frameborder="0" style="border: 0px none transparent;">
</iframe>
<br /><a href="http://www.ustream.tv"
style="font-size: 12px; line-height: 20px; font-weight: normal; text-align: left;"
target="_blank">Broadcast live streaming video on Ustream</a>'''
#embed_streaming = '''<iframe width="420" height="315" src="http://www.youtube.com/embed/lShoVjW3rz0"
# frameborder="0" allowfullscreen></iframe>'''
# Server host name
hostname = '163.10.20.238' # 'xremotebot.example'
video_ws_port = 8084
video_ws = 'ws://{}:{}/'.format(hostname, video_ws_port)
