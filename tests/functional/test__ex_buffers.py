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


class Test_ex_buffers(unittest.ResetCommandLineOutput, unittest.FunctionalTestCase):

    def test_buffers(self):
        self.normal('fi|zz')
        self.feed(':buffers')
        self.assertRegex(
            self.commandLineOutput(),
            '\\d %a \\+ "\\[No Name\\]"\\s+line 1')

    def test_contains_line_number(self):
        self.normal('1\n2\nfi|zz\n4\n')
        self.feed(':buffers')
        self.assertRegex(
            self.commandLineOutput(),
            '\\d %a \\+ "\\[No Name\\]"\\s+line 3')

    @unittest.mock.patch('sublime.View.file_name')
    def test_contains_file_name(self, file_name):
        file_name.return_value = 'tmp/fizz.txt'
        self.normal('1\n2\nfi|zz\n4\n')
        self.feed(':buffers')
        self.assertRegex(
            self.commandLineOutput(),
            '\\d %a \\+ "tmp\\/fizz\\.txt"\\s+line 3')
