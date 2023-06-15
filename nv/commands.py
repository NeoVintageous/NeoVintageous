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

import logging
import re
import textwrap
import time
import webbrowser

from sublime import CLASS_EMPTY_LINE
from sublime import CLASS_WORD_START
from sublime import ENCODED_POSITION
from sublime import LITERAL
from sublime import MONOSPACE_FONT
from sublime import Region
from sublime import version
from sublime_plugin import TextCommand
from sublime_plugin import WindowCommand

from NeoVintageous.nv import macros
from NeoVintageous.nv.cmdline import Cmdline
from NeoVintageous.nv.ex.completions import insert_best_cmdline_completion
from NeoVintageous.nv.ex.completions import on_change_cmdline_completion_prefix
from NeoVintageous.nv.ex.completions import reset_cmdline_completion_state
from NeoVintageous.nv.ex_cmds import do_ex_cmd_edit_wrap
from NeoVintageous.nv.ex_cmds import do_ex_cmdline
from NeoVintageous.nv.ex_cmds import do_ex_command
from NeoVintageous.nv.feed_key import FeedKeyHandler
from NeoVintageous.nv.goto import GotoView
from NeoVintageous.nv.goto import get_linewise_non_blank_target
from NeoVintageous.nv.history import history_get
from NeoVintageous.nv.history import history_get_type
from NeoVintageous.nv.history import history_len
from NeoVintageous.nv.history import history_update
from NeoVintageous.nv.jumplist import jumplist_updater
from NeoVintageous.nv.macros import add_macro_step
from NeoVintageous.nv.marks import get_mark
from NeoVintageous.nv.marks import set_mark
from NeoVintageous.nv.paste import pad_visual_block_paste_contents
from NeoVintageous.nv.paste import resolve_paste_items_with_view_sel
from NeoVintageous.nv.polyfill import set_selection
from NeoVintageous.nv.polyfill import spell_select
from NeoVintageous.nv.polyfill import split_by_newlines
from NeoVintageous.nv.polyfill import toggle_side_bar
from NeoVintageous.nv.process_notation import ProcessNotationHandler
from NeoVintageous.nv.rc import open_rc
from NeoVintageous.nv.rc import reload_rc
from NeoVintageous.nv.registers import get_alternate_file_register
from NeoVintageous.nv.registers import registers_get_for_paste
from NeoVintageous.nv.registers import registers_op_change
from NeoVintageous.nv.registers import registers_op_delete
from NeoVintageous.nv.registers import registers_op_yank
from NeoVintageous.nv.search import add_search_highlighting
from NeoVintageous.nv.search import clear_search_highlighting
from NeoVintageous.nv.search import find_search_occurrences
from NeoVintageous.nv.search import find_word_search_occurrences
from NeoVintageous.nv.search import get_search_occurrences
from NeoVintageous.nv.search import process_search_pattern
from NeoVintageous.nv.search import process_word_search_pattern
from NeoVintageous.nv.settings import append_sequence
from NeoVintageous.nv.settings import get_count
from NeoVintageous.nv.settings import get_glue_until_normal_mode
from NeoVintageous.nv.settings import get_last_search_pattern
from NeoVintageous.nv.settings import get_last_search_pattern_command
from NeoVintageous.nv.settings import get_mode
from NeoVintageous.nv.settings import get_normal_insert_count
from NeoVintageous.nv.settings import get_repeat_data
from NeoVintageous.nv.settings import get_sequence
from NeoVintageous.nv.settings import get_setting
from NeoVintageous.nv.settings import get_xpos
from NeoVintageous.nv.settings import is_processing_notation
from NeoVintageous.nv.settings import set_glue_until_normal_mode
from NeoVintageous.nv.settings import set_last_char_search
from NeoVintageous.nv.settings import set_last_search_pattern
from NeoVintageous.nv.settings import set_mode
from NeoVintageous.nv.settings import set_normal_insert_count
from NeoVintageous.nv.settings import set_repeat_data
from NeoVintageous.nv.settings import set_reset_during_init
from NeoVintageous.nv.settings import set_xpos
from NeoVintageous.nv.settings import toggle_ctrl_keys
from NeoVintageous.nv.settings import toggle_super_keys
from NeoVintageous.nv.state import evaluate_state
from NeoVintageous.nv.state import reset_command_data
from NeoVintageous.nv.state import set_motion
from NeoVintageous.nv.state import update_status_line
from NeoVintageous.nv.ui import ui_bell
from NeoVintageous.nv.ui import ui_highlight_yank
from NeoVintageous.nv.ui import ui_highlight_yank_clear
from NeoVintageous.nv.utils import VisualBlockSelection
from NeoVintageous.nv.utils import calculate_xpos
from NeoVintageous.nv.utils import extract_file_name
from NeoVintageous.nv.utils import extract_url
from NeoVintageous.nv.utils import fix_eol_cursor
from NeoVintageous.nv.utils import fixup_eof
from NeoVintageous.nv.utils import fold
from NeoVintageous.nv.utils import fold_all
from NeoVintageous.nv.utils import folded_rows
from NeoVintageous.nv.utils import get_insertion_point_at_a
from NeoVintageous.nv.utils import get_insertion_point_at_b
from NeoVintageous.nv.utils import get_option_scroll
from NeoVintageous.nv.utils import get_previous_selection
from NeoVintageous.nv.utils import get_scroll_down_target_pt
from NeoVintageous.nv.utils import get_scroll_up_target_pt
from NeoVintageous.nv.utils import get_string_under_cursor
from NeoVintageous.nv.utils import hide_panel
from NeoVintageous.nv.utils import highest_visible_pt
from NeoVintageous.nv.utils import highlow_visible_rows
from NeoVintageous.nv.utils import is_help_view
from NeoVintageous.nv.utils import is_linewise_operation
from NeoVintageous.nv.utils import is_view
from NeoVintageous.nv.utils import lowest_visible_pt
from NeoVintageous.nv.utils import new_inclusive_region
from NeoVintageous.nv.utils import next_blank
from NeoVintageous.nv.utils import next_non_blank
from NeoVintageous.nv.utils import next_non_folded_pt
from NeoVintageous.nv.utils import prev_blank
from NeoVintageous.nv.utils import prev_non_blank
from NeoVintageous.nv.utils import prev_non_ws
from NeoVintageous.nv.utils import previous_non_folded_pt
from NeoVintageous.nv.utils import regions_transform_extend_to_line_count
from NeoVintageous.nv.utils import regions_transform_to_first_non_blank
from NeoVintageous.nv.utils import regions_transformer
from NeoVintageous.nv.utils import regions_transformer_indexed
from NeoVintageous.nv.utils import regions_transformer_reversed
from NeoVintageous.nv.utils import replace_line
from NeoVintageous.nv.utils import requires_motion
from NeoVintageous.nv.utils import resolve_internal_normal_target
from NeoVintageous.nv.utils import resolve_normal_target
from NeoVintageous.nv.utils import resolve_visual_block_begin
from NeoVintageous.nv.utils import resolve_visual_block_reverse
from NeoVintageous.nv.utils import resolve_visual_block_target
from NeoVintageous.nv.utils import resolve_visual_line_target
from NeoVintageous.nv.utils import resolve_visual_target
from NeoVintageous.nv.utils import restore_visual_repeat_data
from NeoVintageous.nv.utils import row_at
from NeoVintageous.nv.utils import save_previous_selection
from NeoVintageous.nv.utils import scroll_horizontally
from NeoVintageous.nv.utils import scroll_viewport_position
from NeoVintageous.nv.utils import sel_observer
from NeoVintageous.nv.utils import sel_to_lines
from NeoVintageous.nv.utils import should_motion_apply_op_transformer
from NeoVintageous.nv.utils import show_if_not_visible
from NeoVintageous.nv.utils import spell_file_add_word
from NeoVintageous.nv.utils import spell_file_remove_word
from NeoVintageous.nv.utils import translate_char
from NeoVintageous.nv.utils import unfold
from NeoVintageous.nv.utils import unfold_all
from NeoVintageous.nv.utils import update_xpos
from NeoVintageous.nv.vi.cmd_defs import ViSearchBackwardImpl
from NeoVintageous.nv.vi.cmd_defs import ViSearchForwardImpl
from NeoVintageous.nv.vi.search import find_in_range
from NeoVintageous.nv.vi.search import find_wrapping
from NeoVintageous.nv.vi.search import reverse_find_wrapping
from NeoVintageous.nv.vi.search import reverse_search
from NeoVintageous.nv.vi.text_objects import big_word_end_reverse
from NeoVintageous.nv.vi.text_objects import big_word_reverse
from NeoVintageous.nv.vi.text_objects import find_next_item_match_pt
from NeoVintageous.nv.vi.text_objects import find_sentences_backward
from NeoVintageous.nv.vi.text_objects import find_sentences_forward
from NeoVintageous.nv.vi.text_objects import get_text_object_region
from NeoVintageous.nv.vi.text_objects import word_end_reverse
from NeoVintageous.nv.vi.text_objects import word_reverse
from NeoVintageous.nv.vi.units import big_word_ends
from NeoVintageous.nv.vi.units import big_word_starts
from NeoVintageous.nv.vi.units import inner_lines
from NeoVintageous.nv.vi.units import lines
from NeoVintageous.nv.vi.units import next_paragraph_start
from NeoVintageous.nv.vi.units import prev_paragraph_start
from NeoVintageous.nv.vi.units import word_ends
from NeoVintageous.nv.vi.units import word_starts
from NeoVintageous.nv.vim import EOF
from NeoVintageous.nv.vim import INSERT
from NeoVintageous.nv.vim import INTERNAL_NORMAL
from NeoVintageous.nv.vim import NORMAL
from NeoVintageous.nv.vim import REPLACE
from NeoVintageous.nv.vim import SELECT
from NeoVintageous.nv.vim import UNKNOWN
from NeoVintageous.nv.vim import VISUAL
from NeoVintageous.nv.vim import VISUAL_BLOCK
from NeoVintageous.nv.vim import VISUAL_LINE
from NeoVintageous.nv.vim import clean_views
from NeoVintageous.nv.vim import enter_insert_mode
from NeoVintageous.nv.vim import enter_normal_mode
from NeoVintageous.nv.vim import enter_visual_block_mode
from NeoVintageous.nv.vim import enter_visual_line_mode
from NeoVintageous.nv.vim import enter_visual_mode
from NeoVintageous.nv.vim import is_visual_mode
from NeoVintageous.nv.vim import reset_status_line
from NeoVintageous.nv.vim import run_motion
from NeoVintageous.nv.vim import status_message
from NeoVintageous.nv.window import window_control
from NeoVintageous.nv.window import window_open_file
from NeoVintageous.nv.window import window_tab_control


__all__ = [
    'Neovintageous',
    'SequenceCommand',
    'nv_enter_insert_mode',
    'nv_enter_normal_mode',
    'nv_enter_replace_mode',
    'nv_enter_select_mode',
    'nv_enter_visual_block_mode',
    'nv_enter_visual_line_mode',
    'nv_enter_visual_mode',
    'nv_cmdline',
    'nv_cmdline_feed_key',
    'nv_ex_cmd_edit_wrap',
    'nv_feed_key',
    'nv_process_notation',
    'nv_run_cmds',
    'nv_view',
    'nv_vi_a',
    'nv_vi_at',
    'nv_vi_b',
    'nv_vi_backtick',
    'nv_vi_bar',
    'nv_vi_big_a',
    'nv_vi_big_b',
    'nv_vi_big_c',
    'nv_vi_big_d',
    'nv_vi_big_e',
    'nv_vi_big_g',
    'nv_vi_big_h',
    'nv_vi_big_i',
    'nv_vi_big_j',
    'nv_vi_big_l',
    'nv_vi_big_m',
    'nv_vi_big_o',
    'nv_vi_big_s',
    'nv_vi_big_w',
    'nv_vi_big_x',
    'nv_vi_big_z_big_q',
    'nv_vi_big_z_big_z',
    'nv_vi_c',
    'nv_vi_cc',
    'nv_vi_ctrl_b',
    'nv_vi_ctrl_d',
    'nv_vi_ctrl_e',
    'nv_vi_ctrl_f',
    'nv_vi_ctrl_g',
    'nv_vi_ctrl_hat',
    'nv_vi_ctrl_r',
    'nv_vi_ctrl_right_square_bracket',
    'nv_vi_ctrl_u',
    'nv_vi_ctrl_w',
    'nv_vi_ctrl_x_ctrl_l',
    'nv_vi_ctrl_y',
    'nv_vi_d',
    'nv_vi_dd',
    'nv_vi_dollar',
    'nv_vi_dot',
    'nv_vi_e',
    'nv_vi_enter',
    'nv_vi_equal',
    'nv_vi_equal_equal',
    'nv_vi_find_in_line',
    'nv_vi_g',
    'nv_vi_g__',
    'nv_vi_g_big_e',
    'nv_vi_g_big_h',
    'nv_vi_g_big_t',
    'nv_vi_g_big_u',
    'nv_vi_g_big_u_big_u',
    'nv_vi_g_tilde',
    'nv_vi_g_tilde_g_tilde',
    'nv_vi_ga',
    'nv_vi_ge',
    'nv_vi_gg',
    'nv_vi_gj',
    'nv_vi_gk',
    'nv_vi_gm',
    'nv_vi_go_to_symbol',
    'nv_vi_gq',
    'nv_vi_greater_than',
    'nv_vi_greater_than_greater_than',
    'nv_vi_gt',
    'nv_vi_gu',
    'nv_vi_guu',
    'nv_vi_gv',
    'nv_vi_gx',
    'nv_vi_h',
    'nv_vi_hat',
    'nv_vi_j',
    'nv_vi_k',
    'nv_vi_l',
    'nv_vi_left_brace',
    'nv_vi_left_paren',
    'nv_vi_left_square_bracket',
    'nv_vi_less_than',
    'nv_vi_less_than_less_than',
    'nv_vi_m',
    'nv_vi_minus',
    'nv_vi_modify_numbers',
    'nv_vi_o',
    'nv_vi_octothorp',
    'nv_vi_paste',
    'nv_vi_percent',
    'nv_vi_q',
    'nv_vi_question_mark',
    'nv_vi_question_mark_impl',
    'nv_vi_quote',
    'nv_vi_r',
    'nv_vi_repeat_buffer_search',
    'nv_vi_reverse_find_in_line',
    'nv_vi_right_brace',
    'nv_vi_right_paren',
    'nv_vi_right_square_bracket',
    'nv_vi_s',
    'nv_vi_search',
    'nv_vi_select_big_j',
    'nv_vi_select_j',
    'nv_vi_select_k',
    'nv_vi_select_text_object',
    'nv_vi_shift_enter',
    'nv_vi_slash',
    'nv_vi_slash_impl',
    'nv_vi_star',
    'nv_vi_tilde',
    'nv_vi_u',
    'nv_vi_underscore',
    'nv_vi_visual_big_u',
    'nv_vi_visual_o',
    'nv_vi_visual_u',
    'nv_vi_w',
    'nv_vi_x',
    'nv_vi_y',
    'nv_vi_yy',
    'nv_vi_z',
    'nv_vi_z_enter',
    'nv_vi_z_minus',
    'nv_vi_zero',
    'nv_vi_zz'
]


_log = logging.getLogger(__name__)


