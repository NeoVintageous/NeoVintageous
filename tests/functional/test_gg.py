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


class Test_gg(unittest.FunctionalTestCase):

    def test_n_gg(self):
        self.eq('foo\nb|ar', 'n_gg', '|foo\nbar')
        self.eq('    foo\nb|ar', 'n_gg', '    |foo\nbar')
        self.eq('|1\n2\n    foo', 'n_G', '1\n2\n    |foo')

    def test_N_gg(self):
        self.eqr('foo\nb|ar', 'gg', 'N_|foo\nbar|')

    def test_v_gg(self):
        self.eqr('fizz\nb|u|zz', 'v_gg', '|fizz\nbu|zz')
        self.eq('fi|zz\n2\n    buzz', 'v_G', 'fi|zz\n2\n    b|uzz')

    def test_v_gg_reverse_sel(self):
        self.eqr('r_fiz|zer\nbu|zz', 'v_gg', '|fizzer\nbu|zz')

    def test_l_gg(self):
        self.eqr('11\n|2\n33\n|44', 'l_gg', '|11\n2\n33\n|44')

    def test_l_gg_reverse(self):
        self.eqr('r_11\n|2\n33\n|44', 'l_gg', '|11\n2\n33\n|44')
