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


@unittest.mock.patch.dict('NeoVintageous.nv.session._session', {}, clear=True)
class TestExShellOut(unittest.ResetCommandLineOutput, unittest.FunctionalTestCase):

    def test_command_output(self):
        self.normal("fi|zz")
        self.feed(':!echo "Testing!"')
        expected = '\\"Testing!\\"\n' if platform() == 'windows' else 'Testing!\n'
        self.assertCommandLineOutput(expected)

    @unittest.skipIf(platform() == 'windows', 'Test does not work on Windows')
    def test_simple_filter_through_shell(self):
        self.normal("tw|o words\nbbb\nccc")
        self.feed(':.! wc -w')
        # Ignore whitespace for the first line as on OS X "wc -l" pads the
        # number with whitespace like this:
        # $ echo hi ho | wc -w
        #        2
        self.assertContentRegex(r"\s*2\nbbb\nccc")

    @unittest.skipIf(platform() == 'windows', 'Test does not work on Windows')
    def test_command_is_escaped_correctly(self):
        self.normal('th|is gets replaced')
        self.feed(':.! echo \\"one\\" \\\'two\\\'')
        self.assertContent('"one" \'two\'\n')

    @unittest.skipIf(platform() == 'windows', 'Test does not work on Windows')
    def test_text_is_escaped_correctly_when_passed_to_command(self):
        line = 'this "contains" \'quotes\' "; false; echo "\n'
        self.write(line)
        self.select(2)
        self.feed(':.! cat')
        self.assertContent(line)

    @unittest.skipIf(platform() == 'windows', 'Test does not work on Windows')
    def test_multiple_filter_through_shell(self):
        self.normal("aaa\nthree |short words\nccc")
        self.feed(':.! wc -w')
        self.assertContentRegex(r"aaa\n\s*3\nccc")

    @unittest.skipIf(platform() == 'windows', 'Test does not work on Windows')
    def test_filter_command_with_multiple_options_through_shell(self):
        self.normal('a\n|one two\nb')
        self.feed(':.! wc -m')
        self.assertContentRegex(r'a\n\s*8\nb')

        self.normal('a\n|one two\nb')
        self.feed(':.! wc -w -m')
        self.assertContentRegex(r'a\n\s*2\s+8\nb')

        self.normal('a\n|one two\nb')
        self.feed(':.! wc -l -w -m')
        self.assertContentRegex(r'a\n\s*1\s*2\s+8\nb')

    @unittest.skipIf(platform() == 'windows', 'Test does not work on Windows')
    def test_filter_piped_command_through_shell(self):
        self.normal('a\n|one two\nb')
        self.feed(':.! echo "one two" | wc -w -m')
        self.assertContentRegex(r'\s*2\s*8')

    def test_echo(self):
        self.feed(':!echo hello')
        self.assertCommandLineOutput('hello\n')

    def test_echo_replace_current_line(self):
        self.normal('1\nt|wo\n3\n')
        self.feed(':.!echo fizz')
        self.assertNormal('1\n|fizz\n3\n')

    def test_echo_replace_between_lines(self):
        self.normal('1\n|2\n3\n4\n5\n6\n7\n')
        self.feed(':4,6!echo fizz')
        self.assertNormal('1\n2\n3\n|fizz\n7\n')

    @unittest.mock_status_message()
    def test_repeat(self):
        self.normal('f|izz\n')
        self.feed(':!echo one')
        self.assertCommandLineOutput('one\n')
        self.assertNormal('f|izz\n')
        self.feed(':!!')
        self.assertCommandLineOutput('one\n')
        self.assertNormal('f|izz\n')
        self.feed(':.!!')
        self.assertNormal('|one\n')
        self.assertNoStatusMessage()

    @unittest.mock_status_message()
    @unittest.mock.patch('NeoVintageous.nv.ex_cmds.get_ex_shell_last_command')
    def test_no_previous_cmd(self, get_ex_shell_last_command):
        get_ex_shell_last_command.return_value = None
        self.normal('f|izz')
        self.feed(':!!')
        self.assertStatusMessage('E34: No previous command')

    def test_error(self):
        self.normal('fi|zz\nbuzz\n')
        self.feed(':!ls foo_test_error')
        self.assertNormal('fi|zz\nbuzz\n')
        if self.platform() == 'osx':
            self.assertCommandLineOutput('ls: foo_test_error: No such file or directory\n')
        else:
            self.assertEqual(self.commandLineOutput().replace('\'', ''), 'ls: cannot access foo_test_error: No such file or directory\n\nPress ENTER to continue')  # noqa: E501
            self.assertSelection(2)

    def test_replacement_error(self):
        self.normal('fizz\nx|xx\nbuzz\n')
        self.feed(':.!ls foo_test_replacement_error')
        if self.platform() == 'osx':
            self.assertNormal('fizz\n|ls: foo_test_replacement_error: No such file or directory\nbuzz\n')
        else:
            self.assertEqual(self.content().replace('\'', ''), 'fizz\nls: cannot access foo_test_replacement_error: No such file or directory\nbuzz\n')  # noqa: E501
            self.assertSelection(5)

    @unittest.mock_status_message()
    def test_empty_file_name_replacement_emits_status_message(self):
        self.feed(':!ls %')
        self.assertStatusMessage('E499: Empty file name for \'%\' or \'#\', only works with ":p:h"')
