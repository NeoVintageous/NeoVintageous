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


class Test_ex_history(unittest.ResetCommandLineOutput, unittest.FunctionalTestCase):

    def test_history(self):
        self.normal('fi|zz')
        self.feed(':history all')
        commandLineOutput = self.commandLineOutput()
        self.assertRegex(commandLineOutput, '\\s*#  cmd history\n')
        self.assertRegex(commandLineOutput, '\\s*#  search history\n')
        self.assertRegex(commandLineOutput, '\\s*#  expr history\n')
        self.assertRegex(commandLineOutput, '\\s*#  input history\n')
        self.assertRegex(commandLineOutput, '\\s*#  debug history\n')
