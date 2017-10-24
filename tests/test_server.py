from unittest import TestCase
from unittest.mock import patch, Mock

from jen.server import Server, App
from .test_cli import CliTestCase
from .output_buffer import OutputBuffer


class ServerCommandTestCase(CliTestCase):

    def setUp(self):
        self.command = Server()
        self.patch = patch('jen.server.GunicornApp.run')
        self.patch.start()

    def tearDown(self):
        self.patch.stop()

    def test_command_aborts_if_source_is_not_found(self):
        with OutputBuffer() as bf:
            with self.assertRaises(SystemExit):
                self.command.run('foobar')
        self.assert_output(bf.out, 'ERROR: source must be a valid directory')

    def test_command_aborts_if_source_is_not_directory(self):
        with OutputBuffer() as bf:
            with self.assertRaises(SystemExit):
                self.command.run('tests/site_example/index.html')
        self.assert_output(bf.out, 'ERROR: source must be a valid directory')

    def test_command_runs_gunicorn_app(self):
        with patch('jen.server.GunicornApp.run') as mock:
            with OutputBuffer():
                self.command.run('tests/site_example')
        mock.assert_called_once_with()


class ServerAppTestCase(TestCase):

    def setUp(self):
        self.app = App('tests/site_example')

    def test_get_simple_page(self):
        env = {'PATH_INFO': '/simple'}
        start_response = Mock()
        body = self.app(env, start_response)
        self.assertEqual(b''.join(body), b'<body><h1>Simple</h1></body>')
        start_response.assert_called_once_with('200 OK', [
            ('Content-Type', 'text/html'),
            ('Content-Length', '28'),
        ])

    def test_get_index_page(self):
        env = {'PATH_INFO': '/'}
        start_response = Mock()
        body = self.app(env, start_response)
        self.assertEqual(b''.join(body), b'<body><h1>Index</h1></body>')
        start_response.assert_called_once_with('200 OK', [
            ('Content-Type', 'text/html'),
            ('Content-Length', '27'),
        ])

    def test_missing_page(self):
        env = {'PATH_INFO': '/missing'}
        start_response = Mock()
        body = self.app(env, start_response)
        self.assertEqual(b''.join(body), b'')
        start_response.assert_called_once_with('404 Not Found', [
            ('Content-Type', 'text/html'),
            ('Content-Length', '0'),
        ])

    def test_static_content(self):
        env = {'PATH_INFO': '/robots.txt'}
        start_response = Mock()
        body = self.app(env, start_response)
        self.assertEqual(b''.join(body), b'User-agent: *\nDisallow: /\n')
        start_response.assert_called_once_with('200 OK', [
            ('Content-Type', 'text/plain'),
            ('Content-Length', '26'),
        ])

    def test_server_can_guess_the_mime_type_of_the_served_static_content(self):
        env = {'PATH_INFO': '/theme.css'}
        start_response = Mock()
        body = self.app(env, start_response)
        self.assertEqual(b''.join(body), b'body { background-color: black; }\n')
        start_response.assert_called_once_with('200 OK', [
            ('Content-Type', 'text/css'),
            ('Content-Length', '34'),
        ])

    def test_static_content_try_does_not_fail_when_target_is_directory(self):
        app = App('tests/site_example/sub-without-index')
        env = {'PATH_INFO': '/'}
        start_response = Mock()
        body = app(env, start_response)
        self.assertEqual(b''.join(body), b'')
        start_response.assert_called_once_with('404 Not Found', [
            ('Content-Type', 'text/html'),
            ('Content-Length', '0'),
        ])

    def test_404_page(self):
        app = App('tests/site_example/sub-with-404')
        env = {'PATH_INFO': '/missing'}
        start_response = Mock()
        body = app(env, start_response)
        self.assertEqual(b''.join(body), b'<body><h1>404 Not Found</h1></body>')
        start_response.assert_called_once_with('404 Not Found', [
            ('Content-Type', 'text/html'),
            ('Content-Length', '35'),
        ])

    def test_404_page_does_not_render_if_theres_dot_on_path(self):
        app = App('tests/site_example/sub-with-404')
        env = {'PATH_INFO': '/missing.txt'}
        start_response = Mock()
        body = app(env, start_response)
        self.assertEqual(b''.join(body), b'')
        start_response.assert_called_once_with('404 Not Found', [
            ('Content-Type', 'text/html'),
            ('Content-Length', '0'),
        ])

    def test_returns_404_if_path_ends_on_slash(self):
        app = App('tests/site_example')
        env = {'PATH_INFO': '/simple/'}
        start_response = Mock()
        body = app(env, start_response)
        self.assertEqual(b''.join(body), b'')
        start_response.assert_called_once_with('404 Not Found', [
            ('Content-Type', 'text/html'),
            ('Content-Length', '0'),
        ])

    def test_returns_404_if_static_path_ends_on_slash(self):
        app = App('tests/site_example')
        env = {'PATH_INFO': '/robots.txt/'}
        start_response = Mock()
        body = app(env, start_response)
        self.assertEqual(b''.join(body), b'')
        start_response.assert_called_once_with('404 Not Found', [
            ('Content-Type', 'text/html'),
            ('Content-Length', '0'),
        ])