class nv_cmdline_feed_key(TextCommand):

    LAST_HISTORY_ITEM_INDEX = None

    def run(self, edit, key):
        if self.view.size() == 0:
            raise RuntimeError('expected a non-empty command-line')

        keys_allow_empty = ('<up>', '<C-n>', '<down>', '<C-p>', '<C-c>', '<C-[>', '<tab>', '<S-tab>')
        if self.view.size() == 1 and key not in keys_allow_empty:
            return

        if key in ('<tab>', '<S-tab>'):
            insert_best_cmdline_completion(self.view, edit, forward=(True if key == '<tab>' else False))

        elif key in ('<up>', '<C-p>'):
            # Recall older command-line from history, whose beginning matches
            # the current command-line.
            self._next_history(edit, backwards=True)

        elif key in ('<down>', '<C-n>'):
            # Recall more recent command-line from history, whose beginning
            # matches the current command-line.
            self._next_history(edit, backwards=False)

        elif key in ('<C-b>', '<home>'):
            # Cursor to beginning of command-line.
            set_selection(self.view, 1)

        elif key in ('<C-c>', '<C-[>'):
            # Quit command-line without executing.
            hide_panel(self.view.window())

        elif key in ('<C-e>', '<end>'):
            # Cursor to end of command-line.
            set_selection(self.view, self.view.size())

        elif key == '<C-h>':
            # Delete the character in front of the cursor.
            pt_end = self.view.sel()[0].b
            pt_begin = pt_end - 1
            self.view.erase(edit, Region(pt_begin, pt_end))

        elif key == '<C-u>':
            # Remove all characters between the cursor position and the
            # beginning of the line.
            self.view.erase(edit, Region(1, self.view.sel()[0].end()))

        elif key == '<C-w>':
            # Delete the |word| before the cursor.
            word_region = self.view.word(self.view.sel()[0].begin())
            word_region = self.view.expand_by_class(self.view.sel()[0].begin(), CLASS_WORD_START)
            word_start_pt = word_region.begin()
            caret_end_pt = self.view.sel()[0].end()
            word_part_region = Region(max(word_start_pt, 1), caret_end_pt)
            self.view.erase(edit, word_part_region)
        else:
            raise NotImplementedError('unknown key')

    def _next_history(self, edit, backwards: bool) -> None:
        if self.view.size() == 0:
            raise RuntimeError('expected a non-empty command-line')

        firstc = self.view.substr(0)
        if not history_get_type(firstc):
            raise RuntimeError('expected a valid command-line')

        if nv_cmdline_feed_key.LAST_HISTORY_ITEM_INDEX is None:
            nv_cmdline_feed_key.LAST_HISTORY_ITEM_INDEX = -1 if backwards else 0
        else:
            nv_cmdline_feed_key.LAST_HISTORY_ITEM_INDEX += -1 if backwards else 1

        count = history_len(firstc)
        if count == 0:
            nv_cmdline_feed_key.LAST_HISTORY_ITEM_INDEX = None

            return ui_bell()

        if abs(nv_cmdline_feed_key.LAST_HISTORY_ITEM_INDEX) > count:
            nv_cmdline_feed_key.LAST_HISTORY_ITEM_INDEX = -count

            return ui_bell()

        if nv_cmdline_feed_key.LAST_HISTORY_ITEM_INDEX >= 0:
            nv_cmdline_feed_key.LAST_HISTORY_ITEM_INDEX = 0

            if self.view.size() > 1:
                return self.view.erase(edit, Region(1, self.view.size()))
            else:
                return ui_bell()

        if self.view.size() > 1:
            self.view.erase(edit, Region(1, self.view.size()))

        item = history_get(firstc, nv_cmdline_feed_key.LAST_HISTORY_ITEM_INDEX)
        if item:
            self.view.insert(edit, 1, item)

    @staticmethod
    def reset_last_history_index() -> None:
        nv_cmdline_feed_key.LAST_HISTORY_ITEM_INDEX = None


class nv_run_cmds(TextCommand):

    def run(self, edit, commands):
        # Run a list of commands one after the other.
        #
        # Args:
        #   commands (list): A list of commands.
        for cmd, args in commands:
            self.view.run_command(cmd, args)


class nv_feed_key(WindowCommand):

    # TODO refactor: rename repeat_count -> count
    def run(self, key, repeat_count=None, do_eval=True, check_user_mappings=True):
        start_time = time.time()

        try:
            FeedKeyHandler(
                self.window.active_view(),
                key,
                repeat_count,
                do_eval,
                check_user_mappings).handle()
        except Exception as e:
            print('NeoVintageous: An error occurred:')
            _log.exception(e)
            clean_views()

        _log.info(
            'key completed in %s ms', '{:.2f}'
            .format((time.time() - start_time) * 1000))


class nv_process_notation(WindowCommand):

    # TODO refactor: rename repeat_count -> count
    def run(self, keys, repeat_count=None, check_user_mappings=True):
        ProcessNotationHandler(
            self.window.active_view(),
            keys,
            repeat_count,
            check_user_mappings).handle()


class nv_ex_cmd_edit_wrap(TextCommand):

    # This command is required to wrap ex commands that need a Sublime Text edit
    # token. Edit tokens can only be obtained from a TextCommand. Some ex
    # commands don't need an edit token, those commands don't need to be wrapped
    # by a text command.

    def run(self, edit, **kwargs):
        do_ex_cmd_edit_wrap(self, edit, **kwargs)


class nv_cmdline(WindowCommand):

    def is_enabled(self):
        return bool(self.window.active_view())

    def run(self, initial_text=None):
        reset_cmdline_completion_state()
        view = self.window.active_view()
        set_reset_during_init(view, False)
        mode = get_mode(view)

        if initial_text is not None:
            # DEPRECATED The initial_text should NOT contain the leading colon.
            # Previously this was accepted and the colon was stripped  before
            # passing dwn the chain, but calling code should be refactored.
            if len(initial_text) > 0:
                if initial_text[0] == Cmdline.EX:
                    initial_text = initial_text[1:]
                    _log.debug('DEPRECATED cmdline initial text contains leading colon')

        elif is_visual_mode(mode):
            initial_text = "'<,'>"
        else:
            initial_text = ""

        self._cmdline = Cmdline(
            view,
            Cmdline.EX,
            self.on_done,
            self.on_change,
            self.on_cancel
        )

        self._cmdline.prompt(initial_text)

    def on_change(self, cmdline):
        on_change_cmdline_completion_prefix(self.window, Cmdline.EX + cmdline)

    def on_done(self, cmdline):
        nv_cmdline_feed_key.reset_last_history_index()
        history_update(Cmdline.EX + cmdline)
        do_ex_cmdline(self.window, Cmdline.EX + cmdline)

    def on_cancel(self):
        nv_cmdline_feed_key.reset_last_history_index()


class nv_view(TextCommand):

    def run(self, edit, action, **kwargs):
        if action == 'insert':
            self.view.insert(edit, 0, **kwargs)
        elif action == 'replace_line':
            replace_line(self.view, edit, **kwargs)


class Neovintageous(WindowCommand):

    def run(self, action, **kwargs):
        if action == 'open_rc_file':
            open_rc(self.window)
        elif action == 'reload_rc_file':
            reload_rc()
        elif action == 'toggle_ctrl_keys':
            toggle_ctrl_keys()
        elif action == 'toggle_side_bar':
            toggle_side_bar(self.window)
        elif action == 'toggle_super_keys':
            toggle_super_keys()


# DEPRECATED Use nv_run_cmds instead
class SequenceCommand(TextCommand):

    def run(self, edit, commands):
        # Run a list of commands one after the other.
        #
        # Args:
        #   commands (list): A list of commands.
        for cmd, args in commands:
            self.view.run_command(cmd, args)


class nv_vi_g_big_u(TextCommand):

    def run(self, edit, mode=None, count=1, motion=None):
        def f(view, s):
            view.replace(edit, s, view.substr(s).upper())
            # Reverse region so that entering NORMAL mode collapses selection.
            return Region(s.b, s.a)

        if mode == INTERNAL_NORMAL:
            requires_motion(motion)
            with sel_observer(self.view) as observer:
                run_motion(self.view, motion)
                if observer.has_sel_changed():
                    regions_transformer(self.view, f)
        else:
            regions_transformer(self.view, f)

        enter_normal_mode(self.view, mode)


class nv_vi_gu(TextCommand):

    def run(self, edit, mode=None, count=1, motion=None):
        def f(view, s):
            view.replace(edit, s, view.substr(s).lower())
            # Reverse region so that entering NORMAL mode collapses selection.
            return Region(s.b, s.a)

        if mode == INTERNAL_NORMAL:
            requires_motion(motion)
            with sel_observer(self.view) as observer:
                run_motion(self.view, motion)
                if observer.has_sel_changed():
                    regions_transformer(self.view, f)
        else:
            regions_transformer(self.view, f)

        enter_normal_mode(self.view, mode)


class nv_vi_gq(TextCommand):

    def run(self, edit, mode=None, count=1, motion=None, linewise=False):
        def _wrap_lines(view):
            if view.settings().get('WrapPlus.include_line_endings') is not None:
                cmd = 'wrap_lines_plus'
            else:
                cmd = 'wrap_lines'

            view.run_command(cmd)

        def reverse(view, s):
            return Region(s.end(), s.begin())

        def shrink(view, s):
            if s.b > s.a and view.substr(s.b - 1) == '\n':
                s.b -= 1
            elif s.b < s.a and view.substr(s.a - 1) == '\n':
                s.a -= 1

            return s

        if mode in (VISUAL, VISUAL_LINE):
            sel = tuple(self.view.sel())
            regions_transformer(self.view, shrink)
            regions_transformer(self.view, reverse)
            _wrap_lines(self.view)
            self.view.sel().clear()
            for s in sel:
                # Cursors should move to the first non-blank character of the line.
                line = self.view.line(s.begin())
                first_non_ws_char_region = self.view.find('[^\\s]', line.begin())
                self.view.sel().add(first_non_ws_char_region.begin())

        elif mode == INTERNAL_NORMAL:
            if motion is None and not linewise:
                raise ValueError('motion is required or must be linewise')

            with sel_observer(self.view) as observer:
                if motion:
                    run_motion(self.view, motion)
                else:
                    regions_transform_extend_to_line_count(self.view, count)

                if observer.has_sel_changed():
                    _wrap_lines(self.view)

                    def f(view, s):
                        line = view.line(s.b)

                        return Region(next_non_blank(view, line.a))

                    regions_transformer(self.view, f)

        enter_normal_mode(self.view, mode)


class nv_vi_u(WindowCommand):

    def run(self, mode=None, count=1, **kwargs):
        self.view = self.window.active_view()

        change_count = self.view.change_count()

        for i in range(count):
            self.view.run_command('undo')

        if self.view.change_count() == change_count:
            return ui_bell('Already at oldest change')

        if self.view.has_non_empty_selection_region():
            def reverse(view, s):
                return Region(s.end(), s.begin())

            regions_transformer(self.view, reverse)
            enter_normal_mode(self.window, VISUAL)  # TODO Review: Why explicitly from VISUAL mode?

        # Ensure regions are clear of any highlighted yanks. For example, ddyyu
        # would otherwise show the restored line as previously highlighted.
        ui_highlight_yank_clear(self.view)


class nv_vi_ctrl_r(WindowCommand):

    def run(self, mode=None, count=1, **kwargs):
        self.view = self.window.active_view()

        change_count = self.view.change_count()

        for i in range(count):
            self.view.run_command('redo')

        if self.view.change_count() == change_count:
            return ui_bell('Already at newest change')

        # Fix EOL issue.
        # See https://github.com/SublimeTextIssues/Core/issues/2121.
        def fixup_eol(view, s):
            pt = s.b
            char = view.substr(pt)
            if (char == '\n' and not view.line(pt).empty()):
                return Region(pt - 1)

            if char == EOF and pt == view.size():
                return Region(s.b - 1)

            return s

        regions_transformer(self.view, fixup_eol)


class nv_vi_a(TextCommand):

    def run(self, edit, mode=None, count=1):
        # Abort if the *actual* mode is insert mode. This prevents nv_vi_a from
        # adding spaces between text fragments when used with a count, as in
        # 5aFOO. In that case, we only need to run 'a' the first time, not for
        # every iteration.
        if get_mode(self.view) == INSERT:
            return

        if mode is None:
            raise ValueError('mode required')
        elif mode != INTERNAL_NORMAL:
            return

        def f(view, s):
            if view.substr(s.b) != '\n' and s.b < view.size():
                return Region(s.b + 1)

            return s

        regions_transformer(self.view, f)

        self.view.window().run_command('nv_enter_insert_mode', {
            'mode': mode,
            'count': get_normal_insert_count(self.view)
        })


class nv_vi_c(TextCommand):

    def run(self, edit, mode=None, count=1, motion=None, register=None):
        if mode is None:
            raise ValueError('mode required')

        if mode == INTERNAL_NORMAL:
            requires_motion(motion)

        if motion:
            with sel_observer(self.view) as observer:
                run_motion(self.view, motion)

                if mode == INTERNAL_NORMAL:
                    if should_motion_apply_op_transformer(motion):
                        def f(view, s):
                            if view.substr(s).strip():
                                if s.b > s.a:
                                    pt = prev_non_ws(view, s.b - 1)

                                    return Region(s.a, pt + 1)

                                pt = prev_non_ws(view, s.a - 1)

                                return Region(pt + 1, s.b)

                            return s

                        regions_transformer(self.view, f)

                if not observer.has_sel_changed():
                    enter_insert_mode(self.view, mode)
                    return

            if all(s.empty() for s in self.view.sel()):
                enter_insert_mode(self.view, mode)
                return

        registers_op_change(self.view, register=register, linewise=is_linewise_operation(mode, motion))
        self.view.run_command('right_delete')
        enter_insert_mode(self.view, mode)


class nv_enter_normal_mode(TextCommand):

    def run(self, edit, mode=None, from_init=False):
        self.view.window().run_command('hide_auto_complete')
        self.view.window().run_command('hide_overlay')

        if ((not from_init and (mode == NORMAL) and not get_sequence(self.view)) or not is_view(self.view)):
            # When nv_enter_normal_mode is requested from init_view, we
            # should not hide output panels; hide them only if the user
            # pressed Esc and we're not cancelling partial state data, or if a
            # panel has the focus.
            # XXX: We are assuming that the sequence will always be empty
            #      when we do the check above. Is that so?
            # XXX: The 'not is_view(self.view)' check above seems to be
            #      redundant, since those views should be ignored by
            #      NeoVintageous altogether.
            if len(self.view.sel()) < 2:
                # Don't hide panel if multiple cursors
                if not from_init:
                    hide_panel(self.view.window())

        self.view.settings().set('command_mode', True)
        self.view.settings().set('inverse_caret_state', True)
        self.view.set_overwrite_status(False)  # Exit replace mode.

        set_mode(self.view, NORMAL)

        def f(view, s):
            if mode == INSERT:
                if view.line(s.b).a != s.b:
                    return Region(s.b - 1)

                return Region(s.b)

            elif mode == INTERNAL_NORMAL:
                return Region(s.b)

            elif mode == VISUAL:
                save_previous_selection(view, mode)

                if s.a < s.b:
                    pt = s.b - 1
                    if view.line(pt).empty():
                        return Region(pt)

                    if view.substr(pt) == '\n':
                        pt -= 1

                    return Region(pt)

                return Region(s.b)

            elif mode in (VISUAL_LINE, VISUAL_BLOCK):
                save_previous_selection(view, mode)

                if s.a < s.b:
                    pt = s.b - 1
                    if (view.substr(pt) == '\n') and not view.line(pt).empty():
                        pt -= 1

                    return Region(pt)
                else:
                    return Region(s.b)

            elif mode == SELECT:
                return Region(s.begin())

            return Region(s.a if s.b >= s.a else s.b)

        if mode != UNKNOWN:
            if len(self.view.sel()) > 1 and mode == NORMAL:
                set_selection(self.view, self.view.sel()[0])

            if mode == VISUAL_BLOCK and len(self.view.sel()) > 1:
                save_previous_selection(self.view, mode)
                set_selection(self.view, VisualBlockSelection(self.view).insertion_point_b())
            else:
                regions_transformer(self.view, f)

            clear_search_highlighting(self.view)
            fix_eol_cursor(self.view, mode)

        if get_glue_until_normal_mode(self.view) and not is_processing_notation(self.view):
            if self.view.is_dirty():
                self.view.window().run_command('glue_marked_undo_groups')
                # We're exiting from insert mode or replace mode. Capture
                # the last native command as repeat data.
                repeat_data = get_repeat_data(self.view)
                if repeat_data and len(repeat_data) == 4 and repeat_data[3]:
                    visual_data = repeat_data[3]
                else:
                    visual_data = None

                set_repeat_data(self.view, ('native', self.view.command_history(0)[:2], mode, visual_data))
                # Required here so that the macro gets recorded.
                set_glue_until_normal_mode(self.view, False)
                add_macro_step(self.view, *self.view.command_history(0)[:2])
                add_macro_step(self.view, 'nv_enter_normal_mode', {'mode': mode, 'from_init': from_init})
            else:
                add_macro_step(self.view, 'nv_enter_normal_mode', {'mode': mode, 'from_init': from_init})
                self.view.window().run_command('unmark_undo_groups_for_gluing')
                set_glue_until_normal_mode(self.view, False)

        normal_insert_count = get_normal_insert_count(self.view)
        if mode == INSERT and normal_insert_count > 1:
            set_mode(self.view, INSERT)
            # TODO: Calculate size the view has grown by and place the caret after the newly inserted text.
            sels = list(self.view.sel())
            self.view.sel().clear()
            new_sels = [Region(s.b + 1) if self.view.substr(s.b) != '\n' else s for s in sels]
            self.view.sel().add_all(new_sels)
            times = normal_insert_count - 1
            set_normal_insert_count(self.view, 1)
            self.view.window().run_command('nv_vi_dot', {
                'count': times,
                'mode': mode,
                'repeat_data': get_repeat_data(self.view),
            })
            set_selection(self.view, new_sels)

        update_xpos(self.view)
        reset_status_line(self.view, get_mode(self.view))
        fix_eol_cursor(self.view, get_mode(self.view))

        # When the commands o and O are immediately followed by <Esc>, then if
        # the current line is only whitespace it should be erased, and the xpos
        # offset by 1 to account for transition from INSERT to NORMAL mode.
        if get_setting(self.view, 'clear_auto_indent_on_esc'):
            if mode == INSERT and self.view.is_dirty():
                if self.view.command_history(0)[0] in ('nv_vi_big_o', 'nv_vi_o'):
                    for s in reversed(list(self.view.sel())):
                        line = self.view.line(s.b)
                        line_str = self.view.substr(line)
                        if re.match('^\\s+$', line_str):
                            self.view.erase(edit, line)
                            col = self.view.rowcol(line.b)[1]
                            set_xpos(self.view, col + 1)


