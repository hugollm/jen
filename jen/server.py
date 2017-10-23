import os.path

from gunicorn.app.base import BaseApplication

from .cli import CliCommand
from .template_renderer import TemplateRenderer


class Server(CliCommand):

    name = 'server'
    usage = 'jen server <source>'
    description = 'Serves content from specified <source> directory'

    def run(self, source):
        server = GunicornApp(source)
        server.run()


class GunicornApp(BaseApplication):

    def __init__(self, directory):
        self.app = App(directory)
        super(GunicornApp, self).__init__()

    def load_config(self):
        pass

    def load(self):
        return self.app


class App(object):

    def __init__(self, directory):
        self.directory = directory
        self.template_renderer = TemplateRenderer(directory)

    def __call__(self, env, start_response):
        return self.handle_request(env, start_response)

    def handle_request(self, env, start_response):
        path = env['PATH_INFO']
        if self.template_renderer.has_page(path):
            body = self.template_renderer.render_page(path)
            return self.response(start_response, '200 OK', 'text/html', body)
        full_path = os.path.join(self.directory, path.strip('/'))
        if not path.endswith('.html') and os.path.exists(full_path):
            with open(full_path, 'rb') as f:
                body = f.read()
            return self.response(start_response, '200 OK', 'application/octet-stream', body)
        return self.response(start_response, '404 Not Found')

    def response(self, start_response, status, mime='text/html', data=''):
        if isinstance(data, str):
            data = data.encode('utf-8')
        start_response(status, [
            ('Content-Type', mime),
            ('Content-Length', str(len(data))),
        ])
        return iter([data])
