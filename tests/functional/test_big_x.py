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


class Test_X(unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()
        self.resetRegisters()

    def test_X(self):
        self.eq('|', 'X', '|')
        self.eq('|\n', 'X', '|\n')
        self.eq('|a\n', 'X', '|a\n')
        self.eq('a|b', 'X', '|b')
        self.eq('a|b\n', 'X', '|b\n')
        self.eq('x\nab|cd', '5X', 'x\n|cd')
        self.eq('7654321|\n', '6X', '|7\n')
        self.assertRegister('"654321\n', linewise=True)
        self.assertRegister('1654321\n', linewise=True)
        self.assertRegisterIsNone('-')
        self.assertRegisterIsNone('0')

    def test_v_X(self):
        self.eq('one\n|two\n|three', 'v_X', 'n_one\n|three')
        self.assertRegister('"two\n', linewise=True)
        self.assertRegister('1two\n', linewise=True)
        self.assertRegisterIsNone('-')
        self.assertRegisterIsNone('0')

    def test_l_X(self):
        self.eq('one\n|two\n|three', 'l_X', 'n_one\n|three')
        self.assertRegister('"two\n', linewise=True)
        self.assertRegister('1two\n', linewise=True)
        self.assertRegisterIsNone('-')
        self.assertRegisterIsNone('0')