class nv_enter_select_mode(TextCommand):

    def run(self, edit, mode=None, count=1):
        set_mode(self.view, SELECT)

        if mode == INTERNAL_NORMAL:
            self.view.window().run_command('find_under_expand')
        elif mode in (VISUAL, VISUAL_LINE):
            self.view.window().run_command('nv_vi_select_j', {'mode': get_mode(self.view)})
        elif mode == VISUAL_BLOCK:
            resolve_visual_block_reverse(self.view)
            enter_normal_mode(self.view.window())

        update_status_line(self.view)


class nv_enter_insert_mode(TextCommand):

    def run(self, edit, mode=None, count=1):
        def f(view, s):
            s.a = s.b = get_insertion_point_at_b(s)

            return s

        regions_transformer(self.view, f)

        self.view.settings().set('inverse_caret_state', False)
        self.view.settings().set('command_mode', False)

        set_mode(self.view, INSERT)
        set_normal_insert_count(self.view, count)
        update_status_line(self.view)


class nv_enter_visual_mode(TextCommand):

    def run(self, edit, mode=None, force=False):
        if get_mode(self.view) == VISUAL and not force:
            enter_normal_mode(self.view, mode)
            return

        if mode == VISUAL_BLOCK:
            visual_block = VisualBlockSelection(self.view)
            visual_block.transform_to_visual()
        else:
            def f(view, s):
                if mode == VISUAL_LINE:
                    return Region(s.a, s.b)
                else:
                    if s.empty() and s.b == view.size():
                        ui_bell()
                        return s

                    # Extending from s.a to s.b because we may be looking at
                    # selections with len>0. For example, if it's been created
                    # using the mouse. Normally, though, the selection will be
                    # empty when we reach here.
                    end = s.b
                    # Only extend .b by 1 if we're looking at empty sels.
                    if not view.has_non_empty_selection_region():
                        end += 1

                    return Region(s.a, end)

            regions_transformer(self.view, f)

        if any(s.empty() for s in self.view.sel()):
            return

        # Sometimes we'll call this command without the global state knowing
        # its metadata. For example, when shift-clicking with the mouse to
        # create visual selections. Always update xpos to cover this case.
        update_xpos(self.view)
        set_mode(self.view, VISUAL)
        update_status_line(self.view)


class nv_enter_visual_line_mode(TextCommand):

    def run(self, edit, mode=None, force=False):
        if get_mode(self.view) == VISUAL_LINE and not force:
            enter_normal_mode(self.view, mode)
            return

        if mode in (NORMAL, INTERNAL_NORMAL):
            # Special-case: If cursor is at the very EOF, then try backup the
            # selection one character so the line, or previous line, is selected
            # (currently only handles non multiple-selections).
            if self.view.size() > 0 and len(self.view.sel()) == 1:
                s = self.view.sel()[0]
                if self.view.substr(s.b) == EOF:
                    set_selection(self.view, s.b - 1)

            # Abort if we are at EOF -- no newline char to hold on to.
            if any(s.b == self.view.size() for s in self.view.sel()):
                ui_bell()
                return

        if mode == VISUAL_BLOCK:
            visual_block = VisualBlockSelection(self.view)
            visual_block.transform_to_visual_line()
        else:
            def f(view, s):
                if mode == VISUAL:
                    if s.a < s.b:
                        if view.substr(s.b - 1) != '\n':
                            return Region(view.line(s.a).a, view.full_line(s.b - 1).b)
                        else:
                            return Region(view.line(s.a).a, s.b)
                    else:
                        if view.substr(s.a - 1) != '\n':
                            return Region(view.full_line(s.a - 1).b, view.line(s.b).a)
                        else:
                            return Region(s.a, view.line(s.b).a)
                else:
                    return view.full_line(s.b)

            regions_transformer(self.view, f)

        set_mode(self.view, VISUAL_LINE)
        update_status_line(self.view)


class nv_enter_replace_mode(TextCommand):

    def run(self, edit, **kwargs):
        def f(view, s):
            s.a = s.b
            return s

        self.view.settings().set('command_mode', False)
        self.view.settings().set('inverse_caret_state', False)
        self.view.set_overwrite_status(True)
        set_mode(self.view, REPLACE)
        regions_transformer(self.view, f)
        update_status_line(self.view)
        reset_command_data(self.view)


class nv_vi_dot(WindowCommand):

    def run(self, mode=None, count=None, repeat_data=None):
        self.view = self.window.active_view()
        reset_command_data(self.view)

        if get_mode(self.view) == INTERNAL_NORMAL:
            set_mode(self.view, NORMAL)

        if repeat_data is None:
            repeat_data = get_repeat_data(self.view)
            if not repeat_data:
                return ui_bell()

        # TODO: Find out if the user actually meant '1'.
        if count and count == 1:
            count = None

        repeat_type, seq_or_cmd, old_mode, visual_data = repeat_data

        if visual_data and (mode != VISUAL):
            restore_visual_repeat_data(self.view, get_mode(self.view), visual_data)
        elif not visual_data and (mode == VISUAL):
            return ui_bell()  # Can't repeat normal mode commands in visual mode.
        elif mode not in (VISUAL, VISUAL_LINE, NORMAL, INTERNAL_NORMAL, INSERT):
            return ui_bell()

        if repeat_type == 'vi':
            self.window.run_command('nv_process_notation', {'keys': seq_or_cmd, 'repeat_count': count})
        elif repeat_type == 'native':
            # FIXME: We're not repeating as we should. It's the motion that should receive this count.
            for i in range(count or 1):
                self.window.run_command(*seq_or_cmd)
        else:
            raise ValueError('bad repeat data')

        enter_normal_mode(self.window, mode)
        set_repeat_data(self.view, repeat_data)


class nv_vi_dd(TextCommand):

    def run(self, edit, mode=None, count=1, register='"'):
        def f(view, s):
            if mode != INTERNAL_NORMAL:
                return s

            return lines(view, s, count)

        def fixup_sel_pos():
            old = [s.a for s in list(self.view.sel())]
            self.view.sel().clear()
            size = self.view.size()
            new = []
            for pt in old:
                # If on the last char, then pur cursor on previous line
                if pt == size and self.view.substr(pt) == EOF:
                    pt = self.view.text_point(self.view.rowcol(pt)[0], 0)
                pt = next_non_blank(self.view, pt)
                new.append(pt)
            self.view.sel().add_all(new)

        regions_transformer(self.view, f)
        registers_op_delete(self.view, register=register, linewise=True)
        self.view.run_command('right_delete')
        fixup_sel_pos()


class nv_vi_cc(TextCommand):

    def run(self, edit, mode=None, count=1, register='"'):
        def f(view, s):
            if mode != INTERNAL_NORMAL:
                return s

            if view.line(s.b).empty():
                return s

            return inner_lines(view, s, count)

        regions_transformer(self.view, f)
        registers_op_change(self.view, register=register, linewise=True)

        if not all(s.empty() for s in self.view.sel()):
            self.view.run_command('right_delete')

        enter_insert_mode(self.view, mode)

        # TODO Review exception handling
        try:
            set_xpos(self.view, self.view.rowcol(self.view.sel()[0].b)[1])
        except Exception as e:
            raise ValueError('could not set xpos:' + str(e))


class nv_vi_visual_o(TextCommand):

    def run(self, edit, mode=None, count=1):
        def f(view, s):
            if mode in (VISUAL, VISUAL_LINE):
                s = Region(s.b, s.a)

            return s

        regions_transformer(self.view, f)
        self.view.show(self.view.sel()[0].b, False)


class nv_vi_yy(TextCommand):

    def run(self, edit, mode=None, count=1, register=None):
        def f(view, s):
            if mode == INTERNAL_NORMAL:
                if count > 1:
                    row, col = self.view.rowcol(s.b)
                    end = view.text_point(row + count - 1, 0)
                    s.a = view.line(s.a).a
                    s.b = view.full_line(end).b
                elif view.line(s.b).empty():
                    s.a = s.b
                    s.b = min(view.size(), s.b + 1)
                else:
                    s = view.full_line(s.b)
            elif mode in (VISUAL, VISUAL_LINE):
                startline = view.line(s.begin())
                endline = view.line(s.end() - 1)
                s.a = startline.a
                s.b = endline.b

            return s

        if mode not in (INTERNAL_NORMAL, VISUAL, VISUAL_LINE):
            enter_normal_mode(self.view, mode)
            ui_bell()
            return

        with sel_observer(self.view) as observer:
            regions_transformer(self.view, f)
            ui_highlight_yank(self.view)
            registers_op_yank(self.view, register=register, linewise=True)
            observer.restore_sel()
            enter_normal_mode(self.view, mode)


class nv_vi_y(TextCommand):

    def run(self, edit, mode=None, count=1, motion=None, register=None):
        if mode == INTERNAL_NORMAL:
            requires_motion(motion)
            run_motion(self.view, motion)

        ui_highlight_yank(self.view)
        registers_op_yank(self.view, register=register, linewise=is_linewise_operation(mode, motion))

        if mode == VISUAL_BLOCK:
            # After a yank, the cursor should move to start of the yanked text.
            resolve_visual_block_begin(self.view)
        else:
            def f(view, s):
                return Region(next_non_blank(view, s.begin()))

            regions_transformer(self.view, f)

        enter_normal_mode(self.view, mode)


class nv_vi_d(TextCommand):

    def run(self, edit, mode=None, count=1, motion=None, register=None):
        if mode == INTERNAL_NORMAL:
            requires_motion(motion)

        if motion:
            with sel_observer(self.view) as observer:
                run_motion(self.view, motion)
                if not observer.has_sel_changed():
                    enter_normal_mode(self.view, mode)
                    ui_bell()
                    return

            if all(s.empty() for s in self.view.sel()):
                enter_normal_mode(self.view, mode)
                ui_bell()
                return

        registers_op_delete(self.view, register=register, linewise=is_linewise_operation(mode, motion))
        self.view.run_command('left_delete')
        fix_eol_cursor(self.view, mode)
        enter_normal_mode(self.view, mode)

        if mode == INTERNAL_NORMAL:
            if should_motion_apply_op_transformer(motion):
                def f(view, s):
                    if motion and 'motion' in motion:
                        if motion['motion'] in ('nv_vi_e', 'nv_vi_big_e'):
                            return Region(s.begin())

                    return Region(next_non_blank(self.view, s.b))

                regions_transformer(self.view, f)
        elif mode == VISUAL_LINE:
            def f(view, s):
                return Region(next_non_blank(self.view, s.b))

            regions_transformer(self.view, f)

        fix_eol_cursor(self.view, mode)


class nv_vi_big_a(TextCommand):

    def run(self, edit, mode=None, count=1):
        def f(view, s):
            if mode == VISUAL_BLOCK:
                if self.view.substr(s.b - 1) == '\n':
                    return Region(s.end() - 1)
                return Region(s.end())

            elif mode == VISUAL:
                pt = s.b
                if self.view.substr(s.b - 1) == '\n':
                    pt -= 1
                if s.a > s.b:
                    pt = s.b

                return Region(pt)

            elif mode == VISUAL_LINE:
                if self.view.substr(s.b - 1) == '\n':
                    return Region(s.b - 1)
                else:
                    return Region(s.b)

            elif mode != INTERNAL_NORMAL:
                return s

            if s.b == view.size():
                return s

            hard_eol = self.view.line(s.b).end()
            return Region(hard_eol, hard_eol)

        if mode == SELECT:
            self.view.window().run_command('find_all_under')
            return

        regions_transformer(self.view, f)
        enter_insert_mode(self.view, mode)


class nv_vi_big_i(TextCommand):

    def run(self, edit, mode=None, count=1):
        def f(view, s):
            if mode in (VISUAL, VISUAL_LINE):
                s = Region(view.line(s.begin()).a)
            elif mode == INTERNAL_NORMAL:
                s = Region(next_non_blank(view, view.line(s.begin()).a))
            elif mode in (VISUAL_BLOCK, SELECT):
                s = Region(s.begin())

            return s

        regions_transformer(self.view, f)
        enter_insert_mode(self.view, mode)


class nv_vi_m(TextCommand):

    def run(self, edit, mode=None, count=1, character=None):
        set_mark(self.view, character)


class nv_vi_quote(TextCommand):

    def run(self, edit, mode=None, count=1, character=None):
        if int(version()) >= 4082 and character == "'":
            self.view.run_command('jump_back')
            return

        def f(view, s):
            if mode == NORMAL:
                resolve_normal_target(s, next_non_blank(view, view.line(target.b).a))
            elif mode == VISUAL:
                resolve_visual_target(s, next_non_blank(view, view.line(target.b).a))
            elif mode == VISUAL_LINE:
                resolve_visual_line_target(view, s, next_non_blank(view, view.line(target.b).a))
            elif mode == INTERNAL_NORMAL:
                if s.a < target.a:
                    s = Region(view.full_line(s.b).a, view.line(target.b).b)
                else:
                    s = Region(view.full_line(s.b).b, view.line(target.b).a)

            return s

        target = get_mark(self.view, character)
        if target is None:
            ui_bell('E20: mark not set')
            return

        if isinstance(target, tuple):
            view, target = target
            self.view.window().focus_view(view)

        with jumplist_updater(self.view):
            regions_transformer(self.view, f)

        if not self.view.visible_region().intersects(target):
            self.view.show_at_center(target)


class nv_vi_backtick(TextCommand):

    def run(self, edit, mode=None, count=1, character=None):
        if int(version()) >= 4082 and character == '`':
            self.view.run_command('jump_back')
            return

        def f(view, s):
            if mode == NORMAL:
                resolve_normal_target(s, target.b)
            elif mode == VISUAL:
                resolve_visual_target(s, target.b)
            elif mode == VISUAL_LINE:
                resolve_visual_line_target(view, s, target.b)
            elif mode == INTERNAL_NORMAL:
                if s.a < target.a:
                    s = Region(view.full_line(s.b).a, view.line(target.b).b)
                else:
                    s = Region(view.full_line(s.b).b, view.line(target.b).a)

            return s

        target = get_mark(self.view, character)
        if target is None:
            ui_bell('E20: mark not set')
            return

        if isinstance(target, tuple):
            view, target = target
            self.view.window().focus_view(view)

        with jumplist_updater(self.view):
            regions_transformer(self.view, f)


class nv_vi_big_d(TextCommand):

    def run(self, edit, mode=None, count=1, register=None):
        def f(view, s):
            if mode == INTERNAL_NORMAL:
                lines = sel_to_lines(view, s, count)
                if lines:
                    s.a = s.b
                    s.b = lines[-1].b

            elif mode == VISUAL:
                startline = view.line(s.begin())
                endline = view.full_line(s.end())
                s.a = startline.a
                s.b = endline.b

            return s

        regions_transformer(self.view, f)
        registers_op_delete(self.view, register=register, linewise=is_visual_mode(mode))
        self.view.run_command('left_delete')

        if mode == VISUAL:
            # TODO Refactor set position cursor after operation into reusable api.
            new_sels = []
            update = False
            for sel in self.view.sel():
                line = self.view.line(sel.b)
                if line.size() > 0:
                    pt = self.view.find('^\\s*', line.begin()).end()
                    new_sels.append(pt)
                    if pt != line.begin():
                        update = True

            if update and new_sels:
                set_selection(self.view, new_sels)

        enter_normal_mode(self.view, mode)


