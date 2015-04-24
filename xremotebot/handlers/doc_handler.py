import markdown
import io
import os.path
from .base_handler import BaseHandler


class DocHandler(BaseHandler):
    docbase = os.path.realpath(
        os.path.join(os.path.dirname(__file__),
                     '..', 'doc-src')
    )

    def get(self, slug):
        buffer = io.BytesIO()
        if slug is not None:
            slug = slug.replace('/', '')

        if slug not in ('ruby', 'python', 'javascript', 'quickref'):
            self.redirect('/doc/javascript')
        else:
            doc = slug

        markdown.markdownFromFile(
            os.path.join(self.docbase, doc + '.md'),
            buffer,
            extensions=['markdown.extensions.fenced_code',
                        'markdown.extensions.toc'],
            extension_configs={
                'markdown.extensions.toc':
                {
                    'title': 'Tabla de contenidos',
                },
            },
        )
        buffer.seek(0)
        self.render('container.html', body=buffer.read())
