# -*- coding: utf-8 -*-
import tornado.web
import tornado.escape
from .base_handler import BaseHandler


class UserHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.render('user.html', api_key=self.current_user.api_key)

    @tornado.web.authenticated
    def post(self):
        self.clear_cookie('error')
        if self.get_argument('renew-api-key', None) == '1':
            self.current_user.renew_api_key()
        if self.get_argument('change-password', None) == '1':
            p1 = self.get_argument('password', '')
            p2 = self.get_argument('repeat-password', '')
            if p1 == p2 and len(p1) > 0:
                self.current_user.password = p1
            else:
                self.set_cookie('error', tornado.escape.url_escape(
                    'Error cambiando contraseña '
                    'verifique que las contraseñas ingresadas '
                    'sean iguales y no se encuentren vacías'
                    )
                )

        self.redirect('/user')
