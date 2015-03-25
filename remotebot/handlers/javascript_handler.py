import tornado.web
from .base_handler import BaseHandler
from ..configuration import tls, hostname, port
from ..lib import db


class JavascriptHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.render('javascript.html',
            api_key=self.current_user.api_key,
            protocol='wss' if tls else 'ws',
            hostname=hostname,
            port=port
        )
