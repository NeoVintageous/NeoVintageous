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


class Test_ex_registers(unittest.ResetRegisters, unittest.ResetCommandLineOutput, unittest.FunctionalTestCase):

    def test_registers(self):
        self.normal('fi|zz')
        self.feed(':registers')
        output = self.commandLineOutput()
        self.assertTrue(output.startswith('Type Name Content'))
        self.assertIn('\n  c  "*   \n', output)
        self.assertIn('\n  c  "+   \n', output)
        self.assertTrue(output.endswith('Press ENTER to continue'))

    def test_yank_registers(self):
        self.normal('fi|zz buzz')
        self.feed('yiw')
        self.feed(':registers')
        output = self.commandLineOutput()
        self.assertIn('\n  c  ""   fizz\n', output)
        self.assertIn('\n  c  "*   \n', output)
        self.assertIn('\n  c  "+   \n', output)
        self.assertIn('\n  c  "0   fizz\n', output)

    def test_newlines(self):
        self.visual('1|\n2\n3\n|4\n')
        self.feed('y')
        self.feed(':registers')
        output = self.commandLineOutput()
        self.assertIn('\n  c  ""   ^J2^J3^J\n', output)

    def test_truncate(self):
        self.visual('|xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|')  # noqa: E501
        self.feed('y')
        self.feed(':registers')
        output = self.commandLineOutput()
        self.assertIn('\n  c  ""   xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx ...\n', output)  # noqa: E501

    def test_no_trailing_newline(self):
        self.eq('[\n  |{\n  }\n]', 'yaB', '[\n  |{\n  }\n]')
        self.feed(':registers')
        self.assertIn('l  ""   {^J  }\n', self.commandLineOutput())
