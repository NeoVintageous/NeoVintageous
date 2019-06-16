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
        self.eq('on|e\ntwo three', 'n_e', 'one\ntw|o three')
        self.eq('on|e  \ntwo three', 'n_e', 'one  \ntw|o three')
        self.eq('on|e\n\n\n\ntwo three', 'n_e', 'one\n\n\n\ntw|o three')
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
        self.eq('r_on|e t|wo x', 'v_e', 'one |two| x')
        self.eq('r_on|e t|wo three x', 'v_2e', 'one |two three| x')
        self.eq('r_o|ne t|wo x', 'v_2e', 'one |two| x')
        self.eq('r_o|ne tw|o', 'v_e', 'r_on|e tw|o')
        self.eq('r_o|ne two three fo|ur', 'v_3e', 'r_one two thre|e fo|ur')
        self.eq('r_o|ne tw|o three four', 'v_3e', 'one t|wo three| four')
        self.eq('f|izz', 'v_e', 'f|izz|')
        self.eq('f|izz\n', 'v_e', 'f|izz|\n')
        self.eq('r_fiz|z buzz fizz|', 'v_e', 'r_fizz buz|z fizz|')
        self.eq('|fizz x', 'v_e', '|fizz| x')
        self.eq('r_|fizz x|', 'v_e', 'r_fiz|z x|')

    def test_b(self):
        self.eq('|fizz|buzz x\n|fizz|buzz x\n', 'b_e', '|fizzbuzz| x\n|fizzbuzz| x\n')

    def test_d(self):
        self.eq('one |two three', 'de', 'one | three')
        self.eq('one t|wo three', 'de', 'one t| three')
        self.eq('one\n|\ntwo\nthree', 'de', 'one\n|three')
        self.eq('one\n|\n\ntwo\nthree', 'de', 'one\n|three')
        self.eq('one\n|\n\n\ntwo\nthree', 'de', 'one\n|three')
        self.eq('one\n|\n\n\n    two\nthree', 'de', 'one\n|three')
        self.eq('one |two three', '2de', 'one| ')
        self.eq('one |two three', 'de', 'one | three')
        self.eq('f|izz buzz', 'de', 'f| buzz')
        self.eq('f|izz        buzz', 'de', 'f|        buzz')
        self.eq('fi|zz    buzz', 'de', 'fi|    buzz')
        self.eq('one tw|o\n\n\none two', 'de', 'one tw| two')
        self.eq('x\n\n|\n\none\ntwo', 'de', 'x\n\n|two')
        self.eq('x\n\n    o|ne two\nthree four\n', '3de', 'x\n\n    o| four\n')
        self.eq('    o|ne\n\n\ntwo three\nx', '2de', '    o| three\nx')
        self.eq('    |one\n\n\ntwo three\nx', '2de', '    | three\nx')
        self.eq('  |  one\n\n\ntwo three\nx', '2de', '  | three\nx')
        self.eq('|    one\n\n\ntwo three\nx', '2de', '| three\nx')
        self.eq('    o|ne\n\n\ntwo\nthree\nx', '2de', '    |o\nthree\nx')
