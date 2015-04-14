#!/usr/bin/env python3
import json

from tornado.testing import AsyncHTTPTestCase, gen_test
import tornado.web
from tornado.websocket import websocket_connect

from xremotebot.handlers.ws_handler import WSHandler

from .test_helper import get_ws_url


class WSocketTest(AsyncHTTPTestCase):
    def setUp(self):
        super(WSocketTest, self).setUp()

    def get_app(self):
        return tornado.web.Application([('/api', WSHandler)])

    @gen_test
    def test_invalid_input_fails_graceful(self):
        ws = yield websocket_connect(
            get_ws_url(self, '/api'),
            io_loop=self.io_loop)

        ws.write_message('')
        response = yield ws.read_message()
        self.assertEqual('error', json.loads(response)['response'])

    @gen_test
    def test_invalid_message_fails_graceful(self):
        ws = yield websocket_connect(
            get_ws_url(self, '/api'),
            io_loop=self.io_loop)

        ws.write_message('{ "foo": "bar" }')
        response = yield ws.read_message()
        self.assertEqual('error', json.loads(response)['response'])
