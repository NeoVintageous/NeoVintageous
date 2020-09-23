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

from NeoVintageous.nv.ex.completions import reset_cmdline_completion_state
from NeoVintageous.nv.settings import set_cmdline_cwd


class TestCmdlineEditing(unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()
        self.settings().set('_nv_ex_mode', True)
        reset_cmdline_completion_state()

    # TODO [refactor] Into usable run test command-line mode command via feed.
    def feed(self, seq):
        self.view.run_command('nv_cmdline_feed_key', {'key': seq})

    def test_c_ctrl_b(self):
        for test_key in ('<C-b>', '<home>'):
            self.normal(':abc|')
            self.feed(test_key)
            self.assertNormal(':|abc')

            # shouldn't change if position already correct.
            self.feed(test_key)
            self.assertNormal(':|abc')

            # should work in the middle of words.
            self.normal(':ab|c')
            self.feed(test_key)
            self.assertNormal(':|abc')

            # shouldn't move cursor when cmdline is empty.
            self.normal(':|')
            self.feed(test_key)
            self.assertNormal(':|')

    def test_c_ctrl_e(self):
        for test_key in ('<C-e>', '<end>'):
            self.normal(':|abc')
            self.feed(test_key)
            self.assertNormal(':abc|')

            # shouldn't change if position already correct.
            self.feed(test_key)
            self.assertNormal(':abc|')

            # should work in the middle of words.
            self.normal(':a|bc')
            self.feed(test_key)
            self.assertNormal(':abc|')

            # shouldn't move cursor when cmdline is empty.
            self.normal(':|')
            self.feed(test_key)
            self.assertNormal(':|')

    def test_c_ctrl_h(self):
        for test_key in ('<C-h>',):
            self.normal(':abc|')
            self.feed(test_key)
            self.assertNormal(':ab|')

            self.normal(':ab|c')
            self.feed(test_key)
            self.assertNormal(':a|c')

            self.normal(':|')
            self.feed(test_key)
            self.assertNormal(':|')

    def test_c_ctrl_u(self):
        self.normal(':abc|')
        self.feed('<C-u>')
        self.assertNormal(':|')

        # shouldn't change when cmdline is empty.
        self.feed('<C-u>')
        self.assertNormal(':|')

        # should only remove characters up to cursor position.
        self.normal(':abc d|ef')
        self.feed('<C-u>')
        self.assertNormal(':|ef')

        # shouldn't change anything if no characters before cursor.
        self.feed('<C-w>')
        self.assertNormal(':|ef')

    def test_c_ctrl_w(self):
        self.normal(':abc|')
        self.feed('<C-w>')
        self.assertNormal(':|')

        # shouldn't change when cmdline is empty.
        self.feed('<C-w>')
        self.assertNormal(':|')

        # should only remove characters up to cursor position.
        self.normal(':ab|c')
        self.feed('<C-w>')
        self.assertNormal(':|c')

        # shouldn't change anything if no characters before cursor.
        self.feed('<C-w>')
        self.assertNormal(':|c')

        # should include whitespace.
        self.normal(':abc def    |')
        self.feed('<C-w>')
        self.assertNormal(':abc |')
        self.feed('<C-w>')
        self.assertNormal(':|')

    def test_c_tab_completions(self):
        self.eq(':bl|', '<tab>', ':blast|')
        self.eq(':bN|', '<tab>', ':bNext|')
        self.eq(':n|', '<tab>', ':new|')
        self.feed('<tab>')
        self.assertNormal(':nnoremap|')
        self.feed('<tab>')
        self.assertNormal(':nohlsearch|')
        self.feed('<tab>')
        self.assertNormal(':noremap|')
        self.feed('<tab>')
        self.assertNormal(':nunmap|')
        self.feed('<tab>')
        self.assertNormal(':n|')
        self.feed('<tab>')
        self.assertNormal(':new|')

    def test_c_shift_tab_completions(self):
        self.eq(':bl|', '<S-tab>', ':blast|')
        self.eq(':bN|', '<S-tab>', ':bNext|')
        self.eq(':n|', '<S-tab>', ':nunmap|')
        self.feed('<S-tab>')
        self.assertNormal(':noremap|')
        self.feed('<S-tab>')
        self.assertNormal(':nohlsearch|')
        self.feed('<S-tab>')
        self.assertNormal(':nnoremap|')
        self.feed('<S-tab>')
        self.assertNormal(':new|')
        self.feed('<S-tab>')
        self.assertNormal(':n|')
        self.feed('<S-tab>')
        self.assertNormal(':nunmap|')

    def test_c_tab_set_completions(self):
        self.eq(':set |', '<tab>', ':set autoindent|')
        self.feed('<tab>')
        self.assertNormal(':set belloff|')
        self.feed('<tab>')
        self.assertNormal(':set expandtabs|')

    def test_c_tab_set_completions_no(self):
        self.eq(':set noi|', '<tab>', ':set noignorecase|')
        self.feed('<tab>')
        self.assertNormal(':set noincsearch|')

    def test_c_tab_set_prefix_single_completion(self):
        self.eq(':set li|', '<tab>', ':set list|')

    def test_c_tab_set_wraps_completions(self):
        self.eq(':set i|', '<tab>', ':set ignorecase|')
        self.feed('<tab>')
        self.assertNormal(':set incsearch|')
        self.feed('<tab>')
        self.assertNormal(':set ignorecase|')
        self.feed('<tab>')
        self.assertNormal(':set incsearch|')

    def test_c_tab_set_no_completions(self):
        self.eq(':set foobar|', '<tab>', ':set foobar|')

    def test_c_tab_set_unknown_prefix(self):
        self.settings().set('translate_tabs_to_spaces', True)
        self.eq(':foobar |', '<tab>', ':foobar     |')
        self.settings().set('translate_tabs_to_spaces', False)
        self.eq(':foobar |', '<tab>', ':foobar \t|')

    @unittest.mock.patch.dict('NeoVintageous.nv.session._session', {})
    @unittest.mock.patch('os.path.expanduser')
    def test_c_tab_edit_tilda(self, expanduser):
        set_cmdline_cwd(self.fixturePath('cwd'))
        cwd = self.fixturePath('cwd')
        expanduser.side_effect = lambda path: path.replace('~', cwd)
        self.eq(':edit ~|', '<tab>', ':edit %s/|' % cwd)
        self.feed('<tab>')
        self.assertNormal(':edit %s/b.txt|' % cwd)
        self.feed('<tab>')
        self.assertNormal(':edit %s/sub/|' % cwd)
        self.feed('<tab>')
        self.assertNormal(':edit %s/sub2/|' % cwd)
        self.feed('<tab>')
        self.assertNormal(':edit %s/x.txt|' % cwd)
        self.feed('<tab>')
        self.assertNormal(':edit %s/|' % cwd)
        self.feed('<tab>')
        self.assertNormal(':edit %s/b.txt|' % cwd)

    @unittest.mock.patch.dict('NeoVintageous.nv.session._session', {})
    def test_c_tab_file_completions(self):
        set_cmdline_cwd(self.fixturePath('cwd'))
        for cmd in (':edit', ':e', ':tabedit', ':split', ':sp', ':vsplit', ':vs'):
            reset_cmdline_completion_state()
            self.eq(cmd + ' |', '<tab>', cmd + ' b.txt|')
            self.feed('<tab>')
            self.assertNormal(cmd + ' sub/|')
            self.feed('<tab>')
            self.assertNormal(cmd + ' sub2/|')
            self.feed('<tab>')
            self.assertNormal(cmd + ' x.txt|')
            self.feed('<tab>')
            self.assertNormal(cmd + ' |')
            self.feed('<tab>')
            self.assertNormal(cmd + ' b.txt|')

    @unittest.mock.patch.dict('NeoVintageous.nv.session._session', {})
    def test_c_tab_cd_completions_only_include_directories(self):
        set_cmdline_cwd(self.fixturePath('cwd'))
        self.eq(':cd |', '<tab>', ':cd sub/|')
        self.feed('<tab>')
        self.assertNormal(':cd sub2/|')
        self.feed('<tab>')
        self.assertNormal(':cd |')
        self.feed('<tab>')
        self.assertNormal(':cd sub/|')

    @unittest.mock.patch.dict('NeoVintageous.nv.session._session', {})
    def test_c_cd_existing_path(self):
        set_cmdline_cwd(self.fixturePath('cwd'))
        self.eq(':cd s|', '<tab>', ':cd sub/|')
        self.feed('<tab>')
        self.assertNormal(':cd sub2/|')

    @unittest.mock.patch.dict('NeoVintageous.nv.session._session', {})
    def test_c_cd_non_existing_path(self):
        set_cmdline_cwd(self.fixturePath('cwd'))
        self.eq(':cd x|', '<tab>', ':cd x|')

    @unittest.mock.patch.dict('NeoVintageous.nv.session._session', {})
    def test_c_tab_edit_completion_backup(self):
        set_cmdline_cwd(self.fixturePath('cwd', 'sub'))
        for cmd in (':edit', ':e', ':tabedit', ':split', ':sp', ':vsplit', ':vs'):
            reset_cmdline_completion_state()
            self.eq(cmd + ' ..|', '<tab>', cmd + ' ../|')
            self.feed('<tab>')
            self.assertNormal(cmd + ' ../b.txt|')
            self.feed('<tab>')
            self.assertNormal(cmd + ' ../sub/|')
            self.feed('<tab>')
            self.assertNormal(cmd + ' ../sub2/|')
            self.feed('<tab>')
            self.assertNormal(cmd + ' ../x.txt|')
            self.feed('<tab>')
            self.assertNormal(cmd + ' ../|')
            self.feed('<tab>')
            self.assertNormal(cmd + ' ../b.txt|')

    @unittest.mock.patch.dict('NeoVintageous.nv.session._session', {})
    def test_c_tab_edit_completion_backup_slash(self):
        set_cmdline_cwd(self.fixturePath('cwd', 'sub'))
        self.eq(':edit ../|', '<tab>', ':edit ../b.txt|')

    @unittest.mock.patch.dict('NeoVintageous.nv.session._session', {})
    def test_c_tab_edit_completion_prefix(self):
        set_cmdline_cwd(self.fixturePath('cwd'))
        self.eq(':edit sub/s|', '<tab>', ':edit sub/sb.txt|')
        self.feed('<tab>')
        self.assertNormal(':edit sub/sc.txt|')
        self.feed('<tab>')
        self.assertNormal(':edit sub/s|')
        self.feed('<tab>')
        self.assertNormal(':edit sub/sb.txt|')

    @unittest.mock_bell()
    @unittest.mock.patch.dict('NeoVintageous.nv.history._storage', {
        1: {'num': 0, 'items': {}},
        2: {'num': 0, 'items': {}},
        3: {'num': 0, 'items': {}},
        4: {'num': 0, 'items': {}},
        5: {'num': 0, 'items': {}}})
    def test_c_history_empty(self):
        self.insert(':|')
        self.feed('<C-p>')
        self.assertBell()
        self.feed('<C-n>')
        self.assertBell()
        self.insert('/|')
        self.feed('<up>')
        self.assertBell()
        self.feed('<down>')
        self.assertBell()

    @unittest.mock_bell()
    @unittest.mock.patch.dict('NeoVintageous.nv.history._storage', {
        1: {
            'num': 72,
            'items': {
                1: 'third',
                2: 'second',
                3: 'first',
            }},
        2: {
            'num': 8,
            'items': {
                2: 'pattern2',
                4: 'pattern1',
            }},
        3: {'num': 0, 'items': {}},
        4: {'num': 0, 'items': {}},
        5: {'num': 0, 'items': {}}})
    def test_c_history(self):
        self.insert(':|')
        self.feed('<up>')
        self.assertInsert(':first|')
        self.feed('<up>')
        self.assertInsert(':second|')
        self.feed('<up>')
        self.assertInsert(':third|')
        self.assertNoBell()
        self.feed('<up>')
        self.assertInsert(':third|')
        self.assertBell()
        self.feed('<down>')
        self.assertInsert(':second|')
        self.feed('<down>')
        self.assertInsert(':first|')
        self.feed('<down>')
        self.assertInsert(':|')
        self.feed('<down>')
        self.assertBell()
        self.insert('/|')
        self.feed('<C-p>')
        self.assertInsert('/pattern1|')
        self.feed('<C-p>')
        self.assertInsert('/pattern2|')
        self.feed('<C-n>')
        self.assertInsert('/pattern1|')
        self.feed('<C-n>')
        self.assertInsert('/|')

    @unittest.mock_run_commands('hide_panel')
    def test_c_ctrl_c(self):
        self.normal(':abc|')
        self.feed('<C-c>')
        self.assertRunCommand('hide_panel', {'cancel': True})

    @unittest.mock_run_commands('hide_panel')
    def test_c_ctrl_bracket(self):
        self.normal(':abc|')
        self.feed('<C-[>')
        self.assertRunCommand('hide_panel', {'cancel': True})
