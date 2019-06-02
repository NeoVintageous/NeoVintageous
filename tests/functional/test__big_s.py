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

from NeoVintageous.tests import unittest


class Test_S(unittest.ResetRegisters, unittest.FunctionalTestCase):

    def test_n(self):
        self.eq('|', 'S', 'i_|')
        self.eq('|aaa\nbbb\nccc', 'S', 'i_|\nbbb\nccc')
        self.eq('aaa\nbb|b\nccc', 'S', 'i_aaa\n|\nccc')
        self.eq('aaa\nbbb\n|ccc', 'S', 'i_aaa\nbbb\n|')
        self.assertRegister('"ccc\n', linewise=True)
        self.assertRegister('1ccc\n', linewise=True)
        self.assertRegister('2bbb\n', linewise=True)
        self.assertRegister('3aaa\n', linewise=True)
        self.assertRegisterEmpty('-')
        self.assertRegisterEmpty('0')
        self.eq('    |one', 'S', 'i_    |')
        self.eq('1\ntw|o', 'S', 'i_1\n|')
        self.eq('1\ntw|o\n', 'S', 'i_1\n|\n')

    def test_v(self):
        self.eq('one\n|two\n|three', 'v_S', 'i_one\n|three')
        self.assertRegister('"two\n', linewise=True)
        self.assertRegister('1two\n', linewise=True)
        self.assertRegisterEmpty('-')
        self.assertRegisterEmpty('0')

    def test_l(self):
        self.eq('one\n|two\n|three', 'V_S', 'i_one\n|three')
        self.assertRegister('"two\n', linewise=True)
        self.assertRegister('1two\n', linewise=True)
        self.assertRegisterEmpty('-')
        self.assertRegisterEmpty('0')
