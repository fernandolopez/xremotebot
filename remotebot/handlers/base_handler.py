import sqlalchemy.orm
import tornado.web
from ..lib import db
from ..models.user import User


class BaseHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        return db.data['session'].query(User).filter(User.username == 'fernando').one()
        username = self.get_secure_cookie('username')
        if username is not None:
            try:
                user = db.data['session'].query(User).filter(User.username == username).one()
            except sqlalchemy.orm.exc.NoResultFound:
                user = None
        else:
            user = None
        return user
