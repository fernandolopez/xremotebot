import myro
import remotebot.robots.abstract_classes as abcs
import logging
import subprocess

logger = logging.getLogger('remotebot')


class Robot(abcs.Robot):
    board = None
    mapping = None
    def __init__(self, id_):
        if mapping is None:
            Robot.mapping = {}
            sub = subprocess.Popen(['rfcomm', '-a'], stdout=subprocess.PIPE)
            out, err = sub.communicate()
            for line in out.splitlines():
                device, mac = line.split(':', 1)
                mac = mac.split()[0]
                Robot.mapping[mac] = '/dev/' + device

        self.robot = myro.Scribbler(mapping[id_])


    def motors(self, left, right):
        left = float(left) * 100
        right = float(right) * 100
        self.robot.motors(left, right)
        logger.info('motors(%d, %d) on robot %s %d',
                     left, right, self.__class__, self.id)


    def getLine(self):
        return self.robot.getLine()

    def getObstacle(self):
        return self.robot.getObstacle()[1]

    def ping(self):
        return self.robot.ping()

    def stop(self):
        self.robot.stop()
