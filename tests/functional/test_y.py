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


class Test_y(unittest.FunctionalTestCase):

    def test_v_y(self):
        self.eq('x|ab|x', 'v_y', 'n_x|abx')
        self.assertRegister('"', 'ab')

        self.eq('x|ab|\nx', 'v_y', 'n_x|ab\nx')
        self.assertRegister('"', 'ab', 'should not capture newline')

        self.eq('x|ab\n|x', 'v_y', 'n_x|ab\nx')
        self.assertRegister('"', 'ab\n', 'should capture newline')

    def test_yiw(self):
        self.eq('x wo|rd x', 'yiw', 'x |word x')
        self.assertRegister('"', 'word')

    def test_ydollar(self):
        self.eq('x a|b x', 'y$', 'x a|b x')
        self.assertRegister('"', 'b x')

        self.eq('x a|b x\n', 'y$', 'x a|b x\n')
        self.assertRegister('"', 'b x', 'should not include eol newline')
