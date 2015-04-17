import tornado.web
from . import configuration
#from controllers.legacy import Legacy
#from controllers.robot import RobotController
from .handlers.ws_handler import WSHandler
from .handlers.login_handler import LoginHandler
from .handlers.logout_handler import LogoutHandler
from .handlers.signin_handler import SignInHandler
from .handlers.user_handler import UserHandler
from .handlers.index_handler import IndexHandler
from .handlers.javascript_handler import JavascriptHandler
from .handlers.doc_handler import DocHandler

url_mapping = [
    #(
    #    r'/js/?',
    #    tornado.web.RedirectHandler,
    #    {'url': '/js/index.html'}
    #),
    #(
    #    r'/js/(.+)',
    #    tornado.web.StaticFileHandler,
    #    {'path': configuration.settings['static_path']}
    #),
    (r'/login', LoginHandler),
    (r'/logout', LogoutHandler),
    (r'/signin', SignInHandler),
    (r'/user', UserHandler),
    (r'/api', WSHandler),
    #(r'/api', WSController),
    (r'/', IndexHandler),
    (
        r'/js/(.+)',
        tornado.web.StaticFileHandler,
        {'path': configuration.settings['static_path'] + '/js'}
    ),
    (
        r'/css/(.+)',
        tornado.web.StaticFileHandler,
        {'path': configuration.settings['static_path'] + '/css'}
    ),
    (
        r'/img/(.+)',
        tornado.web.StaticFileHandler,
        {'path': configuration.settings['static_path'] + '/img'}
    ),
    (r'/javascript', JavascriptHandler),
    (r'/doc(/.*)?', DocHandler),
]
