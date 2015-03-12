import tornado.web
from .base_handler import BaseHandler


class LogoutHandler(BaseHandler):

    def get(self):
        self.clear_all_cookies()
        self.redirect('/')
