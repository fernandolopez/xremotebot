from ..models.user import User
from ..lib import db
import tornado

def invalid_credentials(handler):
    handler.clear_all_cookies()
    handler.set_cookie(
        'error',
        tornado.escape.url_escape(
            'Nombre de usuario o contraseña no válidos'
        )
    )

