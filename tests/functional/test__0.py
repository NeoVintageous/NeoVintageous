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


class Test_0(unittest.FunctionalTestCase):

    def test_n_0(self):
        self.eq('|abc', 'n_0', '|abc')
        self.eq('a|bc', 'n_0', '|abc')
        self.eq('ab|c', 'n_0', '|abc')
        self.eq('x\n|ab\nx', 'n_0', 'x\n|ab\nx')
        self.eq('x\na|b\nx', 'n_0', 'x\n|ab\nx')
        self.eq('x\nab|\nx', 'n_0', 'x\n|ab\nx')

    def test_N_0(self):
        self.eq('|abc', '0', '|abc')
        self.eqr('a|bc', '0', 'N_|a|bc')
        self.eqr('ab|c', '0', 'N_|ab|c')
        self.eq('x\n|ab\nx', '0', 'N_x\n|ab\nx')
        self.eqr('x\na|b\nx', '0', 'N_x\n|a|b\nx')
        self.eqr('x\nab|\nx', '0', 'N_x\n|ab|\nx')

    def test_v_0(self):
        self.eqr('x\nab|c|d\nx', 'v_0', 'x\n|abc|d\nx')
        self.eqr('x\na|bc|d\nx', 'v_0', 'x\n|ab|cd\nx')
        self.eq('x\n|abcd|\nx', 'v_0', 'x\n|a|bcd\nx')

    def test_v_0_multiline(self):
        self.eq('x|a\nabc|d\nx', 'v_0', 'x|a\na|bcd\nx')
