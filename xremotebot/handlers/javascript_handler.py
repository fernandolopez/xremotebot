'''Renders a Web Page with a form to insert Javascript code
to control the robots, the page contains an optional video stream
of the robot.'''
import tornado.web
from .base_handler import BaseHandler
from ..configuration import tls, hostname, port
from ..configuration import video_ws, disable_streaming
from ..configuration import embed_streaming, use_embed_streaming

class JavascriptHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.render('javascript.html',
                    api_key=self.current_user.api_key,
                    protocol='wss' if tls else 'ws',
                    hostname=hostname,
                    port=port,
                    video_ws=video_ws,
                    disable_streaming=disable_streaming,
                    embed_streaming=embed_streaming,
                    use_embed_streaming=use_embed_streaming,
                    )
