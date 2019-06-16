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


class Test_slash(unittest.FunctionalTestCase):

    def test_n(self):
        self.eq('|', 'n_/abc', '|')
        self.assertSearch('')
        self.assertSearchCurrent('')
        self.eq('|xabcx', 'n_/abc', 'x|abcx')
        self.assertSearch('x|abc|x')
        self.assertSearchCurrent('x|abc|x')
        self.eq('|foo\nabc\nbar\nabc\nmoo\nabc\nend', 'n_/abc', 'foo\n|abc\nbar\nabc\nmoo\nabc\nend')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\n|abc|\nbar\nabc\nmoo\nabc\nend')
        self.eq('foo\nabc\nbar\nabc\nmoo\na|bc\nend', 'n_/abc', 'foo\n|abc\nbar\nabc\nmoo\nabc\nend')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\n|abc|\nbar\nabc\nmoo\nabc\nend')
        self.eq('foo\nabc\nbar\nabc\nmoo\n|abc\nend', 'n_/abc', 'foo\n|abc\nbar\nabc\nmoo\nabc\nend')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\n|abc|\nbar\nabc\nmoo\nabc\nend')
        self.eq('foo\nabc\nbar\nabc\nmoo\nabc\n|end', 'n_/abc', 'foo\n|abc\nbar\nabc\nmoo\nabc\nend')

    def test_n_when_view_contains_only_one_match_issue_223(self):
        self.eq('a|bc', 'n_/abc', '|abc')
        self.assertSearch('|abc|')
        self.assertSearchCurrent('|abc|')
        self.eq('x a|bc x', 'n_/abc', 'x |abc x')
        self.assertSearch('x |abc| x')
        self.assertSearchCurrent('x |abc| x')

    def test_v(self):
        self.eq('|x abc y', 'v_/abc', '|x a|bc y')
        self.eq('x abc |y abc z', 'v_/abc', 'x abc |y a|bc z')

    def test_V(self):
        self.eq('|x\n|abc\ny', 'V_/abc', '|x\nabc\n|y')
        self.eq('abc\n|x\n|abc\ny', 'V_/abc', 'abc\n|x\nabc\n|y')

    def test_d(self):
        self.eq('fi|zzabcx', 'd/abc', 'fi|abcx')
        self.eq('|foo\nabc\nbar\nabc\nmoo\nabc\nend', 'd/abc', '|abc\nbar\nabc\nmoo\nabc\nend')
        self.eq('foo\nabc\nbar\nabc\nmoo\na|bc\nend', 'd/abc', 'foo\n|bc\nend')
        self.eq('foo\nabc\nbar\nabc\nmoo\n|abc\nend', 'd/abc', 'foo\n|abc\nend')
        self.eq('foo\nabc\nbar\nabc\nmoo\nabc\n|end', 'd/abc', 'foo\n|end')
