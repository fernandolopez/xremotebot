import duinobot
import xremotebot.robots.abstract_classes as abcs
import logging

logger = logging.getLogger('xremotebot')


class Robot(abcs.Robot):
    board = None

    def __init__(self, id_):
        if Robot.board is None:
            Robot.board = duinobot.Board()
        self.id = int(id_)
        self.robot = duinobot.Robot(Robot.board, self.id)
        logger.debug('n6 with id=%d created', self.id)

    def motors(self, left, right):
        self.robot.motors(left, right)
        logger.info('motors(%d, %d) on robot %s %d',
                     left, right, self.__class__, self.id)

    def analog(self, pin, samples=1):
        return self.robot.analog(pin, samples)

    def digital(self, pin):
        return self.robot.digital(pin)

    def getLine(self):
        return self.robot.getLine()

    def ping(self):
        return self.robot.ping()

    def getObstacle(self, distance=10):
        return self.robot.getObstacle(distance)

    def stop(self):
        self.robot.stop()
