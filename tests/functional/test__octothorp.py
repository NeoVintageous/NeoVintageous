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


class Test_octothorp(unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()
        self.set_option('wrapscan', True)

    def test_n(self):
        self.eq('abc\n|abc', 'n_#', '|abc\nabc')
        self.assertSearch('|abc|\n|abc|')
        self.assertSearchCurrent('|abc|\nabc')
        self.eq('fi|zz', 'n_#', '|fizz')
        self.assertSearch('|fizz|')
        self.assertSearchCurrent('|fizz|')
        self.eq('x fi|zz x', 'n_#', 'x |fizz x')
        self.assertSearch('x |fizz| x')
        self.assertSearchCurrent('x |fizz| x')

    def test_n_empty(self):
        self.eq('|', 'n_#', '|')
        self.assertSearch('')
        self.assertSearchCurrent('')

    def test_n_multiple_cursors(self):
        self.eq('xy xy x|y xy xy x|y xy', 'n_#', 'xy |xy xy xy |xy xy xy')
        self.assertSearch('|xy| |xy| |xy| |xy| |xy| |xy| |xy|')
        self.assertSearchCurrent('xy |xy| xy xy |xy| xy xy')

    def test_n_multiple_cursors_is_noop_if_all_cursors_are_not_on_the_same_word(self):
        self.eq('xy x|y xy xy ab a|b ab', 'n_#', 'xy x|y xy xy ab a|b ab')
        self.assertSearch('xy xy xy xy ab ab ab')
        self.assertSearchCurrent('xy xy xy xy ab ab ab')

    def test_n_select_match_middle(self):
        self.eq('abc\na|bc', 'n_#', '|abc\nabc')
        self.assertSearch('|abc|\n|abc|')
        self.assertSearchCurrent('|abc|\nabc')

    def test_n_select_match_end(self):
        self.eq('abc\nab|c', 'n_#', '|abc\nabc')
        self.assertSearch('|abc|\n|abc|')
        self.assertSearchCurrent('|abc|\nabc')

    def test_n_select_repeat_match(self):
        self.eq('abc\nabc\nfoo\n|abc\nbar', 'n_#', 'abc\n|abc\nfoo\nabc\nbar')
        self.assertSearch('|abc|\n|abc|\nfoo\n|abc|\nbar')
        self.assertSearchCurrent('abc\n|abc|\nfoo\nabc\nbar')
        self.feed('n_#')
        self.assertSearchCurrent('|abc|\nabc\nfoo\nabc\nbar')
        self.feed('n_#')
        self.assertSearchCurrent('abc\nabc\nfoo\n|abc|\nbar')

    def test_n_select_wrap_match(self):
        self.eq('boo\n|abc\nfoo\nabc\nbar', 'n_#', 'boo\nabc\nfoo\n|abc\nbar')
        self.assertSearch('boo\n|abc|\nfoo\n|abc|\nbar')
        self.assertSearchCurrent('boo\nabc\nfoo\n|abc|\nbar')

    def test_n_select_no_partial_match(self):
        self.eq('boo\nabc\nabcxabc\n|abc\nbar', 'n_#', 'boo\n|abc\nabcxabc\nabc\nbar')
        self.assertSearch('boo\n|abc|\nabcxabc\n|abc|\nbar')
        self.assertSearchCurrent('boo\n|abc|\nabcxabc\nabc\nbar')

    def test_n_select_no_match(self):
        self.eq('boo\nabc\nf|oo\nabc\nbar', 'n_#', 'boo\nabc\n|foo\nabc\nbar')
        self.assertSearch('boo\nabc\n|foo|\nabc\nbar')
        self.assertSearchCurrent('boo\nabc\n|foo|\nabc\nbar')

    def test_n_no_match_puts_cursor_on_first_non_blank(self):
        self.eq('    fi|zz\nx\nabc\n', 'n_#', '    |fizz\nx\nabc\n')
        self.assertSearch('    |fizz|\nx\nabc\n')
        self.assertSearchCurrent('    |fizz|\nx\nabc\n')

    def test_n_wrapscan_false(self):
        self.set_option('wrapscan', False)
        self.eq('x\nabc\nx\na|bc\nx', 'n_#', 'x\n|abc\nx\nabc\nx')
        self.eq('x\n|abc\nx\nabc\nx', 'n_#', 'x\n|abc\nx\nabc\nx')
        self.eq('x\nabc\nx\na|bc\nx', 'n_3#', 'x\n|abc\nx\nabc\nx')

    def test_n_ignorecase(self):
        self.normal('xxx\nXXX\nx|xx\nXxX\n')
        self.set_option('ignorecase', True)
        self.feed('n_#')
        self.assertNormal('xxx\n|XXX\nxxx\nXxX\n')
        self.assertSearch('|xxx|\n|XXX|\n|xxx|\n|XxX|\n')
        self.assertSearchCurrent('xxx\n|XXX|\nxxx\nXxX\n')
        self.normal('xxx\nXXX\nx|xx\nXxX\n')
        self.set_option('ignorecase', False)
        self.feed('n_#')
        self.assertNormal('|xxx\nXXX\nxxx\nXxX\n')
        self.assertSearch('|xxx|\nXXX\n|xxx|\nXxX\n')
        self.assertSearchCurrent('|xxx|\nXXX\nxxx\nXxX\n')

    def test_n_smartcase_should_not_be_used_for_word_search(self):
        self.normal('xXx\nXXX\nx|Xx\nXxX\n')
        self.set_option('ignorecase', True)
        self.set_option('smartcase', True)
        self.feed('n_#')
        self.assertSearch('|xXx|\n|XXX|\n|xXx|\n|XxX|\n')
        self.normal('xXx\nXXX\nx|Xx\nXxX\n')
        self.set_option('ignorecase', True)
        self.set_option('smartcase', False)
        self.feed('n_#')
        self.assertSearch('|xXx|\n|XXX|\n|xXx|\n|XxX|\n')
        self.normal('xXx\nXXX\nx|Xx\nXxX\n')
        self.set_option('ignorecase', False)
        self.set_option('smartcase', True)
        self.feed('n_#')
        self.assertSearch('|xXx|\nXXX\n|xXx|\nXxX\n')
        self.normal('xXx\nXXX\nx|Xx\nXxX\n')
        self.set_option('ignorecase', False)
        self.set_option('smartcase', False)
        self.feed('n_#')
        self.assertSearch('|xXx|\nXXX\n|xXx|\nXxX\n')

    @unittest.mock_status_message()
    def test_n_no_string_under_cursor(self):
        self.eq('x | x', 'n_#', 'x | x')
        self.assertStatusMessage('E348: No string under cursor')

    def test_v_octothorp(self):
        self.eq('x\nabc\nx\nab|c\nx', 'v_#', 'r_x\n|abc\nx\nabc|\nx')

    def test_d_octohorp(self):
        self.eq('abc\nx\nabc\nx\na|bc\nx', 'd#', 'abc\nx\n|bc\nx')
