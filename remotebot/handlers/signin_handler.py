from ..models.user import User, UsernameAlreadyTaken
import tornado.web

class SignInHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('signin.html')

    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        try:
            user = User.create(username, password)
        except UsernameAlreadyTaken:
            self.set_cookie(
                'error',
                tornado.escape.url_escape(
                    'El nombre "{}" ya fue utilizado'.format(username)
                )
            )
            self.redirect('/signin')
        else:
            self.redirect('/')

        self.clear_all_cookies()
        self.set_cookie(
            'error',
            tornado.escape.url_escape(
                'Nombre de usuario o contraseña no válidos'
            )
        )
        self.redirect('/login')
