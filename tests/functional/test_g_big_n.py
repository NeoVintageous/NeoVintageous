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


class Test_gN(unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()
        self.setLastSearch('fizz')
        self.set_option('wrapscan', True)

    def test_n(self):
        self.eq('a fizz| fizz fizz b', 'n_gN', 'r_v_a |fizz| fizz fizz b')
        self.eq('a fizz |fizz fizz b', 'n_gN', 'r_v_a fizz |fizz| fizz b')
        self.eq('a fizz fi|zz fizz b', 'n_gN', 'r_v_a fizz |fizz| fizz b')
        self.eq('a fizz fiz|z fizz b', 'n_gN', 'r_v_a fizz |fizz| fizz b')
        self.eq('a fizz fizz| fizz b', 'n_gN', 'r_v_a fizz |fizz| fizz b')
        self.eq('a fizz fizz |fizz b', 'n_gN', 'r_v_a fizz fizz |fizz| b')

    def test_v(self):
        self.eq('r_a fizz fizz |fizz| b', 'v_gN', 'r_a fizz |fizz fizz| b')
        self.eq('r_a fizz |fizz fizz| b', 'v_gN', 'r_a |fizz fizz fizz| b')
        self.eq('r_a |fizz fizz fizz| b', 'v_gN', 'r_a fizz fizz |fizz| b')
        self.eq('r_a |fizz fizz| fizz b', 'v_gN', 'a fizz fiz|z f|izz b')

    def test_V(self):
        self.eq('r_a fizz b\na fizz b\n|a fizz b\n|', 'V_gN', 'r_v_a fizz b\na |fizz b\na fizz b\n|')
        self.assertStatusLineIsVisual()

    def test_c(self):
        self.eq('a fi|zz fizz fizz b', 'n_cgN', 'i_a | fizz fizz b')
        self.eq('a fizz fi|zz fizz b', 'n_cgn', 'i_a fizz | fizz b')
        self.eq('x fizz x fizz f|oo fizz x', 'n_cgN', 'i_x fizz x | foo fizz x')
