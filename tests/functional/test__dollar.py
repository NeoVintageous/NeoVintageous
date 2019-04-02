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

    def test_V(self):
        self.eq('|abc\n|abc\nabc\n', 'l_$', '|abc\n|abc\nabc\n')
        self.eq('1\n|fizz\n|buzz\nfour\nfive', 'l_2$', '1\n|fizz\nbuzz\n|four\nfive')
        self.eq('1\n|fizz\n|buzz\nfour\nfive', 'l_3$', '1\n|fizz\nbuzz\nfour\n|five')
        self.eq('1\n|fizz\n|buzz\nfour\nfive', 'l_4$', '1\n|fizz\nbuzz\nfour\nfive|')
        self.eq('1\n|fizz\n|buzz\nfour\nfive', 'l_9$', '1\n|fizz\nbuzz\nfour\nfive|')
        self.eq('r_1\n|fizz\nbuzz\n|four\nfive', 'l_2$', 'r_1\nfizz\n|buzz\n|four\nfive')
        self.eq('r_1\n|fizz\nbuzz\n|four\nfive', 'l_3$', '1\nfizz\n|buzz\nfour\n|five')

    def test_N(self):
        self.eq('|abc\nabc\n', '$', 'N_|abc\n|abc\n')
        self.eq('|abc\nabc\nabc\nabc\n', '3$', 'N_|abc\nabc\nabc\n|abc\n')
