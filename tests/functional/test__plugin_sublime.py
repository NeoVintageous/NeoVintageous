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


class TestSublime(unittest.FunctionalTestCase):

    def assertBuiltInCommand(self, command: str, args: dict = None) -> None:
        self.assertRunCommand(command, {} if args is None else args)

    @unittest.mock_commands('prompt_select_workspace')
    def test_ctrl_alt_p_should_prompt_select_workspace(self):
        self.eq('|fizz', 'n_<C-M-p>', '|fizz')
        self.assertBuiltInCommand('prompt_select_workspace')

    @unittest.mock_commands('focus_side_bar')
    def test_ctrl_o_should_focus_side_bar(self):
        self.eq('|fizz', 'n_<C-0>', '|fizz')
        self.assertBuiltInCommand('focus_side_bar')

    @unittest.mock_commands('focus_group')
    def test_ctrl_number_should_focus_group(self):
        for number in range(1, 9):
            # F6 is toggle spell check
            if number == 6:
                continue
            self.eq('|fizz', 'n_<C-%s>' % str(number), '|fizz')
            self.assertBuiltInCommand('focus_group', {'group': number - 1})

    def _test_focus_group(self, number: int):
        self.eq('|fizz', 'n_<C-%s>' % str(number), '|fizz')
        self.assertBuiltInCommand('focus_group', {'group': number - 1})

    @unittest.mock_commands('toggle_side_bar')
    def test_ctrl_k_ctrl_b_should_toggle_side_bar(self):
        self.normal('|fizz')
        self.feed('<C-k>')
        self.feed('<C-b>')
        self.assertNormal('|fizz')
        self.assertBuiltInCommand('toggle_side_bar')

    @unittest.mock_commands('show_overlay')
    def test_ctrl_p_should_show_files_overlay(self):
        self.eq('|fizz', 'n_<C-p>', '|fizz')
        self.assertBuiltInCommand('show_overlay', {'overlay': 'goto', 'show_files': True})

    @unittest.mock_commands('build')
    def test_ctrl_B_should_build(self):
        self.eq('|fizz', 'n_<C-B>', '|fizz')
        self.assertBuiltInCommand('build', {'select': True})

    @unittest.mock_commands('show_panel')
    def test_ctrl_F_should_show_find_in_files_panel(self):
        self.eq('|fizz', 'n_<C-F>', '|fizz')
        self.assertBuiltInCommand('show_panel', {'panel': 'find_in_files'})

    @unittest.mock_commands('show_overlay')
    def test_ctrl_P_should_show_command_palette(self):
        self.eq('|fizz', 'n_<C-P>', '|fizz')
        self.assertBuiltInCommand('show_overlay', {'overlay': 'command_palette'})

    @unittest.mock_commands('next_bookmark')
    def test_f2_should_goto_next_bookmark(self):
        self.eq('|fizz', 'n_<F2>', '|fizz')
        self.assertBuiltInCommand('next_bookmark')

    @unittest.mock_commands('find_next')
    def test_f3_should_find_next(self):
        self.eq('|fizz', 'n_<F3>', '|fizz')
        self.assertBuiltInCommand('find_next')

    @unittest.mock_commands('next_result')
    def test_f4_should_goto_next_result(self):
        self.eq('|fizz', 'n_<F4>', '|fizz')
        self.assertBuiltInCommand('next_result')

    @unittest.mock_commands('toggle_setting')
    def test_f6_should_toggle_spell_check(self):
        self.eq('|fizz', 'n_<F6>', '|fizz')
        self.assertBuiltInCommand('toggle_setting', {'setting': 'spell_check'})

    @unittest.mock_commands('build')
    def test_f7_should_build(self):
        self.eq('|fizz', 'n_<F7>', '|fizz')
        self.assertBuiltInCommand('build')

    @unittest.mock_commands('sort_lines')
    def test_f9_should_build(self):
        self.eq('|fizz', 'n_<F9>', '|fizz')
        self.assertBuiltInCommand('sort_lines', {'case_sensitive': False})

    @unittest.mock_commands('toggle_full_screen')
    def test_f11_should_toggle_full_screen(self):
        self.eq('|fizz', 'n_<F11>', '|fizz')
        self.assertBuiltInCommand('toggle_full_screen')

    @unittest.mock_commands('goto_definition')
    def test_f12_should_goto_definition(self):
        self.eq('|fizz', 'n_<F12>', '|fizz')
        self.assertBuiltInCommand('goto_definition')

    @unittest.mock_commands('toggle_bookmark')
    def test_ctrl_f2_should_toggle_bookmark(self):
        self.eq('|fizz', 'n_<C-F2>', '|fizz')
        self.assertBuiltInCommand('toggle_bookmark')

    @unittest.mock_commands('show_overlay')
    def test_ctrl_f12_should_show_overlay(self):
        self.eq('|fizz', 'n_<C-F12>', '|fizz')
        self.assertBuiltInCommand('show_overlay', {
            'overlay': 'goto',
            'text': '@'
        })

    @unittest.mock_commands('prev_bookmark')
    def test_shift_f2_should_prev_bookmark(self):
        self.eq('|fizz', 'n_<S-f2>', '|fizz')
        self.assertBuiltInCommand('prev_bookmark')

    @unittest.mock_commands('prev_result')
    def test_shift_f4_should_prev_result(self):
        self.eq('|fizz', 'n_<S-f4>', '|fizz')
        self.assertBuiltInCommand('prev_result')

    @unittest.mock_commands('toggle_distraction_free')
    def test_shift_f11_should_toggle_distraction_free(self):
        self.eq('|fizz', 'n_<S-f11>', '|fizz')
        self.assertBuiltInCommand('toggle_distraction_free')

    @unittest.mock_commands('clear_bookmarks')
    def test_ctrl_shift_f2_should_clear_bookmarks(self):
        self.eq('|fizz', 'n_<C-S-f2>', '|fizz')
        self.assertBuiltInCommand('clear_bookmarks')

    @unittest.mock_commands('goto_symbol_in_project')
    def test_ctrl_shift_f12_should_goto_symbol_in_project(self):
        self.eq('|fizz', 'n_<C-S-f12>', '|fizz')
        self.assertBuiltInCommand('goto_symbol_in_project')
