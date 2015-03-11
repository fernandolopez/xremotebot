from ..models.user import User
from ..lib import db
import tornado

def set_cookies_as_loggedin(handler, username):
    handler.clear_all_cookies()
    handler.set_secure_cookie('username', username)
    handler.set_cookie('unsafe_name', username)

def invalid_credentials(handler):
    handler.clear_all_cookies()
    handler.set_cookie(
        'error',
        tornado.escape.url_escape(
            'Nombre de usuario o contraseña no válidos'
        )
    )

