import tornado.web


class LoginHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('login.html')

    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        if username == 'fer' and password == 'f':
            self.clear_all_cookies()
            self.set_secure_cookie('username', username)
            self.set_cookie('unsafe_name', username)
            self.redirect('/')

        self.clear_all_cookies()
        self.set_cookie(
            'error',
            tornado.escape.url_escape(
                'Nombre de usuario o contraseña no válidos'
            )
        )
        self.redirect('/login')
