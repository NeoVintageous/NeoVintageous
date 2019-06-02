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


class Test_dollar(unittest.FunctionalTestCase):

    def test_n(self):
        self.eq('one |two three', 'n_$', 'one two thre|e')
        self.eq('one |two three\nfour', 'n_2$', 'one two three\nfou|r')
        self.eq('|abc\nabc\n', 'n_$', 'ab|c\nabc\n')
        self.eq('|abc\nabc\nabc\nabc\nabc\nabc\nabc\nabc\nabc\nabc\n', 'n_5$', 'abc\nabc\nabc\nabc\nab|c\nabc\nabc\nabc\nabc\nabc\n')  # noqa: E501
        self.eq('abc\n|\nabc\n', 'n_$', 'abc\n|\nabc\n')
        self.eq('|', 'n_$', '|')
        self.eq('a|b1\ncd2\nef3\ngh4', 'n_1$', 'ab|1\ncd2\nef3\ngh4')
        self.eq('a|b1\ncd2\nef3\ngh4', 'n_2$', 'ab1\ncd|2\nef3\ngh4')
        self.eq('a|b1\ncd2\nef3\ngh4', 'n_3$', 'ab1\ncd2\nef|3\ngh4')
        self.eq('a|b1\ncd2\nef3\ngh4', 'n_4$', 'ab1\ncd2\nef3\ngh|4')
        self.eq('fi|zz    \nbuzz', 'n_$', 'fizz   | \nbuzz')
        self.eq('\n\n|\n\n\n', 'n_$', '\n\n|\n\n\n')
        self.eq('\n\n|\n\n\n', 'n_1$', '\n\n|\n\n\n')
        self.eq('\n\n|\n\n\n', 'n_2$', '\n\n\n|\n\n')
        self.eq('\n\n|\n\n\n', 'n_3$', '\n\n\n\n|\n')

    def test_v(self):
        self.eq('one |two three', 'v_$', 'one |two three|')
        self.eq('one |two three\nfour', 'v_$', 'one |two three\n|four')
        self.eq('one |two three\nfour', 'v_2$', 'one |two three\nfour|')
        self.eq('|abc\nabc\n', 'v_$', '|abc\n|abc\n')
        self.eq('|abc\nabc\nabc\nabc\nabc\nabc\nabc\nabc\nabc\nabc\n', 'v_5$', '|abc\nabc\nabc\nabc\nabc\n|abc\nabc\nabc\nabc\nabc\n')  # noqa: E501
        self.eq('abc\n|\n|abc\n', 'v_$', 'abc\n|\n|abc\n')
        self.eq('r_a|bc\nab|c\n', 'v_$', 'r_abc|\nab|c\n')
        self.eq('ab|c|\nabc\n', 'v_$', 'ab|c\n|abc\n')
        self.eq('r_abc\n|a|bc\n', 'v_2$', 'abc\n|abc\n|')
        self.eq('r_|abc|\nxy', 'v_$', 'ab|c\n|xy')
        self.eq('a|b1\ncd2\nef3\ngh4', 'v_1$', 'a|b1\n|cd2\nef3\ngh4')
        self.eq('a|b1\ncd2\nef3\ngh4', 'v_2$', 'a|b1\ncd2\n|ef3\ngh4')
        self.eq('a|b1\ncd2\nef3\ngh4', 'v_3$', 'a|b1\ncd2\nef3\n|gh4')
        self.eq('a|b1\ncd2\nef3\ngh4', 'v_4$', 'a|b1\ncd2\nef3\ngh4|')
        self.eq('fi|zz    \nbuzz', 'v_$', 'fi|zz    \n|buzz')

    def test_V(self):
        self.eq('|abc\n|abc\nabc\n', 'V_$', '|abc\n|abc\nabc\n')
        self.eq('1\n|fizz\n|buzz\nfour\nfive', 'V_2$', '1\n|fizz\nbuzz\n|four\nfive')
        self.eq('1\n|fizz\n|buzz\nfour\nfive', 'V_3$', '1\n|fizz\nbuzz\nfour\n|five')
        self.eq('1\n|fizz\n|buzz\nfour\nfive', 'V_4$', '1\n|fizz\nbuzz\nfour\nfive|')
        self.eq('1\n|fizz\n|buzz\nfour\nfive', 'V_9$', '1\n|fizz\nbuzz\nfour\nfive|')
        self.eq('r_1\n|fizz\nbuzz\n|four\nfive', 'V_2$', 'r_1\nfizz\n|buzz\n|four\nfive')
        self.eq('r_1\n|fizz\nbuzz\n|four\nfive', 'V_3$', '1\nfizz\n|buzz\nfour\n|five')

    def test_b(self):
        self.eq('x\n|fizz| buzz\n|fizz| buzz\ny', 'b_$', 'x\n|fizz buzz\n||fizz buzz\n|y')

    @unittest.mock_bell()
    def test_c(self):
        self.eq('fi|zz', 'c$', 'i_fi|')
        self.eq('fi|zz\n', 'c$', 'i_fi|\n')
        self.eq('fi|zz\nbuzz', 'c$', 'i_fi|\nbuzz')
        self.eq('fizz\n|\nbuzz', 'c$', 'i_fizz\n|\nbuzz')
        self.eq('\n\n|\n\n', 'c$', 'i_\n\n|\n\n')
        self.eq('|', 'c$', 'i_|')
        self.eq('fi|zz    ', 'c$', 'i_fi|')
        self.eq('fi|zz    \n', 'c$', 'i_fi|\n')
        self.eq('fi|zz    \nbuzz', 'c$', 'i_fi|\nbuzz')
        self.eq('fizz  |  \nbuzz', 'c$', 'i_fizz  |\nbuzz')
        self.assertNoBell()

    @unittest.mock_bell()
    def test_d(self):
        self.eq('one |two three', 'd$', 'one| ')
        self.eq('one t|wo three', 'd$', 'one |t')
        self.eq('|abc\nabc\n', 'd$', '|\nabc\n')
        self.eq('|abc\nabc\nabc\nabc\n', '3d$', '|abc\n')
        self.eq('|fizz\nbuzz\n', 'd$', '|\nbuzz\n')
        self.eq('|ab1\nab2\nab3\nab4\n', '3d$', '|ab4\n')
        self.eq('123|4', 'd$', '12|3')
        self.eq('123|4\nfizz', 'd$', '12|3\nfizz')
        self.eq('|ab1\ncd2\nef3\ngh4', 'd$', '|\ncd2\nef3\ngh4')
        self.eq('a|b1\ncd2\nef3\ngh4', 'd$', '|a\ncd2\nef3\ngh4')
        self.eq('fi|zz\nfuzz\nabc\ndef', '2d$', 'f|i\nabc\ndef')
        self.eq('fi|zz\nfuzz\nabc\ndef', '2d$', 'f|i\nabc\ndef')
        self.eq('fi|zz\nfuzz\nabc\ndef', '3d$', 'f|i\ndef')
        self.eq('first1\nst|art2\nxxx\nfour\nfive', '2d$', 'first1\ns|t\nfour\nfive')
        self.eq('first1\n|start2\n\n\nfive', '2d$', 'first1\n|\nfive')
        self.eq('fi|zz    \nbuzz', 'd$', 'f|i\nbuzz')
        self.assertNoBell()
        self.eq('\n\n|\n\n', 'd$', '\n\n|\n\n')
        self.eq('fizz\n|\n\n\n\nbuzz', 'd$', 'fizz\n|\n\n\n\nbuzz')
        self.eq('fizz\n|\n\n\n\nbuzz', '1d$', 'fizz\n|\n\n\n\nbuzz')
        self.eq('fizz\n|\n\n\n\nbuzz', '2d$', 'fizz\n|\n\nbuzz')
        self.eq('fizz\n|\n\n\n\nbuzz', '3d$', 'fizz\n|\nbuzz')
