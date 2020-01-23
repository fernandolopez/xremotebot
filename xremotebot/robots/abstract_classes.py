'''ABC for different models of robot, this server
supports any robot using this basic operations.
'''
from abc import ABCMeta, abstractmethod


class Robot(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def motors(self, left, right):
        '''Moves the left and right motors to the given speed'''
        pass

    @abstractmethod
    def ping(self):
        '''
        Returns a value proportional to the distance of an object in front
        of the robot'''
        pass

    @abstractmethod
    def getLine(self):
        '''
        Returns a tuple with values corresponding to two line following
        sensors, the values depends of the sensors used'''
        pass

    @abstractmethod
    def stop(self):
        '''
        Stops the robot movement.'''
        pass
