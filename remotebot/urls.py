import tornado.web
import os.path
from . import configuration
#from controllers.legacy import Legacy
#from controllers.robot import RobotController
from .handlers.ws_handler import WSHandler
from .handlers.login_handler import LoginHandler
from .handlers.index_handler import IndexHandler

url_mapping = [
    (
        r'/js/?',
        tornado.web.RedirectHandler,
        {'url': '/js/index.html'}
    ),
    (
        r'/js/(.+)',
        tornado.web.StaticFileHandler,
        {'path': configuration.settings['static_path']}
    ),
    (r'/login', LoginHandler),
    (r'/api', WSHandler),
    #(r'/api', WSController),
    (r'/', IndexHandler)
]
