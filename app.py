# -*- coding: utf8 -*-
import logging.handlers
from xremotebot import configuration
# Logs
log_formatter = logging.Formatter(
    fmt='%(asctime)s - [%(levelname)s] %(message)s [line: %(lineno)d'
        ' in function: %(funcName)s on file: %(filename)s ]'
)

log_handler = logging.handlers.RotatingFileHandler(
    configuration.log_file,
    maxBytes=1048576,
    backupCount=10)

log_handler.setFormatter(log_formatter)

log_handler.setLevel(configuration.log_level)

logger = logging.getLogger('xremotebot')
logger.setLevel(configuration.log_level)
logger.addHandler(log_handler)

# import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.websocket
from xremotebot import urls
from xremotebot.lib import db
from xremotebot.models.robot_entity import initialize_robots

# Tornado app

application = tornado.web.Application(
    urls.url_mapping,
    **configuration.settings
)


def main(args):
    db.init_engine_session(configuration.dburi)
    initialize_robots()
    logger.info('About to listen on port %d', configuration.port)
    application.listen(configuration.port)
    logger.info('Listening on port %d', configuration.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    import sys
    main(sys.argv)
