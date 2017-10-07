import unittest

import sublime

from NeoVintageous.tests.utils import ViewTestCase


class TestExShellOutNoInput(ViewTestCase):

    def tearDown(self):
        # XXX: Ugly hack to make sure that the output panels created in these
        # tests don't hide the overall progress panel.
        self.view.window().run_command('show_panel', {'panel': 'output.UnitTesting'})
        super().tearDown()

    def test_command_output(self):
        output_panel = self.view.window().get_output_panel('vi_out')

        self.view.run_command('ex_shell_out', {
            'command_line': '!echo "Testing!"'
        })

        if sublime.platform() == 'windows':
            expected = '\\"Testing!\\"\n'
        else:
            expected = 'Testing!\n'

        actual = output_panel.substr(self.Region(0, output_panel.size()))

        self.assertEqual(expected, actual)


class TestExShellOutFilterThroughShell(ViewTestCase):

    # TODO Implement .!{cmd} (Ex Shell Out) test for Windows
    @unittest.skipIf(sublime.platform() == 'windows',
                     'Test does not work on Windows')
    def test_simple_filter_through_shell(self):
        self.write("two words\nbbb\nccc")
        self.select(2)

        self.view.run_command('ex_shell_out', {
            'command_line': '.! wc -w'
        })

        # Ignore whitespace for the first line as on OS X "wc -l" pads the
        # number with whitespace like this:
        # $ echo hi ho | wc -w
        #        2
        self.assertContentMatches(r"\s*2\nbbb\nccc")

    # TODO Implement .!{cmd} (Ex Shell Out) test for Windows
    @unittest.skipIf(sublime.platform() == 'windows',
                     'Test does not work on Windows')
    def test_command_escaping(self):
        """Tests that command is escaped correctly."""
        self.write('this gets replaced')
        self.select(2)

        self.view.run_command('ex_shell_out', {
            'command_line': '.! echo \\"one\\" \\\'two\\\''
        })
        self.assertContent('"one" \'two\'\n')

    # TODO Implement .!{cmd} (Ex Shell Out) test for Windows
    @unittest.skipIf(sublime.platform() == 'windows',
                     'Test does not work on Windows')
    def test_text_escaping(self):
        """Tests that text is escaped correctly when passed to command."""
        line = 'this "contains" \'quotes\' "; false; echo "\n'
        self.write(line)
        self.select(2)

        self.view.run_command('ex_shell_out', {
            'command_line': '.! cat'
        })
        self.assertContent(line)

    # TODO Implement .!{cmd} (Ex Shell Out) test for Windows
    @unittest.skipIf(sublime.platform() == 'windows',
                     'Test does not work on Windows')
    def test_multiple_filter_through_shell(self):
        self.write("aaa\nthree short words\nccc")
        self.select(10)

        self.view.run_command('ex_shell_out', {
            'command_line': '.! wc -w'
        })

        self.assertContentMatches(r"aaa\n\s*3\nccc")
