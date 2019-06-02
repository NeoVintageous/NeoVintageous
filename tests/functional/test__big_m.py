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


class Test_M(unittest.FunctionalTestCase):

    @unittest.mock_ui()
    def test_n(self):
        self.eq('|1\n2\n3', 'n_M', '1\n|2\n3')
        self.eq('1\n|2\n3', 'n_M', '1\n|2\n3')
        self.eq('1\n2\n|3', 'n_M', '1\n|2\n3')
        self.eq('|1\n    2\n3', 'n_M', '1\n    |2\n3')
        self.eq('|1\n2\n3\n4\n5\n6', 'n_M', '1\n2\n|3\n4\n5\n6')

    @unittest.mock_ui(visible_region=(2, 9))
    def test_n_M_should_be_within_visible_region(self):
        self.eq('1\n|2\n3\n4\n5\n6', 'n_M', '1\n2\n|3\n4\n5\n6')

    @unittest.mock_ui(visible_region=(4, 9))
    def test_n_M_should_be_within_visible_region2(self):
        self.eq('1\n2\n3\n4\n|5\n6', 'n_M', '1\n2\n3\n|4\n5\n6')

    @unittest.mock_ui()
    def test_v(self):
        self.eq('a|bc\n2\n    xyz\n4\n5\n6', 'v_M', 'a|bc\n2\n    x|yz\n4\n5\n6')
        self.eq('1\n2\n    xyz\n4\n5\n|abc', 'v_M', 'r_1\n2\n    |xyz\n4\n5\na|bc')
        self.eq('1|11\n2\n    abc\n4\n5\n6|', 'v_M', '1|11\n2\n    a|bc\n4\n5\n6')
        self.eq('1\n2\n    abc\n4|44\n55|5\n6', 'v_M', 'r_1\n2\n    |abc\n44|4\n555\n6')
        self.eq('1|11\n2\n    abc\n4\n55|5\n6', 'v_M', '1|11\n2\n    a|bc\n4\n555\n6')
        self.eq('r_1|11\n22|2\n    abc\n4\n5\n6', 'v_M', '111\n2|22\n    a|bc\n4\n5\n6')
        self.eq('r_1\n2\n    abc\n4|44\n55|5\n6', 'v_M', 'r_1\n2\n    |abc\n444\n55|5\n6')
        self.eq('|1\n2\n    fizz\n4\n5\n6', 'v_M', '|1\n2\n    f|izz\n4\n5\n6')
        self.eq('|1\n2\n    |fizz\n4\n5\n6', 'v_M', '|1\n2\n    f|izz\n4\n5\n6')
        self.eq('|1\n2\n    |fizz\n4\n5\n6', 'v_M', '|1\n2\n    f|izz\n4\n5\n6')
        self.eq('r_|1\n2\n    |fizz\n4\n5\n6', 'v_M', '1\n2\n   | f|izz\n4\n5\n6')
        self.eq('r_1\n2\n  |  |fizz\n4\n5\n6', 'v_M', '1\n2\n   | f|izz\n4\n5\n6')

    @unittest.mock_ui()
    def test_V(self):
        self.eq('|1\n2\n|3\n4\n5\n6', 'V_M', '|1\n2\n3\n|4\n5\n6')
        self.eq('|1\n2\n3\n4\n5\n|6', 'V_M', '|1\n2\n3\n|4\n5\n6')
        self.eq('r_1\n2\n3\n|4\n5\n|6', 'V_M', 'r_1\n2\n|3\n4\n5\n|6')
        self.eq('r_1\n|2\n3\n4\n5\n|6', 'V_M', 'r_1\n2\n|3\n4\n5\n|6')
        self.eq('1\n2\n3\n|4\n5\n|6', 'V_M', 'r_1\n2\n|3\n4\n|5\n6')
        self.eq('r_|1\n2\n|3\n4\n5\n6', 'V_M', '1\n|2\n3\n|4\n5\n6')

    @unittest.mock_ui()
    def test_c(self):
        self.eq('abc\nd|ef\n3x\n4\n5\n6', 'cM', 'i_abc\n|\n4\n5\n6')

    @unittest.mock_ui()
    def test_d(self):
        self.eq('a|bc\n2\n3x\n4\n5\n6', 'dM', '|4\n5\n6')
        self.eq('abc\n2\n3x\n4\nab|c\n6', 'dM', 'abc\n2\n|6')
        self.eq('abc\nd|ef\n3x\n4\n5\n6', 'dM', 'abc\n|4\n5\n6')
