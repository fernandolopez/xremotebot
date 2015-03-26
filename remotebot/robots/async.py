import tornado.ioloop
import functools

def delayed(operation):
    def _delayed(func):
        @functools.wraps(func)
        def _(*args, **kwargs):
            if kwargs.get('time', None) is not None:
                func(*args, **kwargs)
                return IOloop.call_later(operation, args[0])
            else:
                pass

        return _

    return _delayed
