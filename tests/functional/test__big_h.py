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


class Test_H(unittest.FunctionalTestCase):

    @unittest.mock_ui()
    def test_H(self):
        self.eq('1\n2\n|3', 'n_H', '|1\n2\n3')
        self.eq('1\n|2\n3', 'n_H', '|1\n2\n3')
        self.eq('|1\n2\n3', 'n_H', '|1\n2\n3')
        self.eq('    1\n2\n|3', 'n_H', '    |1\n2\n3')

    @unittest.mock_ui(visible_region=(2, 7))
    def test_H_should_be_within_visible_region(self):
        self.eq('1\n2\n3\n|4', 'n_H', '1\n|2\n3\n4')
        self.eq('1\n2\n|3\n4', 'n_H', '1\n|2\n3\n4')
        self.eq('1\n|2\n3\n4', 'n_H', '1\n|2\n3\n4')
        self.eq('1\n    2\n3\n|4', 'n_H', '1\n    |2\n3\n4')

    @unittest.mock_ui(visible_region=(4, 7))
    def test_H_should_be_within_visible_region2(self):
        self.eq('1\n2\n3\n|4', 'n_H', '1\n2\n|3\n4')
        self.eq('1\n2\n|3\n4', 'n_H', '1\n2\n|3\n4')

    @unittest.mock_ui()
    def test_N_H(self):
        self.eq('1\n2\n|3', 'H', 'r_N_|1\n2\n|3')
        self.eq('1\n2\n|3xx', 'H', 'r_N_|1\n2\n|3xx')
        self.eq('|1\n2', 'H', 'N_|1\n2')

    @unittest.mock_ui()
    def test_v_H(self):
        self.eq('1\n2\n|3', 'v_H', 'r_|1\n2\n3|')
        self.eq('1\n2\n|3xx', 'v_H', 'r_|1\n2\n3|xx')
        self.eq('1\n2\n|3\n4', 'v_H', 'r_|1\n2\n3|\n4')
        self.eq('1\n2\n|3\n4\n5\n6|', 'v_H', 'r_|1\n2\n3|\n4\n5\n6')
        self.eq('r_1\n2\n|3\n4|56', 'v_H', 'r_|1\n2\n3\n4|56')
        self.eq('r_1\n2\na|b|c', 'v_H', 'r_|1\n2\nab|c')
        self.eq('1\n2\na|b|c', 'v_H', 'r_|1\n2\nab|c')
        self.eq('    1\n2\na|bc', 'v_H', 'r_    |1\n2\nab|c')
        self.eq('r_    |fiz|z\n2\n3', 'v_H', 'r_    |fiz|z\n2\n3')
        self.eq('    |1|\n2\n3', 'v_H', '    |1|\n2\n3')
        self.eq('    |f|izz\n2\n3', 'v_H', '    |f|izz\n2\n3')
        self.eq('    |fiz|z\n2\n3', 'v_H', '    |f|izz\n2\n3')

    @unittest.mock_ui(visible_region=(4, 11))
    def test_v_H_when_selection_is_partially_offscreen(self):
        self.eq('|1\n2\n    fizz\n4\n5\n6|', 'v_H', '|1\n2\n    f|izz\n4\n5\n6')

    @unittest.mock_ui(visible_region=(7, 11))
    def test_v_H_when_selection_is_offscreen(self):
        self.eq('r_|1\nfi|zz\n    buzz\n4\n5\n6', 'v_H', '1\nf|izz\n    b|uzz\n4\n5\n6')
        self.eq('|1\nfi|zz\n    buzz\n4\n5\n6', 'v_H', '|1\nfizz\n    b|uzz\n4\n5\n6')

    @unittest.mock_ui(visible_region=(4, 7))
    def test_v_H_should_be_within_visible_region2(self):
        self.eq('1\n2\n3\n456\n|xyz', 'v_H', 'r_1\n2\n|3\n456\nx|yz')
        self.eq('1\n2\n    3\n456\n|xyz', 'v_H', 'r_1\n2\n    |3\n456\nx|yz')

    @unittest.mock_ui()
    def test_l_H(self):
        self.eq('1\n|2\n|x', 'l_H', 'r_|1\n2\n|x')
        self.eq('1\n|2\n3\n|x', 'l_H', 'r_|1\n2\n|3\nx')
        self.eq('1\n|2\n3\n4\n|x', 'l_H', 'r_|1\n2\n|3\n4\nx')
        self.eq('r_1\n2\n|3\n|x', 'l_H', 'r_|1\n2\n3\n|x')
        self.eq('r_    1\n|2\n3\n|x', 'l_H', 'r_|    1\n2\n3\n|x')
        self.eq('r_|1\n2\n3\n|x', 'l_H', 'r_|1\n2\n3\n|x')
        self.eq('|1xx\n2\n3\n|4\nx', 'l_H', 'r_|1xx\n|2\n3\n4\nx')

    @unittest.mock_ui(visible_region=(2, 17))
    def test_l_H_visible_regions(self):
        self.eq('x\n|1xx\n2\n3\n|4\nx', 'l_H', 'r_x\n|1xx\n|2\n3\n4\nx')
        self.eq('x\n|    1xx\n2\n3\n|4\nx', 'l_H', 'x\n|    1xx\n|2\n3\n4\nx')
