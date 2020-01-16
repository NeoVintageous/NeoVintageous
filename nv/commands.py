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

from functools import partial
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
from sublime_plugin import TextCommand
from sublime_plugin import WindowCommand

from NeoVintageous.nv import macros
from NeoVintageous.nv import rc
from NeoVintageous.nv.cmdline import Cmdline
from NeoVintageous.nv.ex.completions import insert_best_cmdline_completion
from NeoVintageous.nv.ex.completions import on_change_cmdline_completion_prefix
from NeoVintageous.nv.ex.completions import reset_cmdline_completion_state
from NeoVintageous.nv.ex_cmds import do_ex_cmd_edit_wrap
from NeoVintageous.nv.ex_cmds import do_ex_cmdline
from NeoVintageous.nv.ex_cmds import do_ex_command
from NeoVintageous.nv.ex_cmds import do_ex_user_cmdline
from NeoVintageous.nv.goto import goto_help
from NeoVintageous.nv.goto import goto_line
from NeoVintageous.nv.goto import goto_next_change
from NeoVintageous.nv.goto import goto_next_mispelled_word
from NeoVintageous.nv.goto import goto_next_target
from NeoVintageous.nv.goto import goto_prev_change
from NeoVintageous.nv.goto import goto_prev_mispelled_word
from NeoVintageous.nv.goto import goto_prev_target
from NeoVintageous.nv.history import history_get
from NeoVintageous.nv.history import history_get_type
from NeoVintageous.nv.history import history_len
from NeoVintageous.nv.history import history_update
from NeoVintageous.nv.jumplist import jumplist_update
from NeoVintageous.nv.mappings import Mapping
from NeoVintageous.nv.mappings import mappings_can_resolve
from NeoVintageous.nv.mappings import mappings_is_incomplete
from NeoVintageous.nv.mappings import mappings_resolve
from NeoVintageous.nv.marks import add_mark
from NeoVintageous.nv.marks import get_mark_as_encoded_address
from NeoVintageous.nv.polyfill import spell_select
from NeoVintageous.nv.polyfill import split_by_newlines
from NeoVintageous.nv.registers import registers_get_for_paste
from NeoVintageous.nv.registers import registers_op_change
from NeoVintageous.nv.registers import registers_op_delete
from NeoVintageous.nv.registers import registers_op_yank
from NeoVintageous.nv.search import add_search_highlighting
from NeoVintageous.nv.search import calculate_word_search_flags
from NeoVintageous.nv.search import clear_search_highlighting
from NeoVintageous.nv.search import create_word_search_pattern
from NeoVintageous.nv.search import find_all_buffer_search_occurrences
from NeoVintageous.nv.search import find_all_word_search_occurrences
from NeoVintageous.nv.search import get_search_occurrences
from NeoVintageous.nv.search import process_search_pattern
from NeoVintageous.nv.settings import get_last_buffer_search
from NeoVintageous.nv.settings import get_last_buffer_search_command
from NeoVintageous.nv.settings import get_setting
from NeoVintageous.nv.settings import set_last_buffer_search
from NeoVintageous.nv.settings import set_last_buffer_search_command
from NeoVintageous.nv.settings import set_reset_during_init
from NeoVintageous.nv.settings import toggle_ctrl_keys
from NeoVintageous.nv.settings import toggle_side_bar
from NeoVintageous.nv.settings import toggle_super_keys
from NeoVintageous.nv.state import State
from NeoVintageous.nv.state import init_state
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
from NeoVintageous.nv.utils import gluing_undo_groups
from NeoVintageous.nv.utils import hide_panel
from NeoVintageous.nv.utils import highest_visible_pt
from NeoVintageous.nv.utils import highlow_visible_rows
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
from NeoVintageous.nv.utils import replace_sel
from NeoVintageous.nv.utils import resolve_internal_normal_target
from NeoVintageous.nv.utils import resolve_visual_block_target
from NeoVintageous.nv.utils import resolve_visual_line_target
from NeoVintageous.nv.utils import resolve_visual_target
from NeoVintageous.nv.utils import row_at
from NeoVintageous.nv.utils import row_to_pt
from NeoVintageous.nv.utils import save_previous_selection
from NeoVintageous.nv.utils import scroll_horizontally
from NeoVintageous.nv.utils import scroll_viewport_position
from NeoVintageous.nv.utils import set_selection
from NeoVintageous.nv.utils import should_motion_apply_op_transformer
from NeoVintageous.nv.utils import show_if_not_visible
from NeoVintageous.nv.utils import spell_file_add_word
from NeoVintageous.nv.utils import spell_file_remove_word
from NeoVintageous.nv.utils import translate_char
from NeoVintageous.nv.utils import unfold
from NeoVintageous.nv.utils import unfold_all
from NeoVintageous.nv.vi.cmd_base import ViMissingCommandDef
from NeoVintageous.nv.vi.cmd_base import ViOperatorDef
from NeoVintageous.nv.vi.cmd_defs import ViOpenNameSpace
from NeoVintageous.nv.vi.cmd_defs import ViOpenRegister
from NeoVintageous.nv.vi.cmd_defs import ViSearchBackwardImpl
from NeoVintageous.nv.vi.cmd_defs import ViSearchForwardImpl
from NeoVintageous.nv.vi.core import IrreversibleTextCommand
from NeoVintageous.nv.vi.core import ViMotionCommand
from NeoVintageous.nv.vi.core import ViTextCommandBase
from NeoVintageous.nv.vi.core import ViWindowCommandBase
from NeoVintageous.nv.vi.keys import KeySequenceTokenizer
from NeoVintageous.nv.vi.keys import to_bare_command_name
from NeoVintageous.nv.vi.search import find_in_range
from NeoVintageous.nv.vi.search import find_wrapping
from NeoVintageous.nv.vi.search import reverse_find_wrapping
from NeoVintageous.nv.vi.search import reverse_search
from NeoVintageous.nv.vi.settings import get_repeat_data
from NeoVintageous.nv.vi.settings import set_repeat_data
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
from NeoVintageous.nv.vim import INSERT
from NeoVintageous.nv.vim import INTERNAL_NORMAL
from NeoVintageous.nv.vim import NORMAL
from NeoVintageous.nv.vim import OPERATOR_PENDING
from NeoVintageous.nv.vim import REPLACE
from NeoVintageous.nv.vim import SELECT
from NeoVintageous.nv.vim import UNKNOWN
from NeoVintageous.nv.vim import VISUAL
from NeoVintageous.nv.vim import VISUAL_BLOCK
from NeoVintageous.nv.vim import VISUAL_LINE
from NeoVintageous.nv.vim import enter_insert_mode
from NeoVintageous.nv.vim import enter_normal_mode
from NeoVintageous.nv.vim import enter_visual_mode
from NeoVintageous.nv.vim import is_visual_mode
from NeoVintageous.nv.vim import message
from NeoVintageous.nv.vim import run_motion
from NeoVintageous.nv.vim import status_message
from NeoVintageous.nv.window import window_control
from NeoVintageous.nv.window import window_open_file
from NeoVintageous.nv.window import window_tab_control


__all__ = [
    '_enter_insert_mode',
    '_enter_normal_mode',
    '_enter_normal_mode_impl',
    '_enter_replace_mode',
    '_enter_select_mode',
    '_enter_visual_block_mode',
    '_enter_visual_line_mode',
    '_enter_visual_line_mode_impl',
    '_enter_visual_mode',
    '_enter_visual_mode_impl',
    '_nv_cmdline',
    '_nv_cmdline_feed_key',
    '_nv_ex_cmd_edit_wrap',
    '_nv_feed_key',
    '_nv_process_notation',
    '_nv_replace_line',
    '_nv_run_cmds',
    '_vi_a',
    '_vi_at',
    '_vi_b',
    '_vi_backtick',
    '_vi_bar',
    '_vi_big_a',
    '_vi_big_b',
    '_vi_big_c',
    '_vi_big_d',
    '_vi_big_e',
    '_vi_big_g',
    '_vi_big_h',
    '_vi_big_i',
    '_vi_big_j',
    '_vi_big_l',
    '_vi_big_m',
    '_vi_big_n',
    '_vi_big_o',
    '_vi_big_s',
    '_vi_big_w',
    '_vi_big_x',
    '_vi_big_z_big_q',
    '_vi_big_z_big_z',
    '_vi_c',
    '_vi_cc',
    '_vi_ctrl_b',
    '_vi_ctrl_d',
    '_vi_ctrl_e',
    '_vi_ctrl_f',
    '_vi_ctrl_g',
    '_vi_ctrl_r',
    '_vi_ctrl_right_square_bracket',
    '_vi_ctrl_u',
    '_vi_ctrl_w',
    '_vi_ctrl_x_ctrl_l',
    '_vi_ctrl_y',
    '_vi_d',
    '_vi_dd',
    '_vi_dollar',
    '_vi_dot',
    '_vi_e',
    '_vi_enter',
    '_vi_equal',
    '_vi_equal_equal',
    '_vi_find_in_line',
    '_vi_g',
    '_vi_g__',
    '_vi_g_big_e',
    '_vi_g_big_h',
    '_vi_g_big_t',
    '_vi_g_big_u',
    '_vi_g_big_u_big_u',
    '_vi_g_tilde',
    '_vi_g_tilde_g_tilde',
    '_vi_ga',
    '_vi_ge',
    '_vi_gg',
    '_vi_gj',
    '_vi_gk',
    '_vi_gm',
    '_vi_go_to_symbol',
    '_vi_gq',
    '_vi_greater_than',
    '_vi_greater_than_greater_than',
    '_vi_gt',
    '_vi_gu',
    '_vi_guu',
    '_vi_gv',
    '_vi_gx',
    '_vi_h',
    '_vi_hat',
    '_vi_j',
    '_vi_k',
    '_vi_l',
    '_vi_left_brace',
    '_vi_left_paren',
    '_vi_left_square_bracket',
    '_vi_less_than',
    '_vi_less_than_less_than',
    '_vi_m',
    '_vi_minus',
    '_vi_modify_numbers',
    '_vi_n',
    '_vi_o',
    '_vi_octothorp',
    '_vi_paste',
    '_vi_percent',
    '_vi_q',
    '_vi_question_mark',
    '_vi_question_mark_impl',
    '_vi_quote',
    '_vi_r',
    '_vi_repeat_buffer_search',
    '_vi_reverse_find_in_line',
    '_vi_right_brace',
    '_vi_right_paren',
    '_vi_right_square_bracket',
    '_vi_s',
    '_vi_search',
    '_vi_select_big_j',
    '_vi_select_j',
    '_vi_select_k',
    '_vi_select_text_object',
    '_vi_shift_enter',
    '_vi_slash',
    '_vi_slash_impl',
    '_vi_star',
    '_vi_tilde',
    '_vi_u',
    '_vi_underscore',
    '_vi_visual_big_u',
    '_vi_visual_o',
    '_vi_visual_u',
    '_vi_w',
    '_vi_x',
    '_vi_y',
    '_vi_yy',
    '_vi_z',
    '_vi_z_enter',
    '_vi_z_minus',
    '_vi_zero',
    '_vi_zz',
    'Neovintageous',
    'NeovintageousOpenMyRcFileCommand',
    'NeovintageousReloadMyRcFileCommand',
    'NeovintageousToggleSideBarCommand',
    'SequenceCommand'
]


_log = logging.getLogger(__name__)


