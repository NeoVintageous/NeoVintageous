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


class Test_f(unittest.FunctionalTestCase):

    def test_n(self):
        self.eq('|12x34', 'n_fx', '12|x34')
        self.eq('|12\\34', 'n_f\\', '12|\\34')
        self.eq('0|a23x5', 'n_fx', '0a23|x5')
        self.eq('0|ax345', 'n_fx', '0a|x345')
        self.eq('0|x2345', 'n_fx', '0|x2345')
        self.eq('0|a2xx5', 'n_fx', '0a2|xx5')
        self.eq('0|x2x45', 'n_fx', '0x2|x45')
        self.eq('0|a23:5', 'n_f:', '0a23|:5')
        self.eq('0|a:345', 'n_f:', '0a|:345')
        self.eq('0|:2345', 'n_f:', '0|:2345')
        self.eq('0|a2::5', 'n_f:', '0a2|::5')
        self.eq('0|:2:45', 'n_f:', '0:2|:45')
        self.eq('1|2345', 'n_f<k4>', '123|45')
        self.eq('1|23-5', 'n_f<kminus>', '123|-5')

    def test_n_special_bar_character(self):
        self.normal('12|34')
        # Overwrite the content above with text containing a literal bar
        # character (i.e. "|"). The normal() api method replaces bar characters
        # with selections and this test is testing against a literal bar char.
        self.write('12|34')
        self.select(0)
        self.feed('n_f|')
        self.assertContent('12|34')
        self.assertSelection(2)

    def test_v(self):
        self.eq('0|ab|3x5', 'v_fx', '0|ab3x|5')
        self.eq('0|a23x|5', 'v_fx', '0|a23x|5')
        self.eq('r_0|b2xa|5', 'v_fx', 'r_0b2|xa|5')
        self.eq('r_0|ba|3x5', 'v_fx', '0b|a3x|5')
        self.eq('r_0|b2x|45', 'v_fx', '0b2|x|45')
        self.eq('r_0|x2a|45', 'v_fx', 'r_0|x2a|45')
        self.eq('|012\n4|56', 'v_f2', '|012\n4|56')
        self.eq('|012\n4|56', 'v_f6', '|012\n456|')
        self.eq('|012\n|456', 'v_f2', '|012\n|456')
        self.eq('|012\n|456', 'v_f6', '|012\n|456')
        self.eq('r_|012\n4|56', 'v_f2', 'r_01|2\n4|56')
        self.eq('r_|012\n4|56', 'v_f6', 'r_|012\n4|56')
        self.eq('r_012|\n4|56', 'v_f2', 'r_012|\n4|56')
        self.eq('r_012|\n4|56', 'v_f6', 'r_012|\n4|56')
        self.eq('r_0123\n|56|78', 'v_f8', '0123\n5|678|')
        self.eq('0|ab|xx5', 'v_fx', '0|abx|x5')
        self.eq('0|ax|x45', 'v_fx', '0|axx|45')
        self.eq('r_0|bx|x45', 'v_fx', '0b|x|x45')
        self.eq('r_0|bxx|45', 'v_fx', 'r_0b|xx|45')
        self.eq('r_0|xa|x45', 'v_fx', '0x|ax|45')
        self.eq('|ax|', 'v_fx', '|ax|')
        self.eq('r_|bx|', 'v_fx', 'b|x|')
        self.eq('|f|x', 'v_fx', '|fx|')
        self.eq('r_|r|x', 'v_fx', '|rx|')
        self.eq('|f|', 'v_ff', '|f|')
        self.eq('|ff|ff', 'v_ff', '|fff|f')
        self.eq('r_|r|', 'v_fr', 'r_|r|')
        self.eq('|r|r', 'v_fr', '|rr|')

    @unittest.mock_bell()
    def test_V(self):
        self.eq('|x\n|x\nx\n', 'V_fx', '|x\n|x\nx\n')
        self.assertBell()

    @unittest.mock_bell()
    def test_d(self):
        self.eq('one |two three', 'dft', 'one |hree')
        self.eq('one |two three three', 'd2ft', 'one |hree')
        self.eq('|a = 1', 'df=', '| 1')
        self.eq('0|a23x5', 'dfx', '0|5')
        self.eq('0|ax345', 'dfx', '0|345')
        self.eq('0|a2xx5', 'dfx', '0|x5')
        self.eq('0|x2x45', 'dfx', '0|45')
        self.assertNoBell()
        self.eq('0|x2345', 'dfx', '0|x2345')
        self.assertBellCount(1)
