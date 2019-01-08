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

    def test_gg(self):
        self.eq('foo\nb|ar', 'gg', '|foo\nbar')

    def test_n_gg(self):
        self.eq('foo\nb|ar', 'n_gg', '|foo\nbar')

    def test_v_gg(self):
        self.eq('fizz\nb|u|zz', 'v_gg', '|fizz\nbu|zz')

    def test_v_gg_reverse_sel(self):
        self.rvisual('fiz|zer\nbu|zz')
        self.feed('v_gg')
        self.assertRVisual('|fizzer\nbu|zz')

    def test_l_gg(self):
        self.eqr('11\n|2\n33\n|44', 'l_gg', '|11\n2\n33\n|44')

    def test_l_gg_reverse(self):
        self.rvisual('11\n|2\n33\n|44')
        self.feed('l_gg')
        self.assertVisual('|11\n2\n33\n|44')
        self.assertSelectionIsReveresed()
