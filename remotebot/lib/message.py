import json

def authentication_required():
    return json.dumps({
        'type': 'authentication_required',
    })


def error(message, stack_trace=''):
    return json.dumps({
        'type': 'error',
        'message': message,
        'stack_trace': stack_trace,
    })

