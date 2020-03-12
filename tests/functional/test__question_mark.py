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

    def setUp(self):
        super().setUp()
        self.set_option('wrapscan', True)

    def test_n(self):
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
        self.eq('x abc fizz abc| x', 'n_?abc', 'x abc fizz |abc x')
        self.eq('x abc fizz |abc x', 'n_?abc', 'x |abc fizz abc x')

    def test_n_question_mark_when_view_contains_only_one_match_issue_223(self):
        self.eq('a|bc', 'n_?abc', '|abc')
        self.assertSearch('|abc|')
        self.assertSearchCurrent('|abc|')
        self.eq('x a|bc x', 'n_?abc', 'x |abc x')
        self.assertSearch('x |abc| x')
        self.assertSearchCurrent('x |abc| x')

    def test_n_ignorecase_and_smartcase(self):
        self.normal('abc\naBc\nABC\na|Bc\nabc\n')
        self.set_option('ignorecase', True)
        self.set_option('smartcase', True)
        self.feed('n_?aBc')
        self.assertSearchCurrent('abc\n|aBc|\nABC\naBc\nabc\n')
        self.assertSearch('abc\n|aBc|\nABC\n|aBc|\nabc\n')
        self.normal('abc\naBc\nABC\na|Bc\nabc\n')
        self.set_option('ignorecase', True)
        self.set_option('smartcase', False)
        self.feed('n_?aBc')
        self.assertSearchCurrent('abc\naBc\n|ABC|\naBc\nabc\n')
        self.assertSearch('|abc|\n|aBc|\n|ABC|\n|aBc|\n|abc|\n')
        self.normal('abc\naBc\nABC\na|Bc\nabc\n')
        self.set_option('ignorecase', False)
        self.set_option('smartcase', False)
        self.feed('n_?aBc')
        self.assertSearchCurrent('abc\n|aBc|\nABC\naBc\nabc\n')
        self.assertSearch('abc\n|aBc|\nABC\n|aBc|\nabc\n')

    def test_v(self):
        self.eq('x abc |xy', 'v_?abc', 'r_x |abc x|y')
        self.eq('x abc |xy abc', 'v_?abc', 'r_x |abc x|y abc')
        self.eq('xxabcxxabcxx|fizz|xxabcxxabcxx', 'v_?abc', 'r_xxabcxx|abcxxf|izzxxabcxxabcxx')
        self.assertSearch('xx|abc|xx|abc|xxfizzxx|abc|xx|abc|xx')
        self.eq('r_xxabcxxabcxx|fizz|xxabcxxabcxx', 'v_?abc', 'r_xxabcxx|abcxxfizz|xxabcxxabcxx')
        self.eq('|xxabcxxabcxxfizz|xxabcxxabcxx', 'v_?abc', '|xxabcxxa|bcxxfizzxxabcxxabcxx')
        self.eq('abc |fizz abc |x', 'v_?abc', 'abc |fizz a|bc x')
        self.eq('abc |fizz abc| x', 'v_?abc', 'abc |fizz a|bc x')
        self.eq('abc |fizz ab|c x', 'v_?abc', 'abc |fizz a|bc x')
        self.eq('abc |fizz a|bc x', 'v_?abc', 'r_|abc f|izz abc x')
        self.eq('abc |fizz |abc x', 'v_?abc', 'r_|abc f|izz abc x')
        self.eq('r_abc fizz abc| |x', 'v_?abc', 'r_abc fizz |abc |x')
        self.eq('r_abc fizz ab|c |x', 'v_?abc', 'r_abc fizz |abc |x')
        self.eq('r_abc fizz a|bc |x', 'v_?abc', 'r_|abc fizz abc |x')
        self.eq('r_abc fizz |abc |x', 'v_?abc', 'r_|abc fizz abc |x')
        self.eq('r_abc fizz| abc |x', 'v_?abc', 'r_|abc fizz abc |x')

    def test_V(self):
        self.eq('x\nabc\n|y\n|x', 'V_?abc', 'r_x\n|abc\ny\n|x')
        self.eq('x\nabc\n|x\n|x\nabc\ny', 'V_?abc', 'r_x\n|abc\nx\n|x\nabc\ny')
        self.eq('xxabcx\n|fizz\nbuzz\nfizz\nxabcx\nxabcx\n|', 'V_?abc', 'xxabcx\n|fizz\nbuzz\nfizz\nxabcx\nxabcx\n|')
        self.eq('r_xabcx\n|fizz\nbuzz\n|fizz\nxabcx\nxabcx\n', 'V_?abc', 'r_|xabcx\nfizz\nbuzz\n|fizz\nxabcx\nxabcx\n')
        self.eq('r_xabcx\n|fizz\nbuzz\nxabcx\nxabcx\nfizz\n|', 'V_?abc', 'r_|xabcx\nfizz\nbuzz\nxabcx\nxabcx\nfizz\n|')

    def test_d(self):
        self.eq('|xabcx', 'd?abc', '|abcx')
        self.eq('|foo\nabc\nbar\nabc\nmoo\nabc\nend', 'd?abc', '|abc\nend')
        self.eq('foo\nabc\nbar\nabc\nmoo\nabc\ne|nd', 'd?abc', 'foo\nabc\nbar\nabc\nmoo\n|nd')
        self.eq('foo\nabc\nbar\n|abc\nmoo\nabc\nend', 'd?abc', 'foo\n|abc\nmoo\nabc\nend')
        self.eq('foo\nabc\nbar\nabc\nmoo\nabc\nend|', 'd?abc', 'foo\nabc\nbar\nabc\nmoo\n|')