class nv_vi_big_c(TextCommand):

    def run(self, edit, mode=None, count=1, register=None):
        def f(view, s):
            if mode == INTERNAL_NORMAL:
                lines = sel_to_lines(view, s, count)
                if lines:
                    s.a = s.b
                    s.b = lines[-1].b

            return s

        regions_transformer(self.view, f)
        registers_op_change(self.view, register=register, linewise=is_visual_mode(mode))

        empty = [s for s in list(self.view.sel()) if s.empty()]
        self.view.add_regions('vi_empty_sels', empty)
        for r in empty:
            self.view.sel().subtract(r)

        self.view.run_command('right_delete')
        self.view.sel().add_all(self.view.get_regions('vi_empty_sels'))
        self.view.erase_regions('vi_empty_sels')
        enter_insert_mode(self.view, mode)


class nv_vi_big_s(TextCommand):

    def run(self, edit, mode=None, count=1, register=None):
        def f(view, s):
            if mode == INTERNAL_NORMAL:
                lines = sel_to_lines(view, s, count)
                if lines:
                    s.a = next_non_blank(view, lines[0].a)
                    s.b = lines[-1].b

            return s

        regions_transformer(self.view, f)
        registers_op_change(self.view, register=register, linewise=True)

        empty = [s for s in list(self.view.sel()) if s.empty()]
        self.view.add_regions('vi_empty_sels', empty)
        for r in empty:
            self.view.sel().subtract(r)

        self.view.run_command('right_delete')
        self.view.sel().add_all(self.view.get_regions('vi_empty_sels'))
        self.view.erase_regions('vi_empty_sels')
        self.view.run_command('reindent', {'force_indent': False})
        enter_insert_mode(self.view, mode)


class nv_vi_s(TextCommand):

    def run(self, edit, mode=None, count=1, register=None):
        def f(view, s):
            if mode == INTERNAL_NORMAL:
                line = view.line(s.b)
                if line.empty():
                    return Region(s.b)

                return Region(s.b, min(s.b + count, line.b))

            if mode == VISUAL_LINE:
                return Region(s.begin(), s.end() - 1)

            return Region(s.begin(), s.end())

        if mode not in (VISUAL, VISUAL_LINE, VISUAL_BLOCK, INTERNAL_NORMAL, SELECT):
            enter_normal_mode(self.view, mode)
            ui_bell()
            return

        with sel_observer(self.view) as observer:
            regions_transformer(self.view, f)
            if not observer.has_sel_changed() and mode == INTERNAL_NORMAL:
                enter_insert_mode(self.view, mode)
                return

        registers_op_delete(self.view, register=register, linewise=(mode == VISUAL_LINE))
        self.view.run_command('right_delete')
        enter_insert_mode(self.view, mode)


class nv_vi_x(TextCommand):

    def run(self, edit, mode=None, count=1, register=None):
        def select(view, s):
            if mode == INTERNAL_NORMAL:
                return Region(s.b, min(s.b + count, view.line(s.b).b))

            return s

        if mode not in (VISUAL, VISUAL_LINE, VISUAL_BLOCK, INTERNAL_NORMAL, SELECT):
            enter_normal_mode(self.view, mode)
            ui_bell()
            return

        if mode == INTERNAL_NORMAL and all(self.view.line(s.b).empty() for s in self.view.sel()):
            return

        regions_transformer(self.view, select)
        registers_op_delete(self.view, register=register, linewise=(mode == VISUAL_LINE))
        self.view.run_command('right_delete')

        if mode == VISUAL_BLOCK:
            resolve_visual_block_begin(self.view)

        enter_normal_mode(self.view, mode)


class nv_vi_r(TextCommand):

    def make_replacement_text(self, char: str, r: Region) -> str:
        frags = split_by_newlines(self.view, r)
        new_frags = []
        for fr in frags:
            new_frags.append(char * len(fr))

        return '\n'.join(new_frags)

    def run(self, edit, mode=None, count=1, register=None, char=None):
        def f(view, s):
            if mode == INTERNAL_NORMAL:
                pt = s.b + count
                text = self.make_replacement_text(char, Region(s.a, pt))
                view.replace(edit, Region(s.a, pt), text)

                if char == '\n':
                    return Region(s.b + 1)
                else:
                    return Region(s.b)

            elif mode in (VISUAL, VISUAL_LINE, VISUAL_BLOCK):
                ends_in_newline = (view.substr(s.end() - 1) == '\n')
                text = self.make_replacement_text(char, s)
                if ends_in_newline:
                    text += '\n'

                view.replace(edit, s, text)

                if char == '\n':
                    return Region(s.begin() + 1)
                else:
                    return Region(s.begin())

        char = translate_char(char)
        regions_transformer(self.view, f)
        enter_normal_mode(self.view, mode)


class nv_vi_less_than_less_than(TextCommand):

    def run(self, edit, mode=None, count=1):
        regions_transform_extend_to_line_count(self.view, count)
        self.view.run_command('unindent')
        regions_transform_to_first_non_blank(self.view)
        enter_normal_mode(self.view, mode)


class nv_vi_equal_equal(TextCommand):

    def run(self, edit, mode=None, count=1):
        regions_transform_extend_to_line_count(self.view, count)
        self.view.run_command('reindent', {'force_indent': False})
        regions_transform_to_first_non_blank(self.view)
        enter_normal_mode(self.view, mode)


class nv_vi_greater_than_greater_than(TextCommand):

    def run(self, edit, mode=None, count=1):
        regions_transform_extend_to_line_count(self.view, count)
        self.view.run_command('indent')
        regions_transform_to_first_non_blank(self.view)
        enter_normal_mode(self.view, mode)


class nv_vi_greater_than(TextCommand):

    def run(self, edit, mode=None, count=1, motion=None):
        if mode == VISUAL_BLOCK:
            translate = self.view.settings().get('translate_tabs_to_spaces')
            size = self.view.settings().get('tab_size')

            def f(view, s):
                block = '\t' if not translate else ' ' * size
                self.view.insert(edit, s.begin(), block * count)

                return Region(s.begin() + 1)

            regions_transformer_reversed(self.view, f)
            regions_transform_to_first_non_blank(self.view)

            # Restore only the first sel.
            s = self.view.sel()[0]
            set_selection(self.view, s.a + 1)
            enter_normal_mode(self.view, mode)
            return

        if motion:
            run_motion(self.view, motion)
        elif mode not in (VISUAL, VISUAL_LINE):
            return ui_bell()

        for i in range(count):
            self.view.run_command('indent')

        regions_transform_to_first_non_blank(self.view)
        enter_normal_mode(self.view, mode)


class nv_vi_less_than(TextCommand):

    def run(self, edit, mode=None, count=1, motion=None):
        if motion:
            run_motion(self.view, motion)
        elif mode not in (VISUAL, VISUAL_LINE, VISUAL_BLOCK):
            return ui_bell()

        for i in range(count):
            self.view.run_command('unindent')

        if mode == VISUAL_BLOCK:
            resolve_visual_block_begin(self.view)

        regions_transform_to_first_non_blank(self.view)
        enter_normal_mode(self.view, mode)


class nv_vi_equal(TextCommand):

    def run(self, edit, mode=None, count=1, motion=None):
        if motion:
            run_motion(self.view, motion)
        elif mode not in (VISUAL, VISUAL_LINE, VISUAL_BLOCK):
            return ui_bell()

        self.view.run_command('reindent', {'force_indent': False})

        if mode == VISUAL_BLOCK:
            resolve_visual_block_begin(self.view)

        regions_transform_to_first_non_blank(self.view)
        enter_normal_mode(self.view, mode)


class nv_vi_big_o(TextCommand):

    def run(self, edit, mode=None, count=1):
        def f(view, sel, index):
            real_sel = Region(sel.a + index * count, sel.b + index * count)
            start_of_line = view.full_line(real_sel).begin()
            view.insert(edit, start_of_line, "\n" * count)
            new = []
            for i in range(0, count):
                new.append(Region(start_of_line + i, start_of_line + i))
            return new

        regions_transformer_indexed(self.view, f)
        enter_insert_mode(self.view, mode)
        self.view.run_command('reindent', {'force_indent': False})


class nv_vi_o(TextCommand):
    def run(self, edit, mode=None, count=1):
        def f(view, sel, index):
            real_sel = sel if index == 0 else Region(sel.a + index * count, sel.b + index * count)
            end_of_line = view.line(real_sel).end()
            view.insert(edit, end_of_line, "\n" * count)
            new = []
            for i in range(1, count + 1):
                new.append(Region(end_of_line + i, end_of_line + i))
            return new

        regions_transformer_indexed(self.view, f)
        enter_insert_mode(self.view, mode)
        self.view.run_command('reindent', {'force_indent': False})


class nv_vi_big_x(TextCommand):

    def run(self, edit, mode=None, count=1, register=None):
        def f(view, s):
            nonlocal abort  # type: ignore
            if mode == INTERNAL_NORMAL:
                if view.line(s.b).empty():
                    abort = True
                return Region(s.b, max(s.b - count, self.view.line(s.b).begin()))
            elif mode == VISUAL:
                if s.a < s.b:
                    if view.line(s.b - 1).empty() and s.size() == 1:
                        abort = True
                    return Region(view.full_line(s.b - 1).b, view.line(s.a).a)

                if view.line(s.b).empty() and s.size() == 1:
                    abort = True
                return Region(view.line(s.b).a, view.full_line(s.a - 1).b)
            return Region(s.begin(), s.end())

        abort = False
        regions_transformer(self.view, f)

        registers_op_delete(self.view, register=register, linewise=True)

        if not abort:
            self.view.run_command('left_delete')

        enter_normal_mode(self.view, mode)


class nv_vi_big_z_big_q(WindowCommand):

    def run(self):
        do_ex_command(self.window, 'quit', {'forceit': True})


class nv_vi_big_z_big_z(WindowCommand):

    def run(self):
        do_ex_command(self.window, 'exit')


class nv_vi_paste(TextCommand):

    def run(self, edit, before_cursor, mode=None, count=1, register=None, adjust_indent=False, adjust_cursor=False):
        contents, linewise = registers_get_for_paste(self.view, register, mode)
        if not contents:
            return status_message('E353: Nothing in register ' + register)

        contents = resolve_paste_items_with_view_sel(self.view, contents)
        if not contents:
            ui_bell()
            return

        sels = list(self.view.sel())

        # Some paste operations need to reposition the cursor to a specific
        # point after the paste operation has been completed successfully.
        sel_to_specific_pt = -1

        # When there is one selection and many register contents the contents
        # are pasted as a visual block. Selections are added to match the number
        # of contents and adjusted with left-padded whitespace where neccessary.
        if len(sels) == 1 and len(contents) > 1:
            sels, contents, before_cursor, sel_to_specific_pt = pad_visual_block_paste_contents(
                self.view, sels, contents, before_cursor)

        contents = zip(reversed(contents), reversed(sels))

        def _get_indent(view, level) -> str:
            translate = view.settings().get('translate_tabs_to_spaces')
            tab_size = int(view.settings().get('tab_size'))
            tab_text = ' ' * tab_size if translate else '\t'

            return tab_text * level

        def _indent_text(view, text: str, sel: Region) -> str:
            indentation_level = view.indentation_level(get_insertion_point_at_b(sel))

            return textwrap.indent(
                textwrap.dedent(text),
                _get_indent(view, indentation_level)
            )

        if mode == INTERNAL_NORMAL:
            self.view.sel().clear()

            for text, sel in contents:
                if adjust_indent:
                    text = _indent_text(self.view, text, sel)
                    if text[-1] != '\n':
                        text += '\n'

                    linewise = True

                text *= count

                # If register content is from a linewise operation, then the cursor
                # is put on the first non-blank character of the first line of the
                # content after the content is inserted.
                if linewise:
                    line = self.view.line(sel.a)
                    row = self.view.rowcol(line.a)[0]
                    if before_cursor:
                        pt = self.view.text_point(row, 0)
                    else:
                        pt = self.view.text_point(row + 1, 0)

                    # When the insertion point is at the EOF in linewise and the
                    # EOF is not a newline then the text needs to be prefixed
                    # with one, the selection point needs to be adjusted too.
                    insertion_pt_at_eof = not before_cursor and line.size() > 0 and line.end() >= self.view.size()
                    if insertion_pt_at_eof:
                        text = '\n' + text

                    self.view.insert(edit, pt, text)

                    if adjust_cursor:
                        pt += len(text) + 1
                    else:
                        # The insertion point is at EOF; see above for details.
                        if insertion_pt_at_eof:
                            pt += 1

                        pt = next_non_blank(self.view, pt)

                    self.view.sel().add(pt)

                # If register is charactwise but contains a newline, then the cursor
                # is put at the start of of the text pasted, otherwise the cursor is
                # put on the last character of the text pasted.
                else:
                    # Paste before the cursor if the current line is empty.
                    if before_cursor or self.view.line(sel.a).empty():
                        pt = sel.a
                    else:
                        pt = min(sel.a + 1, self.view.size())

                    self.view.insert(edit, pt, text)

                    if adjust_cursor:
                        pt += len(text)
                    elif '\n' not in text:
                        pt += len(text) - 1

                    self.view.sel().add(pt)

            enter_normal_mode(self.view, mode)
        elif mode in (VISUAL, VISUAL_LINE, SELECT):
            new_sels = []
            for text, sel in contents:
                self.view.replace(edit, sel, text)

                if mode == VISUAL:
                    if '\n' in text and not linewise:
                        new_sels.append(sel.begin())

                elif mode == VISUAL_LINE:
                    new_sels.append(next_non_blank(self.view, sel.begin()))

                enter_normal_mode(self.view, mode)

                # If register content is linewise, then the cursor is put on the
                # first non blank of the line.
                if linewise:
                    def f(view, s):
                        return Region(next_non_blank(view, view.line(s).a))

                    regions_transformer(self.view, f)

            if new_sels:
                set_selection(self.view, new_sels)

        if sel_to_specific_pt >= 0:
            self.view.sel().clear()
            self.view.sel().add(sel_to_specific_pt)


class nv_vi_ga(WindowCommand):

    def run(self, **kwargs):
        def char_to_notation(char: str) -> str:
            # Convert a char to a key notation. Uses vim key notation.
            # See https://vimhelp.appspot.com/intro.txt.html#key-notation
            char_notation_map = {
                '\0': "Nul",
                ' ': "Space",
                '\t': "Tab",
                '\n': "NL"
            }

            if char in char_notation_map:
                char = char_notation_map[char]

            return "<" + char + ">"

        view = self.window.active_view()
        region = view.sel()[-1]
        c_str = view.substr(get_insertion_point_at_b(region))
        c_ord = ord(c_str)
        c_hex = hex(c_ord)
        c_oct = oct(c_ord)
        c_not = char_to_notation(c_str)
        status_message('%7s %3s,  Hex %4s,  Octal %5s' % (c_not, c_ord, c_hex, c_oct))


class nv_vi_gt(WindowCommand):

    def run(self, mode=None, count=0):
        if count > 0:
            window_tab_control(self.window, 'goto', index=count)
        else:
            window_tab_control(self.window, 'next')

        enter_normal_mode(self.window, mode)


class nv_vi_g_big_t(WindowCommand):

    def run(self, mode=None, count=1):
        window_tab_control(self.window, 'previous', count)
        enter_normal_mode(self.window, mode)


class nv_vi_g(TextCommand):

    def run(self, edit, action, **kwargs):
        if action == 'f':
            file_name = extract_file_name(self.view)
            if not file_name:
                ui_bell('E446: No file name under cursor')
                return

            window_open_file(self.view.window(), file_name)
        else:
            raise ValueError('unknown action')


class nv_vi_ctrl_hat(WindowCommand):

    def run(self, **kwargs):
        alternate_file = get_alternate_file_register()
        if not alternate_file:
            ui_bell('E23: No alternate file')
            return

        self.window.open_file(alternate_file)


class nv_vi_ctrl_right_square_bracket(WindowCommand):

    def run(self, mode=None, count=1):
        view = self.window.active_view()
        if is_help_view(view):
            GotoView(view, mode, count).help()
        else:
            self.window.run_command('goto_definition')


class nv_vi_ctrl_w(WindowCommand):

    def run(self, **kwargs):
        window_control(self.window, **kwargs)


