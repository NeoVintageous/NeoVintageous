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


class Test_ctrl_y(unittest.FunctionalTestCase):

    def test_n(self):
        self.normal('1\n2\n3\n4\n5\n6\n7\n|8\n9\n10')
        self.feed('3<C-e>')
        self.assertVisibleRegion((6, 20))
        self.feed('<C-y>')
        self.assertNormal('1\n2\n3\n4\n5\n6\n7\n|8\n9\n10')
        self.assertVisibleRegion((4, 20))
        self.feed('<C-y>')
        self.assertVisibleRegion((2, 20))

    def test_n_count(self):
        self.normal('1\n2\n3\n4\n5\n6\n7\n|8\n9\n10')
        self.feed('4<C-e>')
        self.assertVisibleRegion((8, 20))
        self.feed('3<C-y>')
        self.assertNormal('1\n2\n3\n4\n5\n6\n7\n|8\n9\n10')
        self.assertVisibleRegion((2, 20))

    def test_v(self):
        self.eq('1\nfi|zz\nbu|zz\n3\n4', 'v_<C-y>', '1\nfi|zz\nbu|zz\n3\n4')

    def test_V(self):
        self.eq('1\n|fizz\nbuzz\n|3\n4', 'V_<C-y>', '1\n|fizz\nbuzz\n|3\n4')
