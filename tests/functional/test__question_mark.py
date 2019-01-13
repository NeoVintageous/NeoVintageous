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


class Test_question_mark(unittest.FunctionalTestCase):

    def test_question_mark(self):
        self.eq('|', 'n_?abc', '|')
        self.assertSearch('')
        self.assertSearchCurrent('')
        self.eq('|xabcx', 'n_?abc', 'x|abcx')
        self.assertSearch('x|abc|x')
        self.assertSearchCurrent('x|abc|x')
        self.eq('|foo\nabc\nbar\nabc\nmoo\nabc\nend', 'n_?abc', 'foo\nabc\nbar\nabc\nmoo\n|abc\nend')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\nabc\nbar\nabc\nmoo\n|abc|\nend')
        self.eq('foo\nabc\nbar\nabc\nmoo\nabc\ne|nd', 'n_?abc', 'foo\nabc\nbar\nabc\nmoo\n|abc\nend')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\nabc\nbar\nabc\nmoo\n|abc|\nend')
        self.eq('foo\nabc\nbar\n|abc\nmoo\nabc\nend', 'n_?abc', 'foo\n|abc\nbar\nabc\nmoo\nabc\nend')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\n|abc|\nbar\nabc\nmoo\nabc\nend')
        self.eq('foo\nabc\nbar\nabc\nmoo\nabc\nend|', 'n_?abc', 'foo\nabc\nbar\nabc\nmoo\n|abc\nend')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\nabc\nbar\nabc\nmoo\n|abc|\nend')

    def test_v_question_mark(self):
        self.eqr('x abc |xy', 'v_?abc', 'x |abc x|y')
        self.eqr('x abc |xy abc', 'v_?abc', 'x |abc x|y abc')

    def test_N_question_mark(self):
        self.eq('|xabcx', '?abc', 'N_|x|abcx')
        self.assertSearch('x|abc|x')
        self.eq('|foo\nabc\nbar\nabc\nmoo\nabc\nend', '?abc', 'N_|foo\nabc\nbar\nabc\nmoo\n|abc\nend')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')
        self.eqr('foo\nabc\nbar\nabc\nmoo\nabc\ne|nd', '?abc', 'N_foo\nabc\nbar\nabc\nmoo\n|abc\ne|nd')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')
        self.eqr('foo\nabc\nbar\n|abc\nmoo\nabc\nend', '?abc', 'N_foo\n|abc\nbar\n|abc\nmoo\nabc\nend')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')
        self.eqr('foo\nabc\nbar\nabc\nmoo\nabc\nend|', '?abc', 'N_foo\nabc\nbar\nabc\nmoo\n|abc\nend|')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')

    def test_l_question_mark(self):
        self.eqr('x\nabc\n|y\n|x', 'l_?abc', 'x\n|abc\ny\n|x')
        self.eqr('x\nabc\n|x\n|x\nabc\ny', 'l_?abc', 'x\n|abc\nx\n|x\nabc\ny')
