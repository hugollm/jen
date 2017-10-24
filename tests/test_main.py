from jen.main import run

from .test_cli import CliTestCase
from .output_buffer import OutputBuffer


class MainTestCase(CliTestCase):

    def test_main_app_has_all_commands(self):
        with OutputBuffer() as bf:
            run()
        self.assertIn('jen run', bf.out)
        self.assertIn('jen build', bf.out)
