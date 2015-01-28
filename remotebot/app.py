# -*- coding: utf8 -*-
# import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.websocket
from . import urls
from . import configuration


application = tornado.web.Application(
    urls.url_mapping,
    **configuration.settings
)

if __name__ == '__main__':
    application.listen(settings.port)
    tornado.ioloop.IOLoop.instance().start()
