# Copyright (C) 2018 The NeoVintageous Team (NeoVintageous).
#
# This file is part of NeoVintageous.
#
# NeoVintageous is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# NeoVintageous is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NeoVintageous.  If not, see <https://www.gnu.org/licenses/>.

from sublime import platform

from NeoVintageous.tests import unittest


class TestExShellOutNoInput(unittest.ViewTestCase):

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

        if platform() == 'windows':
            expected = '\\"Testing!\\"\n'
        else:
            expected = 'Testing!\n'

        actual = output_panel.substr(self.Region(0, output_panel.size()))

        self.assertEqual(expected, actual)


class TestExShellOutFilterThroughShell(unittest.ViewTestCase):

    @unittest.skipIf(platform() == 'windows', 'Test does not work on Windows')
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
        self.assertContentRegex(r"\s*2\nbbb\nccc")

    @unittest.skipIf(platform() == 'windows', 'Test does not work on Windows')
    def test_command_is_escaped_correctly(self):
        self.write('this gets replaced')
        self.select(2)

        self.view.run_command('ex_shell_out', {
            'command_line': '.! echo \\"one\\" \\\'two\\\''
        })
        self.assertContent('"one" \'two\'\n')

    @unittest.skipIf(platform() == 'windows', 'Test does not work on Windows')
    def test_text_is_escaped_correctly_when_passed_to_command(self):
        line = 'this "contains" \'quotes\' "; false; echo "\n'
        self.write(line)
        self.select(2)

        self.view.run_command('ex_shell_out', {
            'command_line': '.! cat'
        })
        self.assertContent(line)

    @unittest.skipIf(platform() == 'windows', 'Test does not work on Windows')
    def test_multiple_filter_through_shell(self):
        self.write("aaa\nthree short words\nccc")
        self.select(10)

        self.view.run_command('ex_shell_out', {
            'command_line': '.! wc -w'
        })

        self.assertContentRegex(r"aaa\n\s*3\nccc")

    @unittest.skipIf(platform() == 'windows', 'Test does not work on Windows')
    def test_filter_command_with_multiple_options_through_shell(self):
        self.write("a\none two\nb")
        self.select(2)
        self.view.run_command('ex_shell_out', {'command_line': '.! wc -m'})
        self.assertContentRegex(r'a\n\s*8\nb')

        self.write("a\none two\nb")
        self.select(2)
        self.view.run_command('ex_shell_out', {'command_line': '.! wc -w -m'})
        self.assertContentRegex(r'a\n\s*2\s+8\nb')

        self.write("a\none two\nb")
        self.select(2)
        self.view.run_command('ex_shell_out', {'command_line': '.! wc -l -w -m'})
        self.assertContentRegex(r'a\n\s*1\s*2\s+8\nb')

    @unittest.skipIf(platform() == 'windows', 'Test does not work on Windows')
    def test_filter_piped_command_through_shell(self):
        self.write("a\none two\nb")
        self.select(2)
        self.view.run_command('ex_shell_out', {'command_line': '.! echo "one two" | wc -w -m'})
        self.assertContentRegex(r'\s*2\s*8')
