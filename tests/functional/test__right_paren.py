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


class Test_right_paren(unittest.FunctionalTestCase):

    def test_n(self):
        self.eq('|', 'n_)', '|')
        self.eq('fi|zz', 'n_)', 'fi|zz')
        self.eq('|a b c. xy', 'n_)', 'a b c. |xy')
        self.eq('|a b c? xy', 'n_)', 'a b c? |xy')
        self.eq('|a b c! xy', 'n_)', 'a b c! |xy')
        self.eq('|a b c! x y. a b. xy.', 'n_3)', 'a b c! x y. a b. |xy.')
        self.eq('|fizz? buzz', 'n_)', 'fizz? |buzz')
        self.eq('|fizz! buzz', 'n_)', 'fizz! |buzz')
        self.eq('|fizz. buzz', 'n_)', 'fizz. |buzz')
        self.eq('|fizz.  buzz', 'n_)', 'fizz.  |buzz')
        self.eq('|fizz.   buzz', 'n_)', 'fizz.   |buzz')
        self.eq('|fizz." buzz', 'n_)', 'fizz." |buzz')
        self.eq('|fizz.) buzz', 'n_)', 'fizz.) |buzz')
        self.eq('|fizz.] buzz', 'n_)', 'fizz.] |buzz')
        self.eq("|fizz.' buzz", 'n_)', "fizz.' |buzz")

    def test_n_section_boundary(self):
        self.normal('|one.\ntwo.\n\nthree.\n\n\nfour.\n\n\n\nfive.')
        self.feed('n_)')
        self.assertNormal('one.\n|two.\n\nthree.\n\n\nfour.\n\n\n\nfive.')
        self.feed('n_)')
        self.assertNormal('one.\ntwo.\n|\nthree.\n\n\nfour.\n\n\n\nfive.')
        self.feed('n_)')
        self.assertNormal('one.\ntwo.\n\n|three.\n\n\nfour.\n\n\n\nfive.')
        self.feed('n_)')
        self.assertNormal('one.\ntwo.\n\nthree.\n|\n\nfour.\n\n\n\nfive.')
        self.feed('n_)')
        self.assertNormal('one.\ntwo.\n\nthree.\n\n\n|four.\n\n\n\nfive.')
        self.feed('n_)')
        self.assertNormal('one.\ntwo.\n\nthree.\n\n\nfour.\n|\n\n\nfive.')
        self.feed('n_)')
        self.assertNormal('one.\ntwo.\n\nthree.\n\n\nfour.\n\n\n\n|five.')

    def test_v(self):
        self.eq('|a b c. xyz', 'v_)', '|a b c. x|yz')
        self.eq('|a b c? xyz', 'v_)', '|a b c? x|yz')
        self.eq('|a b c! xyz', 'v_)', '|a b c! x|yz')

    def test_V(self):
        self.eq('1\n|fizz. buzz.\n|fizz. buzz.\n4', 'V_)', '1\n|fizz. buzz.\nfizz. buzz.\n|4')

    def test_d(self):
        self.eq('|a b c. xy', 'd)', '|xy')
        self.eq('|a b c? xy', 'd)', '|xy')
        self.eq('|a b c! xy', 'd)', '|xy')
        self.eq('one. fi|zz buzz. xy', 'd)', 'one. fi|xy')
