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

    def setUp(self):
        super().setUp()
        self.set_option('wrapscan', True)

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
        self.eq('x| abc fizz abc x', 'n_/abc', 'x |abc fizz abc x')
        self.eq('x |abc fizz abc x', 'n_/abc', 'x abc fizz |abc x')
        self.eq('x a|bc fizz abc x', 'n_/abc', 'x abc fizz |abc x')

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
        self.eq('xxabcxxabcxx|xxx|xxabcxxabcxx', 'v_/abc', 'xxabcxxabcxx|xxxxxa|bcxxabcxx')
        self.assertSearch('xx|abc|xx|abc|xxxxxxx|abc|xx|abc|xx')
        self.eq('r_xxabcxxabc fi|zz bu|zz abcxxabcxx', 'v_/abc', 'xxabcxxabc fizz b|uzz a|bcxxabcxx')
        self.assertSearch('xx|abc|xx|abc| fizz buzz |abc|xx|abc|xx')
        self.eq('|fizz| abc abc x', 'v_/abc', '|fizz a|bc abc x')
        self.eq('|fizz |abc abc x', 'v_/abc', '|fizz a|bc abc x')
        self.eq('|fizz a|bc abc x', 'v_/abc', '|fizz abc a|bc x')
        self.eq('|fizz ab|c abc x', 'v_/abc', '|fizz abc a|bc x')
        self.eq('|fizz abc| abc x', 'v_/abc', '|fizz abc a|bc x')
        self.eq('|fizz abc |abc x', 'v_/abc', '|fizz abc a|bc x')
        self.eq('r_x| abc x abc fi|zz', 'v_/abc', 'r_x |abc x abc fi|zz')
        self.eq('r_x |abc x abc fi|zz', 'v_/abc', 'r_x abc x |abc fi|zz')
        self.eq('r_x a|bc x abc fi|zz', 'v_/abc', 'r_x abc x |abc fi|zz')
        self.eq('r_x ab|c x abc fi|zz', 'v_/abc', 'r_x abc x |abc fi|zz')

    def test_V(self):
        self.eq('|x\n|abc\ny', 'V_/abc', '|x\nabc\n|y')
        self.eq('abc\n|x\n|abc\ny', 'V_/abc', 'abc\n|x\nabc\n|y')
        self.eq('xxabcx\n|fizz\nbuzz\n|fizz\nxabcx\nxabcx\n', 'V_/abc', 'xxabcx\n|fizz\nbuzz\nfizz\nxabcx\n|xabcx\n')
        self.eq('r_xxabcx\n|fizz\nbuzz\n|fizz\nxabcx\nxabcx\n', 'V_/abc', 'xxabcx\nfizz\n|buzz\nfizz\nxabcx\n|xabcx\n')
        self.eq('r_xabcx\n|fizz\nbuzz\nxabcx\nxabcx\nfizz\n|', 'V_/abc', 'r_xabcx\nfizz\nbuzz\n|xabcx\nxabcx\nfizz\n|')
        self.eq('|xabcx\nxabcx\n|xabcx\nxabcx\n', 'V_/abc', '|xabcx\nxabcx\nxabcx\n|xabcx\n')

    def test_d(self):
        self.eq('fi|zzabcx', 'd/abc', 'fi|abcx')
        self.eq('fiz|zabcx', 'd/abc', 'fiz|abcx')
        self.eq('|foo\nabc\nbar\nabc\nmoo\nabc\nend', 'd/abc', '|abc\nbar\nabc\nmoo\nabc\nend')
        self.eq('foo\nabc\nbar\nabc\nmoo\na|bc\nend', 'd/abc', 'foo\n|bc\nend')
        self.eq('foo\nabc\nbar\nabc\nmoo\n|abc\nend', 'd/abc', 'foo\n|abc\nend')
        self.eq('foo\nabc\nbar\nabc\nmoo\nabc\n|end', 'd/abc', 'foo\n|end')
