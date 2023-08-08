# Copyright (C) 2018-2023 The NeoVintageous Team (NeoVintageous).
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
# along with NeoVintageous.  If not, see <https://www.gnu.org/licensesubstitute/>.

from NeoVintageous.tests import unittest


class Test_ex_marks(unittest.ResetMarks, unittest.ResetCommandLineOutput, unittest.FunctionalTestCase):

    def test_marks_header_and_footer(self):
        self.normal('fi|zz')
        self.feed(':marks')
        output = self.commandLineOutput()
        self.assertTrue(output.startswith('mark line  col file/text'))
        self.assertTrue(output.endswith('Press ENTER to continue'))

    def test_lowercase_mark(self):
        self.normal('x\n\nf|izz\nbuzz\nx')
        self.feed('m')
        self.feed('a')
        self.feed(':marks')
        self.assertMarksOutput(
            ' a      3    1       fizz')

    @unittest.mock.patch('sublime.Window.find_open_file')
    @unittest.mock.patch('sublime.View.file_name')
    def test_uppercase_mark(self, file_name, find_open_file):
        file_name.return_value = '/tmp/fizz.txt'
        find_open_file.return_value = self.view
        self.normal('x\n\nf|izz\nbuzz\nx')
        self.feed('m')
        self.feed('A')
        self.feed(':marks')
        self.assertMarksOutput(
            ' A      3    1 /tmp/fizz.txt')

    def test_lowercase_multiple_lines(self):
        self.normal('x\n\nf|izz\nbuzz\nping pong\nx')
        self.feed('m')
        self.feed('a')
        self.feed('w')
        self.feed('m')
        self.feed('c')
        self.feed('j')
        self.feed('7l')
        self.feed('m')
        self.feed('b')
        self.feed(':marks')
        self.assertMarksOutput(
            ' a      3    1       fizz\n'
            ' b      5    7  ping pong\n'
            ' c      4    0       buzz')

    @unittest.mock.patch('sublime.Window.find_open_file')
    @unittest.mock.patch('sublime.View.file_name')
    def test_lowercase_and_uppercase_mark(self, file_name, find_open_file):
        file_name.return_value = '/tmp/fizz.txt'
        find_open_file.return_value = self.view
        self.normal('x\n\nf|izz\nbuzz\nping pong\nx')
        self.feed('m')
        self.feed('a')
        self.feed('w')
        self.feed('m')
        self.feed('B')
        self.feed('j')
        self.feed('m')
        self.feed('X')
        self.feed('w')
        self.feed('m')
        self.feed('x')
        self.feed(':marks')
        self.assertMarksOutput(
            ' a      3    1 /tmp/fizz.txt\n'
            ' x      5    5 /tmp/fizz.txt\n'
            ' B      4    0 /tmp/fizz.txt\n'
            ' X      5    0 /tmp/fizz.txt')

    @unittest.mock.patch('sublime.View.file_name')
    def test_mark_file_name(self, file_name):
        file_name.return_value = '/tmp/fizz/buzz.txt'
        self.normal('f|izz')
        self.feed('m')
        self.feed('a')
        self.feed(':marks')
        self.assertMarksOutput(
            ' a      1    1 /tmp/fizz/buzz.txt')
