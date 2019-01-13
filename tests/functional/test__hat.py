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


class TestHat(unittest.FunctionalTestCase):

    def test_n__hat(self):
        self.eq('012|a4', 'n_^', '|012a4')
        self.eq('  2|a4', 'n_^', '  |2a4')
        self.eq(' | 234', 'n_^', '  |234')

    def test_N__hat(self):
        self.eqr('012|a4', '^', 'N_|012|a4')
        self.eqr('  2|a4', '^', 'N_  |2|a4')
        self.eq('|  234', '^', 'N_|  |234')
        self.eqr('  |a|34', '^', 'N_  |a|34')

    def test_v__hat(self):
        self.eqr('r_0|b2a|45', 'v_^', 'v_|0b2a|45')
        self.eqr('0|a2b4|5', 'v_^', 'v_|0a|2b45')
        self.eqr('r_  2|ba5|', 'v_^', 'v_  |2ba5|')
        self.eqr('  2|ab5|', 'v_^', 'v_  |2a|b5')
        self.eq('|  |2345', 'v_^', 'v_|  2|345')
        self.eqr('r_ | 23a5|', 'v_^', 'v_  |23a5|')
        self.eq(' | 23b5|', 'v_^', 'v_ | 2|3b5')
        self.eq('|f|', 'v_^', '|f|')
        self.eq('r_|x|', 'v_^', '|x|')
        self.eq('| 123\n| 678', 'v_^', '| 1|23\n 678')
        self.eqr('r_ 123|\n 67|8', 'v_^', ' |123\n 67|8')
        self.eq(' 1|23\n 67|8', 'v_^', ' 1|23\n 6|78')
        self.eqr('r_ 1|23\n 67|8', 'v_^', ' |123\n 67|8')
