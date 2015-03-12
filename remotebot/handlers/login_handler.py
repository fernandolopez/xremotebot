import tornado.web
from .base_handler import BaseHandler
from ..models.user import User
from ..lib.login import set_cookies_as_loggedin, invalid_credentials


class LoginHandler(BaseHandler):

    def get(self):
        self.render('login.html')

    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')

        if User.login(username, password) is not None:
            set_cookies_as_loggedin(self, username)
            self.redirect(self.get_argument('next', '/'))
        else:
            invalid_credentials(self)
            self.redirect('/login')
