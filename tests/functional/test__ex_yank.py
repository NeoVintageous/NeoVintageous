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


class Test_ex_yank(unittest.FunctionalTestCase):

    def test_yank(self):
        self.eq('1x\n|2x\n3x\n4x\n5x', ':2,4yank', '1x\n|2x\n3x\n4x\n5x')
        self.assertRegister('"2x\n3x\n4x\n')
        self.assertRegister('02x\n3x\n4x\n')

    def test_yank_into_register(self):
        self.eq('1x\n|2x\n3x\n4x\n5x', ':2,4yank b', '1x\n|2x\n3x\n4x\n5x')
        self.assertRegister('b2x\n3x\n4x\n')
        self.assertRegister('"2x\n3x\n4x\n')
        self.assertRegister('02x\n3x\n4x\n')
