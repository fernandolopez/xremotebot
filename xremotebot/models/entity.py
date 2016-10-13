'''
Base class for the entities supported by XRemoteBot
'''
import logging

logger = logging.getLogger('xremotebot')

class Entity(object):
    def _send(self, method, wshandler, *args, **kwargs):
        logger.info('Calling %s.%s with args %s', self.__class__, method, (args, kwargs))
        return getattr(self, method)(wshandler, *args, **kwargs)

    def _delayed_stop(self, method, *args):
        return (False, None)
