import abstract_classes
import duinobot

class Globals(abstract_classes.Globals):
    def wait(self, time=None):
        pass

    def boards(self):
        return duinobot.boards()

    def joysticks(self):
        return duinobot.joysticks()

class Board(abstract_classes.Board, duinobot.Board):
    pass

class Robot(abstract_classes.Robot, duinobot.Robot):
    def __init__(self, board, robot_id):
        super(Robot, self).__init__(board, robot_id)

    def motors(self, left, right):
        duinobot.Robot.motors(self, left, right)

    def stop(self):
        duinobot.Robot.stop(self)

    def analog(self, pin, samples=1):
        return self.board.analog(pin, samples, self.getId())

    def digital(self, pin):
        return self.board.digital(pin, self.getId())

    def getLine(self):
        return duinobot.Robot.getLine(self)

    def ping(self):
        return duinobot.Robot.ping(self)

if __name__ == '__main__':
    print(Globals.__mro__)
    print(Board.__mro__)
    print(Robot.__mro__)
    b = Board()
    r = Robot(b, 7)
    r.forward(50)
    import time
    time.sleep(1)
    r.stop()
    b.exit()
