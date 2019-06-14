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


class Test_left_paren(unittest.FunctionalTestCase):

    def test_n(self):
        self.eq('|', 'n_(', '|')
        self.eq('fi|zz', 'n_(', '|fizz')
        self.eq('one. tw|o', 'n_(', 'one. |two')
        self.eq('one? tw|o', 'n_(', 'one? |two')
        self.eq('one! tw|o', 'n_(', 'one! |two')
        self.eq('one.  tw|o', 'n_(', 'one.  |two')
        self.eq('one.   tw|o', 'n_(', 'one.   |two')

    def test_n_section_boundary(self):
        self.normal('one.\ntwo.\n\nthree.\n\n\nfour.\n\n\n\nfi|ve.')
        self.feed('n_(')
        self.assertNormal('one.\ntwo.\n\nthree.\n\n\nfour.\n\n\n\n|five.')
        self.feed('n_(')
        self.assertNormal('one.\ntwo.\n\nthree.\n\n\nfour.\n\n\n|\nfive.')
        self.feed('n_(')
        self.assertNormal('one.\ntwo.\n\nthree.\n\n\n|four.\n\n\n\nfive.')
        self.feed('n_(')
        self.assertNormal('one.\ntwo.\n\nthree.\n\n|\nfour.\n\n\n\nfive.')
        self.feed('n_(')
        self.assertNormal('one.\ntwo.\n\n|three.\n\n\nfour.\n\n\n\nfive.')
        self.feed('n_(')
        self.assertNormal('one.\ntwo.\n|\nthree.\n\n\nfour.\n\n\n\nfive.')

    def test_v(self):
        self.eq('one. two. th|ree.', 'v_(', 'r_one. two. |thr|ee.')
        self.eq('one. two. |three.', 'v_(', 'r_one. |two. t|hree.')
        self.eq('x. fiz|zbu|zz', 'v_(', 'r_x. |fizz|buzz')
        self.eq('r_x. fiz|zbu|zz', 'v_(', 'r_x. |fizzbu|zz')

    def test_V(self):
        self.eq('fizz\nx. y. z.\n|buzz\n|3', 'V_(', 'r_fizz\n|x. y. z.\nbuzz\n|3')
        self.eq('r_1. 2. 3.\n|a. b. c.\nfizz\n|4', 'V_(', 'r_|1. 2. 3.\na. b. c.\nfizz\n|4')

    def test_d(self):
        self.eq('one. fizz bu|zz', 'd(', 'one. |zz')
