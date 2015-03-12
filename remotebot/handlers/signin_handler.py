from ..models.user import User, UsernameAlreadyTaken
from ..lib import login
from .base_handler import BaseHandler
import tornado.web

class SignInHandler(BaseHandler):

    def get(self):
        self.render('signin.html')

    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        try:
            user = User.create(username, password)
        except UsernameAlreadyTaken:
            login.invalid_credentials(self)
            self.set_cookie(
                'error',
                tornado.escape.url_escape(
                    'El nombre "{}" ya fue utilizado'.format(username)
                )
            )
            self.redirect('/signin')
        else:
            login.set_cookies_as_loggedin(self, username)
            self.redirect(self.get_argument('next', '/'))