class _nv_cmdline_feed_key(TextCommand):

    LAST_HISTORY_ITEM_INDEX = None

    def run(self, edit, key):
        if self.view.size() == 0:
            raise RuntimeError('expected a non-empty command-line')

        keys_allow_empty = ('<up>', '<C-n>', '<down>', '<C-p>', '<C-c>', '<C-[>', '<tab>', '<S-tab>')
        if self.view.size() == 1 and key not in keys_allow_empty:
            return

        if key in ('<tab>', '<S-tab>'):
            insert_best_cmdline_completion(self.view, edit)

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

        if _nv_cmdline_feed_key.LAST_HISTORY_ITEM_INDEX is None:
            _nv_cmdline_feed_key.LAST_HISTORY_ITEM_INDEX = -1 if backwards else 0
        else:
            _nv_cmdline_feed_key.LAST_HISTORY_ITEM_INDEX += -1 if backwards else 1

        count = history_len(firstc)
        if count == 0:
            _nv_cmdline_feed_key.LAST_HISTORY_ITEM_INDEX = None

            return ui_bell()

        if abs(_nv_cmdline_feed_key.LAST_HISTORY_ITEM_INDEX) > count:
            _nv_cmdline_feed_key.LAST_HISTORY_ITEM_INDEX = -count

            return ui_bell()

        if _nv_cmdline_feed_key.LAST_HISTORY_ITEM_INDEX >= 0:
            _nv_cmdline_feed_key.LAST_HISTORY_ITEM_INDEX = 0

            if self.view.size() > 1:
                return self.view.erase(edit, Region(1, self.view.size()))
            else:
                return ui_bell()

        if self.view.size() > 1:
            self.view.erase(edit, Region(1, self.view.size()))

        item = history_get(firstc, _nv_cmdline_feed_key.LAST_HISTORY_ITEM_INDEX)
        if item:
            self.view.insert(edit, 1, item)

    @staticmethod
    def reset_last_history_index() -> None:
        _nv_cmdline_feed_key.LAST_HISTORY_ITEM_INDEX = None


class _nv_run_cmds(TextCommand):

    def run(self, edit, commands):
        # Run a list of commands one after the other.
        #
        # Args:
        #   commands (list): A list of commands.
        for cmd, args in commands:
            self.view.run_command(cmd, args)


class _nv_feed_key(ViWindowCommandBase):

    def run(self, key, repeat_count=None, do_eval=True, check_user_mappings=True):
        start_time = time.time()

        _log.info('key evt: %s count=%s eval=%s mappings=%s', key, repeat_count, do_eval, check_user_mappings)  # noqa: E501

        try:
            self._feed_key(key, repeat_count, do_eval, check_user_mappings)
        except Exception as e:
            print('NeoVintageous: An error occurred during key press handle:')
            _log.exception(e)

            import sublime
            for window in sublime.windows():
                for view in window.views():
                    settings = view.settings()
                    settings.set('command_mode', False)
                    settings.set('inverse_caret_state', False)
                    settings.erase('vintage')

        _log.info('key evt: %s count=%s eval=%s mappings=%s, took %s', key, repeat_count, do_eval, check_user_mappings, '{:.4f}'.format(time.time() - start_time))  # noqa: E501

    def _feed_key(self, key, repeat_count=None, do_eval=True, check_user_mappings=True):
        # Args:
        #   key (str): Key pressed.
        #   repeat_count (int): Count to be used when repeating through the '.' command.
        #   do_eval (bool): Whether to evaluate the global state when it's in a
        #       runnable state. Most of the time, the default value of `True` should
        #       be used. Set to `False` when you want to manually control the global
        #       state's evaluation. For example, this is what the _nv_feed_key
        #       command does.
        #   check_user_mappings (bool):
        state = self.state

        mode = state.mode

        _log.debug('mode: %s', mode)

        # If the user has made selections with the mouse, we may be in an
        # inconsistent state. Try to remedy that.
        if mode not in (VISUAL, VISUAL_LINE, VISUAL_BLOCK, SELECT) and state.view.has_non_empty_selection_region():
            init_state(state.view)

        if key.lower() == '<esc>':
            if mode == SELECT:
                self.window.run_command('_vi_select_big_j', {'mode': mode})
            else:
                enter_normal_mode(self.window, mode)
                state.reset_command_data()
            return

        state.sequence += key
        state.display_status()

        if state.must_capture_register_name:
            _log.debug('capturing register name...')
            state.register = key
            state.partial_sequence = ''

            return

        if state.must_collect_input:
            _log.debug('collecting input...')
            state.process_input(key)
            if state.runnable():
                _log.debug('state is runnable')
                if do_eval:
                    _log.debug('evaluating state...')
                    state.eval()
                    state.reset_command_data()

            return

        # If the user has defined any mappings that starts with a number
        # (count), or " (register character), we need to skip the count handler
        # and go straight to resolving the mapping, otherwise it won't resolve.
        # See https://github.com/NeoVintageous/NeoVintageous/issues/434.
        if not mappings_can_resolve(state.mode, state.partial_sequence + key):
            if repeat_count:
                state.action_count = str(repeat_count)

            if self._handle_count(state, key, repeat_count):
                _log.debug('handled count')

                return

        state.partial_sequence += key

        if check_user_mappings and mappings_is_incomplete(state.mode, state.partial_sequence):
            _log.debug('found incomplete mapping')

            return

        command = mappings_resolve(state, check_user_mappings=check_user_mappings)

        if isinstance(command, ViOpenRegister):
            state.must_capture_register_name = True
            return

        if isinstance(command, Mapping):
            # TODO Review What happens if Mapping + do_eval=False
            if do_eval:
                _log.debug('evaluating user mapping (mode=%s)...', state.mode)

                # TODO Review Why does rhs of mapping need to be resequenced in OPERATOR PENDING mode?
                rhs = command.rhs
                if state.mode == OPERATOR_PENDING:
                    rhs = state.sequence[:-len(state.partial_sequence)] + command.rhs

                # TODO Review Why does state need to be reset before running user mapping?
                reg = state.register
                acount = state.action_count
                mcount = state.motion_count
                state.reset_command_data()
                state.register = reg
                state.motion_count = mcount
                state.action_count = acount

                _log.info('user mapping %s -> %s', command.lhs, rhs)

                if ':' in rhs:

                    # This hacky piece of code (needs refactoring), is to
                    # support mappings in the format of {seq}:{ex-cmd}<CR>{seq},
                    # where leading and trailing sequences are optional.
                    #
                    # Examples:
                    #
                    #   :
                    #   :w
                    #   :sort<CR>
                    #   vi]:sort u<CR>
                    #   vi]:sort u<CR>vi]y<Esc>

                    colon_pos = rhs.find(':')
                    leading = rhs[:colon_pos]
                    rhs = rhs[colon_pos:]

                    cr_pos = rhs.lower().find('<cr>')
                    if cr_pos >= 0:
                        command = rhs[:cr_pos + 4]
                        trailing = rhs[cr_pos + 4:]
                    else:
                        command = rhs
                        trailing = ''

                    _log.debug('parsed user mapping before="%s", cmd="%s", after="%s"', leading, command, trailing)

                    if leading:
                        self.window.run_command('_nv_process_notation',
                                                {'keys': leading, 'check_user_mappings': False})

                    do_ex_user_cmdline(self.window, command)

                    if trailing:
                        self.window.run_command('_nv_process_notation',
                                                {'keys': trailing, 'check_user_mappings': False})

                else:
                    self.window.run_command('_nv_process_notation', {'keys': rhs, 'check_user_mappings': False})

            return

        if isinstance(command, ViOpenNameSpace):
            return

        if isinstance(command, ViMissingCommandDef):

            # TODO We shouldn't need to try resolve the command again. The
            # resolver should handle commands correctly the first time. The
            # reason this logic is still needed is because we might be looking
            # at a command like 'dd', which currently doesn't resolve properly.
            # The first 'd' is mapped for NORMAL mode, but 'dd' is not mapped in
            # OPERATOR PENDING mode, so we get a missing command, and here we
            # try to fix that (user mappings are excluded, since they've already
            # been given a chance to evaluate).

            if state.mode == OPERATOR_PENDING:
                command = mappings_resolve(state, sequence=to_bare_command_name(state.sequence),
                                           mode=NORMAL, check_user_mappings=False)
            else:
                command = mappings_resolve(state, sequence=to_bare_command_name(state.sequence))

            if self._handle_missing_command(state, command):
                return

        if (state.mode == OPERATOR_PENDING and isinstance(command, ViOperatorDef)):

            # TODO This should be unreachable code. The mapping resolver should
            # handle anything that can still reach this point (the first time).
            # We're expecting a motion, but we could still get an action. For
            # example, dd, g~g~ or g~~ remove counts. It looks like it might
            # only be the '>>' command that needs this code.

            command = mappings_resolve(state, sequence=to_bare_command_name(state.sequence), mode=NORMAL)
            if self._handle_missing_command(state, command):
                return

            if not command.motion_required:
                state.mode = NORMAL

        self._handle_command(state, command, do_eval)

    def _handle_command(self, state, command, do_eval: bool):
        state.set_command(command)

        if state.mode == OPERATOR_PENDING:
            state.reset_partial_sequence()

        if do_eval:
            state.eval()

    def _handle_count(self, state, key: str, repeat_count: int):
        """Return True if the processing of the current key needs to stop."""
        if not state.action and key.isdigit():
            if not repeat_count and (key != '0' or state.action_count):
                _log.debug('action count digit %s', key)
                state.action_count += key

                return True

        if (state.action and (state.mode == OPERATOR_PENDING) and key.isdigit()):
            if not repeat_count and (key != '0' or state.motion_count):
                _log.debug('motion count digit %s', key)
                state.motion_count += key

                return True

    def _handle_missing_command(self, state, command):
        if isinstance(command, ViMissingCommandDef):
            if state.mode == OPERATOR_PENDING:
                state.mode = NORMAL

            state.reset_command_data()
            ui_bell()

            return True

        return False


class _nv_process_notation(ViWindowCommandBase):

    def run(self, keys, repeat_count=None, check_user_mappings=True):
        # Args:
        #   keys (str): Key sequence to be run.
        #   repeat_count (int): Count to be applied when repeating through the
        #       '.' command.
        #   check_user_mappings (bool): Whether user mappings should be
        #       consulted to expand key sequences.
        state = self.state
        initial_mode = state.mode
        # Disable interactive prompts. For example, to supress interactive
        # input collection in /foo<CR>.
        state.non_interactive = True

        _log.debug('process notation keys %s for initial mode %s', keys, initial_mode)

        # First, run any motions coming before the first action. We don't keep
        # these in the undo stack, but they will still be repeated via '.'.
        # This ensures that undoing will leave the caret where the  first
        # editing action started. For example, 'lldl' would skip 'll' in the
        # undo history, but store the full sequence for '.' to use.
        leading_motions = ''
        for key in KeySequenceTokenizer(keys).iter_tokenize():
            self.window.run_command('_nv_feed_key', {
                'key': key,
                'do_eval': False,
                'repeat_count': repeat_count,
                'check_user_mappings': check_user_mappings
            })

            if state.action:
                # The last key press has caused an action to be primed. That
                # means there are  no more leading motions. Break out of here.
                _log.debug('first action found in %s', state.sequence)
                state.reset_command_data()
                if state.mode == OPERATOR_PENDING:
                    state.mode = NORMAL

                break

            elif state.runnable():
                # Run any primed motion.
                leading_motions += state.sequence
                state.eval()
                state.reset_command_data()

            else:
                state.eval()

        if state.must_collect_input:
            # State is requesting more input, so this is the last command  in
            # the sequence and it needs more input.
            self.collect_input()
            return

        # Strip the already run commands
        if leading_motions:
            if ((len(leading_motions) == len(keys)) and (not state.must_collect_input)):
                state.non_interactive = False
                return

            keys = keys[len(leading_motions):]

        if not (state.motion and not state.action):
            with gluing_undo_groups(self.window.active_view(), state):
                try:
                    for key in KeySequenceTokenizer(keys).iter_tokenize():
                        if key.lower() == '<esc>':
                            # XXX: We should pass a mode here?
                            enter_normal_mode(self.window)
                            continue

                        elif state.mode not in (INSERT, REPLACE):
                            self.window.run_command('_nv_feed_key', {
                                'key': key,
                                'repeat_count': repeat_count,
                                'check_user_mappings': check_user_mappings
                            })
                        else:
                            self.window.run_command('insert', {
                                'characters': translate_char(key)
                            })

                    if not state.must_collect_input:
                        return

                finally:
                    state.non_interactive = False
                    # Ensure we set the full command for "." to use, but don't
                    # store "." alone.
                    if (leading_motions + keys) not in ('.', 'u', '<C-r>'):
                        set_repeat_data(state.view, ('vi', (leading_motions + keys), initial_mode, None))

        # We'll reach this point if we have a command that requests input whose
        # input parser isn't satistied. For example, `/foo`. Note that
        # `/foo<CR>`, on the contrary, would have satisfied the parser.

        _log.debug('unsatisfied parser action = %s, motion=%s', state.action, state.motion)

        if (state.action and state.motion):
            # We have a parser an a motion that can collect data. Collect data
            # interactively.
            motion_data = state.motion.translate(state) or None

            if motion_data is None:
                state.reset_command_data()
                ui_bell()
                return

            run_motion(self.window, motion_data)
            return

        self.collect_input()

    def collect_input(self) -> None:
        state = self.state
        try:
            motion = state.motion
            action = state.action

            command = None

            if motion and action:
                if motion.accept_input:
                    command = motion
                else:
                    command = action
            else:
                command = action or motion

            if command.input_parser and command.input_parser.is_interactive():
                command.input_parser.run_interactive_command(self.window, command.inp)

        except IndexError:
            _log.debug('could not find a command to collect more user input')
            ui_bell()
        finally:
            state.non_interactive = False


