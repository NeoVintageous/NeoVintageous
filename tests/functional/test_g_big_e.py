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


class Test_gE(unittest.FunctionalTestCase):

    def test_n(self):
        self.eq('one t|wo', 'n_ge', 'on|e two')
        self.eq('one.,()$ t|wo', 'n_gE', 'one.,()|$ two')
        self.eq('one two ,.$;_() four fi|ve', 'n_3gE', 'one tw|o ,.$;_() four five')

    def test_v(self):
        self.eq('one t|w|o', 'v_gE', 'r_on|e tw|o')
        self.eq('1 two ab cd f|i|ve', 'v_3gE', 'r_1 tw|o ab cd fi|ve')
        self.eq('r_1 two a|b cd fi|ve', 'v_gE', 'r_1 tw|o ab cd fi|ve')
        self.eq('1 |two a|b', 'v_gE', '1 |two| ab')

    def test_b(self):
        self.eq('r_one t|wo|\none t|wo|\n', 'b_gE', 'r_on|e two|\non|e two|\n')

    def test_c(self):
        self.eq('fizzx ab|cbuzz', 'cgE', 'i_fizz|buzz')

    def test_d(self):
        self.eq('fizzx ab|cbuzz', 'dgE', 'fizz|buzz')