class nv_vi_z_enter(TextCommand):

    def run(self, edit, mode=None, count=1):
        pt = get_insertion_point_at_b(self.view.sel()[0])
        home_line = self.view.line(pt)
        target_pt = self.view.text_to_layout(home_line.begin())
        self.view.set_viewport_position(target_pt)


class nv_vi_z_minus(TextCommand):

    def run(self, edit, mode=None, count=1):
        layout_coord = self.view.text_to_layout(self.view.sel()[0].b)
        viewport_extent = self.view.viewport_extent()
        new_pos = (0.0, layout_coord[1] - viewport_extent[1])
        self.view.set_viewport_position(new_pos)


class nv_vi_zz(TextCommand):

    def run(self, edit, mode=None, count=1, first_non_blank=False):
        first_sel = self.view.sel()[0]
        current_position = self.view.text_to_layout(first_sel.b)
        viewport_dim = self.view.viewport_extent()
        new_pos = (0.0, current_position[1] - viewport_dim[1] / 2)
        self.view.set_viewport_position(new_pos)
        if first_non_blank:
            row = self.view.rowcol(first_sel.b)[0]
            first_non_blank_pt = next_non_blank(self.view, self.view.text_point(row, 0))
            if mode in (NORMAL, INTERNAL_NORMAL):
                set_selection(self.view, first_non_blank_pt)


class nv_vi_z(TextCommand):

    def run(self, edit, action, count, **kwargs):
        if action == 'c':
            fold(self.view)
        elif action == 'g':
            spell_file_add_word(self.view, kwargs.get('mode'), count)
        elif action == 'ug':
            spell_file_remove_word(self.view, kwargs.get('mode'), count)
        elif action in ('h', '<left>'):
            scroll_horizontally(self.view, edit, amount=-count)
        elif action in ('l', '<right>'):
            scroll_horizontally(self.view, edit, amount=count)
        elif action == 'o':
            unfold(self.view)
        elif action == 'H':
            scroll_horizontally(self.view, edit, amount=-count, half_screen=True)
        elif action == 'L':
            scroll_horizontally(self.view, edit, amount=count, half_screen=True)
        elif action == 'M':
            fold_all(self.view)
        elif action == 'R':
            unfold_all(self.view)
        elif action == '=':
            spell_select(self.view)
        else:
            raise ValueError('unknown action')


class nv_vi_modify_numbers(TextCommand):

    DIGIT_PAT = re.compile('(\\D+?)?(-)?(\\d+)(\\D+)?')
    NUM_PAT = re.compile('\\d')

    def get_editable_data(self, pt):
        sign = -1 if (self.view.substr(pt - 1) == '-') else 1
        end = pt
        while self.view.substr(end).isdigit():
            end += 1

        return (sign, int(self.view.substr(Region(pt, end))), Region(end, self.view.line(pt).b))

    def find_next_num(self, regions):
        # Modify selections that are inside a number already.
        for i, r in enumerate(regions):
            a = r.b

            while self.view.substr(a).isdigit():
                a -= 1

            if a != r.b:
                a += 1

            regions[i] = Region(a)

        lines = [self.view.substr(Region(r.b, self.view.line(r.b).b)) for r in regions]
        matches = [self.NUM_PAT.search(text) for text in lines]
        if all(matches):
            return [(reg.b + ma.start()) for (reg, ma) in zip(regions, matches)]  # type: ignore

        return []

    def run(self, edit, mode=None, count=1, subtract=False):
        # TODO Implement {Visual}CTRL-A
        # TODO Implement {Visual}CTRL-X
        if mode != INTERNAL_NORMAL:
            return

        # TODO Implement CTRL-A and CTRL-X  octal, hex, etc. numbers

        regs = list(self.view.sel())
        pts = self.find_next_num(regs)

        if not pts:
            return ui_bell()

        end_sels = []
        count = count if not subtract else -count
        for pt in reversed(pts):
            sign, num, tail = self.get_editable_data(pt)

            num_as_text = str((sign * num) + count)
            new_text = num_as_text + self.view.substr(tail)

            offset = 0
            if sign == -1:
                offset = -1
                self.view.replace(edit, Region(pt - 1, tail.b), new_text)
            else:
                self.view.replace(edit, Region(pt, tail.b), new_text)

            rowcol = self.view.rowcol(pt + len(num_as_text) - 1 + offset)
            end_sels.append(rowcol)

        self.view.sel().clear()
        for (row, col) in end_sels:
            self.view.sel().add(Region(self.view.text_point(row, col)))


class nv_vi_select_big_j(TextCommand):

    def run(self, edit, mode=None, count=1):
        if get_setting(self.view, 'multi_cursor_exit_from_visual_mode'):
            set_selection(self.view, self.view.sel()[0])

        enter_normal_mode(self.view, mode)


class nv_vi_big_j(TextCommand):
    WHITE_SPACE = ' \t'

    def run(self, edit, mode=None, count=1, dont_insert_or_remove_spaces=False):
        sels = self.view.sel()
        s = Region(sels[0].a, sels[-1].b)
        if mode == INTERNAL_NORMAL:
            end_pos = self.view.line(s.b).b
            start = end = s.b
            if count > 2:
                end = self.view.text_point(row_at(self.view, s.b) + (count - 1), 0)
                end = self.view.line(end).b
            else:
                # Join current line and the next.
                end = self.view.text_point(row_at(self.view, s.b) + 1, 0)
                end = self.view.line(end).b
        elif mode in (VISUAL, VISUAL_LINE, VISUAL_BLOCK):
            if s.a < s.b:
                end_pos = self.view.line(s.a).b
                start = s.a
                if row_at(self.view, s.b - 1) == row_at(self.view, s.a):
                    end = self.view.text_point(row_at(self.view, s.a) + 1, 0)
                else:
                    end = self.view.text_point(row_at(self.view, s.b - 1), 0)
                end = self.view.line(end).b
            else:
                end_pos = self.view.line(s.b).b
                start = s.b
                if row_at(self.view, s.b) == row_at(self.view, s.a - 1):
                    end = self.view.text_point(row_at(self.view, s.a - 1) + 1, 0)
                else:
                    end = self.view.text_point(row_at(self.view, s.a - 1), 0)
                end = self.view.line(end).b
        else:
            return s

        text_to_join = self.view.substr(Region(start, end))
        lines = text_to_join.split('\n')

        def strip_leading_comments(lines):
            shell_vars = self.view.meta_info("shellVariables", start)
            comment_start_tokens = {}
            comment_end_tokens = {}
            for var in shell_vars:
                if var['name'].startswith('TM_COMMENT_'):
                    if 'START' in var['name']:
                        comment_start_tokens[var['name']] = var['value']
                    else:
                        comment_end_tokens[var['name']] = var['value']

            # Strip any leading whitespace.
            first_line = self.view.substr(self.view.line(start)).lstrip(' \t')

            stripped = []
            for i, line in enumerate(lines):
                for name, value in comment_start_tokens.items():
                    # The first line is ignored.
                    if i < 1:
                        continue

                    # Comment definitions that have start AND end tokens are ignored.
                    end_token = comment_end_tokens.get(name.replace('_START', '_END'))
                    if end_token:
                        continue

                    # Lines are ignored if the first line is not a comment.
                    if not first_line.startswith(value):
                        continue

                    # Strip leading and trailing whitespace.
                    line_lstrip = line.lstrip(' \t')
                    line_rstrip = line.rstrip(' \t')
                    value_rstrip = value.rstrip(' \t')

                    is_comment = line_lstrip.startswith(value) or (line_rstrip == value_rstrip)
                    if is_comment:
                        line = line_lstrip[len(value):]

                stripped.append(line)

            return stripped

        lines = strip_leading_comments(lines)

        if not dont_insert_or_remove_spaces:  # J
            joined_text = lines[0]

            for line in lines[1:]:
                line = line.lstrip()
                if joined_text and joined_text[-1] not in self.WHITE_SPACE:
                    line = ' ' + line
                joined_text += line
        else:  # gJ
            joined_text = ''.join(lines)

        self.view.replace(edit, Region(start, end), joined_text)
        sels.clear()
        sels.add(Region(end_pos))
        enter_normal_mode(self.view, mode)


class nv_vi_gv(TextCommand):

    def run(self, edit, mode=None, count=None):
        visual_sel, visual_sel_mode = get_previous_selection(self.view)
        if not visual_sel or not visual_sel_mode:
            return

        def _do_cmd(cmd):
            cmd(self.view, mode=mode, force=True)
            set_selection(self.view, visual_sel)

        if visual_sel_mode == VISUAL:
            _do_cmd(enter_visual_mode)
        elif visual_sel_mode == VISUAL_LINE:
            # Update visual line selections to span full lines.
            for sel in visual_sel:
                if sel.a < sel.b:
                    sel.a = self.view.line(sel.a).a
                    sel.b = self.view.full_line(sel.b - 1).b
                else:
                    sel.a = self.view.full_line(sel.a - 1).b
                    sel.b = self.view.line(sel.b).a

            _do_cmd(enter_visual_line_mode)
        elif visual_sel_mode == VISUAL_BLOCK:
            _do_cmd(enter_visual_block_mode)


class nv_vi_gx(TextCommand):

    def run(self, edit, **kwargs):
        url = extract_url(self.view)
        if url:
            webbrowser.open_new_tab(url)


class nv_vi_ctrl_e(TextCommand):

    def run(self, edit, mode=None, count=1):
        self.view.run_command('scroll_lines', {'amount': -count})


class nv_vi_ctrl_g(WindowCommand):

    def run(self, **kwargs):
        do_ex_command(self.window, 'file')


class nv_vi_ctrl_y(TextCommand):

    def run(self, edit, mode=None, count=1):
        self.view.run_command('scroll_lines', {'amount': count})


class nv_vi_q(TextCommand):

    def run(self, edit, mode=None, count=1, name=None):
        if macros.is_recording():
            macros.stop_recording()
        else:
            if not macros.is_writable(name):
                return ui_bell("E354: Invalid register name: '" + name + "'")

            macros.start_recording(name)


class nv_vi_at(TextCommand):

    def run(self, edit, name, mode=None, count=1):
        if name == '@':
            name = macros.get_last_used_register_name()
            if not name:
                return ui_bell('E748: No previously used register')

        if not macros.is_readable(name):
            return ui_bell("E354: Invalid register name: '" + name + "'")

        cmds = macros.get_recorded(name)
        if not cmds:
            return

        macros.set_last_used_register_name(name)

        for i in range(count):
            for cmd, args in cmds:
                if 'xpos' in args:
                    update_xpos(self.view)
                    args['xpos'] = get_xpos(self.view)
                elif args.get('motion'):
                    motion = args.get('motion')
                    if motion and 'motion_args' in motion and 'xpos' in motion['motion_args']:
                        update_xpos(self.view)
                        motion = args.get('motion')
                        motion['motion_args']['xpos'] = get_xpos(self.view)
                        args['motion'] = motion

                self.view.window().run_command(cmd, args)


class nv_enter_visual_block_mode(TextCommand):

    def run(self, edit, mode=None, force=False):
        if mode in (NORMAL, VISUAL, VISUAL_LINE, INTERNAL_NORMAL):
            VisualBlockSelection.create(self.view)
            set_mode(self.view, VISUAL_BLOCK)
            update_status_line(self.view)

        elif mode == VISUAL_BLOCK and not force:
            enter_normal_mode(self.view, mode)
            update_status_line(self.view)


# TODO Refactor into nv_vi_j
class nv_vi_select_j(WindowCommand):

    def run(self, mode=None, count=1):
        if mode != SELECT:
            raise ValueError('wrong mode')

        for i in range(count):
            self.window.run_command('find_under_expand')


# TODO Refactor into nv_vi_k
class nv_vi_select_k(WindowCommand):

    def run(self, mode=None, count=1):
        self.view = self.window.active_view()
        if mode != SELECT:
            raise ValueError('wrong mode')

        for i in range(count):
            if len(self.view.sel()) > 1:
                self.window.run_command('soft_undo')
            else:
                enter_normal_mode(self.view, mode)


class nv_vi_tilde(TextCommand):

    def run(self, edit, mode=None, count=1, motion=None):
        def select(view, s):
            if mode == VISUAL:
                return Region(s.end(), s.begin())
            return Region(s.begin(), s.end() + count)

        def after(view, s):
            return Region(s.begin())

        regions_transformer(self.view, select)
        self.view.run_command('swap_case')

        if mode in (VISUAL, VISUAL_LINE, VISUAL_BLOCK):
            regions_transformer(self.view, after)

        enter_normal_mode(self.view, mode)


class nv_vi_g_tilde(TextCommand):

    def run(self, edit, mode=None, count=1, motion=None):
        def f(view, s):
            return Region(s.end(), s.begin())

        sels = []
        for s in list(self.view.sel()):
            sels.append(s.a)

        if motion:
            with sel_observer(self.view) as observer:
                run_motion(self.view, motion)
                if not observer.has_sel_changed():
                    ui_bell()
                    enter_normal_mode(self.view, mode)
                    return

        self.view.run_command('swap_case')

        if motion:
            regions_transformer(self.view, f)

        set_selection(self.view, sels)
        enter_normal_mode(self.view, mode)


class nv_vi_visual_u(TextCommand):

    def run(self, edit, mode=None, count=1):
        for s in self.view.sel():
            self.view.replace(edit, s, self.view.substr(s).lower())

        def f(view, s):
            return Region(s.begin())

        regions_transformer(self.view, f)
        enter_normal_mode(self.view, mode)


class nv_vi_visual_big_u(TextCommand):

    def run(self, edit, mode=None, count=1):
        for s in self.view.sel():
            self.view.replace(edit, s, self.view.substr(s).upper())

        def f(view, s):
            return Region(s.begin())

        regions_transformer(self.view, f)
        enter_normal_mode(self.view, mode)


class nv_vi_g_tilde_g_tilde(TextCommand):

    def run(self, edit, mode=None, count=1):
        def select(view, s):
            line = view.line(s.b)

            return Region(line.end(), line.begin())

        if mode != INTERNAL_NORMAL:
            raise ValueError('wrong mode')

        regions_transformer(self.view, select)
        self.view.run_command('swap_case')
        regions_transformer(self.view, select)
        enter_normal_mode(self.view, mode)


class nv_vi_g_big_u_big_u(TextCommand):

    def run(self, edit, mode=None, count=1):
        def select(view, s):
            return lines(view, s, count)

        def to_upper(view, s):
            view.replace(edit, s, view.substr(s).upper())
            return Region(next_non_blank(self.view, s.a))

        regions_transformer(self.view, select)
        regions_transformer(self.view, to_upper)
        enter_normal_mode(self.view, mode)


class nv_vi_guu(TextCommand):

    def run(self, edit, mode=None, count=1):
        def select(view, s):
            line = view.line(s.b)

            return Region(line.end(), line.begin())

        def to_lower(view, s):
            view.replace(edit, s, view.substr(s).lower())
            return s

        regions_transformer(self.view, select)
        regions_transformer(self.view, to_lower)
        enter_normal_mode(self.view, mode)


# Non-standard command. Select all search occurrences and enter multiple cursor
# mode (supports search results from commands such as /, ?, *, #).
class nv_vi_g_big_h(WindowCommand):

    def run(self, mode=None, count=1):
        self.view = self.window.active_view()
        search_occurrences = get_search_occurrences(self.view)
        if search_occurrences:
            self.view.sel().add_all(search_occurrences)
            set_mode(self.view, SELECT)
            update_status_line(self.view)
            return

        ui_bell('no available search matches')
        reset_command_data(self.view)


class nv_vi_ctrl_x_ctrl_l(TextCommand):
    MAX_MATCHES = 20

    def find_matches(self, prefix: str, end: int) -> list:
        escaped = re.escape(prefix)
        matches = []  # type: list
        while end > 0:
            match = reverse_search(self.view, r'^\s*{0}'.format(escaped), 0, end, flags=0)
            if (match is None) or (len(matches) == self.MAX_MATCHES):
                break
            line = self.view.line(match.begin())
            end = line.begin()
            text = self.view.substr(line).lstrip()
            if text not in matches:
                matches.append(text)

        return matches

    def run(self, edit, mode=None, register='"'):
        if mode != INSERT:
            raise ValueError('wrong mode')

        if (len(self.view.sel()) > 1 or not self.view.sel()[0].empty()):
            return ui_bell()

        s = self.view.sel()[0]
        line_begin = self.view.text_point(row_at(self.view, s.b), 0)
        prefix = self.view.substr(Region(line_begin, s.b)).lstrip()
        self._matches = self.find_matches(prefix, end=self.view.line(s.b).a)
        if self._matches:
            self.show_matches(self._matches)
            set_reset_during_init(self.view, False)
            reset_command_data(self.view)
            return

        ui_bell()

    def show_matches(self, items):
        self.view.window().show_quick_panel(items, self.replace, MONOSPACE_FONT)

    def replace(self, s):
        self.view.run_command('nv_view', {'action': 'replace_line', 'replacement': self._matches[s]})
        del self.__dict__['_matches']
        set_selection(self.view, self.view.sel()[0].b)


