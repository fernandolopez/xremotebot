import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

data = {
    'engine': None,
    'session': None,
    'Session': None,
}


def init_engine_session(uri):
    engine = sqlalchemy.create_engine(uri)
    Session = sqlalchemy.orm.sessionmaker(bind=engine)
    data['engine'] = engine
    data['Session'] = Session
    data['session'] = Session()


def get_session(session):
    if session is None:
        return data['session']
    else:
        return session

Base = declarative_base()
