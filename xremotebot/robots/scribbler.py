'''Myro Scribbler robot support for xremotebot'''
import myro
import xremotebot.robots.abstract_classes as abcs
import logging
import subprocess

logger = logging.getLogger('xremotebot')


class Robot(abcs.Robot):
    board = None
    mapping = None
    def __init__(self, id_):
        if Robot.mapping is None:
            # Map robot MAC addresses to rfcomm device files
            Robot.mapping = {}
            sub = subprocess.Popen(['rfcomm', '-a'], stdout=subprocess.PIPE)
            out, err = sub.communicate()
            for line in out.splitlines():
                device, mac = line.split(':', 1)
                mac = mac.split()[0]
                Robot.mapping[mac] = '/dev/' + device

        # Create an instance of the robot to control it
        self.robot = myro.Scribbler(Robot.mapping[id_])
        self.id = id_


    def motors(self, left, right):
        # Speed for this robot is a floatin number from 0 to 1
        left = float(left) / 100.0
        right = float(right) / 100.0
        self.robot.motors(left, right)
        logger.info('motors(%d, %d) on robot %s %s',
                     left, right, self.__class__, self.id)


    def getLine(self):
        return self.robot.getLine()

    def getObstacle(self, distance=10):
        return self.ping() < distance

    def ping(self):
        # This robot uses infrarred sensors to detect obstacles,
        # the measured values must be converted to approximate
        # distances in centimeters.
        # 5900 = 0cm
        # 500 = 95cm
        distance = max(self.robot.getObstacle())
        distance = (distance - 500) / 5400.0 * 95
        if distance > 95:
            return 601
        return int(95 - distance)

    def stop(self):
        self.robot.stop()