class nv_vi_find_in_line(TextCommand):

    # Contrary to *f*, *t* does not look past the caret's position, so if
    # @character is under the caret, nothing happens.
    def run(self, edit, char=None, mode=None, count=1, inclusive=True, skipping=False, save=True):
        if save:
            set_last_char_search(self.view, 'vi_f' if inclusive else 'vi_t', char)

        if mode == VISUAL_LINE:
            ui_bell()
            return

        def f(view, s):
            b = s.b
            # If we are in any visual mode, get the actual insertion point.
            if s.size() > 0:
                b = get_insertion_point_at_b(s)

            # Vim skips a character while performing the search
            # if the command is ';' or ',' after a 't' or 'T'
            if skipping:
                b = b + 1

            eol = view.line(b).end()

            match = Region(b + 1)
            for i in range(count):
                # Define search range as 'rest of the line to the right'.
                search_range = Region(match.end(), eol)
                match = find_in_range(view, char, search_range.a, search_range.b, LITERAL)

                # Count too high or simply no match; break.
                if match is None:
                    if mode != INTERNAL_NORMAL:
                        ui_bell()
                    return s

            target_pos = match.a
            if not inclusive:
                target_pos = target_pos - 1

            if mode == NORMAL:
                return Region(target_pos)
            elif mode == INTERNAL_NORMAL:
                return Region(s.a, target_pos + 1)
            else:  # For visual modes...
                new_a = get_insertion_point_at_a(s)
                return new_inclusive_region(new_a, target_pos)

        if not all([char, mode]):
            raise ValueError('bad parameters')

        char = translate_char(char)

        regions_transformer(self.view, f)


class nv_vi_reverse_find_in_line(TextCommand):

    # Contrary to *F*, *T* does not look past the caret's position, so if
    # ``character`` is right before the caret, nothing happens.
    def run(self, edit, char=None, mode=None, count=1, inclusive=True, skipping=False, save=True):
        if save:
            set_last_char_search(self.view, 'vi_big_f' if inclusive else 'vi_big_t', char)

        if mode == VISUAL_LINE:
            ui_bell()
            return

        def f(view, s):
            b = s.b
            if s.size() > 0:
                b = get_insertion_point_at_b(s)

            # Vim skips a character while performing the search
            # if the command is ';' or ',' after a 't' or 'T'
            if skipping:
                b = b - 1

            line_start = view.line(b).a

            try:
                match = b
                for i in range(count):
                    # line_text does not include character at match
                    line_text = view.substr(Region(line_start, match))
                    found_at = line_text.rindex(char)
                    match = line_start + found_at
            except ValueError:
                if mode != INTERNAL_NORMAL:
                    ui_bell()
                return s

            target_pos = match
            if not inclusive:
                target_pos = target_pos + 1

            if mode == NORMAL:
                return Region(target_pos)
            elif mode == INTERNAL_NORMAL:
                return Region(b, target_pos)
            else:  # For visual modes...
                new_a = get_insertion_point_at_a(s)
                return new_inclusive_region(new_a, target_pos)

        if not all([char, mode]):
            raise ValueError('bad parameters')

        char = translate_char(char)

        regions_transformer(self.view, f)


class nv_vi_slash(TextCommand):

    def run(self, edit, pattern=''):
        set_reset_during_init(self.view, False)

        self._cmdline = Cmdline(
            self.view,
            Cmdline.SEARCH_FORWARD,
            self.on_done,
            self.on_change,
            self.on_cancel
        )

        self._cmdline.prompt(pattern)

    def on_done(self, pattern: str):
        history_update(Cmdline.SEARCH_FORWARD + pattern)
        nv_cmdline_feed_key.reset_last_history_index()
        clear_search_highlighting(self.view)
        append_sequence(self.view, pattern + '<CR>')
        set_motion(self.view, ViSearchForwardImpl(term=pattern))
        evaluate_state(self.view)

    def on_change(self, pattern: str):
        count = get_count(self.view)
        sel = self.view.sel()[0]
        pattern, flags = process_search_pattern(self.view, pattern)
        start = get_insertion_point_at_b(sel) + 1
        end = self.view.size()

        match = find_wrapping(self.view,
                              term=pattern,
                              start=start,
                              end=end,
                              flags=flags,
                              times=count)

        clear_search_highlighting(self.view)

        if not match:
            return status_message('E486: Pattern not found: %s', pattern)

        add_search_highlighting(self.view, find_search_occurrences(self.view, pattern, flags), [match])
        show_if_not_visible(self.view, match)

    def on_cancel(self):
        clear_search_highlighting(self.view)
        reset_command_data(self.view)
        nv_cmdline_feed_key.reset_last_history_index()
        show_if_not_visible(self.view)


class nv_vi_slash_impl(TextCommand):
    def run(self, edit, pattern, mode=None, count=1, save=True):
        if not pattern:
            pattern = get_last_search_pattern(self.view)
            if not pattern:
                ui_bell('E35: no previous regular expression')
                return

        if save:
            set_last_search_pattern(self.view, pattern, 'nv_vi_slash')

        sel = self.view.sel()[0]
        pattern, flags = process_search_pattern(self.view, pattern)
        start = get_insertion_point_at_b(sel) + 1
        end = self.view.size()

        match = find_wrapping(self.view,
                              term=pattern,
                              start=start,
                              end=end,
                              flags=flags,
                              times=count)
        if not match:
            return status_message('E486: Pattern not found: %s', pattern)

        def f(view, s):
            if mode == NORMAL:
                resolve_normal_target(s, target)
            elif mode == VISUAL:
                resolve_visual_target(s, target)
            elif mode == VISUAL_LINE:
                resolve_visual_line_target(view, s, target)
            elif mode == INTERNAL_NORMAL:
                s.b = target

            return s

        target = get_insertion_point_at_a(match)
        regions_transformer(self.view, f)
        add_search_highlighting(self.view, find_search_occurrences(self.view, pattern, flags))


class nv_vi_l(TextCommand):
    def run(self, edit, mode=None, count=1):
        def f(view, s):
            if mode == NORMAL:
                if view.line(s.b).empty():
                    return s

                x_limit = min(view.line(s.b).b - 1, s.b + count, view.size())
                return Region(x_limit, x_limit)

            if mode == INTERNAL_NORMAL:
                x_limit = min(view.line(s.b).b, s.b + count)
                x_limit = max(0, x_limit)
                return Region(s.a, x_limit)

            if mode in (VISUAL, VISUAL_BLOCK):
                if s.a < s.b:
                    x_limit = min(view.full_line(s.b - 1).b, s.b + count)
                    return Region(s.a, x_limit)

                if s.a > s.b:
                    x_limit = min(view.full_line(s.b).b - 1, s.b + count)
                    if view.substr(s.b) == '\n':
                        return s

                    if view.line(s.a) == view.line(s.b) and count >= s.size():
                        x_limit = min(view.full_line(s.b).b, s.b + count + 1)
                        return Region(s.a - 1, x_limit)

                    return Region(s.a, x_limit)

            return s

        regions_transformer(self.view, f)


class nv_vi_h(TextCommand):
    def run(self, edit, mode=None, count=1):
        def f(view, s):
            if mode == INTERNAL_NORMAL:
                x_limit = max(view.line(s.b).a, s.b - count)
                return Region(s.a, x_limit)

            # TODO: Split handling of the two modes for clarity.
            elif mode in (VISUAL, VISUAL_BLOCK):

                if s.a < s.b:
                    if mode == VISUAL_BLOCK and self.view.rowcol(s.b - 1)[1] == baseline:
                        return s

                    x_limit = max(view.line(s.b - 1).a + 1, s.b - count)
                    if view.line(s.a) == view.line(s.b - 1) and count >= s.size():
                        x_limit = max(view.line(s.b - 1).a, s.b - count - 1)
                        return Region(s.a + 1, x_limit)
                    return Region(s.a, x_limit)

                if s.a > s.b:
                    x_limit = max(view.line(s.b).a, s.b - count)
                    return Region(s.a, x_limit)

            elif mode == NORMAL:
                x_limit = max(view.line(s.b).a, s.b - count)
                return Region(x_limit, x_limit)

            # XXX: We should never reach this.
            return s

        # For jagged selections (on the rhs), only those sticking out need to move leftwards.
        # Example ([] denotes the selection):
        #
        #   10 foo bar foo [bar]
        #   11 foo bar foo [bar foo bar]
        #   12 foo bar foo [bar foo]
        #
        #  Only lines 11 and 12 should move when we press h.
        baseline = 0
        if mode == VISUAL_BLOCK:
            sel = self.view.sel()[0]
            if sel.a < sel.b:
                min_ = min(self.view.rowcol(r.b - 1)[1] for r in self.view.sel())
                if any(self.view.rowcol(r.b - 1)[1] != min_ for r in self.view.sel()):
                    baseline = min_

        regions_transformer(self.view, f)


class nv_vi_j(TextCommand):

    def run(self, edit, mode=None, count=1, xpos=0):
        def f(view, s):
            nonlocal xpos

            if mode == NORMAL:
                current_row = view.rowcol(s.b)[0]
                target_row = min(current_row + count, view.rowcol(view.size())[0])
                invisible_rows = folded_rows(view, view.line(s.b).b + 1)
                target_pt = view.text_point(target_row + invisible_rows, 0)
                target_pt = next_non_folded_pt(view, target_pt)

                if view.line(target_pt).empty():
                    s = Region(target_pt, target_pt)
                else:
                    s = Region(calculate_xpos(view, target_pt, xpos)[0])
            elif mode == INTERNAL_NORMAL:
                current_row = view.rowcol(s.b)[0]
                target_row = min(current_row + count, view.rowcol(view.size())[0])
                target_pt = view.text_point(target_row, 0)
                s = Region(view.line(s.a).a, view.full_line(target_pt).b)
            elif mode == VISUAL:
                exact_position = s.b - 1 if (s.a < s.b) else s.b
                current_row = view.rowcol(exact_position)[0]
                target_row = min(current_row + count, view.rowcol(view.size())[0])
                target_pt = view.text_point(target_row, 0)
                _, xpos = calculate_xpos(view, target_pt, xpos)
                end = min(self.view.line(target_pt).b, target_pt + xpos)

                if s.a < s.b:
                    s = Region(s.a, end + 1)
                elif (target_pt + xpos) >= s.a:
                    s = Region(s.a - 1, end + 1)
                else:
                    s = Region(s.a, target_pt + xpos)
            elif mode == VISUAL_LINE:
                if s.a < s.b:
                    current_row = view.rowcol(s.b - 1)[0]
                    target_row = min(current_row + count, view.rowcol(view.size())[0])
                    target_pt = view.text_point(target_row, 0)

                    s = Region(s.a, view.full_line(target_pt).b)
                elif s.a > s.b:
                    current_row = view.rowcol(s.b)[0]
                    target_row = min(current_row + count, view.rowcol(view.size())[0])
                    target_pt = view.text_point(target_row, 0)

                    if target_row > view.rowcol(s.a - 1)[0]:
                        s = Region(view.line(s.a - 1).a, view.full_line(target_pt).b)
                    else:
                        s = Region(s.a, view.full_line(target_pt).a)

            return s

        if mode == VISUAL_BLOCK:
            visual_block = VisualBlockSelection(self.view)
            row, col = visual_block.rowcolb()
            next_line = self.view.full_line(self.view.text_point(row + count, 0))
            next_line_row, next_line_max_col = self.view.rowcol(next_line.b - 1)
            next_line_target_col = min(max(col, get_xpos(self.view)), next_line_max_col)
            next_line_target_pt = self.view.text_point(next_line_row, next_line_target_col)
            visual_block.transform_target(next_line_target_pt)
            return

        regions_transformer(self.view, f)


class nv_vi_k(TextCommand):

    def run(self, edit, mode=None, count=1, xpos=0):
        def f(view, s):
            nonlocal xpos

            if mode == NORMAL:
                current_row = view.rowcol(s.b)[0]
                target_row = min(current_row - count, view.rowcol(view.size())[0])
                target_pt = view.text_point(target_row, 0)
                target_pt = previous_non_folded_pt(view, target_pt)

                if view.line(target_pt).empty():
                    s = Region(target_pt, target_pt)
                else:
                    s = Region(calculate_xpos(view, target_pt, xpos)[0])
            elif mode == INTERNAL_NORMAL:
                current_row = view.rowcol(s.b)[0]
                target_row = min(current_row - count, view.rowcol(view.size())[0])
                target_pt = view.text_point(target_row, 0)
                s = Region(view.full_line(s.a).b, view.line(target_pt).a)
            elif mode == VISUAL:
                exact_position = s.b - 1 if (s.a < s.b) else s.b
                current_row = view.rowcol(exact_position)[0]
                target_row = max(current_row - count, 0)
                target_pt = view.text_point(target_row, 0)
                _, xpos = calculate_xpos(view, target_pt, xpos)
                end = min(self.view.line(target_pt).b, target_pt + xpos)
                if s.b >= s.a:
                    if (self.view.line(s.a).contains(s.b - 1) and not self.view.line(s.a).contains(target_pt)):
                        s = Region(s.a + 1, end)
                    else:
                        if (target_pt + xpos) < s.a:
                            s = Region(s.a + 1, end)
                        else:
                            s = Region(s.a, end + 1)
                else:
                    s = Region(s.a, end)
            elif mode == VISUAL_LINE:
                if s.a < s.b:
                    current_row = view.rowcol(s.b - 1)[0]
                    target_row = min(current_row - count, view.rowcol(view.size())[0])
                    target_pt = view.text_point(target_row, 0)

                    if target_row < view.rowcol(s.begin())[0]:
                        s = Region(view.full_line(s.a).b, view.full_line(target_pt).a)
                    else:
                        s = Region(s.a, view.full_line(target_pt).b)
                elif s.a > s.b:
                    current_row = view.rowcol(s.b)[0]
                    target_row = max(current_row - count, 0)
                    target_pt = view.text_point(target_row, 0)

                    s = Region(s.a, view.full_line(target_pt).a)

            return s

        if mode == VISUAL_BLOCK:
            visual_block = VisualBlockSelection(self.view)
            row, col = visual_block.rowcolb()
            prev_line = self.view.full_line(self.view.text_point(row - count, 0))
            prev_line_row, prev_line_max_col = self.view.rowcol(prev_line.b - 1)
            prev_line_target_col = min(max(col, get_xpos(self.view)), prev_line_max_col)
            prev_line_target_pt = self.view.text_point(prev_line_row, prev_line_target_col)
            visual_block.transform_target(prev_line_target_pt)
            return

        regions_transformer(self.view, f)


class nv_vi_gg(TextCommand):
    def run(self, edit, mode=None, count=None):
        if count:
            GotoView(self.view, mode, count).line()
            return

        def t(view) -> int:
            return next_non_blank(view, 0)

        def f(view, s):
            if mode == NORMAL:
                resolve_normal_target(s, t(view))
            elif mode == VISUAL:
                resolve_visual_target(s, t(view))
            elif mode == VISUAL_LINE:
                resolve_visual_line_target(view, s, 0)
            elif mode == INTERNAL_NORMAL:
                s = Region(view.full_line(s.b).b, 0)

            return s

        with jumplist_updater(self.view):
            if mode == VISUAL_BLOCK:
                resolve_visual_block_target(self.view, t(self.view))
                return

            regions_transformer(self.view, f)


class nv_vi_big_g(TextCommand):
    def run(self, edit, mode=None, count=None):
        if count:
            GotoView(self.view, mode, count).line()
            return

        def t(view) -> int:
            return get_linewise_non_blank_target(view, target)

        def f(view, s):
            if mode == NORMAL:
                resolve_normal_target(s, t(view))
            elif mode == VISUAL:
                resolve_visual_target(s, t(view))
            elif mode == VISUAL_LINE:
                resolve_visual_line_target(view, s, target)
            elif mode == INTERNAL_NORMAL:
                s = Region(max(0, view.line(s.b).a), target)

            return s

        target = self.view.size()

        with jumplist_updater(self.view):
            if mode == VISUAL_BLOCK:
                resolve_visual_block_target(self.view, t(self.view))
                return

            regions_transformer(self.view, f)


