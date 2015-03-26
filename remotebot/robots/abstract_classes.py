from abc import ABCMeta, abstractmethod
from async import delayed

class Globals(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def wait(self, seconds):
        pass

    @abstractmethod
    def boards(self):
        pass

    @abstractmethod
    def joysticks(self):
        pass


class Board(object):
    __metaclass__ = ABCMeta


class Robot(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def motors(self, left, right):
        pass

    @abstractmethod
    def ping(self):
        pass

    @abstractmethod
    def analog(self, pin, samples=1):
        pass

    @abstractmethod
    def digital(self, pin):
        pass

    @abstractmethod
    def getLine(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @delayed(lambda robot: robot.stop)
    def forward(self, speed=50, time=None):
        self.motors(speed, speed)

    @delayed(lambda robot: robot.stop)
    def backward(self, speed=50, time=None):
        self.motors(-speed, -speed)

    @delayed(lambda robot: robot.stop)
    def turnLeft(self, speed=50, time=None):
        self.motors(-speed, speed)

    @delayed(lambda robot: robot.stop)
    def turnRight(self, speed=50, time=None):
        self.motors(speed, -speed)

    def getObstacle(self, distance=10):
        return self.ping() <= distance
