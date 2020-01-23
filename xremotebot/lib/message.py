# -*- coding: utf-8 -*-
'''
API message parsing and generator functions.
'''

import tornado.escape

def value(value, msg_id=None):
    '''Returns a value response message'''
    obj = {
        'response': 'value',
        'value': value,
    }
    if msg_id is not None:
        obj['msg_id'] = msg_id
    return tornado.escape.json_encode(obj)


def error(message, msg_id=None):
    '''Returns an error response message'''
    obj = {
        'response': 'error',
        'message': message,
    }
    if msg_id is not None:
        obj['msg_id'] = msg_id
    return tornado.escape.json_encode(obj)

def valid_client_message(obj):
    '''Check if request message is correctly formated.j
    Returns a tuple with a boolean and an optional error
    message. If the message is invalid the boolean is False
    and the error message is set, else the boolean is set to True
    and the second element can be ignored.'''
    # FIXME MAYBE este tipo de errores no deberían afectar a los usuarios
    # finales por lo que el msg_id para manejar promises no sería necesario
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
