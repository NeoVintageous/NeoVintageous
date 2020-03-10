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


class Test_n(unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()
        self.set_option('wrapscan', True)

    def test_n_repeat_star_forward(self):
        self.normal('foo\n|abc\nbar\nabc\nmoo\nabc\nend')
        self.feed('n_*')
        self.feed('n_n')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\nabc\nbar\nabc\nmoo\n|abc|\nend')
        self.feed('n_n')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\n|abc|\nbar\nabc\nmoo\nabc\nend')
        self.feed('n_n')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\nabc\nbar\n|abc|\nmoo\nabc\nend')

    def test_n_repeat_star_forward_no_partial(self):
        self.normal('foo\n|abc\nbar\nabc\nmoo\nabcxend')
        self.feed('n_*')
        self.feed('n_n')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\nabcxend')
        self.assertSearchCurrent('foo\n|abc|\nbar\nabc\nmoo\nabcxend')
        self.feed('n_n')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\nabcxend')
        self.assertSearchCurrent('foo\nabc\nbar\n|abc|\nmoo\nabcxend')

    def test_n_repeat_star_forward_should_not_use_smartcase(self):
        self.normal('x|Xx\nXXX\nxXx\nXxX\n')
        self.set_option('ignorecase', True)
        self.set_option('smartcase', True)
        self.feed('n_*')
        self.assertSearch('|xXx|\n|XXX|\n|xXx|\n|XxX|\n')
        self.assertSearchCurrent('xXx\n|XXX|\nxXx\nXxX\n')
        self.feed('n_n')
        self.assertSearch('|xXx|\n|XXX|\n|xXx|\n|XxX|\n')
        self.assertSearchCurrent('xXx\nXXX\n|xXx|\nXxX\n')

    def test_n_repeat_octothorp_forward(self):
        self.normal('foo\n|abc\nbar\nabc\nmoo\nabc\nend')
        self.feed('n_#')
        self.feed('n_n')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\nabc\nbar\n|abc|\nmoo\nabc\nend')

    def test_n_repeat_slash_forward(self):
        self.normal('|foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.feed('n_/abc')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\n|abc|\nbar\nabc\nmoo\nabc\nend')
        self.feed('n_n')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\nabc\nbar\n|abc|\nmoo\nabc\nend')
        self.feed('n_n')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\nabc\nbar\nabc\nmoo\n|abc|\nend')
        self.feed('n_n')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\n|abc|\nbar\nabc\nmoo\nabc\nend')

    def test_n_repeat_slash_partial(self):
        self.normal('|foo\nabc\nbar\nabcxmoo\nabc\nend')
        self.feed('n_/abc')
        self.assertSearch('foo\n|abc|\nbar\n|abc|xmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\n|abc|\nbar\nabcxmoo\nabc\nend')
        self.feed('n_n')
        self.assertSearch('foo\n|abc|\nbar\n|abc|xmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\nabc\nbar\n|abc|xmoo\nabc\nend')
        self.feed('n_n')
        self.assertSearch('foo\n|abc|\nbar\n|abc|xmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\nabc\nbar\nabcxmoo\n|abc|\nend')
        self.feed('n_n')
        self.assertSearch('foo\n|abc|\nbar\n|abc|xmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\n|abc|\nbar\nabcxmoo\nabc\nend')

    def test_n_repeat_question_mark_forward(self):
        self.normal('|foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.feed('n_?abc')
        self.feed('n_n')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\nabc\nbar\n|abc|\nmoo\nabc\nend')
        self.feed('n_n')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\n|abc|\nbar\nabc\nmoo\nabc\nend')

    def test_n_repeat_question_mark_partial(self):
        self.normal('|foo\nabc\nbar\nabcxmoo\nabc\nend')
        self.feed('n_?abc')
        self.feed('n_n')
        self.assertSearch('foo\n|abc|\nbar\nabcxmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\n|abc|\nbar\nabcxmoo\nabc\nend')

    def test_n_no_match(self):
        self.feed('n_/abc')
        self.eq('foo|bar', 'n_n', 'foo|bar')

    def test_n_wrapscan_false(self):
        self.set_option('wrapscan', False)
        self.eq('a|bc\nx\nabc\nx', 'n_*', 'abc\nx\n|abc\nx')
        self.eq('abc\nx\n|abc\nx', 'n_n', 'abc\nx\n|abc\nx')
