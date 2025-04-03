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


class Test_minus(unittest.PatchFeedCommandXpos, unittest.FunctionalTestCase):

    def test_n(self):
        self.eq('1\n2\n|3', 'n_-', '1\n|2\n3')
        self.eq('1\n    fizz\n|3', 'n_-', '1\n    |fizz\n3')
        self.eq('1\n2\n3\n4\n5\n|6\n7', 'n_4-', '1\n|2\n3\n4\n5\n6\n7')
        self.eq('  1\n  fizz\n    |y\n', 'n_-', '  1\n  |fizz\n    y\n')

    def test_v(self):
        self.eq('1\n    fizz\n3\n4\n5\nf|izz bu|zz\n7', 'v_4-', 'r_1\n    |fizz\n3\n4\n5\nfi|zz buzz\n7')
        self.eq('|  fizz\nbuzz\n|x', 'v_-', '|  f|izz\nbuzz\nx')

    def test_V(self):
        self.eq('1\nfizz\n|buzz\n|4', 'V_-', 'r_1\n|fizz\nbuzz\n|4')
        self.eq('1|\nfizz\nbuzz\nthree\n|four\n', 'V_-', '1|\nfizz\nbuzz\n|three\nfour\n')
        self.eq('r_1\nfizz\n|buzz\nthree\n|', 'V_-', 'r_1\n|fizz\nbuzz\nthree\n|')

    @unittest.mock_bell()
    def test_d(self):
        self.eq('1\n2\n|3\n4\n5\n', 'd-', '1\n|4\n5\n')
        self.eq('1\n2\n3\n4\n5\n|6\n7\n8', '3d-', '1\n2\n|7\n8')
        self.eq('  1\n  2\n  |3\n  4\n  5\n', 'd-', '  1\n  |4\n  5\n')
        self.eq('  1\n  2\n|  3\n  4\n  5\n', 'd-', '  1\n  |4\n  5\n')
        self.assertNoBell()
