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


class Test_esc(unittest.FunctionalTestCase):

    @unittest.mock_run_commands('hide_panel')
    def test_n_esc(self):
        self.eq('fi|zz', 'n_<esc>', 'n_fi|zz')
        self.eq('fi|zz bu|zz fi|zz', 'n_<esc>', 'n_fi|zz buzz fizz')

    def test_i_esc(self):
        self.eq('fi|zz', 'i_<esc>', 'n_f|izz')

    def test_v_esc(self):
        self.eq('f|iz|z', 'v_<esc>', 'n_fi|zz')
        self.eq('r_f|iz|z', 'v_<esc>', 'n_f|izz')
        self.eq('1\n|\n|3', 'v_<esc>', 'n_1\n|\n3')
        self.eq('1\n2|\n|3', 'v_<esc>', 'n_1\n|2\n3')

    def test_l_esc(self):
        self.eq('1\n|fizz|', 'l_<esc>', 'n_1\nfiz|z')
        self.eq('1\n|fizz|\n', 'l_<esc>', 'n_1\nfiz|z\n')
        self.eq('1\n|fizz\n|3', 'l_<esc>', 'n_1\nfiz|z\n3')
        self.eq('r_1\n|fizz|', 'l_<esc>', 'n_1\n|fizz')

    def test_b_esc(self):
        self.eq('f|iz|z\nb|uz|z\n', 'b_<esc>', 'n_fizz\nbu|zz\n')
        self.eq('r_f|iz|z\nb|uz|z\n', 'b_<esc>', 'n_fizz\nb|uzz\n')

    def test_N_esc(self):
        self.eq('fi|zzb|uzz', '<esc>', 'N_fi|zzb|uzz')

    def test_O_esc(self):
        self.normal('1\n2|\n3')
        self.feed('n_O')
        self.feed('i_<esc>')
        self.assertNormal('1\n|\n2\n3')

    def test_O_esc_strip_leading_whitespace(self):
        self.normal('    1\n    2|\n    3')
        self.feed('n_O')
        self.assertInsert('    1\n    |\n    2\n    3')
        self.feed('i_<esc>')
        self.assertNormal('    1\n|\n    2\n    3')
        self.assertXpos(4)
