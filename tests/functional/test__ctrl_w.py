# Copyright (C) 2018-2023 The NeoVintageous Team (NeoVintageous).
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
from sublime import FORCE_GROUP


class Test_ctrl_w(unittest.FunctionalTestCase):

    def test_i(self):
        self.eq('fizz\nbu|zz\nx', 'i_<C-w>', 'i_fizz\n|zz\nx')
        self.eq('fiz buz fiz bu|zz', 'i_<C-w>', 'i_fiz buz fiz |zz')
        self.eq('fiz buz fiz |zz', 'i_<C-w>', 'i_fiz buz |zz')
        self.eq('fiz buz |zz', 'i_<C-w>', 'i_fiz |zz')

    @unittest.mock.patch('NeoVintageous.nv.window._focus_group_bottom_right')
    def test_ctrl_w_b(self, function):
        self.normal('f|izz')
        self.feed('<C-w>b')
        function.assert_called_once_with(self.view.window())

    @unittest.mock.patch('NeoVintageous.nv.window._move_active_view_to_far_left')
    def test_ctrl_w_H(self, function):
        self.normal('f|izz')
        self.feed('<C-w>H')
        function.assert_called_once_with(self.view.window())

    @unittest.mock.patch('NeoVintageous.nv.window._move_active_view_to_very_bottom')
    def test_ctrl_w_J(self, function):
        self.normal('f|izz')
        self.feed('<C-w>J')
        function.assert_called_once_with(self.view.window())

    @unittest.mock.patch('NeoVintageous.nv.window._move_active_view_to_very_top')
    def test_ctrl_w_K(self, function):
        self.normal('f|izz')
        self.feed('<C-w>K')
        function.assert_called_once_with(self.view.window())

    @unittest.mock.patch('NeoVintageous.nv.window._move_active_view_to_far_right')
    def test_ctrl_w_L(self, function):
        self.normal('f|izz')
        self.feed('<C-w>L')
        function.assert_called_once_with(self.view.window())

    @unittest.mock_commands('focus_neighboring_group')
    def test_ctrl_w_W(self):
        self.normal('f|izz')
        self.feed('<C-w>W')
        self.assertRunCommand('focus_neighboring_group', {'forward': False})

    @unittest.mock.patch('NeoVintageous.nv.window._close_active_view')
    def test_ctrl_w_c(self, function):
        self.normal('f|izz')
        self.feed('<C-w>c')
        function.assert_called_once_with(self.view.window())

    @unittest.mock.patch('NeoVintageous.nv.window.make_all_groups_same_size')
    def test_ctrl_w_equal(self, function):
        self.normal('f|izz')
        self.feed('<C-w>=')
        function.assert_called_once_with(self.view.window())

    @unittest.mock.patch('NeoVintageous.nv.window._increase_group_width')
    def test_ctrl_w_gt(self, function):
        self.normal('f|izz')
        self.feed('<C-w>>')
        function.assert_called_once_with(self.view.window(), 1)

    @unittest.mock.patch('NeoVintageous.nv.window._focus_group_left')
    def test_ctrl_w_h(self, function):
        self.normal('f|izz')
        self.feed('<C-w>h')
        function.assert_called_once_with(self.view.window(), 1)

    @unittest.mock.patch('NeoVintageous.nv.window._focus_group_below')
    def test_ctrl_w_j(self, function):
        self.normal('f|izz')
        self.feed('<C-w>j')
        function.assert_called_once_with(self.view.window(), 1)

    @unittest.mock.patch('NeoVintageous.nv.window._focus_group_above')
    def test_ctrl_w_k(self, function):
        self.normal('f|izz')
        self.feed('<C-w>k')
        function.assert_called_once_with(self.view.window(), 1)

    @unittest.mock.patch('NeoVintageous.nv.window._focus_group_right')
    def test_ctrl_w_l(self, function):
        self.normal('f|izz')
        self.feed('<C-w>l')
        function.assert_called_once_with(self.view.window(), 1)

    @unittest.mock.patch('NeoVintageous.nv.window._decrease_group_width')
    def test_ctrl_w_lt(self, function):
        self.normal('f|izz')
        self.feed('<C-w><lt>')
        function.assert_called_once_with(self.view.window(), 1)

    @unittest.mock.patch('NeoVintageous.nv.window._decrease_group_height')
    def test_ctrl_w_dash(self, function):
        self.normal('f|izz')
        self.feed('<C-w>-')
        function.assert_called_once_with(self.view.window(), 1)

    @unittest.mock_commands('create_pane')
    def test_ctrl_w_n(self):
        self.normal('f|izz')
        for feed in ('<C-w>n', '<C-w><C-n>', ':new'):
            self.feed(feed)
        self.assertRunCommand('create_pane', {'direction': 'down', 'give_focus': True}, count=3)

    @unittest.mock.patch('NeoVintageous.nv.window._close_all_other_views')
    def test_ctrl_w_o(self, function):
        self.normal('f|izz')
        self.feed('<C-w>o')
        function.assert_called_once_with(self.view.window())

    @unittest.mock.patch('NeoVintageous.nv.window._set_group_width')
    def test_ctrl_w_bar(self, function):
        self.normal('f|izz')
        self.feed('<C-w><bar>')
        function.assert_called_once_with(self.view.window(), 1)

    @unittest.mock.patch('NeoVintageous.nv.window._increase_group_height')
    def test_ctrl_w_plus(self, function):
        self.normal('f|izz')
        self.feed('<C-w>+')
        function.assert_called_once_with(self.view.window(), 1)

    @unittest.mock.patch('NeoVintageous.nv.window.window_quit_view')
    def test_ctrl_w_q(self, function):
        self.normal('f|izz')
        self.feed('<C-w>q')
        function.assert_called_once_with(self.view.window())

    @unittest.mock_commands('clone_file_to_pane')
    def test_ctrl_w_s(self):
        self.normal('f|izz')
        for feed in ('<C-w>s', '<C-w>S', '<C-w><C-s>', ':split'):
            self.feed(feed)
        self.assertRunCommand('clone_file_to_pane', {'direction': 'down'}, count=4)

    @unittest.mock.patch('NeoVintageous.nv.window._focus_group_top_left')
    def test_ctrl_w_t(self, function):
        self.normal('f|izz')
        self.feed('<C-w>t')
        function.assert_called_once_with(self.view.window())

    @unittest.mock.patch('NeoVintageous.nv.window._set_group_height')
    def test_ctrl_w__(self, function):
        self.normal('f|izz')
        self.feed('<C-w>_')
        function.assert_called_once_with(self.view.window(), 1)

    @unittest.mock_commands('clone_file_to_pane')
    def test_ctrl_w_v(self):
        self.normal('f|izz')
        for feed in ('<C-w>v', '<C-w><C-v>', ':vsplit'):
            self.feed(feed)
        self.assertRunCommand('clone_file_to_pane', {'direction': 'right'}, count=3)

    @unittest.mock_commands('focus_neighboring_group')
    def test_ctrl_w_w(self):
        self.normal('f|izz')
        for feed in ('<C-w>w', '<C-w><C-w>'):
            self.feed(feed)
        self.assertRunCommand('focus_neighboring_group', {'forward': True}, count=2)

    @unittest.mock.patch('NeoVintageous.nv.window._exchange_view_by_count')
    def test_ctrl_w_x(self, function):
        self.normal('f|izz')
        self.feed('<C-w>x')
        function.assert_called_once_with(self.view.window(), 1)

    @unittest.mock_commands('goto_definition', 'carry_file_to_pane')
    def test_ctrl_w_right_bracket(self):
        self.normal('f|izz')
        self.feed('<C-w>]')
        self.assertRunCommand('goto_definition', {'side_by_side': True})
        self.assertRunCommand('carry_file_to_pane', {'direction': 'right'})

    @unittest.mock.patch('sublime.Window.open_file')
    @unittest.mock.patch('NeoVintageous.nv.window.get_alternate_file_register')
    @unittest.mock_commands('create_pane')
    def test_ctrl_w_hat(self, alternate_file, opener):
        alternate_file.return_value = '/tmp/buzz.txt'
        self.normal('f|izz')
        for feed in ('<C-w>^', '<C-w><C-6>'):
            self.feed(feed)
            opener.assert_called_with('/tmp/buzz.txt', FORCE_GROUP)
        self.assertRunCommand('create_pane', {'direction': 'down', 'give_focus': True}, count=2)
