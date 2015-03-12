# -*- coding: utf8 -*-

'''Manejador de conexiones con websockets
por el momento es un echo server
'''
import json
import logging

import tornado.websocket

from remotebot.lib.message import error, valid_client_message

logger = logging.getLogger('remotebot')

import re
import collections
API_Handler = collections.namedtuple('API_Handler', ('klass', 'allowed_methods'))
public = re.compile(r'(^[a-zA-Z]\w*[a-zA-Z0-9]$|^[a-zA-Z]$)')

class WSHandler(tornado.websocket.WebSocketHandler):
    handlers = {}

    def __init__(self, *args, **kwargs):
        # FIXME
        super(WSHandler, self).__init__(*args, **kwargs)

    def open(self):
        self.authenticated = False

    # FIXME: Hacer asincrónico
    def on_message(self, message):
        try:
            command = json.loads(message)
        except ValueError:
            logger.exception('Error trying to decode client message')
            self.write_message(error('Error decoding client message'))
            return

        valid, error_msg = valid_client_message(command)
        if not valid:
            logger.warning('Invalid client message')
            self.write_message(error_msg)
            return

        if not self.authenticated:
            if command['entity'] != 'global' or \
                    command['method'] not in ('auth_required', 'authenticate'):
                logger.info('Unauthenticated user sending invalid method')
                self.write_message(error('Authentication required'))
                return

        message = self._handle_api_message(command)

        self.write_message(message)

    def _handle_api_message(self, json_msg):
        entity = json_msg['entity']
        method = json_msg['method']
        args = json_msg.get('args', [])

        handler = self.handlers.get(entity, None)

        if handler is None:
            return error('"{}" entity not supported'.format(entity))
        if method not in handler.allowed_methods:
            return error('"{}" method not supported by "{}" handler'.format(method, handler))

        return handler.klass.send(method)

    @classmethod
    def register_api_handler(cls, entity, klass):
        cls.handlers[entity] = API_Handler(klass, filter(public.match, dir(klass)))

