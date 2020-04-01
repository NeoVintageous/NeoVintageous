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


class Test_F(unittest.FunctionalTestCase):

    def test_n(self):
        self.eq('0x23|a5', 'n_Fx', '0|x23a5')
        self.eq('012x|a5', 'n_Fx', '012|xa5')
        self.eq('0123|x5', 'n_Fx', '0123|x5')
        self.eq('0xx3|a5', 'n_Fx', '0x|x3a5')
        self.eq('01x3|x5', 'n_Fx', '01|x3x5')

    def test_v(self):
        self.eq('0x2|ba|5', 'v_Fx', 'r_0|x2b|a5')
        self.eq('r_0|x23a|5', 'v_Fx', 'r_0|x23a|5')
        self.eq('0|ax3b|5', 'v_Fx', '0|ax|3b5')
        self.eq('0x2|ab|5', 'v_Fx', 'r_0|x2a|b5')
        self.eq('01|x3b|5', 'v_Fx', '01|x|3b5')
        self.eq('01|a3x|5', 'v_Fx', '01|a3x|5')
        self.eq('01|2\n456|', 'v_F0', '01|2\n456|')
        self.eq('01|2\n456|', 'v_F4', '01|2\n4|56')
        self.eq('01|2\n|456', 'v_F0', 'r_|012|\n456')
        self.eq('01|2\n|456', 'v_F5', '01|2\n|456')
        self.eq('r_01|2\n456|', 'v_F0', 'r_|012\n456|')
        self.eq('r_01|2\n456|', 'v_F4', 'r_01|2\n456|')
        self.eq('r_012|\n456|', 'v_F0', 'r_|012\n456|')
        self.eq('r_012|\n456|', 'v_F4', 'r_012|\n456|')
        self.eq('01|23|\n5678', 'v_F0', 'r_|012|3\n5678')
        self.eq('r_0xx|ba|5', 'v_Fx', 'r_0x|xba|5')
        self.eq('r_01x|xa|5', 'v_Fx', 'r_01|xxa|5')
        self.eq('01x|xb|5', 'v_Fx', '01x|x|b5')
        self.eq('01|xxb|5', 'v_Fx', '01|xx|b5')
        self.eq('01x|ax|5', 'v_Fx', 'r_01|xa|x5')
        self.eq('r_|xa|', 'v_Fx', 'r_|xa|')
        self.eq('|xb|', 'v_Fx', '|x|b')
        self.eq('r_x|r|', 'v_Fx', 'r_|xr|')
        self.eq('x|f|', 'v_Fx', 'r_|xf|')
        self.eq('r_|r|', 'v_Fr', 'r_|r|')
        self.eq('|f|', 'v_Ff', '|f|')

    @unittest.mock_bell()
    def test_V(self):
        self.eq('x\nx\n|x\n|x\n', 'V_Fx', 'x\nx\n|x\n|x\n')
        self.assertBell()

    @unittest.mock_bell()
    def test_d(self):
        self.eq('0x23|a5', 'dFx', '0|a5')
        self.eq('012x|a5', 'dFx', '012|a5')
        self.eq('0xx3|a5', 'dFx', '0x|a5')
        self.eq('01x3|x5', 'dFx', '01|x5')
        self.assertNoBell()
        self.eq('0123|x5', 'dFx', '0123|x5')
        self.assertBellCount(1)
