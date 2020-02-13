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


class Test_m(unittest.FunctionalTestCase):

    def test_n(self):
        self.eq('1\nfi|zz\nbuzz\n', 'n_mx', '1\nfi|zz\nbuzz\n')

    def test_v(self):
        self.eq('1\nfi|zz bu|zz\n3\n', 'v_mx', '1\nfi|zz bu|zz\n3\n')
        self.assertMark('x', '1\nfizz b|uzz\n3\n')
        self.eq('r_1\nfi|zz bu|zz\n3\n', 'v_mx', 'r_1\nfi|zz bu|zz\n3\n')
        self.assertMark('x', '1\nfi|zz buzz\n3\n')

    def test_V(self):
        self.eq('1\n|fizz buzz\n|3\n', 'V_mx', '1\n|fizz buzz\n|3\n')

    def test_b(self):
        self.eq('1\nf|iz|z\nb|uz|z\n3\n', 'b_mx', '1\nf|iz|z\nb|uz|z\n3\n')
