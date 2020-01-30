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


class Test_ctrl_v(unittest.FunctionalTestCase):

    def test_n(self):
        self.eq('fi|zz', '<C-v>', 'b_fi|z|z')
        self.assertStatusLineIsVisualBlock()

    def test_v(self):
        self.eq('f|iz|z', 'v_<C-v>', 'b_f|iz|z')
        self.eq('f|izz\nbuz|z', 'v_<C-v>', 'b_f|iz|z\nb|uz|z')
        self.eq('|fizz\nb|\n\n\n', 'v_<C-v>', 'b_|f|izz\n|b|\n\n\n')
        self.eq('|fizz\n\n|\n\n', 'v_<C-v>', 'b_|f|izz\n|\n|\n\n')
        self.eq('|fizz\n\n\n|\n', 'v_<C-v>', 'b_|f|izz\n|\n||\n|\n')
        self.eq('f|izz\n\nbuz|z\n', 'v_<C-v>', 'b_f|iz|z\n\nb|uz|z\n')
        self.eq('r_f|izz\nbuz|z', 'v_<C-v>', 'r_b_u_f|iz|z\nb|uz|z')
        self.assertStatusLineIsVisualBlock()

    def test_V(self):
        self.eq('|xxx\nfizz\nbuzz\n|xxx', 'V_<C-v>', 'b_|xxx\n||fizz\n||buzz\n|xxx')
        self.eq('xxx\n|fizz\n|buzz\nxxx', 'V_<C-v>', 'b_xxx\n|fizz\n|buzz\nxxx')
        self.eq('xxx\n|fizz\nbuzz\n|xxx', 'V_<C-v>', 'b_xxx\n|fizz\n||buzz\n|xxx')
        self.assertStatusLineIsVisualBlock()

    def test_b(self):
        self.eq('fi|zz bu|zz', 'b_<C-v>', 'n_fizz b|uzz')
        self.assertStatusLineIsBlank()
