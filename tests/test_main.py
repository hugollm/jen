from jen.main import app

from .test_cli import CliTestCase
from .output_buffer import OutputBuffer


class MainTestCase(CliTestCase):

    def test_main_app_has_all_commands(self):
        with OutputBuffer() as bf:
            app.call()
        self.assertIn('jen server', bf.out)
        self.assertIn('jen build', bf.out)
