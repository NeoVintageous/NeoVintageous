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


class Test_e(unittest.FunctionalTestCase):

    def test_n(self):
        self.eq('one |two three', 'n_e', 'one tw|o three')
        self.eq('one |two three', 'n_2e', 'one two thre|e')
        self.eq('f|izz', 'n_e', 'fiz|z')
        self.eq('f|izz\n', 'n_e', 'fiz|z\n')

    def test_v(self):
        self.visual('o|ne two three four five six\n')
        self.feed('v_e')
        self.assertVisual('o|ne| two three four five six\n')
        self.feed('v_3e')
        self.assertVisual('o|ne two three four| five six\n')
        self.feed('v_2e')
        self.assertVisual('o|ne two three four five six|\n')
        self.eq('r_on|e t|wo x', 'v_2e', 'one |two| x')
        self.eq('r_o|ne t|wo x', 'v_2e', 'one |two| x')
        self.eq('r_o|ne tw|o', 'v_e', 'r_on|e tw|o')
        self.eq('r_o|ne two three fo|ur', 'v_3e', 'r_one two thre|e fo|ur')
        self.eq('r_o|ne tw|o three four', 'v_3e', 'one t|wo three| four')
        self.eq('f|izz', 'v_e', 'f|izz|')
        self.eq('f|izz\n', 'v_e', 'f|izz|\n')

    def test_d(self):
        self.eq('one |two three', 'de', 'one | three')
        self.eq('one t|wo three', 'de', 'one t| three')
        self.eq('one\n|\ntwo\nthree', 'de', 'one\n|three')
        self.eq('one\n|\n\ntwo\nthree', 'de', 'one\n|three')
        self.eq('one\n|\n\n\ntwo\nthree', 'de', 'one\n|three')
        self.eq('one\n|\n\n\n    two\nthree', 'de', 'one\n|three')
        self.eq('one |two three', '2de', 'N_one| ')
