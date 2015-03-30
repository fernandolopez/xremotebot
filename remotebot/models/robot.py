# -*- coding: utf8 -*-
'''
Robot messages supported by XRemoteBot
'''
from .entity import Entity
from .user import User
from .reservation import Reservation
# FIXME
# from .robot import Robot

from remotebot.configuration import robots
from remotebot.lib.exceptions import NoFreeRobots

robot_models = robots.keys()
robot_modules = {}
robot_instances = {}

for model in robot_models:
    robot_modules[model] = __import__('.'.join(('remotebot.robots', model)))
    for id_ in robots[model]:
        robot_instances[(model, id_)] = robot_modules[model].Robot(id_)

class Robot(Entity):

    def forward(self, wshandler, speed=0, time=-1):
        return True