class _nv_replace_line(TextCommand):

    def run(self, edit, with_what):
        pt = next_non_blank(self.view, self.view.line(self.view.sel()[0].b).a)
        self.view.replace(edit, Region(pt, self.view.line(pt).b), with_what)


class _nv_ex_cmd_edit_wrap(TextCommand):

    # This command is required to wrap ex commands that need a Sublime Text edit
    # token. Edit tokens can only be obtained from a TextCommand. Some ex
    # commands don't need an edit token, those commands don't need to be wrapped
    # by a text command.

    def run(self, edit, **kwargs):
        do_ex_cmd_edit_wrap(self, edit, **kwargs)


class _nv_cmdline(WindowCommand):

    def is_enabled(self):
        return bool(self.window.active_view())

    def run(self, initial_text=None):
        reset_cmdline_completion_state()
        view = self.window.active_view()
        set_reset_during_init(view, False)
        mode = State(view).mode

        if initial_text is not None:
            # DEPRECATED The initial_text should NOT contain the leading colon.
            # Previously this was accepted and the colon was stripped  before
            # passing dwn the chain, but calling code should be refactored.
            if len(initial_text) > 0:
                if initial_text[0] == Cmdline.EX:
                    initial_text = initial_text[1:]
                    message('DEPRECATED cmdline initial text contains leading colon')

        elif is_visual_mode(mode):
            initial_text = "'<,'>"
        else:
            initial_text = ""

        self._cmdline = Cmdline(
            self.window,
            Cmdline.EX,
            self.on_done,
            self.on_change,
            self.on_cancel
        )

        self._cmdline.prompt(initial_text)

    def on_change(self, cmdline):
        on_change_cmdline_completion_prefix(self.window, Cmdline.EX + cmdline)

    def on_done(self, cmdline):
        _nv_cmdline_feed_key.reset_last_history_index()
        history_update(Cmdline.EX + cmdline)
        do_ex_cmdline(self.window, Cmdline.EX + cmdline)

    def on_cancel(self):
        _nv_cmdline_feed_key.reset_last_history_index()


class Neovintageous(WindowCommand):

    def run(self, action, **kwargs):
        if action == 'open_rc_file':
            rc.open(self.window)
        elif action == 'reload_rc_file':
            rc.reload()
        elif action == 'toggle_ctrl_keys':
            toggle_ctrl_keys()
        elif action == 'toggle_side_bar':
            toggle_side_bar(self.window)
        elif action == 'toggle_super_keys':
            toggle_super_keys()


# DEPRECATED use 'neovintageous action=open_rc_file' instead
class NeovintageousOpenMyRcFileCommand(Neovintageous):

    def run(self):
        super().run(action='open_rc_file')


# DEPRECATED use 'neovintageous action=reload_rc_file' instead
class NeovintageousReloadMyRcFileCommand(Neovintageous):

    def run(self):
        super().run(action='reload_rc_file')


# DEPRECATED use 'neovintageous action=toggle_side_bar' instead
class NeovintageousToggleSideBarCommand(Neovintageous):

    def run(self):
        super().run(action='toggle_side_bar')


# DEPRECATED Use _nv_run_cmds instead
class SequenceCommand(TextCommand):

    def run(self, edit, commands):
        # Run a list of commands one after the other.
        #
        # Args:
        #   commands (list): A list of commands.
        for cmd, args in commands:
            self.view.run_command(cmd, args)


class _vi_g_big_u(ViTextCommandBase):

    def run(self, edit, mode=None, count=1, motion=None):
        def f(view, s):
            view.replace(edit, s, view.substr(s).upper())
            # Reverse region so that entering NORMAL mode collapses selection.
            return Region(s.b, s.a)

        if mode == INTERNAL_NORMAL:
            if motion is None:
                raise ValueError('motion data required')

            self.save_sel()
            run_motion(self.view, motion)
            if self.has_sel_changed():
                regions_transformer(self.view, f)
            else:
                ui_bell()
        else:
            regions_transformer(self.view, f)

        enter_normal_mode(self.view, mode)


class _vi_gu(ViTextCommandBase):

    def run(self, edit, mode=None, count=1, motion=None):
        def f(view, s):
            view.replace(edit, s, view.substr(s).lower())
            # Reverse region so that entering NORMAL mode collapses selection.
            return Region(s.b, s.a)

        if mode == INTERNAL_NORMAL:
            if motion is None:
                raise ValueError('motion data required')

            self.save_sel()
            run_motion(self.view, motion)
            if self.has_sel_changed():
                regions_transformer(self.view, f)
            else:
                ui_bell()
        else:
            regions_transformer(self.view, f)

        enter_normal_mode(self.view, mode)


class _vi_gq(ViTextCommandBase):

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

            self.save_sel()

            if motion:
                run_motion(self.view, motion)
            else:
                regions_transform_extend_to_line_count(self.view, count)

            if self.has_sel_changed():
                _wrap_lines(self.view)

                def f(view, s):
                    line = view.line(s.b)

                    return Region(next_non_blank(view, line.a))

                regions_transformer(self.view, f)
            else:
                ui_bell()

        enter_normal_mode(self.view, mode)


class _vi_u(ViWindowCommandBase):

    def run(self, mode=None, count=1, **kwargs):
        for i in range(count):
            self.view.run_command('undo')

        if self.view.has_non_empty_selection_region():
            def reverse(view, s):
                return Region(s.end(), s.begin())

            regions_transformer(self.view, reverse)
            enter_normal_mode(self.window, VISUAL)  # TODO Review: Why explicitly from VISUAL mode?

        # Ensure regions are clear of any highlighted yanks. For example, ddyyu
        # would otherwise show the restored line as previously highlighted.
        ui_highlight_yank_clear(self.view)


class _vi_ctrl_r(ViWindowCommandBase):

    def run(self, mode=None, count=1, **kwargs):
        change_count_before = self.view.change_count()

        for i in range(count):
            self.view.run_command('redo')

        if self.view.change_count() == change_count_before:
            return ui_bell()

        # Fix EOL issue.
        # See https://github.com/SublimeTextIssues/Core/issues/2121.
        def fixup_eol(view, s):
            pt = s.b
            char = view.substr(pt)
            if (char == '\n' and not view.line(pt).empty()):
                return Region(pt - 1)

            if char == '\x00' and pt == view.size():
                return Region(s.b - 1)

            return s

        regions_transformer(self.view, fixup_eol)


class _vi_a(ViTextCommandBase):

    def run(self, edit, mode=None, count=1):
        def f(view, s):
            if view.substr(s.b) != '\n' and s.b < view.size():
                return Region(s.b + 1)

            return s

        state = State(self.view)

        # Abort if the *actual* mode is insert mode. This prevents _vi_a from
        # adding spaces between text fragments when used with a count, as in
        # 5aFOO. In that case, we only need to run 'a' the first time, not for
        # every iteration.
        if state.mode == INSERT:
            return

        if mode is None:
            raise ValueError('mode required')
        elif mode != INTERNAL_NORMAL:
            return

        regions_transformer(self.view, f)
        self.view.window().run_command('_enter_insert_mode', {
            'mode': mode,
            'count': state.normal_insert_count
        })


class _vi_c(ViTextCommandBase):

    def run(self, edit, mode=None, count=1, motion=None, register=None):
        if mode is None:
            raise ValueError('mode required')

        if mode == INTERNAL_NORMAL and motion is None:
            raise ValueError('motion data required')

        self.save_sel()

        if motion:
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

            if not self.has_sel_changed():
                enter_insert_mode(self.view, mode)
                return

            if all(s.empty() for s in self.view.sel()):
                enter_insert_mode(self.view, mode)
                return

        registers_op_change(self.view, register=register, linewise=is_linewise_operation(mode, motion))
        self.view.run_command('right_delete')
        enter_insert_mode(self.view, mode)


class _enter_normal_mode(ViTextCommandBase):

    def run(self, edit, mode=None, from_init=False):
        _log.debug('enter NORMAL mode from=%s, from_init=%s', mode, from_init)

        state = self.state

        self.view.window().run_command('hide_auto_complete')
        self.view.window().run_command('hide_overlay')

        if ((not from_init and (mode == NORMAL) and not state.sequence) or not is_view(self.view)):
            # When _enter_normal_mode is requested from init_state, we
            # should not hide output panels; hide them only if the user
            # pressed Esc and we're not cancelling partial state data, or if a
            # panel has the focus.
            # XXX: We are assuming that state.sequence will always be empty
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

        # Exit replace mode
        self.view.set_overwrite_status(False)

        state.enter_normal_mode()

        # XXX: st bug? if we don't do this, selections won't be redrawn
        self.view.run_command('_enter_normal_mode_impl', {'mode': mode})

        if state.glue_until_normal_mode and not state.processing_notation:
            if self.view.is_dirty():
                self.view.window().run_command('glue_marked_undo_groups')
                # We're exiting from insert mode or replace mode. Capture
                # the last native command as repeat data.
                set_repeat_data(self.view, ('native', self.view.command_history(0)[:2], mode, None))
                # Required here so that the macro gets recorded.
                state.glue_until_normal_mode = False
                macros.add_step(state, *self.view.command_history(0)[:2])
                macros.add_step(state, '_enter_normal_mode', {'mode': mode, 'from_init': from_init})
            else:
                macros.add_step(state, '_enter_normal_mode', {'mode': mode, 'from_init': from_init})
                self.view.window().run_command('unmark_undo_groups_for_gluing')
                state.glue_until_normal_mode = False

        if mode == INSERT and int(state.normal_insert_count) > 1:
            state.enter_insert_mode()
            # TODO: Calculate size the view has grown by and place the caret after the newly inserted text.
            sels = list(self.view.sel())
            self.view.sel().clear()
            new_sels = [Region(s.b + 1) if self.view.substr(s.b) != '\n' else s for s in sels]
            self.view.sel().add_all(new_sels)
            times = int(state.normal_insert_count) - 1
            state.normal_insert_count = '1'
            self.view.window().run_command('_vi_dot', {
                'count': times,
                'mode': mode,
                'repeat_data': get_repeat_data(self.view),
            })
            set_selection(self.view, new_sels)

        state.update_xpos(force=True)
        state.reset_status()
        fix_eol_cursor(self.view, state.mode)

        # When the commands o and O are immediately followed by <Esc>, then if
        # the current line is only whitespace it should be erased, and the xpos
        # offset by 1 to account for transition from INSERT to NORMAL mode.
        if get_setting(self.view, 'clear_auto_indent_on_esc'):
            if mode == INSERT and self.view.is_dirty():
                if self.view.command_history(0)[0] in ('_vi_big_o', '_vi_o'):
                    for s in reversed(list(self.view.sel())):
                        line = self.view.line(s.b)
                        line_str = self.view.substr(line)
                        if re.match('^\\s+$', line_str):
                            self.view.erase(edit, line)
                            col = self.view.rowcol(line.b)[1]
                            state.xpos = col + 1


