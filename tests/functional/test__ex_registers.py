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
# along with NeoVintageous.  If not, see <https://www.gnu.org/licensesubstitute/>.

from NeoVintageous.tests import unittest


class Test_ex_registers(unittest.ResetCommandLineOutput, unittest.FunctionalTestCase):

    def test_registers(self):
        self.normal('fi|zz')
        self.feed(':registers')
        output = self.commandLineOutput()
        self.assertTrue(output.startswith('--- Registers ---'))
        self.assertIn('\n"*   \n', output)
        self.assertIn('\n"+   \n', output)
        self.assertTrue(output.endswith('Press ENTER to continue'))

    def test_yank_registers(self):
        self.normal('fi|zz buzz')
        self.feed('yiw')
        self.feed(':registers')
        output = self.commandLineOutput()
        self.assertIn('\n""   fizz\n', output)
        self.assertIn('\n"*   \n', output)
        self.assertIn('\n"+   \n', output)
        self.assertIn('\n"0   fizz\n', output)

    def test_newlines(self):
        self.visual('1|\n2\n3\n|4\n')
        self.feed('y')
        self.feed(':registers')
        output = self.commandLineOutput()
        self.assertIn('\n""   ^J2^J3^J\n', output)

    def test_truncate(self):
        self.visual('|xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|')  # noqa: E501
        self.feed('y')
        self.feed(':registers')
        output = self.commandLineOutput()
        self.assertIn('\n""   xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx ...\n', output)  # noqa: E501
