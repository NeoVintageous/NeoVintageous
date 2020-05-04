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


class Test_r(unittest.ResetRegisters, unittest.FunctionalTestCase):

    def test_n(self):
        self.eq('|a', 'rx', '|x')
        self.eq('a|bc', 'rx', 'a|xc')
        self.eq('ab\n|cd', 'rx', 'ab\n|xd')
        self.eq('f|izz', 'r<cr>', 'f\n|zz')
        self.eq('a|xb', 'r<k3>', 'a|3b')
        self.eq('a|xb', 'r<kenter>', 'a\n|b')
        self.eq('a|xb', 'r<kplus>', 'a|+b')

    def test_v(self):
        self.eq('ab|12345|cd', 'v_rx', 'n_ab|xxxxxcd')
        self.eq('r_ab|12345|cd', 'v_rx', 'n_ab|xxxxxcd')
        self.eq('ab|12345\n|cd', 'v_rx', 'n_ab|xxxxx\ncd')
        self.eq('r_ab|12345\n|cd', 'v_rx', 'n_ab|xxxxx\ncd')
        self.eq('ab|12\n34\n5\n|cd', 'v_rx', 'n_ab|xx\nxx\nx\ncd')
        self.eq('r_ab|12\n34\n5\n|cd', 'v_rx', 'n_ab|xx\nxx\nx\ncd')
        self.eq('fi|zz bu|zz', 'v_r<cr>', 'n_fi\n|\n\n\n\nzz')
