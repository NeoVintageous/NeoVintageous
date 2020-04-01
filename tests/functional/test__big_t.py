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


class Test_T(unittest.FunctionalTestCase):

    def test_n(self):
        self.eq('0x23|a5', 'n_Tx', '0x|23a5')
        self.eq('012x|a5', 'n_Tx', '012x|a5')
        self.eq('0123|x5', 'n_Tx', '0123|x5')
        self.eq('0xx3|a5', 'n_Tx', '0xx|3a5')
        self.eq('01x3|x5', 'n_Tx', '01x|3x5')
        self.eq('x|xxx', 'n_Tx', 'x|xxx')

    def test_v(self):
        self.eq('r_0x2|ba|5', 'v_Tx', 'r_0x|2ba|5')
        self.eq('r_0|x23a|5', 'v_Tx', 'r_0|x23a|5')
        self.eq('0|ax3b|5', 'v_Tx', '0|ax3|b5')
        self.eq('0x2|ab|5', 'v_Tx', 'r_0x|2a|b5')
        self.eq('01|x3b|5', 'v_Tx', '01|x3|b5')
        self.eq('01|a3x|5', 'v_Tx', '01|a3x|5')
        self.eq('r_0x|b3a|5', 'v_Tx', 'r_0x|b3a|5')
        self.eq('0|a2xb|5', 'v_Tx', '0|a2xb|5')
        self.eq('0x|a3b|5', 'v_Tx', '0x|a|3b5')
        self.eq('01|2\n456|', 'v_T0', '01|2\n456|')
        self.eq('01|2\n456|', 'v_T4', '01|2\n45|6')
        self.eq('01|2\n|456', 'v_T0', 'r_0|12|\n456')
        self.eq('01|2\n|456', 'v_T5', '01|2\n|456')
        self.eq('r_01|2\n456|', 'v_T0', 'r_0|12\n456|')
        self.eq('r_01|2\n456|', 'v_T4', 'r_01|2\n456|')
        self.eq('r_012|\n456|', 'v_T0', 'r_0|12\n456|')
        self.eq('r_012|\n456|', 'v_T4', 'r_012|\n456|')
        self.eq('01|23|\n5678', 'v_T0', 'r_0|12|3\n5678')
        self.eq('r_0xx|ba|5', 'v_Tx', 'r_0xx|ba|5')
        self.eq('r_01x|xa|5', 'v_Tx', 'r_01x|xa|5')
        self.eq('01x|xb|5', 'v_Tx', '01x|xb|5')
        self.eq('01|xxb|5', 'v_Tx', '01|xxb|5')
        self.eq('01x|ax|5', 'v_Tx', '01x|a|x5')
        self.eq('r_|xa|', 'v_Tx', 'r_|xa|')
        self.eq('|xb|', 'v_Tx', '|xb|')
        self.eq('r_x|r|', 'v_Tx', 'x|r|')
        self.eq('x|f|', 'v_Tx', 'x|f|')
        self.eq('r_|r|', 'v_Tr', 'r_|r|')
        self.eq('|f|', 'v_Tf', '|f|')

    @unittest.mock_bell()
    def test_V(self):
        self.eq('x\nx\n|x\n|x\n', 'V_Tx', 'x\nx\n|x\n|x\n')
        self.assertBell()

    @unittest.mock_bell()
    def test_d(self):
        self.eq('0x23|a5', 'dTx', '0x|a5')
        self.eq('0xx3|a5', 'dTx', '0xx|a5')
        self.eq('01x3|x5', 'dTx', '01x|x5')
        self.assertNoBell()
        self.eq('0123|x5', 'dTx', '0123|x5')
        self.eq('012x|a5', 'dTx', '012x|a5')
        self.assertBellCount(2)
