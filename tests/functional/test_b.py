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


class Test_b(unittest.FunctionalTestCase):

    def test_b(self):
        self.eqr('ab|c', 'b', '|abc')
        self.eqr('abc\n|', 'b', '|abc\n')
        self.eqr('one two thr|ee', 'b', 'one two |three')
        self.eqr('one two |three', 'b', 'one |two three')
        self.eqr('one two three fo|ur', '3b', 'one |two three four')

    def test_n_b(self):
        self.eq('ab|c', 'n_b', '|abc')
        self.eq('abc\n|', 'n_b', '|abc\n')
        self.eq('one two thr|ee', 'n_b', 'one two |three')
        self.eq('one two |three', 'n_b', 'one |two three')
        self.eq('one two three fo|ur', 'n_3b', 'one |two three four')

    def test_v_b(self):
        self.visual('one two three four f|ive six seven ei|ght')
        self.feed('v_b')
        self.assertVisual('one two three four f|ive six seven e|ight')
        self.feed('v_2b')
        self.assertVisual('one two three four f|ive s|ix seven eight')
        self.feed('v_b')
        self.assertVisual('one two three four |fi|ve six seven eight')
        self.feed('v_3b')
        self.assertRVisual('one |two three four fi|ve six seven eight')
        self.feed('v_b')
        self.assertRVisual('|one two three four fi|ve six seven eight')

    def test_vline_b(self):
        self.eq('x\n|one\n|y\n', 'l_b')
        self.eq('x\n|one\ntwo\n|y\n', 'l_b')

    def test_vblock_b(self):
        self.eqr('one t|w|o\none t|w|o', 'b_b', 'one |tw|o\none |tw|o')
        self.eqr('one two t|hr|ee\none two t|hr|ee', 'b_2b', 'one |two th|ree\none |two th|ree')
