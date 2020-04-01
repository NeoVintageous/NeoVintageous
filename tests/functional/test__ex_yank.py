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


class Test_ex_yank(unittest.ResetRegisters, unittest.FunctionalTestCase):

    def test_yank(self):
        self.eq('1x\n|2x\n3x\n4x\n5x', ':2,4yank', '1x\n|2x\n3x\n4x\n5x')
        self.assertRegisters('"0', '2x\n3x\n4x\n')
        self.assertRegistersEmpty('-1ab')
        self.resetRegisters()

    def test_yank_into_register(self):
        self.eq('1x\n|2x\n3x\n4x\n5x', ':2,4yank b', '1x\n|2x\n3x\n4x\n5x')
        self.assertRegisters('"b', '2x\n3x\n4x\n')
        self.assertRegistersEmpty('-01a')

    def test_yank_marks(self):
        self.normal('1\n|2\n3\n4\n5\n')
        self.feed('ma')
        self.feed('2j')
        self.feed('mx')
        self.feed('gg')
        self.feed(":'a,'xyank")
        self.assertRegisters('"0', '2\n3\n4\n')
        self.assertRegistersEmpty('-1')

    @unittest.mock_bell()
    def test_yank_mark_not_set(self):
        self.normal('1\n|2\n3\n4\n5\n')
        self.feed(":'a,'xyank")
        self.assertRegistersEmpty('"-01')
        self.assertBell('E20: mark not set')
