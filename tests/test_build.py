from shutil import rmtree
import os.path

from jen.build import Build

from .test_cli import CliTestCase
from .output_buffer import OutputBuffer


class BuildTestCase(CliTestCase):

    source = 'tests/site_example'
    target = '/tmp/jen-tests-dist'
    buffer_output = True

    def setUp(self):
        self.command = Build()

    def tearDown(self):
        if os.path.exists(self.target):
            rmtree(self.target)

    def run_command(self, source=None, target=None):
        source = source or self.source
        target = target or self.target
        if self.buffer_output:
            with OutputBuffer() as bf:
                self.command.run(source, target)
            return bf
        else:
            self.command.run(source, target)

    def test_command_fails_if_source_directory_is_invalid(self):
        with self.assertRaises(SystemExit):
            self.run_command(source='invalid')

    def test_command_fails_if_target_directory_already_exists(self):
        with self.assertRaises(SystemExit):
            self.run_command(target='tests/site_example')

    def test_target_contains_templates_after_build(self):
        self.run_command()
        self.assertTrue(os.path.exists(self.target + '/index.html'))
        self.assertTrue(os.path.exists(self.target + '/simple.html'))
        self.assertTrue(os.path.exists(self.target + '/sub-with-404/404.html'))
        self.assertTrue(os.path.exists(self.target + '/sub-with-index/index.html'))
        self.assertTrue(os.path.exists(self.target + '/sub-without-index/simple.html'))

    def test_target_templates_are_rendered(self):
        self.run_command()
        with open(self.target + '/index.html', 'r') as f:
            text = f.read()
        self.assertEqual(text, '<body><h1>Index</h1></body>')

    def test_target_contains_static_files_after_build(self):
        self.run_command()
        self.assertTrue(os.path.exists(self.target + '/robots.txt'))
        self.assertTrue(os.path.exists(self.target + '/theme.css'))

    def test_target_does_not_contain_html_files_starting_with_underscore(self):
        self.run_command()
        self.assertFalse(os.path.exists(self.target + '/_base.html'))

    def test_command_outputs_generated_file_names(self):
        bf = self.run_command()
        self.assertIn('OK: index.html', bf.out)
        self.assertIn('OK: simple.html', bf.out)
        self.assertIn('OK: sub-with-404/404.html', bf.out)
        self.assertIn('OK: sub-with-index/index.html', bf.out)
        self.assertIn('OK: sub-without-index/simple.html', bf.out)
        self.assertIn('OK: robots.txt', bf.out)
        self.assertIn('OK: theme.css', bf.out)
