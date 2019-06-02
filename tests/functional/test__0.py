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

    def test_n(self):
        self.eq('|abc', 'n_0', '|abc')
        self.eq('a|bc', 'n_0', '|abc')
        self.eq('ab|c', 'n_0', '|abc')
        self.eq('x\n|ab\nx', 'n_0', 'x\n|ab\nx')
        self.eq('x\na|b\nx', 'n_0', 'x\n|ab\nx')
        self.eq('x\nab|\nx', 'n_0', 'x\n|ab\nx')

    def test_v(self):
        self.eq('x\nab|c|d\nx', 'v_0', 'r_x\n|abc|d\nx')
        self.eq('x\na|bc|d\nx', 'v_0', 'r_x\n|ab|cd\nx')
        self.eq('x\n|abcd|\nx', 'v_0', 'x\n|a|bcd\nx')
        self.eq('r_1\nfi|zz\nbu|zz', 'v_0', 'r_1\n|fizz\nbu|zz')
        self.eq('fi|zz\n|buzz\n', 'v_0', 'r_|fiz|z\nbuzz\n')
        self.eq('x|a\nabc|d\nx', 'v_0', 'x|a\na|bcd\nx')

    def test_V(self):
        self.eq('fizz\n|buzz\n|fizz', 'V_0', 'r_fizz\n|buzz\n|fizz')
        self.eq('fizz\n|buzz\nfizz\n|buzz\n', 'V_0', 'fizz\n|buzz\nfizz\n|buzz\n')

    def test_b(self):
        self.eq('  fizz b|uzz|\n  fizz b|uzz|\nfizz', 'b_0', 'r_|  fizz bu|zz\n|  fizz bu|zz\nfizz')

    def test_c(self):
        self.eq('|abc', 'c0', 'i_|abc')
        self.eq('a|bc', 'c0', 'i_|bc')
        self.eq('ab|c', 'c0', 'i_|c')
        self.eq('x\n|ab\nx', 'c0', 'i_x\n|ab\nx')
        self.eq('x\na|b\nx', 'c0', 'i_x\n|b\nx')
        self.eq('x\nab|\nx', 'c0', 'i_x\n|\nx')

    def test_d(self):
        self.eq('123|456', 'd0', '|456')
        self.eq('x\n123|456\nx', 'd0', 'x\n|456\nx')
        self.eq('x\n\n|\n\nx', 'd0', 'x\n\n|\n\nx')
