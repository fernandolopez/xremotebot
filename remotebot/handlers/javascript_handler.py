import tornado.web
from .base_handler import BaseHandler
from ..lib import db


class JavascriptHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.render('javascript.html', api_key=self.current_user.api_key)
