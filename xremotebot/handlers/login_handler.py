'''Renders a Web page to log-in in the server'''
from .base_handler import BaseHandler
from ..models.user import User
from ..lib.login import invalid_credentials


class LoginHandler(BaseHandler):

    def get(self):
        # Logout first
        self.clear_cookie('username')
        self.clear_cookie('unsafe_name')
        self.clear_cookie('post_next_redirect')
        self.set_cookie('post_next_redirect',
                        self.get_argument('next', '/'),
                        expires_days=None)
        self.render('login.html')

    def post(self):
        # Try to login
        username = self.get_argument('username')
        password = self.get_argument('password')
        next_ = self.get_cookie('post_next_redirect')
        if next_ is None:
            next_ = '/'

        if User.login(username, password) is not None:
            self.set_current_user(username)
            self.redirect(next_)
        else:
            invalid_credentials(self)
            self.redirect('/login')
