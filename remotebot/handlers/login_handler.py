import tornado.web


class LoginHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('login.html')

    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        if username == 'fer' and password == 'f':
            self.set_secure_cookie('username', self.get_argument('username'))
            self.redirect('/')
        
        # self.render('login.html', error='Nombre de usuario o contraseña no válidos')
        self.render('login.html')