class _enter_normal_mode_impl(ViTextCommandBase):

    def run(self, edit, mode=None):
        _log.debug('enter NORMAL mode from=%s (wrapped)', mode)

        def f(view, s):
            if mode == INSERT:
                if view.line(s.b).a != s.b:
                    return Region(s.b - 1)

                return Region(s.b)

            if mode == INTERNAL_NORMAL:
                return Region(s.b)

            if mode == VISUAL:
                save_previous_selection(self.view, mode)

                if s.a < s.b:
                    pt = s.b - 1
                    if view.line(pt).empty():
                        return Region(pt)

                    if view.substr(pt) == '\n':
                        pt -= 1

                    return Region(pt)

                return Region(s.b)

            if mode in (VISUAL_LINE, VISUAL_BLOCK):
                save_previous_selection(self.view, mode)

                if s.a < s.b:
                    pt = s.b - 1
                    if (view.substr(pt) == '\n') and not view.line(pt).empty():
                        pt -= 1

                    return Region(pt)
                else:
                    return Region(s.b)

            if mode == SELECT:
                return Region(s.begin())

            return Region(s.b)

        if mode == UNKNOWN:
            return

        if (len(self.view.sel()) > 1) and (mode == NORMAL):
            set_selection(self.view, self.view.sel()[0])

        regions_transformer(self.view, f)

        if mode == VISUAL_BLOCK and len(self.view.sel()) > 1:
            set_selection(self.view, VisualBlockSelection(self.view).b)

        clear_search_highlighting(self.view)
        fix_eol_cursor(self.view, mode)


class _enter_select_mode(ViWindowCommandBase):

    def run(self, mode=None, count=1):
        _log.debug('enter SELECT mode from=%s, count=%s', mode, count)

        state = self.state
        state.enter_select_mode()

        if not self.view.has_non_empty_selection_region():
            self.window.run_command('find_under_expand')

        if mode == VISUAL:
            self.window.run_command('_vi_select_j', {'mode': state.mode})

        state.display_status()


class _enter_insert_mode(ViTextCommandBase):

    def run(self, edit, mode=None, count=1):
        _log.debug('enter INSERT mode from=%s, count=%s', mode, count)

        def f(view, s):
            s.a = s.b = get_insertion_point_at_b(s)

            return s

        regions_transformer(self.view, f)

        self.view.settings().set('inverse_caret_state', False)
        self.view.settings().set('command_mode', False)

        state = self.state
        state.enter_insert_mode()
        state.normal_insert_count = str(count)
        state.display_status()


class _enter_visual_mode(ViTextCommandBase):

    def run(self, edit, mode=None, force=False):
        _log.debug('enter VISUAL mode from=%s, force=%s', mode, force)

        state = self.state

        # TODO If all selections are non-zero-length, we may be looking at a
        # pseudo-visual selection, like the ones that are created pressing
        # Alt+Enter when using ST's built-in search dialog. What shall we really
        # do in that case?

        # XXX: In response to the above, we would probably already be in visual
        # mode, but we should double-check that.

        if state.mode == VISUAL and not force:
            enter_normal_mode(self.view, mode)
            return

        self.view.run_command('_enter_visual_mode_impl', {'mode': mode})

        if any(s.empty() for s in self.view.sel()):
            return

        # Sometimes we'll call this command without the global state knowing
        # its metadata. For example, when shift-clicking with the mouse to
        # create visual selections. Always update xpos to cover this case.
        state.update_xpos(force=True)
        state.enter_visual_mode()
        state.display_status()


class _enter_visual_mode_impl(ViTextCommandBase):

    def run(self, edit, mode=None):
        _log.debug('enter VISUAL mode from=%s (wrapped)', mode)

        def f(view, s):
            if mode == VISUAL_LINE:
                return Region(s.a, s.b)
            else:
                if s.empty() and (s.b == self.view.size()):
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

        if mode == VISUAL_BLOCK:
            visual_block = VisualBlockSelection(self.view)
            visual_block.transform_to_visual()
            return

        regions_transformer(self.view, f)


class _enter_visual_line_mode(ViTextCommandBase):

    def run(self, edit, mode=None, force=False):
        _log.debug('enter VISUAL LINE mode from=%s, force=%s', mode, force)

        state = self.state

        if state.mode == VISUAL_LINE and not force:
            enter_normal_mode(self.view, mode)
            return

        if mode in (NORMAL, INTERNAL_NORMAL):
            # Special-case: If cursor is at the very EOF, then try backup the
            # selection one character so the line, or previous line, is selected
            # (currently only handles non multiple-selections).
            if self.view.size() > 0 and len(self.view.sel()) == 1:
                s = self.view.sel()[0]
                if self.view.substr(s.b) == '\x00':
                    set_selection(self.view, s.b - 1)

            # Abort if we are at EOF -- no newline char to hold on to.
            if any(s.b == self.view.size() for s in self.view.sel()):
                return ui_bell()

        self.view.run_command('_enter_visual_line_mode_impl', {'mode': mode})
        state.enter_visual_line_mode()
        state.display_status()


class _enter_visual_line_mode_impl(ViTextCommandBase):

    def run(self, edit, mode=None):
        _log.debug('enter VISUAL LINE mode from=%s (wrapped)', mode)

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

        if mode == VISUAL_BLOCK:
            visual_block = VisualBlockSelection(self.view)
            visual_block.transform_to_visual_line()
            return

        regions_transformer(self.view, f)


class _enter_replace_mode(ViTextCommandBase):

    def run(self, edit, **kwargs):
        _log.debug('enter REPLACE mode kwargs=%s', kwargs)

        def f(view, s):
            return Region(s.b)

        self.view.settings().set('command_mode', False)
        self.view.settings().set('inverse_caret_state', False)
        self.view.set_overwrite_status(True)
        state = self.state
        state.enter_replace_mode()
        regions_transformer(self.view, f)
        state.display_status()
        state.reset()


class _vi_dot(ViWindowCommandBase):

    def run(self, mode=None, count=None, repeat_data=None):
        state = self.state
        state.reset_command_data()

        if state.mode == INTERNAL_NORMAL:
            state.mode = NORMAL

        if repeat_data is None:
            return ui_bell()

        # TODO: Find out if the user actually meant '1'.
        if count and count == 1:
            count = None

        type_, seq_or_cmd, old_mode, visual_data = repeat_data
        _log.debug('type=%s, seqorcmd=%s, oldmode=%s', type_, seq_or_cmd, old_mode)

        if visual_data and (mode != VISUAL):
            state.restore_visual_data(visual_data)
        elif not visual_data and (mode == VISUAL):
            # Can't repeat normal mode commands in visual mode.
            return ui_bell()
        elif mode not in (VISUAL, VISUAL_LINE, NORMAL, INTERNAL_NORMAL, INSERT):
            return ui_bell()

        view = self.window.active_view()

        if type_ == 'vi':
            self.window.run_command('_nv_process_notation', {'keys': seq_or_cmd, 'repeat_count': count})
        elif type_ == 'native':
            sels = list(view.sel())
            # FIXME: We're not repeating as we should. It's the motion that
            # should receive this count.
            for i in range(count or 1):
                self.window.run_command(*seq_or_cmd)

            # FIXME: What happens in visual mode?
            set_selection(view, sels)
        else:
            raise ValueError('bad repeat data')

        enter_normal_mode(self.window, mode)
        set_repeat_data(view, repeat_data)
        state.update_xpos()


class _vi_dd(ViTextCommandBase):

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
                if pt == size and self.view.substr(pt) == '\x00':
                    pt = self.view.text_point(self.view.rowcol(pt)[0], 0)
                pt = next_non_blank(self.view, pt)
                new.append(pt)
            self.view.sel().add_all(new)

        regions_transformer(self.view, f)
        registers_op_delete(self.view, register=register, linewise=True)
        self.view.run_command('right_delete')
        fixup_sel_pos()


class _vi_cc(ViTextCommandBase):

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

        try:
            self.state.xpos = self.view.rowcol(self.view.sel()[0].b)[1]
        except Exception as e:
            raise ValueError('could not set xpos:' + str(e))


class _vi_visual_o(ViTextCommandBase):

    def run(self, edit, mode=None, count=1):
        def f(view, s):
            if mode in (VISUAL, VISUAL_LINE):
                s = Region(s.b, s.a)

            return s

        regions_transformer(self.view, f)
        self.view.show(self.view.sel()[0].b, False)


class _vi_yy(ViTextCommandBase):

    def run(self, edit, mode=None, count=1, register=None):
        def f(view, s):
            if mode == INTERNAL_NORMAL:
                if count > 1:
                    row, col = self.view.rowcol(s.b)
                    end = view.text_point(row + count - 1, 0)
                    s = Region(view.line(s.a).a, view.full_line(end).b)
                elif view.line(s.b).empty():
                    s = Region(s.b, min(view.size(), s.b + 1))
                else:
                    s = view.full_line(s.b)
            elif mode == VISUAL:
                startline = view.line(s.begin())
                endline = view.line(s.end() - 1)
                s = Region(startline.a, endline.b)

            return s

        def restore():
            set_selection(self.view, list(self.old_sel))

        if mode not in (INTERNAL_NORMAL, VISUAL):
            enter_normal_mode(self.view, mode)
            ui_bell()
            return

        self.save_sel()
        regions_transformer(self.view, f)
        ui_highlight_yank(self.view)
        registers_op_yank(self.view, register=register, linewise=True)
        restore()
        enter_normal_mode(self.view, mode)


class _vi_y(ViTextCommandBase):

    def run(self, edit, mode=None, count=1, motion=None, register=None):
        def f(view, s):
            return Region(next_non_blank(view, s.begin()))

        if mode == INTERNAL_NORMAL:
            if motion is None:
                raise ValueError('motion data required')

            run_motion(self.view, motion)
        elif mode not in (VISUAL, VISUAL_LINE, VISUAL_BLOCK, SELECT):
            return

        ui_highlight_yank(self.view)
        registers_op_yank(self.view, register=register, linewise=is_linewise_operation(mode, motion))
        regions_transformer(self.view, f)
        enter_normal_mode(self.view, mode)


class _vi_d(ViTextCommandBase):

    def run(self, edit, mode=None, count=1, motion=None, register=None):
        if mode not in (INTERNAL_NORMAL, VISUAL, VISUAL_LINE, VISUAL_BLOCK, SELECT):
            raise ValueError('wrong mode')

        if mode == INTERNAL_NORMAL and not motion:
            raise ValueError('motion data required')

        if motion:
            self.save_sel()
            run_motion(self.view, motion)
            if not self.has_sel_changed():
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
                    if motion:
                        if 'motion' in motion:
                            if motion['motion'] in ('_vi_e', '_vi_big_e'):
                                return Region(s.begin())

                    return Region(next_non_blank(self.view, s.b))

                regions_transformer(self.view, f)
        elif mode == VISUAL_LINE:
            def f(view, s):
                return Region(next_non_blank(self.view, s.b))

            regions_transformer(self.view, f)

        fix_eol_cursor(self.view, mode)


class _vi_big_a(ViTextCommandBase):

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


class _vi_big_i(ViTextCommandBase):

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


class _vi_m(ViTextCommandBase):

    def run(self, edit, mode=None, count=1, character=None):
        add_mark(self.view, character)
        enter_normal_mode(self.view, mode)


