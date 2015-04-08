import tornado.web
import markdown
import io
import os.path
from .base_handler import BaseHandler

class DocHandler(BaseHandler):
    docbase = os.path.realpath(
        os.path.join(os.path.basename(__file__),
                     '..', 'doc-src')
    )
    def get(self):
        buffer = io.BytesIO()
        markdown.markdownFromFile('remotebot/doc-src/index.md', buffer)
        buffer.seek(0)
        self.render('container.html', body=buffer.read())
