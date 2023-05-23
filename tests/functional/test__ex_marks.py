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
        self.assertMarks(
            ' a      3    1       fizz')

    def test_uppercase_mark(self):
        self.normal('x\n\nf|izz\nbuzz\nx')
        self.feed('m')
        self.feed('A')
        self.feed(':marks')
        self.assertMarks(
            ' A      3    1       fizz')

    def test_lowercase_and_uppercase_mark(self):
        self.normal('x\n\nf|izz\nbuzz\nx')
        self.feed('m')
        self.feed('a')
        self.feed('w')
        self.feed('m')
        self.feed('B')
        self.feed(':marks')
        self.assertMarks(
            ' a      3    1       fizz\n'
            ' B      4    0       buzz')

    @unittest.mock.patch('sublime.View.file_name')
    def test_mark_file_name(self, file_name):
        file_name.return_value = '/tmp/fizz/buzz.txt'
        self.normal('f|izz')
        self.feed('m')
        self.feed('a')
        self.feed(':marks')
        self.assertMarks(
            ' a      1    1 /tmp/fizz/buzz.txt')

    def assertMarks(self, expected: str):
        output = self.commandLineOutput()
        self.assertEquals('mark line  col file/text\n' + expected + '\n\nPress ENTER to continue', output)
