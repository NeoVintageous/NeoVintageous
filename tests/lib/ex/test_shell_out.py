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

        actual = output_panel.substr(self.R(0, output_panel.size()))

        self.assertEqual(expected, actual)


class TestExShellOutFilterThroughShell(ViewTestCase):

    # TODO Implement .!{cmd} (Ex Shell Out) test for Windows and OSX
    @unittest.skipIf(sublime.platform() == 'windows' or sublime.platform() == "osx", 'Test only works in Linux')
    def test_simple_filter_through_shell(self):
        self.write("two words\nbbb\nccc")
        self.select(2)

        self.view.run_command('ex_shell_out', {
            'command_line': '.! wc -w'
        })

        self.assertContent("2\nbbb\nccc")

    # TODO Implement .!{cmd} (Ex Shell Out) test for Windows and OSX
    @unittest.skipIf(sublime.platform() == 'windows' or sublime.platform() == "osx", 'Test only works in Linux')
    def test_multiple_filter_through_shell(self):
        self.write("aaa\nthree short words\nccc")
        self.select(10)

        self.view.run_command('ex_shell_out', {
            'command_line': '.! wc -w'
        })

        self.assertContent("aaa\n3\nccc")
