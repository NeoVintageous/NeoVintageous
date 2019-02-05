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


class Test_o(unittest.FunctionalTestCase):

    def test_o(self):
        self.eq('|', 'o', 'i_\n|')
        self.eq('|\n', 'o', 'i_\n|\n')
        self.eq('|a\nb\n', 'o', 'i_a\n|\nb\n')

    def test_v_o(self):
        self.eq('x|fizz|x', 'v_o__alt1', 'r_x|fizz|x')
        self.eq('r_x|fizz|x', 'v_o__alt1', 'x|fizz|x')

    def test_N_o(self):
        self.eq('x|fizz|x', 'o__alt1', 'N_x|fizz|x')
        self.eq('r_x|fizz|x', 'o__alt1', 'N_x|fizz|x')

    def test_l_o(self):
        self.eq('x\n|fizz\n|x', 'l_o__alt1', 'r_x\n|fizz\n|x')
        self.eq('r_x\n|fizz\n|x', 'l_o__alt1', 'x\n|fizz\n|x')

    def test_multiple_count_o(self):
        self.eq('|', '2o', 'i_\n|\n|')

    def test_multiple_count_v_o(self):
        self.eq('fo|o\nba|r', '2o', 'i_foo\n|\n|\nbar\n|\n|')
