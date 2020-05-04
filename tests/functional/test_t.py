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


class Test_t(unittest.FunctionalTestCase):

    def test_n(self):
        self.eq('|12x34', 'n_tx', '1|2x34')
        self.eq('|12\\34', 'n_t\\', '1|2\\34')
        self.eq('0|a23x5', 'n_tx', '0a2|3x5')
        self.eq('0|ax345', 'n_tx', '0|ax345')
        self.eq('0|x2345', 'n_tx', '0|x2345')
        self.eq('0|a2xx5', 'n_tx', '0a|2xx5')
        self.eq('0|x2x45', 'n_tx', '0x|2x45')
        self.eq('0|a23:5', 'n_t:', '0a2|3:5')
        self.eq('0|a:345', 'n_t:', '0|a:345')
        self.eq('0|:2345', 'n_t:', '0|:2345')
        self.eq('0|a2::5', 'n_t:', '0a|2::5')
        self.eq('0|:2:45', 'n_t:', '0:|2:45')
        self.eq('xx|xx', 'n_tx', 'xx|xx')
        self.eq('1|23*5', 'n_t<kmultiply>', '12|3*5')

    def test_n_special_bar_char(self):
        self.normal('12|34')
        # Overwrite the content above with text containing a literal bar
        # character (i.e. "|"). The normal() api method replaces bar characters
        # with selections and this test is testing against a literal bar char.
        self.write('12|34')
        self.select(0)
        self.feed('n_t|')
        self.assertContent('12|34')
        self.assertSelection(1)

    def test_v(self):
        self.eq('0|ab|3x5', 'v_tx', '0|ab3|x5')
        self.eq('0|a23x|5', 'v_tx', '0|a23x|5')
        self.eq('r_0|b2xa|5', 'v_tx', 'r_0b|2xa|5')
        self.eq('r_0|ba|3x5', 'v_tx', '0b|a3|x5')
        self.eq('r_0|b2x|45', 'v_tx', 'r_0b|2x|45')
        self.eq('r_0|x2a|45', 'v_tx', 'r_0|x2a|45')
        self.eq('0|a2b|x5', 'v_tx', '0|a2b|x5')
        self.eq('r_0|bx3a|5', 'v_tx', 'r_0|bx3a|5')
        self.eq('r_0|b2a|x5', 'v_tx', '0b2|a|x5')
        self.eq('|012\n4|56', 'v_t2', '|012\n4|56')
        self.eq('|012\n4|56', 'v_t6', '|012\n45|6')
        self.eq('|012\n|456', 'v_t2', '|012\n|456')
        self.eq('|012\n|456', 'v_t6', '|012\n|456')
        self.eq('r_|012\n4|56', 'v_t2', 'r_0|12\n4|56')
        self.eq('r_|012\n4|56', 'v_t6', 'r_|012\n4|56')
        self.eq('r_012|\n4|56', 'v_t2', 'r_012|\n4|56')
        self.eq('r_012|\n4|56', 'v_t6', 'r_012|\n4|56')
        self.eq('r_0123\n|56|78', 'v_t8', '0123\n5|67|8')
        self.eq('0|ab|xx5', 'v_tx', '0|ab|xx5')
        self.eq('0|ax|x45', 'v_tx', '0|ax|x45')
        self.eq('r_0|bx|x45', 'v_tx', 'r_0|bx|x45')
        self.eq('r_0|bxx|45', 'v_tx', 'r_0|bxx|45')
        self.eq('r_0|xa|x45', 'v_tx', '0x|a|x45')
        self.eq('|ax|', 'v_tx', '|ax|')
        self.eq('r_|bx|', 'v_tx', 'r_|bx|')
        self.eq('|f|x', 'v_tx', '|f|x')
        self.eq('r_|r|x', 'v_tx', '|r|x')
        self.eq('|f|', 'v_tf', '|f|')
        self.eq('r_|r|', 'v_tr', 'r_|r|')

    @unittest.mock_bell()
    def test_V(self):
        self.eq('|x\n|x\nx\n', 'V_tx', '|x\n|x\nx\n')
        self.assertBell()

    @unittest.mock_bell()
    def test_d(self):
        self.eq('0|a23x5', 'dtx', '0|x5')
        self.eq('0|ax345', 'dtx', '0|x345')
        self.eq('0|a2xx5', 'dtx', '0|xx5')
        self.eq('0|x2x45', 'dtx', '0|x45')
        self.assertNoBell()
        self.eq('0|x2345', 'dtx', '0|x2345')
        self.assertBellCount(1)
