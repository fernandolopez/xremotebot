from sqlalchemy.ext.declarative import declarative_base

def init_engine_session(uri):
    global engine, session, Session
    engine = sqlalchemy.create_engine(uri)
    Session = sqlalchemy.orm.sessionmaker(bind=engine)
    session = Session()

Base = declarative_base()


