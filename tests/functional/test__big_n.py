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


class Test_N(unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()
        self.set_option('wrapscan', True)

    def test_N_repeat_star(self):
        self.normal('foo\nabc\nbar\n|abc\nmoo\nabc\nend')
        self.feed('n_*')
        self.feed('n_N')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\nabc\nbar\n|abc|\nmoo\nabc\nend')
        self.feed('n_N')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\n|abc|\nbar\nabc\nmoo\nabc\nend')
        self.feed('n_N')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\nabc\nbar\nabc\nmoo\n|abc|\nend')

    def test_N_repeat_star_only_matches_whole_words(self):
        self.normal('foo\n|abc\nbar\nabc\nmoo\nabcxend')
        self.feed('n_*')
        self.feed('n_N')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\nabcxend')
        self.assertSearchCurrent('foo\n|abc|\nbar\nabc\nmoo\nabcxend')
        self.feed('n_N')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\nabcxend')
        self.assertSearchCurrent('foo\nabc\nbar\n|abc|\nmoo\nabcxend')
        self.feed('n_N')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\nabcxend')
        self.assertSearchCurrent('foo\n|abc|\nbar\nabc\nmoo\nabcxend')

    def test_N_repeat_octothorp(self):
        self.normal('foo\nabc\nbar\n|abc\nmoo\nabc\nend')
        self.feed('n_#')
        self.feed('n_N')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\nabc\nbar\n|abc|\nmoo\nabc\nend')
        self.feed('n_N')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\nabc\nbar\nabc\nmoo\n|abc|\nend')
        self.feed('n_N')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\n|abc|\nbar\nabc\nmoo\nabc\nend')

    def test_N_repeat_octothorp_only_matches_whole_words(self):
        self.normal('foo\nabc\nbar\n|abc\nmoo\nabcxend\nabc\n')
        self.feed('n_#')
        self.feed('n_N')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\nabcxend\n|abc|\n')
        self.assertSearchCurrent('foo\nabc\nbar\n|abc|\nmoo\nabcxend\nabc\n')
        self.feed('n_N')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\nabcxend\n|abc|\n')
        self.assertSearchCurrent('foo\nabc\nbar\nabc\nmoo\nabcxend\n|abc|\n')
        self.feed('n_N')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\nabcxend\n|abc|\n')
        self.assertSearchCurrent('foo\n|abc|\nbar\nabc\nmoo\nabcxend\nabc\n')

    def test_N_repeat_slash(self):
        self.normal('|foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.feed('n_/abc')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\n|abc|\nbar\nabc\nmoo\nabc\nend')
        self.feed('n_N')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\nabc\nbar\nabc\nmoo\n|abc|\nend')
        self.feed('n_N')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\nabc\nbar\n|abc|\nmoo\nabc\nend')
        self.feed('n_N')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\n|abc|\nbar\nabc\nmoo\nabc\nend')
        self.feed('n_N')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\nabc\nbar\nabc\nmoo\n|abc|\nend')
        self.feed('n_2N')
        self.assertSearch('foo\n|abc|\nbar\n|abc|\nmoo\n|abc|\nend')
        self.assertSearchCurrent('foo\n|abc|\nbar\nabc\nmoo\nabc\nend')

    def test_n_repeat_question_mark(self):
        self.normal('foo\nabc\nb|ar\nabcmoo\nabc\nend')
        self.feed('n_?abc')
        self.assertSearchCurrent('foo\n|abc|\nbar\nabcmoo\nabc\nend')
        self.feed('n_N')
        self.assertSearch('foo\n|abc|\nbar\n|abc|moo\n|abc|\nend')
        self.assertSearchCurrent('foo\nabc\nbar\n|abc|moo\nabc\nend')
        self.feed('n_N')
        self.assertSearch('foo\n|abc|\nbar\n|abc|moo\n|abc|\nend')
        self.assertSearchCurrent('foo\nabc\nbar\nabcmoo\n|abc|\nend')
        self.feed('n_2N')
        self.assertSearch('foo\n|abc|\nbar\n|abc|moo\n|abc|\nend')
        self.assertSearchCurrent('foo\nabc\nbar\n|abc|moo\nabc\nend')
