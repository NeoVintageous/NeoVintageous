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


class Test_I(unittest.FunctionalTestCase):

    def test_n(self):
        self.eq('|', 'I', 'i_|')
        self.eq('abc|d', 'I', 'i_|abcd')
        self.eq('x\nab|cd', 'I', 'i_x\n|abcd')

    def test_v(self):
        self.eq('x|ab|x', 'v_I', 'i_|xabx')
        self.eq('x\na|bx|\n', 'v_I', 'i_x\n|abx\n')
        self.eq('r_xa|bc|x', 'v_I', 'i_|xabcx')
        self.eq('x\n|ab\n|x', 'l_I', 'i_x\n|ab\nx')
        self.eq('r_x\n|ab\n|x', 'l_I', 'i_x\n|ab\nx')
        self.eq('r_|    fizz\n|x', 'l_I', 'i_|    fizz\nx')
        self.eq('fizz\nbu|zz\nfi|zz', 'l_I', 'i_fizz\n|buzz\nfizz')

    def test_V(self):
        self.eq('x\n|two\n|y', 'l_I', 'i_x\n|two\ny')

    def test_b(self):
        self.eq('x\na|bc|d\nx\nc|de|f\nx', 'b_I', 'i_x\na|bcd\nx\nc|def\nx')

    def test_s(self):
        self.eq('|fizz|', 's_I', 'i_|fizz')
        self.eq('x |fizz| y', 's_I', 'i_x |fizz y')
        self.eq('x |fizz| |buzz| y', 's_I', 'i_x |fizz |buzz y')
        self.eq('x |fizz| y\nx |buzz| y', 's_I', 'i_x |fizz y\nx |buzz y')
