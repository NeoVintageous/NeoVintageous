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


class Test_comma(unittest.FunctionalTestCase):

    def test_n(self):
        self.normal('_x__x__x__x__x__x_|_x_')
        self.feed('fx')
        self.feed(',')
        self.assertNormal('_x__x__x__x__x__|x__x_')
        self.feed('3,')
        self.assertNormal('_x__x__|x__x__x__x__x_')
        self.feed('Fx')
        self.assertNormal('_x__|x__x__x__x__x__x_')
        self.feed(',')
        self.assertNormal('_x__x__|x__x__x__x__x_')
        self.feed('Tx')
        self.assertNormal('_x__x|__x__x__x__x__x_')
        self.feed(',')
        self.assertNormal('_x__x_|_x__x__x__x__x_')
        self.feed('2,')
        self.assertNormal('_x__x__x__x_|_x__x__x_')
        self.feed('tx')
        self.assertNormal('_x__x__x__x_|_x__x__x_')
        self.feed(',')
        self.assertNormal('_x__x__x__x|__x__x__x_')
        self.feed(',')
        self.assertNormal('_x__x__x|__x__x__x__x_')

    @unittest.mock_bell()
    def test_V(self):
        self.eq('x\nx\n|xx\nx\n', 'n_fx', 'x\nx\nx|x\nx\n')
        self.feed('V')
        self.assertVline('x\nx\n|xx\n|x\n')
        self.feed(',')
        self.assertVline('x\nx\n|xx\n|x\n')
        self.assertBell()
