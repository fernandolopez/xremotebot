'''Renders documentation written in Markdown'''
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
        # markdown.markdownFromFile() requires a file-like object to store
        # the result of translating the markdown content to HTML
        buffer = io.BytesIO()

        # Remove slashes from slug
        if slug is not None:
            slug = slug.replace('/', '')

        # Do not render filenames given by the user unless the filenames
        # are the expected options, if the option is not valid or empty
        # load the javascript documentation.
        if slug not in ('ruby', 'python', 'javascript', 'quickref'):
            self.redirect('/doc/javascript')
        else:
            doc = slug

        # Parse the documentation file and convert it to HTML
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

        # Set the current file position to 0 in order to
        # be readaboe by self.render()
        buffer.seek(0)
        self.render('container.html', body=buffer.read())