class _vi_quote(ViTextCommandBase):

    def run(self, edit, mode=None, count=1, character=None):
        def f(view, s):
            if mode == VISUAL:
                resolve_visual_target(s, next_non_blank(view, address.b))
            elif mode in (VISUAL_LINE, VISUAL_BLOCK):
                if s.a <= s.b:
                    if address.b < s.b:
                        s = Region(s.a + 1, address.b)
                    else:
                        s = Region(s.a, address.b)
                else:
                    s = Region(s.a + 1, address.b)
            elif mode == NORMAL:
                s = Region(next_non_blank(view, address.b))
            elif mode == INTERNAL_NORMAL:
                if s.a < address.a:
                    s = Region(view.full_line(s.b).a, view.line(address.b).b)
                else:
                    s = Region(view.full_line(s.b).b, view.line(address.b).a)

            return s

        address = get_mark_as_encoded_address(self.view, character)
        if address is None:
            return

        if isinstance(address, str):
            if not address.startswith('<command'):
                self.view.window().open_file(address, ENCODED_POSITION)
            else:
                # We get a command in this form: <command _vi_double_quote>
                self.view.run_command(address.split(' ')[1][:-1])

            return

        jumplist_update(self.view)
        regions_transformer(self.view, f)
        jumplist_update(self.view)

        if not self.view.visible_region().intersects(address):
            self.view.show_at_center(address)


class _vi_backtick(ViTextCommandBase):

    def run(self, edit, mode=None, count=1, character=None):
        def f(view, s):
            if mode == VISUAL:
                resolve_visual_target(s, next_non_blank(view, address.b))
            elif mode == NORMAL:
                s = Region(next_non_blank(view, address.b))
            elif mode == INTERNAL_NORMAL:
                if s.a < address.a:
                    s = Region(view.full_line(s.b).a, view.line(address.b).b)
                else:
                    s = Region(view.full_line(s.b).b, view.line(address.b).a)

            return s

        address = get_mark_as_encoded_address(self.view, character, exact=True)
        if address is None:
            return

        if isinstance(address, str):
            if not address.startswith('<command'):
                self.view.window().open_file(address, ENCODED_POSITION)

            return

        jumplist_update(self.view)
        regions_transformer(self.view, f)
        jumplist_update(self.view)


class _vi_big_d(ViTextCommandBase):

    def run(self, edit, mode=None, count=1, register=None):
        def f(view, s):
            if mode == INTERNAL_NORMAL:
                if count == 1:
                    if view.line(s.b).size() > 0:
                        s = Region(s.b, view.line(s.b).b)

            elif mode == VISUAL:
                startline = view.line(s.begin())
                endline = view.full_line(s.end())

                s = Region(startline.a, endline.b)

            return s

        self.save_sel()
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


class _vi_big_c(ViTextCommandBase):

    def run(self, edit, mode=None, count=1, register=None):
        def f(view, s):
            if mode == INTERNAL_NORMAL:
                if count == 1:
                    if view.line(s.b).size() > 0:
                        eol = view.line(s.b).b
                        return Region(s.b, eol)
                    return s
            return s

        self.save_sel()
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


class _vi_big_s(ViTextCommandBase):

    def run(self, edit, mode=None, count=1, register=None):
        def f(view, s):
            if mode == INTERNAL_NORMAL:
                if count == 1:
                    if view.line(s.b).size() > 0:
                        eol = view.line(s.b).b
                        begin = view.line(s.b).a
                        begin = next_non_blank(view, begin)
                        return Region(begin, eol)
                    return s
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


class _vi_s(ViTextCommandBase):

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

        self.save_sel()
        regions_transformer(self.view, f)

        if not self.has_sel_changed() and mode == INTERNAL_NORMAL:
            enter_insert_mode(self.view, mode)
            return

        registers_op_delete(self.view, register=register, linewise=(mode == VISUAL_LINE))
        self.view.run_command('right_delete')
        enter_insert_mode(self.view, mode)


class _vi_x(ViTextCommandBase):

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
        enter_normal_mode(self.view, mode)


class _vi_r(ViTextCommandBase):

    def make_replacement_text(self, char, r):
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

            if mode in (VISUAL, VISUAL_LINE, VISUAL_BLOCK):
                ends_in_newline = (view.substr(s.end() - 1) == '\n')
                text = self.make_replacement_text(char, s)
                if ends_in_newline:
                    text += '\n'

                view.replace(edit, s, text)

                if char == '\n':
                    return Region(s.begin() + 1)
                else:
                    return Region(s.begin())

        if char is None:
            raise ValueError('bad parameters')

        char = translate_char(char)
        regions_transformer(self.view, f)
        enter_normal_mode(self.view, mode)


class _vi_less_than_less_than(ViTextCommandBase):

    def run(self, edit, mode=None, count=1):
        regions_transform_extend_to_line_count(self.view, count)
        self.view.run_command('unindent')
        regions_transform_to_first_non_blank(self.view)
        enter_normal_mode(self.view, mode)


class _vi_equal_equal(ViTextCommandBase):

    def run(self, edit, mode=None, count=1):
        regions_transform_extend_to_line_count(self.view, count)
        self.view.run_command('reindent', {'force_indent': False})
        regions_transform_to_first_non_blank(self.view)
        enter_normal_mode(self.view, mode)


class _vi_greater_than_greater_than(ViTextCommandBase):

    def run(self, edit, mode=None, count=1):
        regions_transform_extend_to_line_count(self.view, count)
        self.view.run_command('indent')
        regions_transform_to_first_non_blank(self.view)
        enter_normal_mode(self.view, mode)


class _vi_greater_than(ViTextCommandBase):

    def run(self, edit, mode=None, count=1, motion=None):
        def indent_from_begin(view, s, level=1):
            block = '\t' if not translate else ' ' * size
            self.view.insert(edit, s.begin(), block * level)
            return Region(s.begin() + 1)

        if mode == VISUAL_BLOCK:
            translate = self.view.settings().get('translate_tabs_to_spaces')
            size = self.view.settings().get('tab_size')
            indent = partial(indent_from_begin, level=count)

            regions_transformer_reversed(self.view, indent)
            regions_transform_to_first_non_blank(self.view)

            # Restore only the first sel.
            s = self.view.sel()[0]
            replace_sel(self.view, s.a + 1)
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


class _vi_less_than(ViTextCommandBase):

    def run(self, edit, mode=None, count=1, motion=None):
        if motion:
            run_motion(self.view, motion)
        elif mode not in (VISUAL, VISUAL_LINE, VISUAL_BLOCK):
            return ui_bell()

        for i in range(count):
            self.view.run_command('unindent')

        regions_transform_to_first_non_blank(self.view)
        enter_normal_mode(self.view, mode)


class _vi_equal(ViTextCommandBase):

    def run(self, edit, mode=None, count=1, motion=None):
        if motion:
            run_motion(self.view, motion)
        elif mode not in (VISUAL, VISUAL_LINE, VISUAL_BLOCK):
            return ui_bell()

        self.view.run_command('reindent', {'force_indent': False})

        regions_transform_to_first_non_blank(self.view)
        enter_normal_mode(self.view, mode)


class _vi_big_o(ViTextCommandBase):

    def run(self, edit, mode=None, count=1):
        def create_selections(view, sel, index):
            real_sel = Region(sel.a + index * count, sel.b + index * count)
            start_of_line = view.full_line(real_sel).begin()
            view.insert(edit, start_of_line, "\n" * count)
            new = []
            for i in range(0, count):
                new.append(Region(start_of_line + i, start_of_line + i))
            return new

        regions_transformer_indexed(self.view, create_selections)
        enter_insert_mode(self.view, mode)
        self.view.run_command('reindent', {'force_indent': False})


class _vi_o(ViTextCommandBase):
    def run(self, edit, mode=None, count=1):
        def create_selections(view, sel, index):
            real_sel = sel if index == 0 else Region(sel.a + index * count, sel.b + index * count)
            end_of_line = view.line(real_sel).end()
            view.insert(edit, end_of_line, "\n" * count)
            new = []
            for i in range(1, count + 1):
                new.append(Region(end_of_line + i, end_of_line + i))
            return new

        regions_transformer_indexed(self.view, create_selections)
        enter_insert_mode(self.view, mode)
        self.view.run_command('reindent', {'force_indent': False})


class _vi_big_x(ViTextCommandBase):

    def line_start(self, pt):
        return self.view.line(pt).begin()

    def run(self, edit, mode=None, count=1, register=None):
        def f(view, s):
            nonlocal abort  # type: ignore
            if mode == INTERNAL_NORMAL:
                if view.line(s.b).empty():
                    abort = True
                return Region(s.b, max(s.b - count, self.line_start(s.b)))
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


class _vi_big_z_big_q(WindowCommand):

    def run(self):
        do_ex_command(self.window, 'quit', {'forceit': True})


class _vi_big_z_big_z(WindowCommand):

    def run(self):
        do_ex_command(self.window, 'exit')


class _vi_paste(ViTextCommandBase):

    def run(self, edit, before_cursor, mode=None, count=1, register=None, adjust_indent=False, adjust_cursor=False):
        contents, linewise = registers_get_for_paste(self.view, register, mode)
        if not contents:
            return status_message('E353: Nothing in register ' + register)

        _log.debug('paste %s count=%s register=%s before=%s indent=%s end=%s linewise=%s content >>>%s<<<', mode, count, register, before_cursor, adjust_indent, adjust_cursor, linewise, contents)  # noqa: E501

        sels = list(self.view.sel())

        # The register contents are concatenated into one string when the
        # current selection count is 1; otherwise if the register content count
        # is not equal to the current selection count a bell is rung.

        if len(sels) > 1 and len(contents) != len(sels):
            return ui_bell()

        if len(sels) == 1 and len(contents) > 1:
            contents = [''.join(contents)]

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

                    self.view.insert(edit, pt, text)

                    if adjust_cursor:
                        pt += len(text) + 1
                    else:
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
        elif mode in (VISUAL, VISUAL_LINE):
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


class _vi_ga(WindowCommand):

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

        for region in view.sel():
            c_str = view.substr(get_insertion_point_at_b(region))
            c_ord = ord(c_str)
            c_hex = hex(c_ord)
            c_oct = oct(c_ord)
            c_not = char_to_notation(c_str)
            status_message('%7s %3s,  Hex %4s,  Octal %5s' % (c_not, c_ord, c_hex, c_oct))


class _vi_gt(WindowCommand):

    def run(self, mode=None, count=0):
        if count > 0:
            window_tab_control(self.window, action='goto', index=count)
        else:
            window_tab_control(self.window, action='next')

        enter_normal_mode(self.window, mode)


class _vi_g_big_t(WindowCommand):

    def run(self, mode=None, count=1):
        window_tab_control(self.window, action='previous')
        enter_normal_mode(self.window, mode)


class _vi_g(TextCommand):

    def run(self, edit, action, **kwargs):
        if action == 'f':
            file_name = extract_file_name(self.view)
            if file_name:
                window_open_file(self.view.window(), file_name)
        else:
            raise ValueError('unknown action')


class _vi_ctrl_right_square_bracket(WindowCommand):

    def run(self):
        view = self.window.active_view()
        if view and view.score_selector(0, 'text.neovintageous.help') > 0:
            goto_help(self.window)
        else:
            self.window.run_command('goto_definition')


class _vi_ctrl_w(WindowCommand):

    def run(self, **kwargs):
        window_control(self.window, **kwargs)


class _vi_z_enter(IrreversibleTextCommand):

    def run(self, mode=None, count=1):
        pt = get_insertion_point_at_b(self.view.sel()[0])
        home_line = self.view.line(pt)
        taget_pt = self.view.text_to_layout(home_line.begin())
        self.view.set_viewport_position(taget_pt)


class _vi_z_minus(IrreversibleTextCommand):

    def run(self, mode=None, count=1):
        layout_coord = self.view.text_to_layout(self.view.sel()[0].b)
        viewport_extent = self.view.viewport_extent()
        new_pos = (0.0, layout_coord[1] - viewport_extent[1])
        self.view.set_viewport_position(new_pos)


class _vi_zz(IrreversibleTextCommand):

    def run(self, mode=None, count=1, first_non_blank=False):
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


class _vi_z(TextCommand):

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


class _vi_modify_numbers(ViTextCommandBase):

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


class _vi_select_big_j(IrreversibleTextCommand):

    def run(self, mode=None, count=1):
        if get_setting(self.view, 'multi_cursor_exit_from_visual_mode'):
            set_selection(self.view, self.view.sel()[0])

        enter_normal_mode(self.view, mode)