class Test_slash_cmdline_prompt(unittest.FunctionalTestCase):

    @unittest.mock.patch('NeoVintageous.nv.commands.history_update')
    @unittest.mock.patch('NeoVintageous.nv.commands.Cmdline')
    def test_on_done(self, cmdline, history_update):
        self.normal('x fiz x f|iz x')
        self.initCmdlineSearchMock(cmdline, '?', 'on_done', 'fiz')
        self.feed('n_?')
        self.assertNormal('x |fiz x fiz x')
        self.assertSearch('x |fiz| x |fiz| x')
        self.assertSearchCurrent('x |fiz| x fiz x')
        self.assertSearchIncremental('x fiz x fiz x')

    @unittest.mock_status_message()
    @unittest.mock.patch('NeoVintageous.nv.commands.get_last_buffer_search')
    @unittest.mock.patch('NeoVintageous.nv.commands.Cmdline')
    def test_on_done_no_previous_pattern(self, cmdline, get_last_buffer_search):
        get_last_buffer_search.return_value = None
        self.normal('x fiz x f|iz x')
        self.initCmdlineSearchMock(cmdline, '?', 'on_done', '')
        self.feed('n_?')
        self.assertNormal('x fiz x f|iz x')
        self.assertSearch('x fiz x fiz x')
        self.assertStatusMessage('E35: no previous regular expression')

    @unittest.mock_status_message()
    @unittest.mock.patch('NeoVintageous.nv.commands.get_last_buffer_search')
    @unittest.mock.patch('NeoVintageous.nv.commands.Cmdline')
    def test_on_done_with_previous_pattern(self, cmdline, get_last_buffer_search):
        get_last_buffer_search.return_value = 'fi'
        self.normal('x fiz x f|iz x')
        self.initCmdlineSearchMock(cmdline, '?', 'on_done', '')
        self.feed('n_?')
        self.assertNormal('x |fiz x fiz x')
        self.assertSearch('x |fi|z x |fi|z x')
        self.assertSearchCurrent('x |fi|z x fiz x')
        self.assertNoStatusMessage()

    @unittest.mock.patch('NeoVintageous.nv.commands.history_update')
    @unittest.mock.patch('NeoVintageous.nv.commands.Cmdline')
    def test_on_done_should_repeat_last_search(self, cmdline, history_update):
        self.feed('n_?abc')
        self.normal('x abc x a|bc x')
        self.initCmdlineSearchMock(cmdline, '?', 'on_done', '')
        self.feed('n_?')
        self.assertNormal('x |abc x abc x')
        self.assertSearch('x |abc| x |abc| x')
        self.assertSearchCurrent('x |abc| x abc x')
        self.assertSearchIncremental('x abc x abc x')

    @unittest.mock.patch('NeoVintageous.nv.commands.history_update')
    @unittest.mock.patch('NeoVintageous.nv.commands.Cmdline')
    def test_on_change(self, cmdline, history_update):
        self.normal('x buz x b|uz x')
        self.initCmdlineSearchMock(cmdline, '?', 'on_change', 'buz')
        self.feed('n_?')
        self.assertNormal('x buz x b|uz x')
        self.assertSearch('x |buz| x |buz| x')
        self.assertSearchCurrent('x buz x |buz| x')
        self.assertSearchIncremental('x |buz| x buz x')

    @unittest.mock_status_message()
    @unittest.mock.patch('NeoVintageous.nv.commands.history_update')
    @unittest.mock.patch('NeoVintageous.nv.commands.Cmdline')
    def test_on_change_pattern_not_found(self, cmdline, history_update):
        self.normal('x b|uz x buz x')
        self.initCmdlineSearchMock(cmdline, '?', 'on_change', 'fizz')
        self.feed('n_?')
        self.assertNormal('x b|uz x buz x')
        self.assertSearch('x buz x buz x')
        self.assertSearchCurrent('x buz x buz x')
        self.assertSearchIncremental('x buz x buz x')
        self.assertStatusMessage('E486: Pattern not found: fizz')

    @unittest.mock.patch('NeoVintageous.nv.commands.history_update')
    @unittest.mock.patch('NeoVintageous.nv.commands.Cmdline')
    def test_on_cancel(self, cmdline, history_update):
        self.normal('x f|oo x foo x')
        self.initCmdlineSearchMock(cmdline, '?', 'on_cancel')
        self.feed('n_?')
        self.assertNormal('x f|oo x foo x')
        self.assertSearch('x foo x foo x')
        self.assertSearchCurrent('x foo x foo x')
        self.assertSearchIncremental('x foo x foo x')
