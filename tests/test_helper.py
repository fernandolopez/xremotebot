import sqlalchemy


def db():
    engine = sqlalchemy.create_engine('sqlite://')
    Session = sqlalchemy.orm.sessionmaker(bind=engine)
    session = Session()
    return (engine, session)


def get_ws_url(tornado_test_case, uri):
    return tornado_test_case.get_url(uri).replace('http', 'ws', 1)

# FIXME
"""
import os
import re
import sys

def find(path, pattern):
    files = []
    if not os.path.isabs(path):
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), path))
    for current, dirs, fnames in os.walk(path):
        for name in fnames:
            if pattern.match(name) is not None:
                files.append(os.path.join(current, name))
    return files

source_files = find('..', re.compile(r'.+\.py$'))

if sys.path[0] != '' and os.path.basename(sys.path[0]) == 'tests':
    sys.path.insert(0, os.path.realpath(os.path.join(sys.path[0], '..')))
"""
