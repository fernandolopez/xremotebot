# -*- coding: utf8 -*-
'''
Robot messages supported by XRemoteBot
'''
import logging

logger = logging.getLogger('xremotebot')

import importlib
from .entity import Entity
from xremotebot.configuration import robots
from xremotebot.robots.abstract_classes import Robot as RobotABC

robot_models = robots.keys()
robot_modules = {}
robot_instances = {}


def initialize_robots():
    '''Setup instances for all configured robots'''
    for model in robot_models:
        logger.debug('Importing "%s" plugin module', model)
        robot_modules[model] = importlib.import_module(
            '.'.join(('xremotebot.robots', model)))
        for id_ in robots[model]:
            id_ = str(id_)
            logger.debug('Accessing "%s.Robot(%s)"', model, id_)
            try:
                robot_instances[(model, id_)] =\
                    getattr(robot_modules[model], 'Robot')(id_)
            except Exception as e:
                logger.error('Error creating instance of %s/%s. %s',
                             model, id_, e.message)


def _normalize_speed(s):
    '''Normalize motor speed values to be in the range -100 to 100.'''
    if s is None:
        s = 50
    s = int(s)
    sign = 1 if s > 0 else -1
    s = abs(s)
    if s < 0:
        return 0
    elif s > 100:
        return 100 * sign

    return s * sign


def _normalize_pin(p):
    '''Normalize pin values to positive integers'''
    return abs(int(p))


def _dict_to_tuple(d):
    return (str(d['robot_model']), str(d['robot_id']))


class Robot(Entity, RobotABC):

    def _delayed_stop(self, method, *args):
        '''Returns (True, amount) if a stop method must be called after an
        amount of seconds.'''
        time_arg = None
        delayed = method in (
            'motors',
            'forward',
            'backward',
            'turnLeft',
            'turnRight',
        )
        if delayed:
            # motors command has more arguments
            if method == 'motors':
                time_arg = 3
            else:
                time_arg = 2

        return (delayed, time_arg)

    def motors(self, wshandler, robot_obj, left, right, time=None):
        '''Dispatch the motors method to the corresponding robot instance'''
        logger.debug('motors called on the Robot entity instance')
        robot_instances[_dict_to_tuple(robot_obj)].motors(
            _normalize_speed(left),
            _normalize_speed(right),
        )

    def ping(self, wshandler, robot_obj):
        '''Dispatch the ping method to the corresponding robot instance'''
        logger.debug('ping called on the Robot entity instance')
        return robot_instances[_dict_to_tuple(robot_obj)].ping()

    def getLine(self, wshandler, robot_obj):
        '''Dispatch the getLine method to the corresponding robot instance'''
        logger.debug('getLine called on the Robot entity instance')
        return robot_instances[_dict_to_tuple(robot_obj)].getLine()

    def stop(self, wshandler, robot_obj):
        '''Dispatch the stop method to the corresponding robot instance'''
        logger.debug('stop called on the Robot entity instance')
        robot_instances[_dict_to_tuple(robot_obj)].stop()

    def forward(self, wshandler, robot_obj, speed=50, time=None):
        '''Dispatch the motors method to the corresponding robot instance'''
        logger.debug('forward called on the Robot entity instance')
        self.motors(wshandler, robot_obj, speed, speed)

    def backward(self, wshandler, robot_obj, speed=50, time=None):
        '''Dispatch the motors method to the corresponding robot instance'''
        logger.debug('backward called on the Robot entity instance')
        self.motors(wshandler, robot_obj, -speed, -speed)

    def turnLeft(self, wshandler, robot_obj, speed=50, time=None):
        '''Dispatch the motors method to the corresponding robot instance'''
        logger.debug('turnLeft called on the Robot entity instance')
        self.motors(wshandler, robot_obj, speed, -speed)

    def turnRight(self, wshandler, robot_obj, speed=50, time=None):
        '''Dispatch the motors method to the corresponding robot instance'''
        logger.debug('turnRight called on the Robot entity instance')
        self.motors(wshandler, robot_obj, -speed, speed)

    def getObstacle(self, wshandler, robot_obj, distance=10):
        '''Dispatch the getObstacle method to the corresponding robot instance'''
        logger.debug('getObstacle called on the Robot entity instance')
        if distance is None:
            distance = 10
        return robot_instances[_dict_to_tuple(robot_obj)].getObstacle(distance)
