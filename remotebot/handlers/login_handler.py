import tornado.web
from .base_handler import BaseHandler
from ..models.user import User
from ..lib.login import invalid_credentials


class LoginHandler(BaseHandler):

    def get(self):
        self.clear_cookie('username')
        self.clear_cookie('unsafe_name')
        self.render('login.html')

    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')

        if User.login(username, password) is not None:
            self.set_current_user(username)
            self.redirect(self.get_query_argument('next', '/'))
        else:
            invalid_credentials(self)
            self.redirect('/login')
