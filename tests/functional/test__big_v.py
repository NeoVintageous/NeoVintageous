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


class Test_V(unittest.FunctionalTestCase):

    def test_V(self):
        self.eq('fi|zz', 'V', 'l_|fizz|')
        self.eq('x\nfi|zz\nx', 'V', 'l_x\n|fizz\n|x')
        self.eq('x\nbar|\n', 'V', 'l_x\n|bar\n|')

    def test_V_special_case_when_cursor_at_eof(self):
        self.eq('x\nbar\n|', 'V', 'l_x\n|bar\n|')
        self.eq('x\nbar|\n', 'V', 'l_x\n|bar\n|')
        self.eq('|', 'V', '|')
        self.eq('|\n', 'V', 'l_|\n|')
        self.eq('|\n\n', 'V', 'l_|\n|\n')
        self.eq('|    ', 'V', 'l_|    |')
        self.eq('|    \n', 'V', 'l_|    \n|')

    def test_n_V_special_case_when_cursor_at_eof(self):
        self.eq('x\nbar\n|', 'n_V', 'l_x\n|bar\n|')
        self.eq('x\nbar|\n', 'n_V', 'l_x\n|bar\n|')
        self.eq('|', 'n_V', '|')
        self.eq('|\n', 'n_V', 'l_|\n|')
        self.eq('|\n\n', 'n_V', 'l_|\n|\n')
        self.eq('|    ', 'n_V', 'l_|    |')
        self.eq('|    \n', 'n_V', 'l_|    \n|')

    def test_visual_line_enters_normal(self):
        self.eq('x\n|fizz\n|x', 'l_V', 'n_x\nfiz|z\nx')

    def test_v(self):
        self.eq('x\nfi|zz bu|zz\nx', 'v_V', 'l_x\n|fizz buzz\n|x')
        self.eq('x\nfi|zz buzz\n|x', 'v_V', 'l_x\n|fizz buzz\n|x')
        self.eqr('r_x\nfi|zz bu|zz\nx', 'v_V', 'l_x\n|fizz buzz\n|x')
        self.eqr('r_x\nfi|zz buzz\n|x', 'v_V', 'l_x\n|fizz buzz\n|x')
        self.eq('x\nfi|zz\nbu|zz\nx', 'v_V', 'l_x\n|fizz\nbuzz\n|x')
        self.eqr('r_x\nfi|zz\nbu|zz\nx', 'v_V', 'l_x\n|fizz\nbuzz\n|x')

    @unittest.mock_bell()
    def test_V_bell_on_empty_content(self):
        self.eq('|', 'V', '|')
        self.assertBell()

    @unittest.mock_bell()
    def test_n_V_bell_on_empty_content(self):
        self.eq('|', 'n_V', '|')
        self.assertBell()
