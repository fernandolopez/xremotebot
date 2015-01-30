import json


def values(*args):
    return json.dumps({
        'response': 'values',
        'values': args,
    })


def error(message, stack_trace=''):
    return json.dumps({
        'response': 'error',
        'message': message,
        'stack_trace': stack_trace,
    })


def valid_client_message(obj):
    if not isinstance(obj, dict):
        return (False, error('The messages should be JSON objects'))

    if 'entity' not in obj or 'method' not in obj:
        return (False, error('"entity" and "method" are mandatory fields'))

    # FIXME:
    if obj['entity'] not in ('global', 'robot'):
        return (False, error('Only "global" and "robot" entities are allowed'))

    if not isinstance(obj.get('values', []), list):
        return (False, error('If present "args" should be an array'))

    return (True, None)
