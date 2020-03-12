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

    def test_n_repeat_star(self):
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

    def test_n_repeat_star_should_only_match_whole_words(self):
        self.normal('foo\n|abc\nbar\nabc\nmoo\nabcxend\nabc\n')
        self.feed('n_*')
        self.feed('n_n')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\nabcxend\n|abc|\n')
        self.assertSearchCurrent('foo\nabc\nbar\nabc\nmoo\nabcxend\n|abc|\n')
        self.feed('n_n')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\nabcxend\n|abc|\n')
        self.assertSearchCurrent('foo\n|abc|\nbar\nabc\nmoo\nabcxend\nabc\n')

    def test_n_repeat_star_should_use_ignorecase_option_but_not_smartcase_option(self):
        self.normal('x|Xx\nXXX\nxXx\nXxX\n')
        self.set_option('ignorecase', True)
        self.set_option('smartcase', True)
        self.feed('n_*')
        self.assertSearch('|xXx|\n|XXX|\n|xXx|\n|XxX|\n')
        self.assertSearchCurrent('xXx\n|XXX|\nxXx\nXxX\n')
        self.feed('n_n')
        self.assertSearch('|xXx|\n|XXX|\n|xXx|\n|XxX|\n')
        self.assertSearchCurrent('xXx\nXXX\n|xXx|\nXxX\n')

    def test_n_repeat_octothorp(self):
        self.normal('foo\nabc\nbar\nabc\nmoo\n|abc\nend')
        self.feed('n_#')
        self.feed('n_n')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\n|abc|\nbar\nabc\nmoo\nabc\nend')
        self.feed('n_n')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\nabc\nbar\nabc\nmoo\n|abc|\nend')
        self.feed('n_n')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\nabc\nbar\n|abc|\nmoo\nabc\nend')

    def test_n_repeat_slash(self):
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
        self.feed('n_2n')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\nabc\nbar\nabc\nmoo\n|abc|\nend')

    def test_n_repeat_slash_matches_all_occurences(self):
        self.normal('|foo\nabc\nbar\nabcmoo\nabc\nend')
        self.feed('n_/abc')
        self.feed('n_n')
        self.assertSearch('foo\n|abc|\nbar\n|abc|moo\n|abc|\nend')
        self.assertSearchCurrent('foo\nabc\nbar\n|abc|moo\nabc\nend')
        self.feed('n_2n')
        self.assertSearch('foo\n|abc|\nbar\n|abc|moo\n|abc|\nend')
        self.assertSearchCurrent('foo\n|abc|\nbar\nabcmoo\nabc\nend')

    def test_n_repeat_slash_should_use_ignorecase_and_smartcase(self):
        self.normal('abc\na|Bc\nABC\naBc\nabc\naBc\nABC\naBc\n')
        self.set_option('ignorecase', True)
        self.set_option('smartcase', True)
        self.feed('n_/aBc')
        self.feed('n_n')
        self.assertSearch('abc\n|aBc|\nABC\n|aBc|\nabc\n|aBc|\nABC\n|aBc|\n')
        self.assertSearchCurrent('abc\naBc\nABC\naBc\nabc\n|aBc|\nABC\naBc\n')
        self.feed('n_n')
        self.assertSearch('abc\n|aBc|\nABC\n|aBc|\nabc\n|aBc|\nABC\n|aBc|\n')
        self.assertSearchCurrent('abc\naBc\nABC\naBc\nabc\naBc\nABC\n|aBc|\n')
        self.normal('abc\na|Bc\nABC\naBc\nabc\naBc\nABC\naBc\n')
        self.set_option('ignorecase', True)
        self.set_option('smartcase', False)
        self.feed('n_/aBc')
        self.feed('n_n')
        self.assertSearch('|abc|\n|aBc|\n|ABC|\n|aBc|\n|abc|\n|aBc|\n|ABC|\n|aBc|\n')
        self.assertSearchCurrent('abc\naBc\nABC\n|aBc|\nabc\naBc\nABC\naBc\n')
        self.feed('n_n')
        self.assertSearch('|abc|\n|aBc|\n|ABC|\n|aBc|\n|abc|\n|aBc|\n|ABC|\n|aBc|\n')
        self.assertSearchCurrent('abc\naBc\nABC\naBc\n|abc|\naBc\nABC\naBc\n')
        self.feed('n_2n')
        self.assertSearch('|abc|\n|aBc|\n|ABC|\n|aBc|\n|abc|\n|aBc|\n|ABC|\n|aBc|\n')
        self.assertSearchCurrent('abc\naBc\nABC\naBc\nabc\naBc\n|ABC|\naBc\n')

    def test_n_repeat_slash_only_matches_whole_words(self):
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

    def test_n_repeat_question_mark(self):
        self.normal('foo\nabc\nbar\nabc\nmoo\nabc\ne|nd')
        self.feed('n_?abc')
        self.feed('n_n')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\nabc\nbar\n|abc|\nmoo\nabc\nend')
        self.feed('n_n')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\n|abc|\nbar\nabc\nmoo\nabc\nend')
        self.feed('n_n')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\nabc\nbar\nabc\nmoo\n|abc|\nend')
        self.feed('n_2n')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\n|abc|\nbar\nabc\nmoo\nabc\nend')

    def test_n_repeat_question_mark_matches_all_occurences(self):
        self.normal('foo\nabc\nbar\nabcxmoo\nabc\ne|nd')
        self.feed('n_?abc')
        self.feed('n_n')
        self.assertSearch('foo\n|abc|\nbar\n|abc|xmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\nabc\nbar\n|abc|xmoo\nabc\nend')
        self.feed('n_n')
        self.assertSearch('foo\n|abc|\nbar\n|abc|xmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\n|abc|\nbar\nabcxmoo\nabc\nend')
        self.feed('n_n')
        self.assertSearch('foo\n|abc|\nbar\n|abc|xmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\nabc\nbar\nabcxmoo\n|abc|\nend')
        self.feed('n_2n')
        self.assertSearch('foo\n|abc|\nbar\n|abc|xmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\n|abc|\nbar\nabcxmoo\nabc\nend')

    def test_n_no_match(self):
        self.feed('n_/abc')
        self.eq('foo|bar', 'n_n', 'foo|bar')

    def test_n_wrapscan_false(self):
        self.set_option('wrapscan', False)
        self.eq('a|bc\nx\nabc\nx', 'n_*', 'abc\nx\n|abc\nx')
        self.eq('abc\nx\n|abc\nx', 'n_n', 'abc\nx\n|abc\nx')
