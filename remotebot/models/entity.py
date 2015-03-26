'''
Base class for the entities supported by XRemoteBot
'''

class Entity(object):
    def _send(self, method, *args, **kwargs):
        return getattr(self, method)(*args, **kwargs)

