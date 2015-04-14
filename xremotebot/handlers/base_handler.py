import sqlalchemy.orm
import tornado.web
from ..lib import db
from ..models.user import User

import logging
logger = logging.getLogger('xremotebot')


class BaseHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        username = self.get_secure_cookie('username')
        logger.debug('cookie username = "%s"', username)
        if username is not None:
            username = username.decode() # unicode string
            try:
                user = db.data['session'].query(User).filter(User.username == username).one()
                logger.debug('username "%s" found in database', username)
            except sqlalchemy.orm.exc.NoResultFound:
                user = None
                logger.debug('username "%s" not found in database', username)
        else:
            user = None
        return user

    def set_current_user(self, username):
        self.clear_all_cookies()
        self.set_secure_cookie('username', username, expires_days=None)
        self.set_cookie('unsafe_name', username, expires_days=None)

