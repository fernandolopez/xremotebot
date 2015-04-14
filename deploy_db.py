from xremotebot import configuration
from xremotebot.lib import db

# FIXME: toma la uri desde configuration
from xremotebot import configuration
from xremotebot.lib import db
import os.path
import importlib

models = os.listdir('remotebot/models/')
for model in models:
    if not model.endswith('.py'):
        continue
    model = os.path.basename(model).split('.')[0]
    importlib.import_module('remotebot.models.' + model)


# FIXME: toma la uri desde configuration
db.init_engine_session('sqlite:///test.db')

session = db.data['session']

db.Base.metadata.create_all(db.data['engine'])

db.init_engine_session('sqlite:///test.db')

session = db.data['session']

db.Base.metadata.create_all(db.data['engine'])

