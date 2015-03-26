# -*- coding: utf8 -*-

'''Manejador de conexiones con websockets
por el momento es un echo server
'''
import logging

import tornado.websocket
import tornado.escape
from remotebot.lib.message import value, error, valid_client_message
from remotebot.models.user import User
from remotebot.models.global_entity import Global

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
            command = tornado.escape.json_decode(message)
        except ValueError:
            logger.exception('Error trying to decode client message')
            self.write_message(error('Error decoding client message'))
            return

        valid, error_msg = valid_client_message(command)
        if not valid:
            logger.warning(error_msg)
            self.write_message(error_msg)
            return

        if not self.authenticated:
            if command['entity'] != 'global' or \
                    command['method'] not in ('authentication_required', 'authenticate'):
                logger.info('Unauthenticated user sending invalid method')
                self.write_message(error('Authentication required'))
                return

        message = self._handle_api_message(command)

        self.write_message(message)

    def get_current_user(self):
        if not self.authenticated:
            return None

        return self.user

    def set_current_user(self, user):
        self.authenticated = True
        self.user = user



    def _handle_api_message(self, json_msg):
        entity = json_msg['entity']
        method = json_msg['method']
        msg_id = json_msg.get('msg_id', None)
        args = json_msg.get('args', [])

        handler = self.handlers.get(entity, None)
        # FIXME
        logger.info('{%s}', method)
        logger.info(handler)
        if handler is None:
            logger.info('"%s" entity not supported', entity)
            return error('"{}" entity not supported'.format(entity))
        if method not in handler.allowed_methods:
            logger.info('"%s" method not supported by "%s" handler with allowed methods %s',
                    method, type(handler.klass), list(handler.allowed_methods))
            return error('"{}" method not supported by "{}" handler'.format(method, str(handler)))

        try:
            return handler.klass._send(method, self, msg_id, *args)
        except TypeError as e:
            return error(e.message)

    @classmethod
    def register_api_handler(cls, entity, entity_handler):
        cls.handlers[entity] = API_Handler(entity_handler, tuple(filter(public.match, dir(entity_handler))))
        # FIXME debug ineficiente
        logger.debug("%s entity handled by instance of %s with public methods %s", entity,
                type(entity_handler), list(cls.handlers[entity].allowed_methods))


WSHandler.register_api_handler('global', Global())
