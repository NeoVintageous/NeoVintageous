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


class Test_Y(unittest.ResetRegisters, unittest.FunctionalTestCase):

    def test_Y(self):
        self.eq('one\nt|wo\nthree', 'Y', 'one\nt|wo\nthree')
        self.assertLinewiseRegister('"two\n')
        self.assertLinewiseRegister('0two\n')
        self.eq('o|ne', 'Y', 'o|ne')
        self.assertLinewiseRegister('"', 'one\n')
        self.assertLinewiseRegister('0', 'one\n')
        self.assertRegisterEmpty('1')
        self.assertRegisterEmpty('-')

    def test_issue_353_Y_should_yank_complete_lines_touched_by_visual_mode(self):
        for mode in ('v', 'V'):
            self.eq('one\n|two\n|three', mode + '_Y', 'n_one\ntw|o\nthree')
            self.assertLinewiseRegister('"two\n')
            self.assertLinewiseRegister('0two\n')
            self.eq('x\n22|22\n33\n4\n|x', mode + '_Y', 'n_x\n2222\n33\n|4\nx')
            self.assertLinewiseRegister('"2222\n33\n4\n')
            self.assertLinewiseRegister('02222\n33\n4\n')
            self.assertRegisterEmpty('-')
            self.assertRegisterEmpty('1')

    def test_issue_827_Y_should_work_in_visual_line_mode(self):
        self.eq('x\n|fizz\nbuzz\n|x\n', 'V_Y', 'n_x\nfizz\nbuz|z\nx\n')
        self.assertLinewiseRegister('"fizz\nbuzz\n')
        self.assertLinewiseRegister('0fizz\nbuzz\n')
