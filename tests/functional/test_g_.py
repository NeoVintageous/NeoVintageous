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


class Test_g_(unittest.FunctionalTestCase):

    def test_n(self):
        self.eq('1\n|fizz\nbuzz', 'n_g_', '1\nfiz|z\nbuzz')
        self.eq('1\n|fizz    \nbuzz', 'n_g_', '1\nfiz|z    \nbuzz')
        self.eq('|fizz\nbuzz  \nx', 'n_2g_', 'fizz\nbuz|z  \nx')
        self.eq('|', 'n_g_', '|')
        self.eq('| ', 'n_g_', '| ')
        self.eq('1\n|2\nfizz', 'n_5g_', '1\n2\nfiz|z')
        self.eq('1\n|2\n\n', 'n_5g_', '1\n2\n|\n')
        self.eq('1\n|2\n\n\n', 'n_5g_', '1\n2\n\n|\n')

    def test_v(self):
        self.eq('1\n|fizz\nbuzz', 'v_g_', '1\n|fizz|\nbuzz')
        self.eq('1\nfi|zz buzz\n3', 'v_g_', '1\nfi|zz buzz|\n3')
        self.eq('r_1\nfi|zz b|uzz\n3', 'v_g_', '1\nfizz |buzz|\n3')
        self.eq('1\n|fizz', 'v_g_', '1\n|fizz|')
        self.eq('r_|fizz|', 'v_g_', 'r_fiz|z|')
        self.eq('r_|fizz|\n', 'v_g_', 'r_fiz|z|\n')
        self.eq('|fizz|', 'v_g_', '|fizz|')
        self.eq('r_1\nfi|zz buzz|\n3', 'v_g_', 'r_1\nfizz buz|z|\n3')
        self.eq('|f|izz    \nx', 'v_g_', '|fizz|    \nx')

    def test_V(self):
        self.eq('fizz1\n|fizz2\n|fizz3  \nfizz4\n', 'V_2g_', 'fizz1\n|fizz2\nfizz3  \n|fizz4\n')

    def test_b(self):
        self.eq('|fi|zzbuzz\n|fi|zz    \n', 'b_g_', '|fizz|buzz\n|fizz|    \n')

    def test_c(self):
        self.eq('fi|zz\nbuzz', 'cg_', 'i_fi|\nbuzz')
        self.eq('fi|zz  \nbuzz', 'cg_', 'i_fi|  \nbuzz')
        self.eq('fi|zz\nbuzz\nfizz', '2cg_', 'i_fi|\nfizz')
        self.eq('fi|zz\nbuzz  \nfizz', '2cg_', 'i_fi|  \nfizz')

    def test_d(self):
        self.eq('|fizz\nbuzz', 'dg_', '|\nbuzz')
        self.eq('|fizz  \nbuzz', 'dg_', '|  \nbuzz')
        self.eq('1\n|fizz\nbuzz', 'dg_', '1\n|\nbuzz')
        self.eq('1\nf|izz\nbuzz', 'dg_', '1\n|f\nbuzz')
        self.eq('fi|zz    \nbuzz', 'dg_', 'fi|    \nbuzz')
