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


class Test_v(unittest.FunctionalTestCase):

    def test_v(self):
        self.eq('fi|zz', 'v', 'v_fi|z|z')

    def test_visual_enters_normal(self):
        self.eq('f|izz bu|zz', 'v_v', 'n_fizz b|uzz')
        self.eq('r_f|izz bu|zz', 'v_v', 'n_f|izz buzz')

    def test_visual_line_enters_visual(self):
        self.eq('x\n|fizz\n|x', 'l_v', 'v_x\n|fizz\n|x')
        self.eqr('r_x\n|fizz\n|x', 'l_v', 'v_x\n|fizz\n|x')
