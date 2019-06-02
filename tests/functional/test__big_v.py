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

    def test_n_V(self):
        self.eq('a|bc', 'n_V', 'V_|abc|')
        self.eq('a|bc\n', 'n_V', 'V_|abc\n|')
        self.eq('x\na|bc\nx', 'n_V', 'V_x\n|abc\n|x')
        self.eq('\n|\n\n', 'n_V', 'V_\n|\n|\n')
        self.eq('x\ny|\n', 'n_V', 'V_x\n|y\n|')
        self.eq('x\ny|', 'n_V', 'V_x\n|y|')
        self.eq('x\ny|\n', 'n_V', 'V_x\n|y\n|')
        self.eq('x\ny\n|', 'n_V', 'V_x\n|y\n|')
        self.eq('x\nbar\n|', 'n_V', 'V_x\n|bar\n|')
        self.eq('x\nbar|\n', 'n_V', 'V_x\n|bar\n|')
        self.eq('|', 'n_V', '|')
        self.eq('|\n', 'n_V', 'V_|\n|')
        self.eq('|\n\n', 'n_V', 'V_|\n|\n')
        self.eq('|    ', 'n_V', 'V_|    |')
        self.eq('|    \n', 'n_V', 'V_|    \n|')
        self.assertStatusLineIsVisualLine()

    @unittest.mock_bell()
    def test_n_V_bell_on_empty_content(self):
        self.eq('|', 'n_V', '|')
        self.assertBell()

    def test_v_V(self):
        self.eq('x\nfi|zz bu|zz\nx', 'v_V', 'V_x\n|fizz buzz\n|x')
        self.eq('x\nfi|zz buzz\n|x', 'v_V', 'V_x\n|fizz buzz\n|x')
        self.eq('r_x\nfi|zz bu|zz\nx', 'v_V', 'r_V_x\n|fizz buzz\n|x')
        self.eq('r_x\nfi|zz buzz\n|x', 'v_V', 'r_V_x\n|fizz buzz\n|x')
        self.eq('x\nfi|zz\nbu|zz\nx', 'v_V', 'V_x\n|fizz\nbuzz\n|x')
        self.eq('r_x\nfi|zz\nbu|zz\nx', 'v_V', 'r_V_x\n|fizz\nbuzz\n|x')
        self.eq('f|iz|z', 'v_V', 'V_|fizz|')
        self.eq('x\nf|iz|z\nx', 'v_V', 'V_x\n|fizz\n|x')
        self.eq('r_x\nf|iz|z\nx', 'v_V', 'r_V_x\n|fizz\n|x')
        self.eq('x\nfi|zz\n\nx\nbuz|z\nx\ny', 'v_V', 'V_x\n|fizz\n\nx\nbuzz\n|x\ny')
        self.eq('r_x\nfi|zz\n\nx\nb|uzz\nx\ny', 'v_V', 'r_V_x\n|fizz\n\nx\nbuzz\n|x\ny')
        self.eq('x\n|abc\n|x', 'v_V', 'V_x\n|abc\n|x')
        self.eq('x\na|bc\n|x', 'v_V', 'V_x\n|abc\n|x')
        self.eq('r_x\n|abc\n|x', 'v_V', 'r_V_x\n|abc\n|x')
        self.eq('r_x\na|bc\n|x', 'v_V', 'r_V_x\n|abc\n|x')
        self.assertStatusLineIsVisualLine()

    def test_V(self):
        self.eq('x\n|fizz\n|x', 'V_V', 'n_x\nfiz|z\nx')
        self.eq('x\n|abc\n|x', 'V_V', 'n_x\nab|c\nx')
        self.eq('r_x\n|abc\n|x', 'V_V', 'n_x\n|abc\nx')
        self.assertStatusLineIsNormal()

    def test_b(self):
        self.eq('f|iz|z', 'b_V', 'V_|fizz|')
        self.eq('f|iz|z\n', 'b_V', 'V_|fizz\n|')
        self.eq('x\nf|iz|z\ny\n', 'b_V', 'V_x\n|fizz\n|y\n')
        self.eq('x\nf|iz|z\nb|uz|z\ny\n', 'b_V', 'V_x\n|fizz\nbuzz\n|y\n')
        self.eq('u_x\nf|iz|z\nb|uz|z\ny\n', 'b_V', 'V_x\n|fizz\nbuzz\n|y\n')
        self.eq('r_u_x\nf|iz|z\nb|uz|z\ny\n', 'b_V', 'V_x\n|fizz\nbuzz\n|y\n')
        self.eq('r_x\nf|iz|z\nb|uz|z\ny\n', 'b_V', 'V_x\n|fizz\nbuzz\n|y\n')
        self.assertStatusLineIsVisualLine()

    def test_N_V(self):
        self.eq('fi|zz', 'V', 'V_|fizz|')
        self.eq('x\nfi|zz\nx', 'V', 'V_x\n|fizz\n|x')
        self.eq('x\nbar|\n', 'V', 'V_x\n|bar\n|')
        self.eq('x\nbar\n|', 'V', 'V_x\n|bar\n|')
        self.eq('x\nbar|\n', 'V', 'V_x\n|bar\n|')
        self.eq('|', 'V', '|')
        self.eq('|\n', 'V', 'V_|\n|')
        self.eq('|\n\n', 'V', 'V_|\n|\n')
        self.eq('|    ', 'V', 'V_|    |')
        self.eq('|    \n', 'V', 'V_|    \n|')
        self.assertStatusLineIsVisualLine()

    @unittest.mock_bell()
    def test_V_N_bell_on_empty_content(self):
        self.eq('|', 'V', '|')
        self.assertBell()
