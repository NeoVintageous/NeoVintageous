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


class Test_enter(unittest.PatchFeedCommandXpos, unittest.FunctionalTestCase):

    def test_n(self):
        self.eq('|1\n2\n3', 'n_<CR>', '1\n|2\n3')
        self.eq('|1\n    fizz\n3', 'n_<CR>', '1\n    |fizz\n3')
        self.eq('1\n|2\n3\n4\n5\n6\n7', 'n_4<CR>', '1\n2\n3\n4\n5\n|6\n7')
        self.eq('    |x\n  fizz\n', 'n_<CR>', '    x\n  |fizz\n')

    def test_v(self):
        self.eq('1\n|2\n3\n4\n5\n6\n7', 'v_4<CR>', '1\n|2\n3\n4\n5\n6|\n7')
        self.eq('1\n|2\n3\n4\n5\n    fizz\n7', 'v_4<CR>', '1\n|2\n3\n4\n5\n    f|izz\n7')
        self.eq('|fi|zz\n     buzz\n', 'v_<CR>', '|fizz\n     b|uzz\n')
        self.eq('      |fi|zz\n  buzz\n', 'v_<CR>', '      |fizz\n  b|uzz\n')
        self.eq('  |fizz\n|  buzz\n', 'v_<CR>', '  |fizz\n  b|uzz\n')
        self.eq('r_|fi|zz\n  buzz\n', 'v_<CR>', 'f|izz\n  b|uzz\n')

    def test_V(self):
        self.eq('1\n|fizz\n|buzz\n4', 'V_<CR>', '1\n|fizz\nbuzz\n|4')
        self.eq('1\n|fizz\nbuzz\n|three\nfour\n', 'V_<CR>', '1\n|fizz\nbuzz\nthree\n|four\n')
        self.eq('r_1\n|fizz\nbuzz\n|three\n', 'V_<CR>', 'r_1\nfizz\n|buzz\n|three\n')