class nv_vi_dollar(TextCommand):
    def run(self, edit, mode=None, count=1):
        def _get_target(view, start, count):
            if count > 1:
                start = view.text_point(row_at(view, start) + (count - 1), 0)

            target = view.line(start).b

            return target

        if mode == VISUAL_BLOCK:
            resolve_visual_block_target(self.view, _get_target, count)
            return

        def f(view, s):
            target = _get_target(view, get_insertion_point_at_b(s), count)

            if mode == NORMAL:
                resolve_normal_target(s, target if view.line(target).empty() else (target - 1))
            elif mode == VISUAL:
                resolve_visual_target(s, target)
            elif mode == VISUAL_LINE:
                resolve_visual_line_target(view, s, target)
            elif mode == INTERNAL_NORMAL:
                if count > 1 and view.rowcol(s.a)[1] == 0:
                    target += 1

                s.b = target

            return s

        regions_transformer(self.view, f)


class nv_vi_w(TextCommand):
    def run(self, edit, mode=None, count=1):
        if mode == VISUAL_BLOCK:
            resolve_visual_block_target(self.view, word_starts, count)
            return

        def f(view, s):
            target = word_starts(view, get_insertion_point_at_b(s), count, internal=(mode == INTERNAL_NORMAL))

            if mode == NORMAL:
                resolve_normal_target(s, fixup_eof(view, target))
            elif mode == VISUAL:
                resolve_visual_target(s, target)
            elif mode == INTERNAL_NORMAL:
                if (not view.substr(view.line(s.a)).strip() and view.line(s.b) != view.line(target)):
                    s.a = view.line(s.a).a

                s.b = target

            return s

        regions_transformer(self.view, f)


class nv_vi_big_w(TextCommand):
    def run(self, edit, mode=None, count=1):
        if mode == VISUAL_BLOCK:
            resolve_visual_block_target(self.view, big_word_starts, count)
            return

        def f(view, s):
            target = big_word_starts(view, get_insertion_point_at_b(s), count, internal=(mode == INTERNAL_NORMAL))

            if mode == NORMAL:
                resolve_normal_target(s, fixup_eof(view, target))
            elif mode == VISUAL:
                resolve_visual_target(s, target)
            elif mode == INTERNAL_NORMAL:
                if (not view.substr(view.line(s.a)).strip() and view.line(s.b) != view.line(target)):
                    s.a = view.line(s.a).a

                s.b = target

            return s

        regions_transformer(self.view, f)


class nv_vi_e(TextCommand):
    def run(self, edit, mode=None, count=1):
        def _get_target(view, start, count):
            # TODO Is the word_ends() function off-by-one?
            return word_ends(view, start, count) - 1

        if mode == VISUAL_BLOCK:
            resolve_visual_block_target(self.view, _get_target, count)
            return

        def f(view, s):
            target = _get_target(view, get_insertion_point_at_b(s), count)

            if mode == NORMAL:
                resolve_normal_target(s, target)
            elif mode == VISUAL:
                resolve_visual_target(s, target)
            elif mode == INTERNAL_NORMAL:
                if (not view.substr(view.line(s.a)).strip() and view.line(s.b) != view.line(target)):
                    if view.line(s.a).empty():
                        target += 1

                    s.a = view.line(s.a).a

                s.b = target + 1

            return s

        regions_transformer(self.view, f)


class nv_vi_zero(TextCommand):
    def run(self, edit, mode=None, count=1):
        def _get_target(view, start, count):
            return view.line(start).a

        if mode == VISUAL_BLOCK:
            resolve_visual_block_target(self.view, _get_target, count)
            return

        def f(view, s):
            target = _get_target(view, get_insertion_point_at_b(s), count)

            if mode == NORMAL:
                resolve_normal_target(s, target)
            elif mode == VISUAL:
                resolve_visual_target(s, target)
            elif mode == VISUAL_LINE:
                resolve_visual_line_target(view, s, target)
            elif mode == INTERNAL_NORMAL:
                s.b = target

            return s

        regions_transformer(self.view, f)


class nv_vi_right_brace(TextCommand):
    def run(self, edit, mode=None, count=1):
        def f(view, s):
            target = next_paragraph_start(view, get_insertion_point_at_b(s), count)

            if mode == NORMAL:
                resolve_normal_target(s, target)
            elif mode == VISUAL:
                resolve_visual_target(s, target)
            elif mode == VISUAL_LINE:
                resolve_visual_line_target(view, s, target)
            elif mode == INTERNAL_NORMAL:
                if target == (view.size() - 1):
                    s = Region(s.a, view.size())
                elif view.substr(s.a - 1) == '\n' or s.a == 0:
                    s.b = target
                else:
                    s = Region(s.a, target - 1)

            return s

        regions_transformer(self.view, f)


class nv_vi_left_brace(TextCommand):
    def run(self, edit, mode=None, count=1):
        def f(view, s):
            target = prev_paragraph_start(view, get_insertion_point_at_b(s), count)

            if mode == NORMAL:
                resolve_normal_target(s, target)
            elif mode == VISUAL:
                resolve_visual_target(s, target)
            elif mode == VISUAL_LINE:
                start = prev_non_ws(view, s.b - 1)
                par_as_region = view.expand_by_class(start, CLASS_EMPTY_LINE)
                target = par_as_region.a
                resolve_visual_line_target(view, s, target)
            elif mode == INTERNAL_NORMAL:
                s.b = target

            return s

        regions_transformer(self.view, f)


class nv_vi_percent(TextCommand):

    def run(self, edit, mode=None, count=None):
        if count:
            # {count}% Go to {count} percentage in the file, on the first non-blank
            # in the line linewise. To compute the new line number this formula is
            # used: ({count} * number-of-lines + 99) / 100
            row = self.view.rowcol(self.view.size())[0] * (count / 100)

            def f(view, s):
                return Region(view.text_point(row, 0))

            regions_transformer(self.view, f)
            show_if_not_visible(self.view)
        else:
            def f(view, s):
                if mode == NORMAL:
                    target = find_next_item_match_pt(view, s)
                    if target is not None:
                        resolve_normal_target(s, target)
                elif mode == VISUAL:
                    target = find_next_item_match_pt(view, s)
                    if target is not None:
                        resolve_visual_target(s, target)
                elif mode == VISUAL_LINE:
                    if s.a > s.b:
                        target = find_next_item_match_pt(view, Region(s.b, self.view.line(s.b).end()))
                    else:
                        target = find_next_item_match_pt(view, Region(s.a, s.b - 1))

                    if target is not None:
                        resolve_visual_line_target(view, s, target)
                elif mode == INTERNAL_NORMAL:
                    found = find_next_item_match_pt(view, s)
                    if found is not None:
                        if found < s.a:
                            s.a += 1
                            s.b = found
                        else:
                            s.b = found + 1

                return s

            regions_transformer(self.view, f)


class nv_vi_big_h(TextCommand):
    def run(self, edit, mode=None, count=None):
        def f(view, s):
            if mode == NORMAL:
                resolve_normal_target(s, target)
            elif mode == VISUAL:
                resolve_visual_target(s, target)
            elif mode == VISUAL_LINE:
                resolve_visual_line_target(view, s, target)
            elif mode == INTERNAL_NORMAL:
                resolve_internal_normal_target(view, s, target, linewise=True)

            return s

        target = next_non_blank(self.view, highest_visible_pt(self.view))
        regions_transformer(self.view, f)


class nv_vi_big_l(TextCommand):
    def run(self, edit, mode=None, count=None):
        def f(view, s):
            if mode == NORMAL:
                resolve_normal_target(s, target)
            elif mode == VISUAL:
                resolve_visual_target(s, target)
            elif mode == VISUAL_LINE:
                resolve_visual_line_target(view, s, target)
            elif mode == INTERNAL_NORMAL:
                resolve_internal_normal_target(view, s, target, linewise=True)

            return s

        target = next_non_blank(self.view, lowest_visible_pt(self.view))
        regions_transformer(self.view, f)


class nv_vi_big_m(TextCommand):
    def run(self, edit, mode=None, count=None):
        def f(view, s):
            if mode == NORMAL:
                resolve_normal_target(s, target)
            elif mode == VISUAL:
                resolve_visual_target(s, target)
            elif mode == VISUAL_LINE:
                resolve_visual_line_target(view, s, target)
            elif mode == INTERNAL_NORMAL:
                resolve_internal_normal_target(view, s, target, linewise=True)

            return s

        highest_row, lowest_row = highlow_visible_rows(self.view)
        half_visible_lines = (lowest_row - highest_row) // 2
        middle_row = highest_row + half_visible_lines
        target = next_non_blank(self.view, self.view.text_point(middle_row, 0))
        regions_transformer(self.view, f)


class nv_vi_star(TextCommand):
    def run(self, edit, mode=None, count=1, pattern=None, save=True):
        def f(view, s):
            match = find_wrapping(
                view,
                term=pattern,
                start=view.word(s.end()).end(),
                end=view.size(),
                flags=flags,
                times=count
            )

            if match:
                if mode == NORMAL:
                    resolve_normal_target(s, match.begin())
                elif mode == VISUAL:
                    resolve_visual_target(s, match.begin())
                elif mode == INTERNAL_NORMAL:
                    s.b = match.begin()

            return s

        word = pattern or get_string_under_cursor(self.view)
        if not word.strip():
            ui_bell('E348: No string under cursor')
            return

        # All cursors must be on the same word.
        if len(set([self.view.substr(self.view.word(sel.end())) for sel in self.view.sel()])) != 1:
            return

        pattern, flags = process_word_search_pattern(self.view, word)

        with jumplist_updater(self.view):
            regions_transformer(self.view, f)

        add_search_highlighting(self.view, find_word_search_occurrences(self.view, pattern, flags))

        if save:
            set_last_search_pattern(self.view, word, 'nv_vi_star')

        show_if_not_visible(self.view)


class nv_vi_octothorp(TextCommand):
    def run(self, edit, mode=None, count=1, pattern=None, save=True):
        def f(view, s):
            match = reverse_find_wrapping(
                view,
                term=pattern,
                start=0,
                end=(s.b if s.a > s.b else s.a),
                flags=flags,
                times=count
            )

            if match:
                if mode == NORMAL:
                    resolve_normal_target(s, match.begin())
                elif mode == VISUAL:
                    resolve_visual_target(s, match.begin())
                elif mode == INTERNAL_NORMAL:
                    s.a = s.b
                    s.b = match.begin()

            return s

        word = pattern or get_string_under_cursor(self.view)
        if not word.strip():
            ui_bell('E348: No string under cursor')
            return

        # All cursors must be on the same word.
        if len(set([self.view.substr(self.view.word(sel.end())) for sel in self.view.sel()])) != 1:
            return

        pattern, flags = process_word_search_pattern(self.view, word)

        with jumplist_updater(self.view):
            regions_transformer(self.view, f)

        add_search_highlighting(self.view, find_word_search_occurrences(self.view, pattern, flags))

        if save:
            set_last_search_pattern(self.view, word, 'nv_vi_octothorp')

        show_if_not_visible(self.view)


class nv_vi_b(TextCommand):
    def run(self, edit, mode=None, count=1):
        if mode == VISUAL_BLOCK:
            resolve_visual_block_target(self.view, word_reverse, count)
            return

        def f(view, s):
            target = word_reverse(view, get_insertion_point_at_b(s), count)

            if mode == NORMAL:
                resolve_normal_target(s, target)
            elif mode == VISUAL:
                resolve_visual_target(s, target)
            elif mode == INTERNAL_NORMAL:
                s.b = target

            return s

        regions_transformer(self.view, f)


class nv_vi_big_b(TextCommand):

    def run(self, edit, mode=None, count=1):
        if mode == VISUAL_BLOCK:
            resolve_visual_block_target(self.view, big_word_reverse, count)
            return

        def f(view, s):
            target = big_word_reverse(view, get_insertion_point_at_b(s), count)

            if mode == NORMAL:
                resolve_normal_target(s, target)
            elif mode == VISUAL:
                resolve_visual_target(s, target)
            elif mode == INTERNAL_NORMAL:
                s.b = target

            return s

        regions_transformer(self.view, f)


class nv_vi_underscore(TextCommand):
    def run(self, edit, mode=None, count=1):
        def _get_target(view, start, count):
            current_row = view.rowcol(start)[0]
            last_row = view.rowcol(view.size() - 1)[0]
            target_row = current_row + (count - 1)
            if target_row > last_row:
                target_row = last_row

            return next_non_blank(view, view.text_point(target_row, 0))

        if mode == VISUAL_BLOCK:
            resolve_visual_block_target(self.view, _get_target, count)
            return

        def f(view, s):
            target = _get_target(view, get_insertion_point_at_b(s), count)

            if mode == NORMAL:
                resolve_normal_target(s, target)
            elif mode == VISUAL:
                resolve_visual_target(s, target)
            elif mode == VISUAL_LINE:
                resolve_visual_line_target(view, s, target)
            elif mode == INTERNAL_NORMAL:
                resolve_internal_normal_target(view, s, target, linewise=True)

            return s

        regions_transformer(self.view, f)


class nv_vi_hat(TextCommand):
    def run(self, edit, mode=None, count=None):
        def _get_target(view, start, count):
            return next_non_blank(view, view.line(start).a)

        if mode == VISUAL_BLOCK:
            resolve_visual_block_target(self.view, _get_target, count)
            return

        def f(view, s):
            target = _get_target(view, get_insertion_point_at_b(s), count)

            if mode == NORMAL:
                resolve_normal_target(s, target)
            elif mode == VISUAL:
                resolve_visual_target(s, target)
            elif mode == INTERNAL_NORMAL:
                s.b = target

            return s

        regions_transformer(self.view, f)


class nv_vi_gj(TextCommand):
    def run(self, edit, mode=None, count=1):
        if mode == NORMAL:
            for i in range(count):
                self.view.run_command('move', {'by': 'lines', 'forward': True, 'extend': False})
        elif mode == VISUAL:
            for i in range(count):
                self.view.run_command('move', {'by': 'lines', 'forward': True, 'extend': True})
        elif mode == VISUAL_LINE:
            self.view.run_command('nv_vi_j', {'mode': mode, 'count': count})
        elif mode == INTERNAL_NORMAL:
            for i in range(count):
                self.view.run_command('move', {'by': 'lines', 'forward': True, 'extend': False})


class nv_vi_gk(TextCommand):
    def run(self, edit, mode=None, count=1):
        if mode == NORMAL:
            for i in range(count):
                self.view.run_command('move', {'by': 'lines', 'forward': False, 'extend': False})
        elif mode == VISUAL:
            for i in range(count):
                self.view.run_command('move', {'by': 'lines', 'forward': False, 'extend': True})
        elif mode == VISUAL_LINE:
            self.view.run_command('nv_vi_k', {'mode': mode, 'count': count})
        elif mode == INTERNAL_NORMAL:
            for i in range(count):
                self.view.run_command('move', {'by': 'lines', 'forward': False, 'extend': False})


class nv_vi_g__(TextCommand):
    def run(self, edit, mode=None, count=1):
        def _get_target(view, start, count):
            current_row = view.rowcol(start)[0]
            last_row = view.rowcol(view.size() - 1)[0]
            target_row = current_row + (count - 1)
            if target_row > last_row:
                target_row = last_row

            line = view.line(view.text_point(target_row, 0))
            target = prev_non_blank(view, line.b - 1) if line.size() else line.b

            return target

        if mode == VISUAL_BLOCK:
            resolve_visual_block_target(self.view, _get_target, count)
            return

        def f(view, s):
            target = _get_target(view, get_insertion_point_at_b(s), count)

            if mode == NORMAL:
                resolve_normal_target(s, target)
            elif mode == VISUAL:
                resolve_visual_target(s, target)
            elif mode == VISUAL_LINE:
                resolve_visual_line_target(view, s, target)
            elif mode == INTERNAL_NORMAL:
                s.b = target + 1

            return s

        regions_transformer(self.view, f)


