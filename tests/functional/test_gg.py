# Copyright (C) 2018-2023 The NeoVintageous Team (NeoVintageous).
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


class Test_gg(unittest.FunctionalTestCase):

    def test_n(self):
        self.eq('foo\nb|ar', 'n_gg', '|foo\nbar')
        self.eq('    foo\nb|ar', 'n_gg', '    |foo\nbar')
        self.eq('|1\n2\n3\n4\n5', 'n_3gg', '1\n2\n|3\n4\n5')
        self.eq('|1\n2\n    3x\n4\n5', 'n_3gg', '1\n2\n    |3x\n4\n5')
        self.eq('|1\n2\n3\n4\n5', 'n_5gg', '1\n2\n3\n4\n|5')
        self.eq('|1\n2\n3', 'n_9gg', '1\n2\n|3')
        self.eq('|1\n2\n3\n', 'n_9gg', '1\n2\n3|\n')
        self.eq('|1\n2\n3\n\n', 'n_9gg', '1\n2\n3\n|\n')

    def test_v(self):
        self.eq('fizz\nb|u|zz', 'v_gg', 'r_|fizz\nbu|zz')
        self.eq('r_1x\n2x\n3|x\n4|x\n5x', 'v_gg', 'r_|1x\n2x\n3x\n4|x\n5x')
        self.eq('1x\n2x\n3|x\n4|x\n5x', 'v_gg', 'r_|1x\n2x\n3x|\n4x\n5x')
        self.eq('r_fiz|zer\nbu|zz', 'v_gg', 'r_|fizzer\nbu|zz')
        self.eq('1x\n2x\n3|x\n4|x\n5x', 'v_2gg', 'r_1x\n|2x\n3x|\n4x\n5x')
        self.eq('r_1x\n2x\n3|x\n4|x\n5x', 'v_2gg', 'r_1x\n|2x\n3x\n4|x\n5x')

    def test_l(self):
        self.eq('11\n|2\n33\n|44', 'V_gg', 'r_|11\n2\n|33\n44')
        self.eq('r_11\n|2\n33\n|44', 'V_gg', 'r_|11\n2\n33\n|44')

    def test_d(self):
        self.eq('foo\nb|ar', 'dgg', '|')
        self.eq('1x\n2x\n3x\n4|x\n5x', '2dgg', '1x\n|5x')

    def test_b(self):
        self.eq('1\n2\n|3|\nx\n', 'b_gg', 'u_|1|\n|2|\n|3|\nx\n')
        self.eq('111\n222\n|333|\nx\n', 'b_gg', 'u_|1|11\n|2|22\n|3|33\nx\n')
        self.eq('111\n222\n3|33|\nx\n', 'b_gg', 'r_u_|11|1\n|22|2\n|33|3\nx\n')
        self.eq('1111\n2222\n33|3|3\nx\n', 'b_gg', 'r_u_|111|1\n|222|2\n|333|3\nx\n')
        self.eq('1111\n\n33|3|3\nx\n', 'b_gg', 'r_u_|111|1\n|\n||333|3\nx\n')
        self.eq('1\n2222\n33|3|3\nx\n', 'b_gg', 'r_u_|1\n||222|2\n|333|3\nx\n')
        self.eq('1\n2222\n33|3|3\nx\n', 'b_gg', 'r_u_|1\n||222|2\n|333|3\nx\n')
        self.eq('  11111\n2222222\n3333|33|3\n', 'b_gg', 'r_u_  |111|11\n22|222|22\n33|333|33\n')
        self.eq('     11\n2222222\n3|33|3333\n', 'b_gg', 'u_ |    1|1\n2|22222|2\n3|33333|3\n')
