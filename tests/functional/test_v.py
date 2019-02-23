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

    @unittest.mock_bell()
    def test_n_v(self):
        self.eq('fi|zz', 'n_v', 'v_fi|z|z')
        self.eq('\n|\n', 'n_v', 'v_\n|\n|')
        self.eq('\n|\n\n', 'n_v', 'v_\n|\n|\n')
        self.assertStatusLineIsVisual()
        self.assertNoBell()

    @unittest.mock_bell()
    def test_n_v_empty_invokes_bell(self):
        self.eq('|', 'n_v', 'n_|')
        self.assertBell()

    def test_v(self):
        self.eq('f|izz bu|zz', 'v_v', 'n_fizz b|uzz')
        self.eq('r_f|izz bu|zz', 'v_v', 'n_f|izz buzz')

    def test_visual_line_enters_visual(self):
        self.eq('x\n|fizz\n|x', 'l_v', 'v_x\n|fizz\n|x')
        self.eq('r_x\n|fizz\n|x', 'l_v', 'r_v_x\n|fizz\n|x')
        self.assertStatusLineIsVisual()
