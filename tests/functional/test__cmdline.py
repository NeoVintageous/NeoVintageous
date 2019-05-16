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
from NeoVintageous.nv.vi.settings import set_cmdline_cwd


class TestCmdlineEditing(unittest.FunctionalTestCase):

    def setUp(self):
        super().setUp()
        self.view.settings().set('_nv_ex_mode', True)
        reset_cmdline_completion_state()

    # TODO [refactor] Into usable run test command-line mode command via feed.
    def feed(self, seq):
        self.view.run_command('_nv_cmdline_feed_key', {'key': seq})

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

    def test_c_tab_set_completions(self):
        self.eq(':set |', '<tab>', ':set autoindent|')
        self.feed('<tab>')
        self.assertNormal(':set hlsearch|')
        self.feed('<tab>')
        self.assertNormal(':set ignorecase|')

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

    @unittest.mock.patch.dict('NeoVintageous.nv.vi.settings._storage', {})
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

    @unittest.mock.patch.dict('NeoVintageous.nv.vi.settings._storage', {})
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

    @unittest.mock.patch.dict('NeoVintageous.nv.vi.settings._storage', {})
    def test_c_tab_cd_completions_only_include_directories(self):
        set_cmdline_cwd(self.fixturePath('cwd'))
        self.eq(':cd |', '<tab>', ':cd sub/|')
        self.feed('<tab>')
        self.assertNormal(':cd sub2/|')
        self.feed('<tab>')
        self.assertNormal(':cd |')
        self.feed('<tab>')
        self.assertNormal(':cd sub/|')

    @unittest.mock.patch.dict('NeoVintageous.nv.vi.settings._storage', {})
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

    @unittest.mock.patch.dict('NeoVintageous.nv.vi.settings._storage', {})
    def test_c_tab_edit_completion_backup_slash(self):
        set_cmdline_cwd(self.fixturePath('cwd', 'sub'))
        self.eq(':edit ../|', '<tab>', ':edit ../b.txt|')

    @unittest.mock.patch.dict('NeoVintageous.nv.vi.settings._storage', {})
    def test_c_tab_edit_completion_prefix(self):
        set_cmdline_cwd(self.fixturePath('cwd'))
        self.eq(':edit sub/s|', '<tab>', ':edit sub/sb.txt|')
        self.feed('<tab>')
        self.assertNormal(':edit sub/sc.txt|')
        self.feed('<tab>')
        self.assertNormal(':edit sub/s|')
        self.feed('<tab>')
        self.assertNormal(':edit sub/sb.txt|')
