from unittest import TestCase
from unittest.mock import patch

from jen.cli import CliApp, CliCommand, CliPrinter

from .output_buffer import OutputBuffer


class CliTestCase(TestCase):

    def assert_output(self, actual_output, expected_output):
        actual_output = self._clean_output(actual_output)
        expected_output = self._clean_output(expected_output)
        self.assertEqual(actual_output, expected_output)

    def _clean_output(self, output):
        lines = []
        output = output.strip()
        for line in output.splitlines():
            lines.append(line.strip())
        return '\n'.join(lines) + '\n'


class CliPrinterTestCase(TestCase):

    def setUp(self):
        self.printer = CliPrinter()

    def test_printer_adds_newline_before_the_first_print(self):
        with OutputBuffer() as bf:
            self.printer.echo('hello world')
        self.assertTrue(bf.out.startswith('\n'))

    def test_printer_adds_two_spaces_before_each_line(self):
        with OutputBuffer() as bf:
            self.printer.echo('hello world')
        self.assertTrue(bf.out[1:].startswith('  '))

    def test_printer_final_echo_does_nothing_if_nothing_was_previously_printed(self):
        with OutputBuffer() as bf:
            self.printer.final_echo()
        self.assertEqual(bf.out, '')

    def test_printer_final_echo_prints_newline_if_something_was_previously_printed(self):
        with OutputBuffer() as bf:
            self.printer.echo('hello world')
            self.printer.final_echo()
        self.assertTrue(bf.out.endswith('\n\n'))


class CliAppTestCase(CliTestCase):

    def setUp(self):
        self.app = CliApp()

    def call(self, input):
        args = [input]
        args += input.split()[1:]
        with OutputBuffer() as bf:
            with patch('sys.argv', new=args):
                self.app.call()
        return bf

    def test_app_can_route_call_to_command(self):
        self.app.command(SayHello())
        bf = self.call('app hello John')
        self.assert_output(bf.out, 'Hello John')

    def test_app_can_handle_calls_from_sys_argv(self):
        self.app.command(SayHello())
        bf = self.call('app hello John')
        self.assert_output(bf.out, 'Hello John')

    def test_app_shows_help_if_called_without_arguments(self):
        self.app.command(SayHello())
        bf = self.call('app')
        self.assertIn(SayHello.usage, bf.out)
        self.assertIn(SayHello.description, bf.out)

    def test_app_aborts_call_with_message_if_specified_command_is_unknown(self):
        self.app.command(SayHello())
        bf = self.call('app foo')
        self.assert_output(bf.out, 'ERROR: Unknown command "foo"')


class CliCommandTestCase(CliTestCase):

    def test_can_be_called_with_proper_arguments(self):
        command = SayHello()
        with OutputBuffer() as bf:
            command.call('John')
        self.assert_output(bf.out, 'Hello John')

    def test_prints_usage_and_error_if_called_with_invalid_arguments(self):
        command = SayHello()
        with OutputBuffer() as bf:
            command.call()
        self.assert_output(bf.out, """
            USAGE: app hello <name>
            ERROR: missing 1 required positional argument: 'name'
        """)

    def test_command_can_echo(self):
        command = CliCommand()
        with OutputBuffer() as bf:
            command.echo('hello world')
        self.assert_output(bf.out, 'hello world')

    def test_command_can_abort_without_message(self):
        command = CliCommand()
        with OutputBuffer() as bf:
            with self.assertRaises(SystemExit):
                command.abort()

    def test_command_can_abort_with_echoed_message(self):
        command = CliCommand()
        with OutputBuffer() as bf:
            with self.assertRaises(SystemExit):
                command.abort('hello', 'world')
        self.assert_output(bf.out, 'hello world')


class SayHello(CliCommand):

    name = 'hello'
    usage = 'app hello <name>'
    description = 'Says hello to the specified name.'

    def run(self, name):
        self.echo('Hello ' + name)
