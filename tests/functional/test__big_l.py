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


class Test_L(unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()
        self.set_option('scrolloff', 0)

    @unittest.mock_ui()
    def test_n(self):
        self.eq('|1\n2\n3', 'n_L', '1\n2\n|3')
        self.eq('|1\n2\n3', 'n_L', '1\n2\n|3')
        self.eq('1\n|2\n3', 'n_L', '1\n2\n|3')
        self.eq('1\n2\n|3', 'n_L', '1\n2\n|3')
        self.eq('|1\n2\n    3', 'n_L', '1\n2\n    |3')

    @unittest.mock_ui()
    def test_n_with_scrolloff(self):
        self.set_option('scrolloff', 2)
        self.eq('1\n2\n3\n4\n|5\n6\n7\n8\n', 'n_L', '1\n2\n3\n4\n5\n|6\n7\n8\n')

    @unittest.mock_ui(visible_region=(0, 5))
    def test_n_L_should_be_within_visible_region(self):
        self.eq('|1\n2\n3\n4', 'n_L', '1\n2\n|3\n4')
        self.eq('1\n|2\n3\n4', 'n_L', '1\n2\n|3\n4')
        self.eq('1\n2\n|3\n4', 'n_L', '1\n2\n|3\n4')
        self.eq('|1\n2\n    3\n4', 'n_L', '1\n2\n    |3\n4')

    @unittest.mock_ui(visible_region=(0, 3))
    def test_n_L_should_be_within_visible_region2(self):
        self.eq('|1\n2\n3\n4', 'n_L', '1\n|2\n3\n4')
        self.eq('1\n|2\n3\n4', 'n_L', '1\n|2\n3\n4')

    @unittest.mock_ui()
    def test_d(self):
        self.eq('1\n2\n|3', 'dL', '1\n2\n|')
        self.eq('1\n2\n|3x', 'dL', '1\n2\n|')
        self.eq('|1\n2\n3', 'dL', '|')
        self.eq('|1\n2\n3x', 'dL', '|')
        self.eq('x|1\n2\n3x', 'dL', '|')
        self.eq('x|1\n2\nx3', 'dL', '|')
        self.eq('1\n|2\n3', 'dL', '1\n|')
        self.eq('1\n|2\n3\n', 'dL', '1\n|')
        self.eq('1\n|2\n    3', 'dL', '1\n|')
        self.eq('1\n|2\n    3\n', 'dL', '1\n|')
        self.eq('    x|1\n2\n    x3', 'dL', '|')
        self.eq('fizz\nbu|zz\nfizz\n', 'dL', 'fizz\n|')

    @unittest.mock_ui()
    def test_v(self):
        self.eq('|1\n2\n3', 'v_L', '|1\n2\n3|')
        self.eq('|1\n2\n3x', 'v_L', '|1\n2\n3|x')
        self.eq('|1\n2\n    3x', 'v_L', '|1\n2\n    3|x')
        self.eq('1\na|bc\n3x', 'v_L', '1\na|bc\n3|x')
        self.eq('a|bc\nxyz', 'v_L', 'a|bc\nx|yz')
        self.eq('r_a|b|c\nxyz', 'v_L', 'a|bc\nx|yz')
        self.eq('r_a|b|c\n2\n3\nxyz', 'v_L', 'a|bc\n2\n3\nx|yz')
        self.eq('r_a|bc\nab|c\n3\nxyz', 'v_L', 'abc\na|bc\n3\nx|yz')
        self.eq('a|bc\nab|c\n3\nxyz', 'v_L', 'a|bc\nabc\n3\nx|yz')
        self.eq('1\n|2\n|3', 'v_L', '1\n|2\n3|')
        self.eq('r_1\n|2\n|3', 'v_L', '1\n2|\n3|')
        self.eq('r_1\n2\n    |f|izz', 'v_L', 'r_1\n2\n    |f|izz')
        self.eq('r_1\n2\n  |  f|izz', 'v_L', 'r_1\n2\n    |f|izz')
        self.eq('1\n2\n  |  f|izz', 'v_L', '1\n2\n  |  f|izz')

    @unittest.mock_ui()
    def test_V(self):
        self.eq('1x\n2x\n3x\n4x\n|5x|', 'V_L', 'r_1x\n2x\n3x\n4x\n|5x|')
        self.eq('1x\n2x\n3x\n4x\n|5x\n|', 'V_L', 'r_1x\n2x\n3x\n4x\n|5x\n|')
        self.eq('1x\n2x\n3x\n|4x\n5x|', 'V_L', '1x\n2x\n3x\n|4x\n5x|')
        self.eq('1x\n2x\n3x\n|4x\n|5x', 'V_L', '1x\n2x\n3x\n|4x\n5x|')
        self.eq('1x\n2x\n|3x\n4x\n5x', 'V_L', '1x\n2x\n|3x\n4x\n5x|')
        self.eq('1x\n2x\n|3x\n4x\n|5x', 'V_L', '1x\n2x\n|3x\n4x\n5x|')
        self.eq('1x\n|2x\n3x\n4x\n5x', 'V_L', '1x\n|2x\n3x\n4x\n5x|')
        self.eq('1x\n|2x\n3x\n4x\n|5x', 'V_L', '1x\n|2x\n3x\n4x\n5x|')
        self.eq('1x\n|2x\n3x\n|4x\n5x', 'V_L', '1x\n|2x\n3x\n4x\n5x|')
        self.eq('|1x\n2x\n3x\n|4x\n5x', 'V_L', '|1x\n2x\n3x\n4x\n5x|')
        self.eq('|1x\n2x\n|3x\n4x\n5x', 'V_L', '|1x\n2x\n3x\n4x\n5x|')
        self.eq('|1x\n2x\n|3x\n4x\n5x\n', 'V_L', '|1x\n2x\n3x\n4x\n5x\n|')
        self.eq('|1\n2x\n3x|', 'V_L', '|1\n2x\n3x|')
        self.eq('|1\n2x\n|3x', 'V_L', '|1\n2x\n3x|')
        self.eq('r_1x\n2x\n|3x\n4x\n|5x', 'V_L', '1x\n2x\n3x\n|4x\n5x|')
        self.eq('r_1x\n2x\n|3x\n|4x\n5x', 'V_L', '1x\n2x\n|3x\n4x\n5x|')
        self.eq('r_1x\n|2x\n3x\n|4x\n5x', 'V_L', '1x\n2x\n|3x\n4x\n5x|')
        self.eq('r_|1x\n2x\n3x\n|4x\n5x', 'V_L', '1x\n2x\n|3x\n4x\n5x|')
        self.eq('r_|1\n2x\n3x|', 'V_L', 'r_1\n2x\n|3x|')
        self.eq('r_|1\n2x\n3x\n|', 'V_L', 'r_1\n2x\n|3x\n|')
        self.eq('r_|1\n2x\n3x|\n', 'V_L', 'r_1\n2x\n|3x|\n')