class _vi_big_j(ViTextCommandBase):
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


class _vi_gv(IrreversibleTextCommand):

    def run(self, mode=None, count=None):
        visual_sel, visual_sel_mode = get_previous_selection(self.view)
        if not visual_sel or not visual_sel_mode:
            return

        if visual_sel_mode == VISUAL:
            cmd = '_enter_visual_mode'
        elif visual_sel_mode == VISUAL_LINE:
            cmd = '_enter_visual_line_mode'
            # Ensure VISUAL LINE selections span full lines.
            for sel in visual_sel:
                if sel.a < sel.b:
                    sel.a = self.view.line(sel.a).a
                    sel.b = self.view.full_line(sel.b - 1).b
                else:
                    sel.a = self.view.full_line(sel.a - 1).b
                    sel.b = self.view.line(sel.b).a

        elif visual_sel_mode == VISUAL_BLOCK:
            cmd = '_enter_visual_block_mode'
        else:
            raise RuntimeError('unexpected visual sel mode')

        self.view.window().run_command(cmd, {'mode': mode, 'force': True})
        set_selection(self.view, visual_sel)


class _vi_gx(IrreversibleTextCommand):

    def run(self, **kwargs):
        url = extract_url(self.view)
        if url:
            webbrowser.open_new_tab(url)


class _vi_ctrl_e(ViTextCommandBase):

    def run(self, edit, mode=None, count=1):
        self.view.run_command('scroll_lines', {'amount': -count})


class _vi_ctrl_g(WindowCommand):

    def run(self, **kwargs):
        do_ex_command(self.window, 'file')


class _vi_ctrl_y(ViTextCommandBase):

    def run(self, edit, mode=None, count=1):
        self.view.run_command('scroll_lines', {'amount': count})


class _vi_q(IrreversibleTextCommand):

    def run(self, mode=None, count=1, name=None):
        window = self.view.window()

        if macros.is_recording(window):
            macros.stop_recording(window)
        else:
            if not macros.is_valid_writable_register(name):
                return ui_bell("E354: Invalid register name: '" + name + "'")

            macros.start_recording(window, name)


class _vi_at(IrreversibleTextCommand):

    def run(self, name, mode=None, count=1):
        window = self.view.window()

        if name == '@':
            name = macros.get_last_used_register_name(window)
            if not name:
                return ui_bell('E748: No previously used register')

        if not macros.is_valid_readable_register(name):
            return ui_bell("E354: Invalid register name: '" + name + "'")

        cmds = macros.get_recorded(window, name)
        if not cmds:
            return

        macros.set_last_used_register_name(window, name)

        state = State(self.view)
        for i in range(count):
            for cmd, args in cmds:
                if 'xpos' in args:
                    state.update_xpos(force=True)
                    args['xpos'] = State(self.view).xpos
                elif args.get('motion'):
                    motion = args.get('motion')
                    if motion and 'motion_args' in motion and 'xpos' in motion['motion_args']:
                        state.update_xpos(force=True)
                        motion = args.get('motion')
                        motion['motion_args']['xpos'] = State(self.view).xpos
                        args['motion'] = motion

                self.view.window().run_command(cmd, args)


class _enter_visual_block_mode(ViTextCommandBase):

    def run(self, edit, mode=None, force=False):
        _log.debug('enter VISUAL BLOCK mode from=%s, force=%s', mode, force)

        if mode == VISUAL_LINE:
            pass
        elif mode == VISUAL_BLOCK and not force:
            enter_normal_mode(self.view, mode)
        elif mode == VISUAL:
            first = self.view.sel()[0]

            if self.view.line(first.end() - 1).empty():
                enter_normal_mode(self.view, mode)
                ui_bell()
                return

            self.view.sel().clear()
            lhs_edge = self.view.rowcol(first.b)[1]  # FIXME # noqa: F841
            regs = split_by_newlines(self.view, first)

            offset_a, offset_b = self.view.rowcol(first.a)[1], self.view.rowcol(first.b)[1]
            min_offset_x = min(offset_a, offset_b)
            max_offset_x = max(offset_a, offset_b)

            new_regs = []
            for r in regs:
                if r.empty():
                    break
                row, _ = self.view.rowcol(r.end() - 1)
                a = self.view.text_point(row, min_offset_x)
                eol = self.view.rowcol(self.view.line(r.end() - 1).b)[1]
                b = self.view.text_point(row, min(max_offset_x, eol))

                if first.a <= first.b:
                    if offset_b < offset_a:
                        new_r = Region(a - 1, b + 1, eol)
                    else:
                        new_r = Region(a, b, eol)
                elif offset_b < offset_a:
                    new_r = Region(a, b, eol)
                else:
                    new_r = Region(a - 1, b + 1, eol)

                new_regs.append(new_r)

            if not new_regs:
                new_regs.append(first)

            self.view.sel().add_all(new_regs)
            state = State(self.view)
            state.enter_visual_block_mode()
            state.display_status()
        else:
            first = list(self.view.sel())[0]
            set_selection(self.view, first)

            state = State(self.view)
            state.enter_visual_block_mode()

            def f(view, s):
                return Region(s.b, s.b + 1)

            if not self.view.has_non_empty_selection_region():
                regions_transformer(self.view, f)

            state.display_status()


# TODO Refactor into _vi_j
class _vi_select_j(ViWindowCommandBase):

    def run(self, mode=None, count=1):
        if mode != SELECT:
            raise ValueError('wrong mode')

        for i in range(count):
            self.window.run_command('find_under_expand')


# TODO Refactor into _vi_k
class _vi_select_k(ViWindowCommandBase):

    def run(self, mode=None, count=1):
        if mode != SELECT:
            raise ValueError('wrong mode')

        for i in range(count):
            if len(self.view.sel()) > 1:
                self.window.run_command('soft_undo')
            else:
                enter_normal_mode(self.view, mode)


class _vi_tilde(ViTextCommandBase):

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


class _vi_g_tilde(ViTextCommandBase):

    def run(self, edit, mode=None, count=1, motion=None):
        def f(view, s):
            return Region(s.end(), s.begin())

        sels = []
        for s in list(self.view.sel()):
            sels.append(s.a)

        if motion:
            self.save_sel()
            run_motion(self.view, motion)
            if not self.has_sel_changed():
                ui_bell()
                enter_normal_mode(self.view, mode)
                return

        self.view.run_command('swap_case')

        if motion:
            regions_transformer(self.view, f)

        set_selection(self.view, sels)
        enter_normal_mode(self.view, mode)


class _vi_visual_u(ViTextCommandBase):

    def run(self, edit, mode=None, count=1):
        for s in self.view.sel():
            self.view.replace(edit, s, self.view.substr(s).lower())

        def after(view, s):
            return Region(s.begin())

        regions_transformer(self.view, after)
        enter_normal_mode(self.view, mode)


class _vi_visual_big_u(ViTextCommandBase):

    def run(self, edit, mode=None, count=1):
        for s in self.view.sel():
            self.view.replace(edit, s, self.view.substr(s).upper())

        def after(view, s):
            return Region(s.begin())

        regions_transformer(self.view, after)
        enter_normal_mode(self.view, mode)


class _vi_g_tilde_g_tilde(ViTextCommandBase):

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


class _vi_g_big_u_big_u(ViTextCommandBase):

    def run(self, edit, mode=None, count=1):
        def select(view, s):
            return lines(view, s, count)

        def to_upper(view, s):
            view.replace(edit, s, view.substr(s).upper())
            return Region(next_non_blank(self.view, s.a))

        regions_transformer(self.view, select)
        regions_transformer(self.view, to_upper)
        enter_normal_mode(self.view, mode)


class _vi_guu(ViTextCommandBase):

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


# Non-standard command. After a search has been performed via '/' or '?',
# selects all matches and enters select mode.
class _vi_g_big_h(ViWindowCommandBase):

    def run(self, mode=None, count=1):
        state = self.state
        view = self.window.active_view()
        search_occurrences = get_search_occurrences(view)
        if search_occurrences:
            view.sel().add_all(search_occurrences)

            state.enter_select_mode()
            state.display_status()
            return

        ui_bell()
        status_message('no available search matches')
        state.reset_command_data()


class _vi_ctrl_x_ctrl_l(ViTextCommandBase):
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
            state = State(self.view)
            set_reset_during_init(self.view, False)
            state.reset_command_data()
            return

        ui_bell()

    def show_matches(self, items):
        self.view.window().show_quick_panel(items, self.replace, MONOSPACE_FONT)

    def replace(self, s):
        self.view.run_command('_nv_replace_line', {'with_what': self._matches[s]})
        del self.__dict__['_matches']
        set_selection(self.view, self.view.sel()[0].b)


class _vi_find_in_line(ViMotionCommand):

    # Contrary to *f*, *t* does not look past the caret's position, so if
    # @character is under the caret, nothing happens.
    def run(self, char=None, mode=None, count=1, inclusive=True, skipping=False):
        def f(view, s):
            if mode == VISUAL_LINE:
                raise ValueError('wrong mode')

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


class _vi_reverse_find_in_line(ViMotionCommand):

    # Contrary to *F*, *T* does not look past the caret's position, so if
    # ``character`` is right before the caret, nothing happens.
    def run(self, char=None, mode=None, count=1, inclusive=True, skipping=False):
        def f(view, s):
            if mode == VISUAL_LINE:
                raise ValueError('wrong mode')

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


class _vi_slash(ViMotionCommand):

    def run(self, pattern=''):
        set_reset_during_init(self.view, False)

        self._cmdline = Cmdline(
            self.view.window(),
            Cmdline.SEARCH_FORWARD,
            self.on_done,
            self.on_change,
            self.on_cancel
        )

        self._cmdline.prompt(pattern)

    def on_done(self, pattern):
        history_update(Cmdline.SEARCH_FORWARD + pattern)
        _nv_cmdline_feed_key.reset_last_history_index()

        state = self.state
        state.sequence += pattern + '<CR>'
        clear_search_highlighting(self.view)
        set_last_buffer_search_command(self.view, 'vi_slash')
        state.motion = ViSearchForwardImpl(term=pattern)
        set_last_buffer_search(self.view, pattern or get_last_buffer_search(self.view))
        state.eval()

    def on_change(self, pattern):
        state = self.state
        count = state.count

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

        add_search_highlighting(self.view, find_all_buffer_search_occurrences(self.view, pattern, flags), [match])
        show_if_not_visible(self.view, match)

    def on_cancel(self):
        clear_search_highlighting(self.view)
        self.state.reset_command_data()
        _nv_cmdline_feed_key.reset_last_history_index()
        show_if_not_visible(self.view)


class _vi_slash_impl(ViMotionCommand):
    def run(self, search_string, mode=None, count=1):
        # TODO Rename "search_string" argument "pattern"
        pattern = search_string
        if not pattern:
            return

        set_last_buffer_search_command(self.view, 'vi_slash')
        set_last_buffer_search(self.view, pattern)

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
                s = Region(target)
            elif mode == VISUAL:
                resolve_visual_target(s, target)
            elif mode == VISUAL_LINE:
                resolve_visual_line_target(view, s, target)
            elif mode == INTERNAL_NORMAL:
                s = Region(s.a, target)

            return s

        target = get_insertion_point_at_a(match)
        regions_transformer(self.view, f)
        add_search_highlighting(self.view, find_all_buffer_search_occurrences(self.view, pattern, flags))


class _vi_l(ViMotionCommand):
    def run(self, mode=None, count=1):
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


class _vi_h(ViMotionCommand):
    def run(self, mode=None, count=1):
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


class _vi_j(ViMotionCommand):

    def run(self, mode=None, count=1, xpos=0):
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

        state = State(self.view)

        if mode == VISUAL_BLOCK:
            visual_block = VisualBlockSelection(self.view)
            row, col = visual_block.rowcolb()
            next_line = self.view.full_line(self.view.text_point(row + count, 0))
            next_line_row, next_line_max_col = self.view.rowcol(next_line.b - 1)
            next_line_target_col = min(max(col, state.xpos), next_line_max_col)
            next_line_target_pt = self.view.text_point(next_line_row, next_line_target_col)
            visual_block.transform_target(next_line_target_pt)
            return

        regions_transformer(self.view, f)


