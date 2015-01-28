#!/usr/bin/env python3
from functools import partial
import unittest

from tornado.testing import AsyncHTTPTestCase, gen_test
import tornado.web
from tornado.websocket import websocket_connect

from remotebot.handlers.ws_handler import WSHandler
from .test_helper import get_ws_url

class WSocketTest(tornado.testing.AsyncHTTPTestCase):
    def setUp(self):
        super(WSocketTest, self).setUp()
        #self.ws = websocket.create_connection(
        #    self.get_url('/api').replace('http', 'ws', 1)
        #)

    def get_app(self):
        return tornado.web.Application([('/api', WSHandler)])

    @gen_test
    def test_invalid_input_fails_graceful(self):
        ws = yield websocket_connect(
                get_ws_url(self, '/api'),
                io_loop=self.io_loop)

        ws.write_message('')
        response = yield ws.read_message()
        self.assertEqual('', response)