class nv_vi_ctrl_u(TextCommand):
    def run(self, edit, mode=None, count=0):
        if mode == INSERT:
            def t(view, s):
                s.a = view.line(get_insertion_point_at_b(s)).a
                return s

            regions_transformer(self.view, t)
            self.view.run_command('left_delete')
            return

        def f(view, s):
            if mode == NORMAL:
                resolve_normal_target(s, target)
            elif mode == VISUAL:
                resolve_visual_target(s, target)
            elif mode == VISUAL_LINE:
                resolve_visual_line_target(view, s, target)
            elif mode == INTERNAL_NORMAL:
                s.b = target

            return s

        number_of_scroll_lines = count if count >= 1 else get_option_scroll(self.view)
        target = get_scroll_up_target_pt(self.view, number_of_scroll_lines)
        if target is None:
            return ui_bell()

        regions_transformer(self.view, f)
        if not self.view.visible_region().contains(0):
            scroll_viewport_position(self.view, number_of_scroll_lines, forward=False)


class nv_vi_ctrl_d(TextCommand):
    def run(self, edit, mode=None, count=0):
        def f(view, s):
            if mode == NORMAL:
                resolve_normal_target(s, target)
            elif mode == VISUAL:
                resolve_visual_target(s, target)
            elif mode == VISUAL_LINE:
                resolve_visual_line_target(view, s, target)
            elif mode == INTERNAL_NORMAL:
                s.b = target

            return s

        number_of_scroll_lines = count if count >= 1 else get_option_scroll(self.view)
        target = get_scroll_down_target_pt(self.view, number_of_scroll_lines)
        if target is None:
            return ui_bell()

        regions_transformer(self.view, f)
        if not self.view.visible_region().contains(self.view.size()):
            scroll_viewport_position(self.view, number_of_scroll_lines)


class nv_vi_bar(TextCommand):
    def run(self, edit, mode=None, count=1):
        def _get_target(view, start, col):
            line = view.line(start)
            if line.empty():
                return start

            target = line.a + (col - 1)
            if target >= line.b:
                target = line.b - 1

            return target

        if mode == VISUAL_BLOCK:
            resolve_visual_block_target(self.view, _get_target, count)
            return

        def f(view, s):
            target = _get_target(view, get_insertion_point_at_b(s), count)

            if mode == NORMAL:
                resolve_normal_target(s, target)
            elif mode == VISUAL:
                resolve_visual_target(s, target)
            elif mode == INTERNAL_NORMAL:
                s.b = target

            return s

        regions_transformer(self.view, f)


class nv_vi_ge(TextCommand):
    def run(self, edit, mode=None, count=1):
        if mode == VISUAL_BLOCK:
            resolve_visual_block_target(self.view, word_end_reverse, count)
            return

        def f(view, s):
            target = word_end_reverse(view, get_insertion_point_at_b(s), count)

            if mode == NORMAL:
                resolve_normal_target(s, target)
            elif mode == VISUAL:
                resolve_visual_target(s, target)
            elif mode == INTERNAL_NORMAL:
                resolve_internal_normal_target(view, s, target, inclusive=True)

            return s

        regions_transformer(self.view, f)


class nv_vi_g_big_e(TextCommand):
    def run(self, edit, mode=None, count=1):
        if mode == VISUAL_BLOCK:
            resolve_visual_block_target(self.view, big_word_end_reverse, count)
            return

        def f(view, s):
            target = big_word_end_reverse(view, get_insertion_point_at_b(s), count)

            if mode == NORMAL:
                resolve_normal_target(s, target)
            elif mode == VISUAL:
                resolve_visual_target(s, target)
            elif mode == INTERNAL_NORMAL:
                resolve_internal_normal_target(view, s, target, inclusive=True)

            return s

        regions_transformer(self.view, f)


class nv_vi_left_paren(TextCommand):

    def run(self, edit, mode=None, count=1):
        def f(view, s):
            start = s.a if s.b >= s.a else s.b
            previous_sentence = find_sentences_backward(view, start, count)
            target = previous_sentence.a

            if mode == NORMAL:
                resolve_normal_target(s, target)
            elif mode == VISUAL:
                resolve_visual_target(s, target)
            elif mode == VISUAL_LINE:
                resolve_visual_line_target(view, s, target)
            elif mode == INTERNAL_NORMAL:
                s.b = target

            return s

        regions_transformer(self.view, f)


class nv_vi_right_paren(TextCommand):

    def run(self, edit, mode=None, count=1):
        def f(view, s):
            next_sentence = find_sentences_forward(view, s, count)
            if next_sentence is None:
                return s

            target = next_sentence.b

            if mode == NORMAL:
                resolve_normal_target(s, min(target, view.size() - 1))
            elif mode == VISUAL:
                s = Region(s.a, min(target + 1, view.size() - 1))
            elif mode == VISUAL_LINE:
                resolve_visual_line_target(view, s, target)
            elif mode == INTERNAL_NORMAL:
                s.b = target

            return s

        regions_transformer(self.view, f)


class nv_vi_question_mark_impl(TextCommand):
    def run(self, edit, pattern, mode=None, count=1, save=True):
        if not pattern:
            pattern = get_last_search_pattern(self.view)
            if not pattern:
                ui_bell('E35: no previous regular expression')
                return

        if save:
            set_last_search_pattern(self.view, pattern, 'nv_vi_question_mark')

        sel = self.view.sel()[0]
        pattern, flags = process_search_pattern(self.view, pattern)
        start = 0
        end = sel.b + 1 if not sel.empty() else sel.b

        match = reverse_find_wrapping(self.view,
                                      term=pattern,
                                      start=start,
                                      end=end,
                                      flags=flags,
                                      times=count)

        if not match:
            return status_message('E486: Pattern not found: %s', pattern)

        def f(view, s):
            if mode == NORMAL:
                resolve_normal_target(s, target)
            elif mode == VISUAL:
                resolve_visual_target(s, target)
            elif mode == VISUAL_LINE:
                resolve_visual_line_target(view, s, target)
            elif mode == INTERNAL_NORMAL:
                s.a, s.b = s.end(), target

            return s

        target = get_insertion_point_at_a(match)
        regions_transformer(self.view, f)
        add_search_highlighting(self.view, find_search_occurrences(self.view, pattern, flags))


class nv_vi_question_mark(TextCommand):

    def run(self, edit, pattern=''):
        set_reset_during_init(self.view, False)

        self._cmdline = Cmdline(
            self.view,
            Cmdline.SEARCH_BACKWARD,
            self.on_done,
            self.on_change,
            self.on_cancel
        )

        self._cmdline.prompt(pattern)

    def on_done(self, pattern: str):
        history_update(Cmdline.SEARCH_BACKWARD + pattern)
        nv_cmdline_feed_key.reset_last_history_index()
        clear_search_highlighting(self.view)
        append_sequence(self.view, pattern + '<CR>')
        set_motion(self.view, ViSearchBackwardImpl(term=pattern))
        evaluate_state(self.view)

    def on_change(self, pattern: str):
        count = get_count(self.view)
        sel = self.view.sel()[0]
        pattern, flags = process_search_pattern(self.view, pattern)
        start = 0
        end = sel.b + 1 if not sel.empty() else sel.b

        match = reverse_find_wrapping(self.view,
                                      term=pattern,
                                      start=start,
                                      end=end,
                                      flags=flags,
                                      times=count)

        clear_search_highlighting(self.view)

        if not match:
            return status_message('E486: Pattern not found: %s', pattern)

        add_search_highlighting(self.view, find_search_occurrences(self.view, pattern, flags), [match])
        show_if_not_visible(self.view, match)

    def on_cancel(self):
        clear_search_highlighting(self.view)
        reset_command_data(self.view)
        nv_cmdline_feed_key.reset_last_history_index()
        show_if_not_visible(self.view)


class nv_vi_repeat_buffer_search(TextCommand):

    commands = {
        'nv_vi_slash': ['nv_vi_slash_impl', 'nv_vi_question_mark_impl'],
        'nv_vi_question_mark': ['nv_vi_question_mark_impl', 'nv_vi_slash_impl'],
        'nv_vi_star': ['nv_vi_star', 'nv_vi_octothorp'],
        'nv_vi_octothorp': ['nv_vi_octothorp', 'nv_vi_star'],
    }

    def run(self, edit, mode=None, count=1, reverse=False):
        last_pattern = get_last_search_pattern(self.view)
        last_command = get_last_search_pattern_command(self.view)
        command = self.commands[last_command][int(reverse)]

        _log.debug('repeat search %s reverse=%s -> %s (pattern=%s)', last_command, reverse, command, last_pattern)

        self.view.run_command(command, {
            'mode': mode,
            'count': count,
            'pattern': last_pattern,
            'save': False
        })

        self.view.show(self.view.sel(), show_surrounds=True)


class nv_vi_search(TextCommand):

    def run(self, edit, mode=None, count=1, forward=True):
        last_search = get_last_search_pattern(self.view)

        def f(view, s):
            b = get_insertion_point_at_b(s)

            if forward:
                start = prev_blank(view, b) if mode in (NORMAL, INTERNAL_NORMAL) else b
                target = find_wrapping(self.view, last_search, start, self.view.size())
                if target is not None:
                    if mode in (NORMAL, INTERNAL_NORMAL):
                        s.a = target.a
                        s.b = target.a + 1

                    resolve_visual_target(s, target.b - 1)

            else:
                start = next_blank(view, b) if mode in (NORMAL, INTERNAL_NORMAL) else b
                target = reverse_find_wrapping(self.view, last_search, 0, start)
                if target is not None:
                    if mode in (NORMAL, INTERNAL_NORMAL):
                        s.a = target.b
                        s.b = target.b - 1

                    resolve_visual_target(s, target.a)

            return s

        regions_transformer(self.view, f)

        # Ensure we're in Visual mode, but only if a match was found.
        if mode in (NORMAL, VISUAL_LINE, VISUAL_BLOCK):
            for sel in self.view.sel():
                if not sel.empty():
                    enter_visual_mode(self.view, mode)
                    break


class nv_vi_big_e(TextCommand):
    def run(self, edit, mode=None, count=1):
        def _get_target(view, start, count):
            # TODO Is the big_word_ends() function off-by-one?
            return big_word_ends(view, start, count) - 1

        if mode == VISUAL_BLOCK:
            resolve_visual_block_target(self.view, _get_target, count)
            return

        def f(view, s):
            target = _get_target(view, get_insertion_point_at_b(s), count)

            if mode == NORMAL:
                resolve_normal_target(s, target)
            elif mode == VISUAL:
                resolve_visual_target(s, target)
            elif mode == INTERNAL_NORMAL:
                resolve_internal_normal_target(view, s, target, inclusive=True)

            return s

        regions_transformer(self.view, f)


class nv_vi_ctrl_f(TextCommand):
    def run(self, edit, mode=None, count=1):
        if mode == NORMAL:
            self.view.run_command('move', {'by': 'pages', 'forward': True})
        elif mode == VISUAL:
            self.view.run_command('move', {'by': 'pages', 'forward': True, 'extend': True})
        elif mode == VISUAL_LINE:
            self.view.run_command('move', {'by': 'pages', 'forward': True, 'extend': True})

            new_sels = []
            for sel in self.view.sel():
                line = self.view.full_line(sel.b)
                if sel.b > sel.a:
                    new_sels.append(Region(sel.a, line.end()))
                else:
                    new_sels.append(Region(sel.a, line.begin()))

            if new_sels:
                set_selection(self.view, new_sels)


class nv_vi_ctrl_b(TextCommand):
    def run(self, edit, mode=None, count=1):
        if mode == NORMAL:
            self.view.run_command('move', {'by': 'pages', 'forward': False})
        elif mode == VISUAL:
            self.view.run_command('move', {'by': 'pages', 'forward': False, 'extend': True})
        elif mode == VISUAL_LINE:
            self.view.run_command('move', {'by': 'pages', 'forward': False, 'extend': True})

            new_sels = []
            for sel in self.view.sel():
                line = self.view.full_line(sel.b)
                if sel.b > sel.a:
                    new_sels.append(Region(sel.a, line.end()))
                else:
                    new_sels.append(Region(sel.a, line.begin()))

            if new_sels:
                set_selection(self.view, new_sels)


class nv_vi_enter(TextCommand):
    def run(self, edit, mode=None, count=1):
        self.view.run_command('nv_vi_j', {'mode': mode, 'count': count})

        def f(view, s):
            target = next_non_blank(view, get_insertion_point_at_b(s))

            if mode == NORMAL:
                resolve_normal_target(s, target)
            elif mode == VISUAL:
                resolve_visual_target(s, target)
            elif mode == VISUAL_LINE:
                resolve_visual_line_target(view, s, target)

            return s

        regions_transformer(self.view, f)


class nv_vi_minus(TextCommand):
    def run(self, edit, mode=None, count=1):
        self.view.run_command('nv_vi_k', {'mode': mode, 'count': count})

        def f(view, s):
            target = next_non_blank(view, get_insertion_point_at_b(s))

            if mode == NORMAL:
                resolve_normal_target(s, target)
            elif mode == VISUAL:
                resolve_visual_target(s, target)
            elif mode == VISUAL_LINE:
                resolve_visual_line_target(view, s, target)

            return s

        regions_transformer(self.view, f)


class nv_vi_shift_enter(TextCommand):
    def run(self, edit, mode=None, count=1):
        self.view.run_command('nv_vi_ctrl_f', {'mode': mode, 'count': count})


class nv_vi_select_text_object(TextCommand):
    def run(self, edit, text_object=None, mode=None, count=1, extend=False, inclusive=False):
        def f(view, s):
            if mode in (INTERNAL_NORMAL, VISUAL, VISUAL_LINE, VISUAL_BLOCK):
                return get_text_object_region(view, s, text_object,
                                              inclusive=inclusive,
                                              count=count)

            return s

        regions_transformer(self.view, f)


class nv_vi_go_to_symbol(TextCommand):
    """
    Go to local declaration.

    Differs from Vim because it leverages Sublime Text's ability to actually
    locate symbols (Vim simply searches from the top of the file).
    """

    def find_symbol(self, r, globally=False):
        query = self.view.substr(self.view.word(r))
        fname = self.view.file_name().replace('\\', '/')

        locations = self.view.window().lookup_symbol_in_index(query)
        if not locations:
            return

        try:
            if not globally:
                location = [hit[2] for hit in locations if fname.endswith(hit[1])][0]
                return location[0] - 1, location[1] - 1
            else:
                # TODO: There might be many symbols with the same name.
                return locations[0]
        except IndexError:
            return

    def run(self, edit, mode=None, count=1, globally=False):

        def f(view, s):
            if mode == NORMAL:
                return Region(location)
            elif mode == VISUAL:
                return Region(s.a + 1, location)
            elif mode == INTERNAL_NORMAL:
                return Region(s.a, location)

            return s

        current_sel = self.view.sel()[0]
        set_selection(self.view, current_sel)

        location = self.find_symbol(current_sel, globally=globally)
        if not location:
            return

        if globally:
            # Global symbol; simply open the file; not a motion.
            # TODO: Perhaps must be a motion if the target file happens to be
            #       the current one?
            with jumplist_updater(self.view):
                self.view.window().open_file(
                    location[0] + ':' + ':'.join([str(x) for x in location[2]]),
                    ENCODED_POSITION
                )

            return

        # Local symbol; select.
        location = self.view.text_point(*location)

        with jumplist_updater(self.view):
            regions_transformer(self.view, f)


class nv_vi_gm(TextCommand):
    def run(self, edit, mode=None, count=1):
        def f(view, s):
            line = view.line(s.b)
            if line.empty():
                return s

            mid_pt = line.size() // 2
            row_start = view.text_point(row_at(view, s.b), 0)

            return Region(min(row_start + mid_pt, line.b - 1))

        if mode != NORMAL:
            return ui_bell()

        regions_transformer(self.view, f)


class nv_vi_left_square_bracket(TextCommand):
    def run(self, edit, action, mode, count=1, **kwargs):
        goto = GotoView(self.view, mode, count)
        if action == 'c':
            goto.prev_change()
        elif action == 's':
            goto.prev_mispelled_word()
        elif action == 'target':
            goto.prev_target(**kwargs)
        else:
            raise ValueError('unknown action')


class nv_vi_right_square_bracket(TextCommand):
    def run(self, edit, action, mode, count=1, **kwargs):
        goto = GotoView(self.view, mode, count)
        if action == 'c':
            goto.next_change()
        elif action == 's':
            goto.next_mispelled_word()
        elif action == 'target':
            goto.next_target(**kwargs)
        else:
            raise ValueError('unknown action')