class _vi_k(ViMotionCommand):

    def run(self, mode=None, count=1, xpos=0):
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

        state = State(self.view)

        if mode == VISUAL_BLOCK:
            visual_block = VisualBlockSelection(self.view)
            row, col = visual_block.rowcolb()
            prev_line = self.view.full_line(self.view.text_point(row - count, 0))
            prev_line_row, prev_line_max_col = self.view.rowcol(prev_line.b - 1)
            prev_line_target_col = min(max(col, state.xpos), prev_line_max_col)
            prev_line_target_pt = self.view.text_point(prev_line_row, prev_line_target_col)
            visual_block.transform_target(prev_line_target_pt)
            return

        regions_transformer(self.view, f)


class _vi_gg(ViMotionCommand):
    def run(self, mode=None, count=None):
        if count:
            goto_line(self.view, mode, count)
            return

        def f(view, s):
            if mode == NORMAL:
                s = Region(next_non_blank(view, 0))
            elif mode == VISUAL:
                resolve_visual_target(s, next_non_blank(view, 0))
            elif mode == VISUAL_LINE:
                resolve_visual_line_target(view, s, 0)
            elif mode == INTERNAL_NORMAL:
                s = Region(view.full_line(s.b).b, 0)

            return s

        jumplist_update(self.view)
        regions_transformer(self.view, f)
        jumplist_update(self.view)


class _vi_big_g(ViMotionCommand):
    def run(self, mode=None, count=None):
        if count:
            goto_line(self.view, mode, count)
            return

        def f(view, s):
            if mode == NORMAL:
                s = Region(next_non_blank(view, view.line(target).a))
            elif mode == VISUAL:
                resolve_visual_target(s, next_non_blank(view, view.line(target).a))
            elif mode == VISUAL_LINE:
                resolve_visual_line_target(view, s, target)
            elif mode == INTERNAL_NORMAL:
                s = Region(max(0, view.line(s.b).a), target)

            return s

        jumplist_update(self.view)
        target = self.view.size()
        regions_transformer(self.view, f)
        jumplist_update(self.view)


class _vi_dollar(ViMotionCommand):
    def run(self, mode=None, count=1):
        def _get_target(view, start, count):
            if count > 1:
                start = row_to_pt(view, row_at(view, start) + (count - 1))

            target = view.line(start).b

            return target

        if mode == VISUAL_BLOCK:
            resolve_visual_block_target(self.view, _get_target, count)
            return

        def f(view, s):
            target = _get_target(view, get_insertion_point_at_b(s), count)

            if mode == NORMAL:
                s = Region(target if view.line(target).empty() else (target - 1))
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


class _vi_w(ViMotionCommand):
    def run(self, mode=None, count=1):
        if mode == VISUAL_BLOCK:
            resolve_visual_block_target(self.view, word_starts, count)
            return

        def f(view, s):
            target = word_starts(view, get_insertion_point_at_b(s), count, internal=(mode == INTERNAL_NORMAL))

            if mode == NORMAL:
                s = Region(fixup_eof(view, target))
            elif mode == VISUAL:
                resolve_visual_target(s, target)
            elif mode == INTERNAL_NORMAL:
                if (not view.substr(view.line(s.a)).strip() and view.line(s.b) != view.line(target)):
                    s.a = view.line(s.a).a

                s.b = target

            return s

        regions_transformer(self.view, f)


class _vi_big_w(ViMotionCommand):
    def run(self, mode=None, count=1):
        if mode == VISUAL_BLOCK:
            resolve_visual_block_target(self.view, big_word_starts, count)
            return

        def f(view, s):
            target = big_word_starts(view, get_insertion_point_at_b(s), count, internal=(mode == INTERNAL_NORMAL))

            if mode == NORMAL:
                s = Region(fixup_eof(view, target))
            elif mode == VISUAL:
                resolve_visual_target(s, target)
            elif mode == INTERNAL_NORMAL:
                if (not view.substr(view.line(s.a)).strip() and view.line(s.b) != view.line(target)):
                    s.a = view.line(s.a).a

                s.b = target

            return s

        regions_transformer(self.view, f)


class _vi_e(ViMotionCommand):
    def run(self, mode=None, count=1):
        def _get_target(view, start, count):
            # TODO Is the word_ends() function off-by-one?
            return word_ends(view, start, count) - 1

        if mode == VISUAL_BLOCK:
            resolve_visual_block_target(self.view, _get_target, count)
            return

        def f(view, s):
            target = _get_target(view, get_insertion_point_at_b(s), count)

            if mode == NORMAL:
                s = Region(target)
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


class _vi_zero(ViMotionCommand):
    def run(self, mode=None, count=1):
        def _get_target(view, start, count):
            return view.line(start).a

        if mode == VISUAL_BLOCK:
            resolve_visual_block_target(self.view, _get_target, count)
            return

        def f(view, s):
            target = _get_target(view, get_insertion_point_at_b(s), count)

            if mode == NORMAL:
                s = Region(target)
            elif mode == VISUAL:
                resolve_visual_target(s, target)
            elif mode == VISUAL_LINE:
                resolve_visual_line_target(view, s, target)
            elif mode == INTERNAL_NORMAL:
                s.b = target

            return s

        regions_transformer(self.view, f)


class _vi_right_brace(ViMotionCommand):
    def run(self, mode=None, count=1):
        def f(view, s):
            target = next_paragraph_start(view, get_insertion_point_at_b(s), count)

            if mode == NORMAL:
                s = Region(target)
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


class _vi_left_brace(ViMotionCommand):
    def run(self, mode=None, count=1):
        def f(view, s):
            target = prev_paragraph_start(view, get_insertion_point_at_b(s), count)

            if mode == NORMAL:
                s = Region(target)
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


class _vi_percent(ViMotionCommand):

    def run(self, mode=None, count=None):
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
                        s = Region(target)
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


class _vi_big_h(ViMotionCommand):
    def run(self, mode=None, count=None):
        def f(view, s):
            if mode == NORMAL:
                s = Region(target)
            elif mode == VISUAL:
                resolve_visual_target(s, target)
            elif mode == VISUAL_LINE:
                resolve_visual_line_target(view, s, target)
            elif mode == INTERNAL_NORMAL:
                resolve_internal_normal_target(view, s, target, linewise=True)

            return s

        target = next_non_blank(self.view, highest_visible_pt(self.view))
        regions_transformer(self.view, f)


class _vi_big_l(ViMotionCommand):
    def run(self, mode=None, count=None):
        def f(view, s):
            if mode == NORMAL:
                s = Region(target)
            elif mode == VISUAL:
                resolve_visual_target(s, target)
            elif mode == VISUAL_LINE:
                resolve_visual_line_target(view, s, target)
            elif mode == INTERNAL_NORMAL:
                resolve_internal_normal_target(view, s, target, linewise=True)

            return s

        target = next_non_blank(self.view, lowest_visible_pt(self.view))
        regions_transformer(self.view, f)


class _vi_big_m(ViMotionCommand):
    def run(self, mode=None, count=None):
        def f(view, s):
            if mode == NORMAL:
                s = Region(target)
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


class _vi_star(ViMotionCommand):
    def run(self, mode=None, count=1, search_string=None):
        def f(view, s):
            pattern = create_word_search_pattern(view, query)
            flags = calculate_word_search_flags(view, query)
            match = find_wrapping(
                view,
                term=pattern,
                start=view.word(s.end()).end(),
                end=view.size(),
                flags=flags,
                times=1
            )

            if match:
                if mode == NORMAL:
                    s = Region(match.begin())
                elif mode == VISUAL:
                    resolve_visual_target(s, match.begin())
                elif mode == INTERNAL_NORMAL:
                    s = Region(s.a, match.begin())
            elif mode == NORMAL:
                s = Region(view.word(s.end()).begin())

            return s

        query = search_string or self.view.substr(self.view.word(self.view.sel()[0].end()))

        jumplist_update(self.view)
        regions_transformer(self.view, f)
        jumplist_update(self.view)

        if query:
            add_search_highlighting(self.view, find_all_word_search_occurrences(self.view, query))
            set_last_buffer_search(self.view, query)

        if not search_string:
            set_last_buffer_search_command(self.view, 'vi_star')

        show_if_not_visible(self.view)


class _vi_octothorp(ViMotionCommand):
    def run(self, mode=None, count=1, search_string=None):
        def f(view, s):
            pattern = create_word_search_pattern(view, query)
            flags = calculate_word_search_flags(view, query)
            match = reverse_find_wrapping(
                view,
                term=pattern,
                start=0,
                end=(start_sel.b if s.a > s.b else start_sel.a),
                flags=flags,
                times=1
            )

            if match:
                if mode == NORMAL:
                    s = Region(match.begin())
                elif mode == VISUAL:
                    resolve_visual_target(s, match.begin())
                elif mode == INTERNAL_NORMAL:
                    s = Region(s.b, match.begin())

            return s

        query = search_string or self.view.substr(self.view.word(self.view.sel()[0].end()))

        jumplist_update(self.view)
        start_sel = self.view.sel()[0]
        regions_transformer(self.view, f)
        jumplist_update(self.view)

        if query:
            add_search_highlighting(self.view, find_all_word_search_occurrences(self.view, query))
            set_last_buffer_search(self.view, query)

        if not search_string:
            set_last_buffer_search_command(self.view, 'vi_octothorp')

        show_if_not_visible(self.view)


class _vi_b(ViMotionCommand):
    def run(self, mode=None, count=1):
        if mode == VISUAL_BLOCK:
            resolve_visual_block_target(self.view, word_reverse, count)
            return

        def f(view, s):
            target = word_reverse(view, get_insertion_point_at_b(s), count)

            if mode == NORMAL:
                s = Region(target)
            elif mode == VISUAL:
                resolve_visual_target(s, target)
            elif mode == INTERNAL_NORMAL:
                s.b = target

            return s

        regions_transformer(self.view, f)


class _vi_big_b(ViMotionCommand):

    def run(self, mode=None, count=1):
        if mode == VISUAL_BLOCK:
            resolve_visual_block_target(self.view, big_word_reverse, count)
            return

        def f(view, s):
            target = big_word_reverse(view, get_insertion_point_at_b(s), count)

            if mode == NORMAL:
                s = Region(target)
            elif mode == VISUAL:
                resolve_visual_target(s, target)
            elif mode == INTERNAL_NORMAL:
                s.b = target

            return s

        regions_transformer(self.view, f)


class _vi_underscore(ViMotionCommand):
    def run(self, mode=None, count=1):
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
                s = Region(target)
            elif mode == VISUAL:
                resolve_visual_target(s, target)
            elif mode == VISUAL_LINE:
                resolve_visual_line_target(view, s, target)
            elif mode == INTERNAL_NORMAL:
                resolve_internal_normal_target(view, s, target, linewise=True)

            return s

        regions_transformer(self.view, f)


class _vi_hat(ViMotionCommand):
    def run(self, mode=None, count=None):
        def _get_target(view, start, count):
            return next_non_blank(view, view.line(start).a)

        if mode == VISUAL_BLOCK:
            resolve_visual_block_target(self.view, _get_target, count)
            return

        def f(view, s):
            target = _get_target(view, get_insertion_point_at_b(s), count)

            if mode == NORMAL:
                s = Region(target)
            elif mode == VISUAL:
                resolve_visual_target(s, target)
            elif mode == INTERNAL_NORMAL:
                s.b = target

            return s

        regions_transformer(self.view, f)


