from abc import ABCMeta, abstractmethod


class Robot(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def motors(self, left, right):
        pass

    @abstractmethod
    def ping(self):
        pass

    #@abstractmethod
    #def analog(self, pin, samples=1):
    #    pass

    #@abstractmethod
    #def digital(self, pin):
    #    pass

    @abstractmethod
    def getLine(self):
        pass

    @abstractmethod
    def stop(self):
        pass
