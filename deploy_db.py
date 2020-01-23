'''Helper script to create database schemas'''

from xremotebot import configuration
from xremotebot.lib import db
import os.path
import importlib

models = os.listdir('xremotebot/models/')
for model in models:
    if not model.endswith('.py'):
        continue
    model = os.path.basename(model).split('.')[0]
    importlib.import_module('xremotebot.models.' + model)


db.init_engine_session(configuration.dburi)

session = db.data['session']

db.Base.metadata.create_all(db.data['engine'])