class _vi_gj(ViMotionCommand):
    def run(self, mode=None, count=1):
        if mode == NORMAL:
            for i in range(count):
                self.view.run_command('move', {'by': 'lines', 'forward': True, 'extend': False})
        elif mode == VISUAL:
            for i in range(count):
                self.view.run_command('move', {'by': 'lines', 'forward': True, 'extend': True})
        elif mode == VISUAL_LINE:
            self.view.run_command('_vi_j', {'mode': mode, 'count': count})
        elif mode == INTERNAL_NORMAL:
            for i in range(count):
                self.view.run_command('move', {'by': 'lines', 'forward': True, 'extend': False})


class _vi_gk(ViMotionCommand):
    def run(self, mode=None, count=1):
        if mode == NORMAL:
            for i in range(count):
                self.view.run_command('move', {'by': 'lines', 'forward': False, 'extend': False})
        elif mode == VISUAL:
            for i in range(count):
                self.view.run_command('move', {'by': 'lines', 'forward': False, 'extend': True})
        elif mode == VISUAL_LINE:
            self.view.run_command('_vi_k', {'mode': mode, 'count': count})
        elif mode == INTERNAL_NORMAL:
            for i in range(count):
                self.view.run_command('move', {'by': 'lines', 'forward': False, 'extend': False})


class _vi_g__(ViMotionCommand):
    def run(self, mode=None, count=1):
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
                s = Region(target)
            elif mode == VISUAL:
                resolve_visual_target(s, target)
            elif mode == VISUAL_LINE:
                resolve_visual_line_target(view, s, target)
            elif mode == INTERNAL_NORMAL:
                s.b = target + 1

            return s

        regions_transformer(self.view, f)


class _vi_ctrl_u(ViMotionCommand):
    def run(self, mode=None, count=0):
        def f(view, s):
            if mode == NORMAL:
                s = Region(target)
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


class _vi_ctrl_d(ViMotionCommand):
    def run(self, mode=None, count=0):
        def f(view, s):
            if mode == NORMAL:
                s = Region(target)
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


class _vi_bar(ViMotionCommand):
    def run(self, mode=None, count=1):
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
                s = Region(target)
            elif mode == VISUAL:
                resolve_visual_target(s, target)
            elif mode == INTERNAL_NORMAL:
                s.b = target

            return s

        regions_transformer(self.view, f)


class _vi_ge(ViMotionCommand):
    def run(self, mode=None, count=1):
        if mode == VISUAL_BLOCK:
            resolve_visual_block_target(self.view, word_end_reverse, count)
            return

        def f(view, s):
            target = word_end_reverse(view, get_insertion_point_at_b(s), count)

            if mode == NORMAL:
                s = Region(target)
            elif mode == VISUAL:
                resolve_visual_target(s, target)
            elif mode == INTERNAL_NORMAL:
                resolve_internal_normal_target(view, s, target, inclusive=True)

            return s

        regions_transformer(self.view, f)


class _vi_g_big_e(ViMotionCommand):
    def run(self, mode=None, count=1):
        if mode == VISUAL_BLOCK:
            resolve_visual_block_target(self.view, big_word_end_reverse, count)
            return

        def f(view, s):
            target = big_word_end_reverse(view, get_insertion_point_at_b(s), count)

            if mode == NORMAL:
                s = Region(target)
            elif mode == VISUAL:
                resolve_visual_target(s, target)
            elif mode == INTERNAL_NORMAL:
                resolve_internal_normal_target(view, s, target, inclusive=True)

            return s

        regions_transformer(self.view, f)


class _vi_left_paren(ViMotionCommand):

    def run(self, mode=None, count=1):
        def f(view, s):
            start = s.a if s.b >= s.a else s.b
            previous_sentence = find_sentences_backward(view, start, count)
            if previous_sentence is None:
                return s

            target = previous_sentence.a

            if mode == NORMAL:
                s = Region(target)
            elif mode == VISUAL:
                resolve_visual_target(s, target)
            elif mode == VISUAL_LINE:
                resolve_visual_line_target(view, s, target)
            elif mode == INTERNAL_NORMAL:
                s.b = target

            return s

        regions_transformer(self.view, f)


class _vi_right_paren(ViMotionCommand):

    def run(self, mode=None, count=1):
        def f(view, s):
            next_sentence = find_sentences_forward(view, s, count)
            if next_sentence is None:
                return s

            target = next_sentence.b

            if mode == NORMAL:
                s = Region(min(target, view.size() - 1))
            elif mode == VISUAL:
                s = Region(s.a, min(target + 1, view.size() - 1))
            elif mode == VISUAL_LINE:
                resolve_visual_line_target(view, s, target)
            elif mode == INTERNAL_NORMAL:
                s.b = target

            return s

        regions_transformer(self.view, f)


class _vi_question_mark_impl(ViMotionCommand):
    def run(self, search_string, mode=None, count=1):
        # TODO Rename "search_string" argument "pattern"
        pattern = search_string
        if not pattern:
            return

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
                s = Region(target)
            elif mode == VISUAL:
                resolve_visual_target(s, target)
            elif mode == VISUAL_LINE:
                resolve_visual_line_target(view, s, target)
            elif mode == INTERNAL_NORMAL:
                s = Region(s.end(), target)

            return s

        target = get_insertion_point_at_a(match)
        regions_transformer(self.view, f)
        add_search_highlighting(self.view, find_all_buffer_search_occurrences(self.view, pattern, flags))


class _vi_question_mark(ViMotionCommand):

    def run(self, pattern=''):
        set_reset_during_init(self.view, False)

        self._cmdline = Cmdline(
            self.view.window(),
            Cmdline.SEARCH_BACKWARD,
            self.on_done,
            self.on_change,
            self.on_cancel
        )

        self._cmdline.prompt(pattern)

    def on_done(self, pattern):
        history_update(Cmdline.SEARCH_BACKWARD + pattern)
        _nv_cmdline_feed_key.reset_last_history_index()

        state = self.state
        state.sequence += pattern + '<CR>'
        clear_search_highlighting(self.view)
        set_last_buffer_search_command(self.view, 'vi_question_mark')
        state.motion = ViSearchBackwardImpl(term=pattern)
        set_last_buffer_search(self.view, pattern or get_last_buffer_search(self.view))
        state.eval()

    def on_change(self, pattern):
        state = self.state
        count = state.count

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

        add_search_highlighting(self.view, find_all_buffer_search_occurrences(self.view, pattern, flags), [match])
        show_if_not_visible(self.view, match)

    def on_cancel(self):
        clear_search_highlighting(self.view)
        self.state.reset_command_data()
        _nv_cmdline_feed_key.reset_last_history_index()
        show_if_not_visible(self.view)


class _vi_repeat_buffer_search(ViMotionCommand):

    commands = {
        'vi_slash': ['_vi_slash_impl', '_vi_question_mark_impl'],
        'vi_question_mark': ['_vi_question_mark_impl', '_vi_slash_impl'],
        'vi_star': ['_vi_star', '_vi_octothorp'],
        'vi_octothorp': ['_vi_octothorp', '_vi_star'],
    }

    def run(self, mode=None, count=1, reverse=False):
        search_string = get_last_buffer_search(self.view)
        search_command = get_last_buffer_search_command(self.view)
        command = self.commands[search_command][int(reverse)]

        _log.debug('repeat search %s reverse=%s -> %s (pattern=%s)', search_command, reverse, command, search_string)

        self.view.run_command(command, {
            'mode': mode,
            'count': count,
            'search_string': search_string
        })

        self.view.show(self.view.sel(), show_surrounds=True)


class _vi_search(ViMotionCommand):

    def run(self, mode=None, count=1, forward=True):
        last_search = get_last_buffer_search(self.view)

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


class _vi_n(ViMotionCommand):

    def run(self, mode=None, count=1, search_string=''):
        self.view.run_command('_vi_slash_impl', {'mode': mode, 'count': count, 'search_string': search_string})


class _vi_big_n(ViMotionCommand):

    def run(self, mode=None, count=1, search_string=''):
        self.view.run_command('_vi_question_mark_impl', {'mode': mode, 'count': count, 'search_string': search_string})


class _vi_big_e(ViMotionCommand):
    def run(self, mode=None, count=1):
        def _get_target(view, start, count):
            # TODO Is the big_word_ends() function off-by-one?
            return big_word_ends(view, start, count) - 1

        if mode == VISUAL_BLOCK:
            resolve_visual_block_target(self.view, _get_target, count)
            return

        def f(view, s):
            target = _get_target(view, get_insertion_point_at_b(s), count)

            if mode == NORMAL:
                s = Region(target)
            elif mode == VISUAL:
                resolve_visual_target(s, target)
            elif mode == INTERNAL_NORMAL:
                resolve_internal_normal_target(view, s, target, inclusive=True)

            return s

        regions_transformer(self.view, f)


class _vi_ctrl_f(ViMotionCommand):
    def run(self, mode=None, count=1):
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


class _vi_ctrl_b(ViMotionCommand):
    def run(self, mode=None, count=1):
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


class _vi_enter(ViMotionCommand):
    def run(self, mode=None, count=1):
        self.view.run_command('_vi_j', {'mode': mode, 'count': count})

        def f(view, s):
            target = next_non_blank(view, get_insertion_point_at_b(s))

            if mode == NORMAL:
                s = Region(target)
            elif mode == VISUAL:
                resolve_visual_target(s, target)
            elif mode == VISUAL_LINE:
                resolve_visual_line_target(view, s, target)

            return s

        regions_transformer(self.view, f)


class _vi_minus(ViMotionCommand):
    def run(self, mode=None, count=1):
        self.view.run_command('_vi_k', {'mode': mode, 'count': count})

        def f(view, s):
            target = next_non_blank(view, get_insertion_point_at_b(s))

            if mode == NORMAL:
                s = Region(target)
            elif mode == VISUAL:
                resolve_visual_target(s, target)
            elif mode == VISUAL_LINE:
                resolve_visual_line_target(view, s, target)

            return s

        regions_transformer(self.view, f)


class _vi_shift_enter(ViMotionCommand):
    def run(self, mode=None, count=1):
        self.view.run_command('_vi_ctrl_f', {'mode': mode, 'count': count})


class _vi_select_text_object(ViMotionCommand):
    def run(self, text_object=None, mode=None, count=1, extend=False, inclusive=False):
        def f(view, s):
            if mode in (INTERNAL_NORMAL, VISUAL, VISUAL_LINE, VISUAL_BLOCK):
                return get_text_object_region(view, s, text_object,
                                              inclusive=inclusive,
                                              count=count)

            return s

        regions_transformer(self.view, f)


class _vi_go_to_symbol(ViMotionCommand):
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

    def run(self, mode=None, count=1, globally=False):

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
            jumplist_update(self.view)
            self.view.window().open_file(
                location[0] + ':' + ':'.join([str(x) for x in location[2]]),
                ENCODED_POSITION
            )
            jumplist_update(self.view)

            return

        # Local symbol; select.
        location = self.view.text_point(*location)

        jumplist_update(self.view)
        regions_transformer(self.view, f)
        jumplist_update(self.view)


class _vi_gm(ViMotionCommand):
    def run(self, mode=None, count=1):
        def f(view, s):
            line = view.line(s.b)
            if line.empty():
                return s

            mid_pt = line.size() // 2
            row_start = row_to_pt(view, row_at(view, s.b))

            return Region(min(row_start + mid_pt, line.b - 1))

        if mode != NORMAL:
            return ui_bell()

        regions_transformer(self.view, f)


class _vi_left_square_bracket(ViMotionCommand):
    def run(self, action, mode, count=1, **kwargs):
        if action == 'c':
            goto_prev_change(self.view, mode, count)
        elif action == 's':
            goto_prev_mispelled_word(self.view, mode, count)
        elif action == 'target':
            goto_prev_target(self.view, mode, count, **kwargs)
        else:
            raise ValueError('unknown action')


class _vi_right_square_bracket(ViMotionCommand):
    def run(self, action, mode, count=1, **kwargs):
        if action == 'c':
            goto_next_change(self.view, mode, count)
        elif action == 's':
            goto_next_mispelled_word(self.view, mode, count)
        elif action == 'target':
            goto_next_target(self.view, mode, count, **kwargs)
        else:
            raise ValueError('unknown action')
