# -*- coding: utf8 -*-

'''Manejador de conexiones con websockets
por el momento es un echo server
'''
import json
import logging

import tornado.websocket

from remotebot.lib.message import error, valid_client_message

logger = logging.getLogger('remotebot')


class WSHandler(tornado.websocket.WebSocketHandler):

    def __init__(self, *args, **kwargs):
        # FIXME
        super(WSHandler, self).__init__(*args, **kwargs)

    def on_open(self):
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
                    command['method'] not in ['auth_required', 'authenticate']:
                logger.info('Unauthenticated user sending invalid method')
                self.write_message(error('Authentication required'))
                return

        self.write_message(message)
