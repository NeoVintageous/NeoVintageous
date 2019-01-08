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


class Test_Y(unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()
        self.resetRegisters()

    def test_Y(self):
        self.eq('one\nt|wo\nthree', 'Y', 'one\nt|wo\nthree')
        self.assertRegister('"two\n', linewise=True)
        self.assertRegister('0two\n', linewise=True)
        self.eq('o|ne', 'Y', 'o|ne')
        self.assertRegister('"', 'one\n', linewise=True)
        self.assertRegister('0', 'one\n', linewise=True)
        self.assertRegisterIsNone('1')
        self.assertRegisterIsNone('-')

    def test_issue_353_Y_should_yank_complete_lines_touched_by_visual_mode(self):
        self.eq('one\n|two\n|three', 'v_Y', 'n_one\ntw|o\nthree')
        self.assertRegister('"two\n', linewise=True)
        self.assertRegister('0two\n', linewise=True)
        self.eq('x\n22|22\n33\n4\n|x', 'v_Y', 'n_x\n2222\n33\n|4\nx')
        self.assertRegister('"2222\n33\n4\n', linewise=True)
        self.assertRegister('02222\n33\n4\n', linewise=True)
        self.assertRegisterIsNone('-')
        self.assertRegisterIsNone('1')
