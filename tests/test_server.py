from unittest import TestCase
from unittest.mock import Mock

from jen.server import App


class ServerAppTestCase(TestCase):

    def setUp(self):
        self.app = App('tests/site_example')

    def test_get_simple_page(self):
        env = {'PATH_INFO': '/simple'}
        start_response = Mock()
        body = self.app.handle_request(env, start_response)
        self.assertEqual(b''.join(body), b'<body><h1>Simple</h1></body>')
        start_response.assert_called_once_with('200 OK', [
            ('Content-Type', 'text/html'),
            ('Content-Length', '28'),
        ])

    def test_missing_page(self):
        env = {'PATH_INFO': '/missing'}
        start_response = Mock()
        body = self.app.handle_request(env, start_response)
        self.assertEqual(b''.join(body), b'')
        start_response.assert_called_once_with('404 Not Found', [
            ('Content-Type', 'text/html'),
            ('Content-Length', '0'),
        ])

    def test_static_content(self):
        env = {'PATH_INFO': '/robots.txt'}
        start_response = Mock()
        body = self.app.handle_request(env, start_response)
        self.assertEqual(b''.join(body), b'User-agent: *\nDisallow: /\n')
        start_response.assert_called_once_with('200 OK', [
            ('Content-Type', 'application/octet-stream'),
            ('Content-Length', '26'),
        ])

    def test_404_page(self):
        app = App('tests/site_example/sub-with-404')
        env = {'PATH_INFO': '/missing'}
        start_response = Mock()
        body = app.handle_request(env, start_response)
        self.assertEqual(b''.join(body), b'<body><h1>404 Not Found</h1></body>')
        start_response.assert_called_once_with('404 Not Found', [
            ('Content-Type', 'text/html'),
            ('Content-Length', '35'),
        ])

    def test_404_page_does_not_render_if_theres_dot_on_path(self):
        app = App('tests/site_example/sub-with-404')
        env = {'PATH_INFO': '/missing.txt'}
        start_response = Mock()
        body = app.handle_request(env, start_response)
        self.assertEqual(b''.join(body), b'')
        start_response.assert_called_once_with('404 Not Found', [
            ('Content-Type', 'text/html'),
            ('Content-Length', '0'),
        ])
