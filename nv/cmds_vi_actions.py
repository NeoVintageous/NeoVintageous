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
import webbrowser

from sublime import ENCODED_POSITION
from sublime import MONOSPACE_FONT
from sublime import Region

from NeoVintageous.nv.ex_cmds import do_ex_command
from NeoVintageous.nv.jumplist import jumplist_update
from NeoVintageous.nv.state import State
from NeoVintageous.nv.ui import ui_blink
from NeoVintageous.nv.vi import search
from NeoVintageous.nv.vi import units
from NeoVintageous.nv.vi import utils
from NeoVintageous.nv.vi.core import IrreversibleTextCommand
from NeoVintageous.nv.vi.core import ViTextCommandBase
from NeoVintageous.nv.vi.core import ViWindowCommandBase
from NeoVintageous.nv.vi.utils import first_sel
from NeoVintageous.nv.vi.utils import is_view
from NeoVintageous.nv.vi.utils import next_non_blank
from NeoVintageous.nv.vi.utils import next_non_white_space_char
from NeoVintageous.nv.vi.utils import previous_non_white_space_char
from NeoVintageous.nv.vi.utils import regions_transformer
from NeoVintageous.nv.vi.utils import regions_transformer_indexed
from NeoVintageous.nv.vi.utils import regions_transformer_reversed
from NeoVintageous.nv.vi.utils import resolve_insertion_point_at_b
from NeoVintageous.nv.vim import INSERT
from NeoVintageous.nv.vim import INTERNAL_NORMAL
from NeoVintageous.nv.vim import is_visual_mode
from NeoVintageous.nv.vim import NORMAL
from NeoVintageous.nv.vim import SELECT
from NeoVintageous.nv.vim import status_message
from NeoVintageous.nv.vim import UNKNOWN
from NeoVintageous.nv.vim import VISUAL
from NeoVintageous.nv.vim import VISUAL_BLOCK
from NeoVintageous.nv.vim import VISUAL_LINE
from NeoVintageous.nv.window import window_tab_control
from NeoVintageous.nv.window import WindowAPI


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
    '_vi_a',
    '_vi_at',
    '_vi_backtick',
    '_vi_big_a',
    '_vi_big_c',
    '_vi_big_d',
    '_vi_big_i',
    '_vi_big_j',
    '_vi_big_o',
    '_vi_big_p',
    '_vi_big_s',
    '_vi_big_x',
    '_vi_big_z_big_q',
    '_vi_big_z_big_z',
    '_vi_c',
    '_vi_cc',
    '_vi_ctrl_e',
    '_vi_ctrl_g',
    '_vi_ctrl_r',
    '_vi_ctrl_r_equal',
    '_vi_ctrl_right_square_bracket',
    '_vi_ctrl_w_b',
    '_vi_ctrl_w_big_h',
    '_vi_ctrl_w_big_j',
    '_vi_ctrl_w_big_k',
    '_vi_ctrl_w_big_l',
    '_vi_ctrl_w_c',
    '_vi_ctrl_w_equal',
    '_vi_ctrl_w_greater_than',
    '_vi_ctrl_w_h',
    '_vi_ctrl_w_j',
    '_vi_ctrl_w_k',
    '_vi_ctrl_w_l',
    '_vi_ctrl_w_less_than',
    '_vi_ctrl_w_minus',
    '_vi_ctrl_w_n',
    '_vi_ctrl_w_o',
    '_vi_ctrl_w_pipe',
    '_vi_ctrl_w_plus',
    '_vi_ctrl_w_q',
    '_vi_ctrl_w_s',
    '_vi_ctrl_w_t',
    '_vi_ctrl_w_underscore',
    '_vi_ctrl_w_v',
    '_vi_ctrl_w_x',
    '_vi_ctrl_x_ctrl_l',
    '_vi_ctrl_y',
    '_vi_d',
    '_vi_dd',
    '_vi_dot',
    '_vi_equal',
    '_vi_equal_equal',
    '_vi_g_big_c',
    '_vi_g_big_h',
    '_vi_g_big_t',
    '_vi_g_big_u',
    '_vi_g_big_u_big_u',
    '_vi_g_tilde',
    '_vi_g_tilde_g_tilde',
    '_vi_ga',
    '_vi_gc',
    '_vi_gcc_action',  # TODO Refactor name (remove _action)
    '_vi_gcc_motion',  # TODO Refactor name (remove _motion)
    '_vi_gq',
    '_vi_greater_than',
    '_vi_greater_than_greater_than',
    '_vi_gt',
    '_vi_gu',
    '_vi_guu',
    '_vi_gv',
    '_vi_gx',
    '_vi_less_than',
    '_vi_less_than_less_than',
    '_vi_m',
    '_vi_modify_numbers',
    '_vi_o',
    '_vi_p',
    '_vi_q',
    '_vi_quote',
    '_vi_r',
    '_vi_s',
    '_vi_select_big_j',
    '_vi_select_j',
    '_vi_select_k',
    '_vi_tilde',
    '_vi_u',
    '_vi_visual_big_u',
    '_vi_visual_o',
    '_vi_visual_u',
    '_vi_x',
    '_vi_y',
    '_vi_yy',
    '_vi_z_enter',
    '_vi_z_minus',
    '_vi_zz'
]


_log = logging.getLogger(__name__)


class _vi_g_big_u(ViTextCommandBase):

    def run(self, edit, mode=None, count=1, motion=None):
        def f(view, s):
            view.replace(edit, s, view.substr(s).upper())
            # Reverse the resulting region so that _enter_normal_mode
            # collapses the selection as we want it.
            return Region(s.b, s.a)

        if mode not in (INTERNAL_NORMAL, VISUAL, VISUAL_LINE, VISUAL_BLOCK):
            raise ValueError('bad mode: ' + mode)

        if motion is None and mode == INTERNAL_NORMAL:
            raise ValueError('motion data required')

        if mode == INTERNAL_NORMAL:
            self.save_sel()

            self.view.run_command(motion['motion'], motion['motion_args'])

            if self.has_sel_changed():
                regions_transformer(self.view, f)
            else:
                ui_blink()
        else:
            regions_transformer(self.view, f)

        self.enter_normal_mode(mode)


class _vi_gu(ViTextCommandBase):

    def run(self, edit, mode=None, count=1, motion=None):
        def f(view, s):
            view.replace(edit, s, view.substr(s).lower())
            # reverse the resulting region so that _enter_normal_mode collapses the
            # selection as we want it.
            return Region(s.b, s.a)

        if mode not in (INTERNAL_NORMAL, VISUAL, VISUAL_LINE, VISUAL_BLOCK):
            raise ValueError('bad mode: ' + mode)

        if motion is None and mode == INTERNAL_NORMAL:
            raise ValueError('motion data required')

        if mode == INTERNAL_NORMAL:
            self.save_sel()

            self.view.run_command(motion['motion'], motion['motion_args'])

            if self.has_sel_changed():
                regions_transformer(self.view, f)
            else:
                ui_blink()
        else:
            regions_transformer(self.view, f)

        self.enter_normal_mode(mode)


class _vi_gq(ViTextCommandBase):

    def run(self, edit, mode=None, count=1, motion=None):
        def wrap_command():
            hasWrapPlus = self.view.settings().get('WrapPlus.include_line_endings')
            if hasWrapPlus is None:
                return 'wrap_lines'
            else:
                return 'wrap_lines_plus'

        def reverse(view, s):
            return Region(s.end(), s.begin())

        def shrink(view, s):
            if view.substr(s.b - 1) == '\n':
                return Region(s.a, s.b - 1)
            return s

        wrap_lines = wrap_command()

        if mode in (VISUAL, VISUAL_LINE):
            sel = tuple(self.view.sel())

            # TODO: ST seems to always reformat whole paragraphs with 'wrap_lines'.
            regions_transformer(self.view, shrink)
            regions_transformer(self.view, reverse)
            self.view.run_command(wrap_lines)

            self.view.sel().clear()
            for s in sel:
                # Cursors should move to the first non-blank character of the line.
                line = self.view.line(s.begin())
                first_non_ws_char_region = self.view.find('[^\\s]', line.begin())
                self.view.sel().add(first_non_ws_char_region.begin())

            self.enter_normal_mode(mode)

            return

        elif mode == INTERNAL_NORMAL:
            if motion is None:
                raise ValueError('motion data required')

            self.save_sel()

            self.view.run_command(motion['motion'], motion['motion_args'])

            if self.has_sel_changed():
                self.save_sel()
                self.view.run_command(wrap_lines)
                self.view.sel().clear()

                if 'is_jump' in motion and motion['is_jump']:
                    # Cursors should move to end position of motion (exclusive-linewise).
                    self.view.sel().add_all(self.old_sel)
                else:
                    # Cursors should move to start position of motion.
                    for s in self.old_sel:
                        self.view.sel().add(s.begin())
            else:
                ui_blink()

            self.enter_normal_mode(mode)

        else:
            raise ValueError('bad mode: ' + mode)


class _vi_u(ViWindowCommandBase):

    # TODO: surely must accept a mode?
    def run(self, count=1):
        for i in range(count):
            self._view.run_command('undo')

        if self._view.has_non_empty_selection_region():
            def reverse(view, s):
                return Region(s.end(), s.begin())

            # TODO: xpos is misaligned after this.
            regions_transformer(self._view, reverse)
            # FIXME: why from VISUAL?
            self.window.run_command('_enter_normal_mode', {
                'mode': VISUAL
            })

        # If we yy, then u, we might end up with outlined regions if we
        # don't erase them here, because ST will restore them when undoing.
        self._view.erase_regions('highlightedyank')


class _vi_ctrl_r(ViWindowCommandBase):

    def run(self, count=1, mode=None):
        change_count_before = self._view.change_count()

        for i in range(count):
            self._view.run_command('redo')

        change_count_after = self._view.change_count()

        if change_count_after == change_count_before:
            ui_blink()

        # Fix eol issue.
        # See https://github.com/SublimeTextIssues/Core/issues/2121.
        def f(view, s):
            pt = s.b
            char = view.substr(pt)
            if (char == '\n' and not view.line(pt).empty()):
                return Region(pt - 1)

            if char == '\x00' and pt == self._view.size():
                return Region(s.b - 1)

            return s

        regions_transformer(self._view, f)


class _vi_a(ViTextCommandBase):

    def run(self, edit, count=1, mode=None):
        def f(view, s):
            if view.substr(s.b) != '\n' and s.b < view.size():
                return Region(s.b + 1)
            return s

        state = State(self.view)
        # Abort if the *actual* mode is insert mode. This prevents
        # _vi_a from adding spaces between text fragments when used with a
        # count, as in 5aFOO. In that case, we only need to run 'a' the first
        # time, not for every iteration.
        if state.mode == INSERT:
            return

        if mode is None:
            raise ValueError('mode required')
        # TODO: We should probably not define the keys for these modes
        # in the first place.
        elif mode != INTERNAL_NORMAL:
            return

        regions_transformer(self.view, f)
        self.view.window().run_command('_enter_insert_mode', {
            'mode': mode,
            'count': state.normal_insert_count
        })


class _vi_c(ViTextCommandBase):

    def run(self, edit, count=1, mode=None, motion=None, register=None):
        def compact(view, s):
            if view.substr(s).strip():
                if s.b > s.a:
                    pt = previous_non_white_space_char(view, s.b - 1, white_space=' \t\n')

                    return Region(s.a, pt + 1)

                pt = previous_non_white_space_char(view, s.a - 1, white_space=' \t\n')

                return Region(pt + 1, s.b)

            return s

        if mode is None:
            raise ValueError('mode required')

        if (mode == INTERNAL_NORMAL) and (motion is None):
            raise ValueError('motion required')

        self.save_sel()

        if motion:
            self.view.run_command(motion['motion'], motion['motion_args'])

            # Vim ignores trailing white space for c. XXX Always?
            if mode == INTERNAL_NORMAL:
                regions_transformer(self.view, compact)

            if not self.has_sel_changed():
                self.enter_insert_mode(mode)

                return

            # If we ci' and the target is an empty pair of quotes, we should
            # not delete anything.
            # FIXME: This will not work well with multiple selections.
            if all(s.empty() for s in self.view.sel()):
                self.enter_insert_mode(mode)

                return

        self.state.registers.op_change(register=register, linewise=(mode == VISUAL_LINE))
        self.view.run_command('right_delete')
        self.enter_insert_mode(mode)


class _enter_normal_mode(ViTextCommandBase):
    """
    The equivalent of pressing the Esc key in Vim.

    @mode
      The mode we're coming from, which should still be the current mode.

    @from_init
      Whether _enter_normal_mode has been called from init_state. This
      is important to know in order to not hide output panels when the user
      is only navigating files or clicking around, not pressing Esc.
    """

    def run(self, edit, mode=None, from_init=False):
        _log.debug('enter normal mode (mode=%s, from_init=%s)', mode, from_init)
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
                    self.view.window().run_command('hide_panel', {'cancel': True})

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
                state.repeat_data = ('native', self.view.command_history(0)[:2], mode, None)
                # Required here so that the macro gets recorded.
                state.glue_until_normal_mode = False
                state.add_macro_step(*self.view.command_history(0)[:2])
                state.add_macro_step('_enter_normal_mode', {'mode': mode, 'from_init': from_init})
            else:
                state.add_macro_step('_enter_normal_mode', {'mode': mode, 'from_init': from_init})
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
                'repeat_data': state.repeat_data,
            })
            self.view.sel().clear()
            self.view.sel().add_all(new_sels)

        state.update_xpos(force=True)
        state.reset_status()

        self.view.run_command('_nv_fix_st_eol_caret', {'mode': state.mode})


class _enter_normal_mode_impl(ViTextCommandBase):

    def run(self, edit, mode=None):
        _log.debug('enter normal mode (mode=%s) (impl)', mode)

        def f(view, s):
            if mode == INSERT:
                if view.line(s.b).a != s.b:
                    return Region(s.b - 1)

                return Region(s.b)

            if mode == INTERNAL_NORMAL:
                return Region(s.b)

            if mode == VISUAL:
                # Save selections for gv. But only if there are non-empty sels.
                # We might be in visual mode and not have non-empty sels because
                # we've just existed from an action.
                if self.view.has_non_empty_selection_region():
                    self.view.add_regions('visual_sel', list(self.view.sel()))
                    self.view.settings().set('_nv_visual_sel_mode', mode)

                if s.a < s.b:
                    pt = s.b - 1
                    if view.line(pt).empty():
                        return Region(pt)

                    if view.substr(pt) == '\n':
                        pt -= 1

                    return Region(pt)

                return Region(s.b)

            if mode in (VISUAL_LINE, VISUAL_BLOCK):
                # Save selections for gv. But only if there are non-empty sels.
                # We might be in visual mode and not have non-empty sels because
                # we've just existed from an action.
                if self.view.has_non_empty_selection_region():
                    self.view.add_regions('visual_sel', list(self.view.sel()))
                    self.view.settings().set('_nv_visual_sel_mode', mode)

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
            sel = self.view.sel()[0]
            self.view.sel().clear()
            self.view.sel().add(sel)

        regions_transformer(self.view, f)

        if mode == VISUAL_BLOCK and len(self.view.sel()) > 1:
            sel = self.view.sel()[-1]
            self.view.sel().clear()
            self.view.sel().add(Region(sel.b))

        self.view.erase_regions('vi_search')
        self.view.erase_regions('vi_search_current')
        self.view.run_command('_nv_fix_st_eol_caret', {'mode': mode})


class _enter_select_mode(ViWindowCommandBase):

    def run(self, mode=None, count=1):
        self.state.enter_select_mode()

        view = self.window.active_view()

        # If there are no visual selections, do some work work for the user.
        if not view.has_non_empty_selection_region():
            self.window.run_command('find_under_expand')

        state = State(view)
        state.display_status()


class _enter_insert_mode(ViTextCommandBase):

    def run(self, edit, mode=None, count=1):
        self.view.settings().set('inverse_caret_state', False)
        self.view.settings().set('command_mode', False)

        self.state.enter_insert_mode()
        self.state.normal_insert_count = str(count)
        self.state.display_status()


class _enter_visual_mode(ViTextCommandBase):

    def run(self, edit, mode=None):
        state = self.state

        # TODO If all selections are non-zero-length, we may be
        # looking at a pseudo-visual selection, like the ones that are
        # created pressing Alt+Enter when using ST's built-in search dialog.
        # What shall we really do in that case?
        # XXX: In response to the above, we would probably already be in
        # visual mode, but we should double-check that.
        if state.mode == VISUAL:
            self.view.run_command('_enter_normal_mode', {'mode': mode})
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
    """
    Transform the view's selections.

    We don't do this inside the EnterVisualMode window command because ST seems
    to neglect to repaint the selections. (bug?)
    """

    def run(self, edit, mode=None):
        def f(view, s):
            if mode == VISUAL_LINE:
                return Region(s.a, s.b)
            else:
                if s.empty() and (s.b == self.view.size()):
                    ui_blink()

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


class _enter_visual_line_mode(ViTextCommandBase):

    def run(self, edit, mode=None):
        state = self.state

        if state.mode == VISUAL_LINE:
            self.view.run_command('_enter_normal_mode', {'mode': mode})
            return

        if mode in (NORMAL, INTERNAL_NORMAL):

            # Special-case: If cursor is at the very EOF, then try  backup the
            # selection one character so the line, or  previous line is
            # selected (currently only handles non multiple-selections).
            if self.view.size() > 0 and len(self.view.sel()) == 1:
                s = self.view.sel()[0]
                if self.view.substr(s.b) == '\x00':
                    self.view.sel().clear()
                    self.view.sel().add(s.b - 1)

            # Abort if we are at EOF -- no newline char to hold on to.
            if any(s.b == self.view.size() for s in self.view.sel()):
                return ui_blink()

        self.view.run_command('_enter_visual_line_mode_impl', {'mode': mode})
        state.enter_visual_line_mode()
        state.display_status()


class _enter_visual_line_mode_impl(ViTextCommandBase):

    def run(self, edit, mode=None):
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


class _enter_replace_mode(ViTextCommandBase):

    def run(self, edit):
        def f(view, s):
            return Region(s.b)

        state = self.state
        state.settings.view['command_mode'] = False
        state.settings.view['inverse_caret_state'] = False
        state.view.set_overwrite_status(True)
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
            _log.debug('nothing to repeat')
            return

        # TODO: Find out if the user actually meant '1'.
        if count and count == 1:
            count = None

        type_, seq_or_cmd, old_mode, visual_data = repeat_data
        _log.debug('type=%s, seq or cmd=%s, old mode=%s', type_, seq_or_cmd, old_mode)

        if visual_data and (mode != VISUAL):
            state.restore_visual_data(visual_data)
        elif not visual_data and (mode == VISUAL):
            # Can't repeat normal mode commands in visual mode.
            return ui_blink()
        elif mode not in (VISUAL, VISUAL_LINE, NORMAL, INTERNAL_NORMAL, INSERT):
            return ui_blink()

        if type_ == 'vi':
            self.window.run_command('_nv_process_notation', {'keys': seq_or_cmd, 'repeat_count': count})
        elif type_ == 'native':
            sels = list(self.window.active_view().sel())
            # FIXME: We're not repeating as we should. It's the motion that
            # should receive this count.
            for i in range(count or 1):
                self.window.run_command(*seq_or_cmd)
            # FIXME: What happens in visual mode?
            self.window.active_view().sel().clear()
            self.window.active_view().sel().add_all(sels)
        else:
            raise ValueError('bad repeat data')

        self.window.run_command('_enter_normal_mode', {'mode': mode})
        state.repeat_data = repeat_data
        state.update_xpos()


class _vi_dd(ViTextCommandBase):

    def run(self, edit, mode=None, count=1, register='"'):
        def do_motion(view, s):
            if mode != INTERNAL_NORMAL:
                return s

            return units.lines(view, s, count)

        def fixup_sel_pos():
            old = [s.a for s in list(self.view.sel())]
            self.view.sel().clear()
            size = self.view.size()
            new = []
            for pt in old:
                # If on the last char, then pur cursor on previous line
                if pt == size and self.view.substr(pt) == '\x00':
                    pt = self.view.text_point(self.view.rowcol(pt)[0], 0)
                pt = next_non_white_space_char(self.view, pt)
                new.append(pt)
            self.view.sel().add_all(new)

        regions_transformer(self.view, do_motion)
        self.state.registers.op_delete(register=register, linewise=True)
        self.view.run_command('right_delete')
        fixup_sel_pos()


class _vi_cc(ViTextCommandBase):

    def run(self, edit, mode=None, count=1, register='"'):
        def do_motion(view, s):
            if mode != INTERNAL_NORMAL:
                return s

            if view.line(s.b).empty():
                return s

            return units.inner_lines(view, s, count)

        regions_transformer(self.view, do_motion)
        self.state.registers.op_change(register=register, linewise=True)

        if not all(s.empty() for s in self.view.sel()):
            self.view.run_command('right_delete')

        self.enter_insert_mode(mode)
        self.set_xpos(self.state)


class _vi_visual_o(ViTextCommandBase):

    def run(self, edit, mode=None, count=1):
        def f(view, s):
            if mode in (VISUAL, VISUAL_LINE):
                return Region(s.b, s.a)

            return s

        regions_transformer(self.view, f)
        self.view.show(self.view.sel()[0].b, False)


class _vi_yy(ViTextCommandBase):

    def run(self, edit, mode=None, count=1, register=None):
        def select(view, s):

            if mode == INTERNAL_NORMAL:
                if count > 1:
                    row, col = self.view.rowcol(s.b)
                    end = view.text_point(row + count - 1, 0)

                    return Region(view.line(s.a).a, view.full_line(end).b)

                if view.line(s.b).empty():
                    return Region(s.b, min(view.size(), s.b + 1))

                return view.full_line(s.b)

            elif mode == VISUAL:
                startline = view.line(s.begin())
                endline = view.line(s.end() - 1)

                return Region(startline.a, endline.b)

            return s

        def restore():
            self.view.sel().clear()
            self.view.sel().add_all(list(self.old_sel))

        if mode not in (INTERNAL_NORMAL, VISUAL):
            self.enter_normal_mode(mode)
            ui_blink()

            return

        self.save_sel()
        regions_transformer(self.view, select)

        self.outline_target()
        self.state.registers.op_yank(register=register, linewise=True)
        restore()
        self.enter_normal_mode(mode)


class _vi_y(ViTextCommandBase):

    def run(self, edit, mode=None, count=1, motion=None, register=None):
        def f(view, s):
            return Region(next_non_blank(self.view, s.begin()))

        linewise = (mode == VISUAL_LINE)

        if mode == INTERNAL_NORMAL:
            if motion is None:
                raise ValueError('bad args')

            self.view.run_command(motion['motion'], motion['motion_args'])

            # Some text object motions should be treated as a linewise
            # operation, but only if the motion contains a newline.
            if 'text_object' in motion['motion_args']:
                if motion['motion_args']['text_object'] in '%()`/?nN{}':
                    if not linewise:
                        linewise = 'maybe'

        elif mode not in (VISUAL, VISUAL_LINE, VISUAL_BLOCK):
            return

        self.outline_target()

        self.state.registers.op_yank(register=register, linewise=linewise)
        regions_transformer(self.view, f)
        self.enter_normal_mode(mode)


class _vi_d(ViTextCommandBase):

    def run(self, edit, count=1, mode=None, motion=None, register=None):
        if mode not in (INTERNAL_NORMAL, VISUAL, VISUAL_LINE):
            raise ValueError('wrong mode')

        if mode == INTERNAL_NORMAL and not motion:
            raise ValueError('missing motion')

        if motion:
            self.save_sel()
            self.view.run_command(motion['motion'], motion['motion_args'])

            # The motion has failed, so abort.
            if not self.has_sel_changed():
                self.enter_normal_mode(mode)
                ui_blink()

                return

            # If the target's an empty pair of quotes, don't delete.
            # FIXME: This won't work well with multiple sels.
            if all(s.empty() for s in self.view.sel()):
                self.enter_normal_mode(mode)

                return

        self.state.registers.op_delete(register=register, linewise=(mode == VISUAL_LINE))
        self.view.run_command('left_delete')
        self.view.run_command('_nv_fix_st_eol_caret')
        self.enter_normal_mode(mode)

        # XXX: abstract this out for all types of selections.
        def advance_to_text_start(view, s):
            if motion:
                if 'motion' in motion:
                    if motion['motion'] == '_vi_e':
                        return Region(s.begin())
                    elif motion['motion'] == '_vi_dollar':
                        return Region(s.begin())
                    elif motion['motion'] == '_vi_find_in_line':
                        return Region(s.begin())

            return Region(next_non_white_space_char(self.view, s.b))

        if mode == INTERNAL_NORMAL:
            regions_transformer(self.view, advance_to_text_start)

        if mode == VISUAL_LINE:
            def f(view, s):
                return Region(next_non_blank(self.view, s.b))

            regions_transformer(self.view, f)


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

        self.enter_insert_mode(mode)


class _vi_big_i(ViTextCommandBase):

    def run(self, edit, count=1, mode=None):
        def f(view, s):
            if mode == VISUAL_BLOCK:
                return Region(s.begin())
            elif mode == VISUAL:
                return Region(view.line(s.a).a)
            elif mode == VISUAL_LINE:
                return Region(next_non_white_space_char(view, view.line(s.begin()).a))
            elif mode != INTERNAL_NORMAL:
                return s

            return Region(next_non_white_space_char(view, view.line(s.b).a))

        regions_transformer(self.view, f)

        self.enter_insert_mode(mode)


class _vi_m(ViTextCommandBase):

    def run(self, edit, mode=None, count=1, character=None):
        state = self.state
        state.marks.add(character, self.view)

        # TODO: What if we are in visual mode?
        self.enter_normal_mode(mode)


class _vi_quote(ViTextCommandBase):

    def run(self, edit, mode=None, character=None, count=1):
        def f(view, s):
            if mode in (VISUAL, VISUAL_LINE, VISUAL_BLOCK):
                if s.a <= s.b:
                    if address.b < s.b:
                        return Region(s.a + 1, address.b)
                    else:
                        return Region(s.a, address.b)
                else:
                    return Region(s.a + 1, address.b)

            elif mode == NORMAL:
                return address

            elif mode == INTERNAL_NORMAL:
                if s.a < address.a:
                    return Region(view.full_line(s.b).a, view.line(address.b).b)
                return Region(view.full_line(s.b).b, view.line(address.b).a)

            return s

        state = self.state
        address = state.marks.get_as_encoded_address(character)

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

    def run(self, edit, count=1, mode=None, character=None):
        def f(view, s):
            if mode == VISUAL:
                if s.a <= s.b:
                    if address.b < s.b:
                        return Region(s.a + 1, address.b)
                    else:
                        return Region(s.a, address.b)
                else:
                    return Region(s.a + 1, address.b)
            elif mode == NORMAL:
                return address
            elif mode == INTERNAL_NORMAL:
                return Region(s.a, address.b)

            return s

        state = self.state
        address = state.marks.get_as_encoded_address(character, exact=True)

        if address is None:
            return

        if isinstance(address, str):
            if not address.startswith('<command'):
                self.view.window().open_file(address, ENCODED_POSITION)
            return

        # This is a motion in a composite command.
        jumplist_update(self.view)
        regions_transformer(self.view, f)
        jumplist_update(self.view)


class _vi_big_d(ViTextCommandBase):

    def run(self, edit, mode=None, count=1, register=None):
        def f(view, s):
            if mode == INTERNAL_NORMAL:
                if count == 1:
                    if view.line(s.b).size() > 0:
                        return Region(s.b, view.line(s.b).b)

            elif mode == VISUAL:
                startline = view.line(s.begin())
                endline = view.full_line(s.end())

                return Region(startline.a, endline.b)

            return s

        self.save_sel()
        regions_transformer(self.view, f)

        self.state.registers.op_delete(register=register, linewise=is_visual_mode(mode))
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
                self.view.sel().clear()
                self.view.sel().add_all(new_sels)

        self.enter_normal_mode(mode)


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
        self.state.registers.op_change(register=register, linewise=is_visual_mode(mode))

        empty = [s for s in list(self.view.sel()) if s.empty()]
        self.view.add_regions('vi_empty_sels', empty)
        for r in empty:
            self.view.sel().subtract(r)

        self.view.run_command('right_delete')
        self.view.sel().add_all(self.view.get_regions('vi_empty_sels'))
        self.view.erase_regions('vi_empty_sels')
        self.enter_insert_mode(mode)


class _vi_big_s(ViTextCommandBase):

    def run(self, edit, mode=None, count=1, register=None):
        def sel_line(view, s):
            if mode == INTERNAL_NORMAL:
                if count == 1:
                    if view.line(s.b).size() > 0:
                        eol = view.line(s.b).b
                        begin = view.line(s.b).a
                        begin = next_non_white_space_char(view, begin, white_space=' \t')
                        return Region(begin, eol)
                    return s
            return s

        regions_transformer(self.view, sel_line)
        self.state.registers.op_change(register=register, linewise=True)

        empty = [s for s in list(self.view.sel()) if s.empty()]
        self.view.add_regions('vi_empty_sels', empty)
        for r in empty:
            self.view.sel().subtract(r)

        self.view.run_command('right_delete')
        self.view.sel().add_all(self.view.get_regions('vi_empty_sels'))
        self.view.erase_regions('vi_empty_sels')
        self.view.run_command('reindent', {'force_indent': False})
        self.enter_insert_mode(mode)


class _vi_s(ViTextCommandBase):

    def run(self, edit, mode=None, count=1, register=None):
        def select(view, s):
            if mode == INTERNAL_NORMAL:
                line = view.line(s.b)
                if line.empty():
                    return Region(s.b)

                # Should not delete past eol.
                return Region(s.b, min(s.b + count, line.b))

            if mode == VISUAL_LINE:
                return Region(s.begin(), s.end() - 1)

            return Region(s.begin(), s.end())

        if mode not in (VISUAL, VISUAL_LINE, VISUAL_BLOCK, INTERNAL_NORMAL):
            self.enter_normal_mode(mode)
            ui_blink()
            return

        self.save_sel()
        regions_transformer(self.view, select)

        if not self.has_sel_changed() and mode == INTERNAL_NORMAL:
            self.enter_insert_mode(mode)
            return

        self.state.registers.op_delete(register=register, linewise=(mode == VISUAL_LINE))
        self.view.run_command('right_delete')
        self.enter_insert_mode(mode)


class _vi_x(ViTextCommandBase):

    def run(self, edit, mode=None, count=1, register=None):
        def select(view, s):
            if mode == INTERNAL_NORMAL:
                return Region(s.b, min(s.b + count, utils.get_eol(view, s.b)))

            return s

        if mode not in (VISUAL, VISUAL_LINE, VISUAL_BLOCK, INTERNAL_NORMAL):
            self.enter_normal_mode(mode)
            ui_blink()

            return

        if mode == INTERNAL_NORMAL and all(self.view.line(s.b).empty() for s in self.view.sel()):
            return

        regions_transformer(self.view, select)

        self.state.registers.op_delete(register=register, linewise=(mode == VISUAL_LINE))
        self.view.run_command('right_delete')
        self.enter_normal_mode(mode)


class _vi_r(ViTextCommandBase):

    def make_replacement_text(self, char, r):
        frags = self.view.split_by_newlines(r)
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

        char = utils.translate_char(char)
        regions_transformer(self.view, f)
        self.enter_normal_mode(mode)


class _vi_less_than_less_than(ViTextCommandBase):

    def run(self, edit, mode=None, count=None):
        def motion(view, s):
            if mode != INTERNAL_NORMAL:
                return s

            if count <= 1:
                return s

            a = utils.get_bol(view, s.a)
            pt = view.text_point(utils.row_at(view, a) + (count - 1), 0)
            return Region(a, utils.get_eol(view, pt))

        def action(view, s):
            bol = utils.get_bol(view, s.begin())
            pt = next_non_white_space_char(view, bol, white_space='\t ')
            return Region(pt)

        regions_transformer(self.view, motion)
        self.view.run_command('unindent')
        regions_transformer(self.view, action)


class _vi_equal_equal(ViTextCommandBase):

    def run(self, edit, mode=None, count=1):
        def f(view, s):
            return Region(s.begin())

        def select(view):
            s0 = utils.first_sel(self.view)
            end_row = utils.row_at(view, s0.b) + (count - 1)
            view.sel().clear()
            view.sel().add(Region(s0.begin(), view.text_point(end_row, 1)))

        if count > 1:
            select(self.view)

        self.view.run_command('reindent', {'force_indent': False})
        regions_transformer(self.view, f)
        self.enter_normal_mode(mode)


class _vi_greater_than_greater_than(ViTextCommandBase):

    def run(self, edit, mode=None, count=1):
        def f(view, s):
            bol = utils.get_bol(view, s.begin())
            pt = next_non_white_space_char(view, bol, white_space='\t ')
            return Region(pt)

        def select(view):
            s0 = utils.first_sel(view)
            end_row = utils.row_at(view, s0.b) + (count - 1)
            utils.replace_sel(view, Region(s0.begin(), view.text_point(end_row, 1)))

        if count > 1:
            select(self.view)

        self.view.run_command('indent')
        regions_transformer(self.view, f)
        self.enter_normal_mode(mode)


class _vi_greater_than(ViTextCommandBase):

    def run(self, edit, mode=None, count=1, motion=None):
        def f(view, s):
            bol = utils.get_bol(view, s.begin())
            pt = next_non_white_space_char(view, bol, white_space='\t ')

            return Region(pt)

        def indent_from_begin(view, s, level=1):
            block = '\t' if not translate else ' ' * size
            self.view.insert(edit, s.begin(), block * level)
            return Region(s.begin() + 1)

        if mode == VISUAL_BLOCK:
            translate = self.view.settings().get('translate_tabs_to_spaces')
            size = self.view.settings().get('tab_size')
            indent = partial(indent_from_begin, level=count)

            regions_transformer_reversed(self.view, indent)
            regions_transformer(self.view, f)

            # Restore only the first sel.
            s = utils.first_sel(self.view)
            utils.replace_sel(self.view, s.a + 1)
            self.enter_normal_mode(mode)
            return

        if motion:
            self.view.run_command(motion['motion'], motion['motion_args'])
        elif mode not in (VISUAL, VISUAL_LINE):
            return ui_blink()

        for i in range(count):
            self.view.run_command('indent')

        regions_transformer(self.view, f)
        self.enter_normal_mode(mode)


class _vi_less_than(ViTextCommandBase):

    def run(self, edit, mode=None, count=1, motion=None):
        def f(view, s):
            bol = utils.get_bol(view, s.begin())
            pt = next_non_white_space_char(view, bol, white_space='\t ')

            return Region(pt)

        # Note: Vim does not unindent in visual block mode.

        if motion:
            self.view.run_command(motion['motion'], motion['motion_args'])
        elif mode not in (VISUAL, VISUAL_LINE):
            return ui_blink()

        for i in range(count):
            self.view.run_command('unindent')

        regions_transformer(self.view, f)
        self.enter_normal_mode(mode)


class _vi_equal(ViTextCommandBase):

    def run(self, edit, mode=None, count=1, motion=None):
        def f(view, s):
            return Region(s.begin())

        if motion:
            self.view.run_command(motion['motion'], motion['motion_args'])
        elif mode not in (VISUAL, VISUAL_LINE):
            return ui_blink()

        self.view.run_command('reindent', {'force_indent': False})

        regions_transformer(self.view, f)
        self.enter_normal_mode(mode)


class _vi_big_o(ViTextCommandBase):

    def run(self, edit, count=1, mode=None):
        def create_selections(view, sel, index):
            real_sel = Region(sel.a + index * count, sel.b + index * count)
            start_of_line = view.full_line(real_sel).begin()
            view.insert(edit, start_of_line, "\n" * count)
            new = []
            for i in range(0, count):
                new.append(Region(start_of_line + i, start_of_line + i))
            return new

        regions_transformer_indexed(self.view, create_selections)
        self.enter_insert_mode(mode)


class _vi_o(ViTextCommandBase):
    def run(self, edit, count=1, mode=None):
        def create_selections(view, sel, index):
            real_sel = sel if index == 0 else Region(sel.a + index * count, sel.b + index * count)
            end_of_line = view.line(real_sel).end()
            view.insert(edit, end_of_line, "\n" * count)
            new = []
            for i in range(1, count + 1):
                new.append(Region(end_of_line + i, end_of_line + i))
            return new

        regions_transformer_indexed(self.view, create_selections)
        self.enter_insert_mode(mode)


class _vi_big_x(ViTextCommandBase):

    def line_start(self, pt):
        return self.view.line(pt).begin()

    def run(self, edit, count=1, mode=None, register=None):
        def select(view, s):
            nonlocal abort
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
        regions_transformer(self.view, select)

        self.state.registers.op_delete(register=register, linewise=True)

        if not abort:
            self.view.run_command('left_delete')

        self.enter_normal_mode(mode)


class _vi_big_z_big_q(ViWindowCommandBase):

    def run(self):
        do_ex_command(self.window, 'quit', {'forceit': True})


class _vi_big_z_big_z(ViWindowCommandBase):

    def run(self):
        do_ex_command(self.window, 'exit')


class _vi_big_p(ViTextCommandBase):

    def run(self, edit, register=None, count=1, mode=None):
        if len(self.view.sel()) > 1:
            return  # TODO Support multiple selections

        state = self.state

        text, linewise = state.registers.get_for_big_p(register, state.mode)
        if not text:
            return status_message('E353: Nothing in register ' + register)

        sel = self.view.sel()[0]

        if mode == INTERNAL_NORMAL:

            # If register content is from a linewise operation, then the cursor
            # is put on the first non-blank character of the first line of the
            # content after the content is inserted.
            if linewise:
                row = self.view.rowcol(self.view.line(sel.a).a)[0]
                pt = self.view.text_point(row, 0)

                self.view.insert(edit, pt, text)

                pt = next_non_white_space_char(self.view, pt)

                self.view.sel().clear()
                self.view.sel().add(pt)

            # If register is charactwise but contains a newline, then the cursor
            # is put at the start of of the text pasted, otherwise the cursor is
            # put on the last character of the text pasted.
            else:
                if '\n' in text:
                    pt = sel.a
                else:
                    pt = sel.a + len(text) - 1

                self.view.insert(edit, sel.a, text)
                self.view.sel().clear()
                self.view.sel().add(pt)

            self.enter_normal_mode(mode=mode)

        elif mode == VISUAL:

            self.view.replace(edit, sel, text)
            self.enter_normal_mode(mode=mode)

            # If register content is linewise, then the cursor is put on the
            # first non blank of the line.
            if linewise:
                def selection_first_non_blank(view, s):
                    return Region(next_non_white_space_char(view, view.line(s).a))

                regions_transformer(self.view, selection_first_non_blank)

        # Issue #222 Implement VISUAL LINE mode


class _vi_p(ViTextCommandBase):

    def run(self, edit, register=None, count=1, mode=None):
        state = self.state

        register_values, linewise = state.registers.get_for_p(register, state.mode)
        if not register_values:
            return status_message('E353: Nothing in register ' + register)

        sels = list(self.view.sel())
        # If we have the same number of pastes and selections, map 1:1,
        # otherwise paste paste[0] to all target selections.
        if len(sels) == len(register_values):
            sel_to_frag_mapped = zip(sels, register_values)
        else:
            sel_to_frag_mapped = zip(sels, [register_values[0], ] * len(sels))

        # FIXME: Fix this mess. Separate linewise from charwise pasting.
        pasting_linewise = True
        offset = 0
        paste_locations = []
        for selection, fragment in reversed(list(sel_to_frag_mapped)):
            fragment = self.prepare_fragment(fragment)
            if fragment.startswith('\n'):
                # Pasting linewise...
                # If pasting at EOL or BOL, make sure we paste before the newline character.
                if (utils.is_at_eol(self.view, selection) or utils.is_at_bol(self.view, selection)):
                    pa = self.paste_all(edit, selection, self.view.line(selection.b).b, fragment, count)
                    paste_locations.append(pa)
                else:
                    pa = self.paste_all(edit, selection, self.view.line(selection.b - 1).b, fragment, count)
                    paste_locations.append(pa)
            else:
                pasting_linewise = False
                # Pasting charwise...
                # If pasting at EOL, make sure we don't paste after the newline character.
                if self.view.substr(selection.b) == '\n':
                    pa = self.paste_all(edit, selection, selection.b + offset, fragment, count)
                    paste_locations.append(pa)
                else:
                    pa = self.paste_all(edit, selection, selection.b + offset + 1, fragment, count)
                    paste_locations.append(pa)
                offset += len(fragment) * count

        if pasting_linewise:
            self.reset_carets_linewise(paste_locations)
        else:
            self.reset_carets_charwise(paste_locations, len(fragment))

        self.enter_normal_mode(mode)

    def reset_carets_charwise(self, pts, paste_len):
        # FIXME: Won't work for multiple jagged pastes...
        b_pts = [s.b for s in list(self.view.sel())]
        if len(b_pts) > 1:
            self.view.sel().clear()
            self.view.sel().add_all([Region(ploc + paste_len - 1, ploc + paste_len - 1)
                                    for ploc in pts])
        else:
            self.view.sel().clear()
            self.view.sel().add(Region(pts[0] + paste_len - 1, pts[0] + paste_len - 1))

    def reset_carets_linewise(self, pts):
        self.view.sel().clear()

        if self.state.mode == VISUAL_LINE:
            self.view.sel().add_all([Region(loc) for loc in pts])
            return

        pts = [next_non_white_space_char(self.view, pt + 1) for pt in pts]

        self.view.sel().add_all([Region(pt) for pt in pts])

    def prepare_fragment(self, text):
        if text.endswith('\n') and text != '\n':
            text = '\n' + text[0:-1]
        return text

    # TODO: Improve this signature.
    def paste_all(self, edit, sel, at, text, count):
        state = self.state

        if state.mode not in (VISUAL, VISUAL_LINE):
            # TODO: generate string first, then insert?
            # Make sure we can paste at EOF.
            at = at if at <= self.view.size() else self.view.size()
            for x in range(count):
                self.view.insert(edit, at, text)
            return at

        else:
            if text.startswith('\n'):
                text = text * count
                if not text.endswith('\n'):
                    text = text + '\n'
            else:
                text = text * count

            if state.mode == VISUAL_LINE:
                if text.startswith('\n'):
                    text = text[1:]

            self.view.replace(edit, sel, text)
            return sel.begin()


class _vi_ga(ViWindowCommandBase):

    def run(self):
        def char_to_notation(char):
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
            c_str = view.substr(region.begin())
            c_ord = ord(c_str)
            c_hex = hex(c_ord)
            c_oct = oct(c_ord)
            c_not = char_to_notation(c_str)
            status_message('%7s %3s,  Hex %4s,  Octal %5s' % (c_not, c_ord, c_hex, c_oct))


class _vi_gt(ViWindowCommandBase):

    def run(self, count=0, mode=None):
        if count > 0:
            window_tab_control(self.window, action='goto', index=count)
        else:
            window_tab_control(self.window, action='next')

        self.window.run_command('_enter_normal_mode', {'mode': mode})


class _vi_g_big_t(ViWindowCommandBase):

    def run(self, count=1, mode=None):
        window_tab_control(self.window, action='previous')

        self.window.run_command('_enter_normal_mode', {'mode': mode})


# TODO <C-]> could learn visual mode
# TODO <C-]> could learn to count
class _vi_ctrl_right_square_bracket(ViWindowCommandBase):

    def run(self):
        self.window.run_command('goto_definition')


class _vi_ctrl_w_b(ViWindowCommandBase):

    def run(self):
        WindowAPI(self.window).move_group_focus_to_bottom_right()


class _vi_ctrl_w_big_h(ViWindowCommandBase):

    def run(self):
        WindowAPI(self.window).move_current_view_to_far_left()


class _vi_ctrl_w_big_j(ViWindowCommandBase):

    def run(self):
        WindowAPI(self.window).move_current_view_to_very_bottom()


class _vi_ctrl_w_big_k(ViWindowCommandBase):

    def run(self):
        WindowAPI(self.window).move_current_view_to_very_top()


class _vi_ctrl_w_big_l(ViWindowCommandBase):

    def run(self):
        WindowAPI(self.window).move_current_view_to_far_right()


class _vi_ctrl_w_c(ViWindowCommandBase):

    def run(self):
        WindowAPI(self.window).close_current_view()


class _vi_ctrl_w_equal(ViWindowCommandBase):

    def run(self):
        WindowAPI(self.window).resize_groups_almost_equally()


class _vi_ctrl_w_greater_than(ViWindowCommandBase):

    def run(self, count=1):
        WindowAPI(self.window).increase_current_group_width_by_n(count)


class _vi_ctrl_w_h(ViWindowCommandBase):

    def run(self, count=1):
        WindowAPI(self.window).move_group_focus_to_nth_left_of_current_one(count)


class _vi_ctrl_w_j(ViWindowCommandBase):

    def run(self, count=1):
        WindowAPI(self.window).move_group_focus_to_nth_below_current_one(count)


class _vi_ctrl_w_k(ViWindowCommandBase):

    def run(self, count=1):
        WindowAPI(self.window).move_group_focus_to_nth_above_current_one(count)


class _vi_ctrl_w_l(ViWindowCommandBase):

    def run(self, count=1):
        WindowAPI(self.window).move_group_focus_to_nth_right_of_current_one(count)


class _vi_ctrl_w_less_than(ViWindowCommandBase):

    def run(self, count=1):
        WindowAPI(self.window).decrease_current_group_width_by_n(count)


class _vi_ctrl_w_minus(ViWindowCommandBase):

    def run(self, count=1):
        WindowAPI(self.window).decrease_current_group_height_by_n(count)


class _vi_ctrl_w_n(ViWindowCommandBase):

    def run(self, count=1):
        WindowAPI(self.window).split_with_new_file(count)


class _vi_ctrl_w_o(ViWindowCommandBase):

    def run(self):
        WindowAPI(self.window).close_all_other_views()


class _vi_ctrl_w_pipe(ViWindowCommandBase):

    def run(self, count=None):
        WindowAPI(self.window).set_current_group_width_to_n(count)


class _vi_ctrl_w_plus(ViWindowCommandBase):

    def run(self, count=1):
        WindowAPI(self.window).increase_current_group_height_by_n(count)


class _vi_ctrl_w_q(IrreversibleTextCommand):

    def run(self):
        WindowAPI(self.view.window()).quit_current_view(exit_sublime_if_last=True)


class _vi_ctrl_w_s(ViWindowCommandBase):

    def run(self, count=None):
        WindowAPI(self.window).split_current_view_in_two(count)


class _vi_ctrl_w_t(ViWindowCommandBase):

    def run(self):
        WindowAPI(self.window).move_group_focus_to_top_left()


class _vi_ctrl_w_underscore(ViWindowCommandBase):

    def run(self, count=None):
        WindowAPI(self.window).set_current_group_height_to_n(count)


class _vi_ctrl_w_v(ViWindowCommandBase):

    def run(self, count=1, mode=None):
        WindowAPI(self.window).split_current_view_in_two_vertically(count)


class _vi_ctrl_w_x(ViWindowCommandBase):

    def run(self, count=1):
        WindowAPI(self.window).exchange_current_view_with_view_in_next_or_previous_group(count)


# TODO: z<CR> != zt
# TODO if count is given should be the same as CTRL-W__
class _vi_z_enter(IrreversibleTextCommand):

    def run(self, count=1, mode=None):
        pt = resolve_insertion_point_at_b(first_sel(self.view))
        home_line = self.view.line(pt)

        taget_pt = self.view.text_to_layout(home_line.begin())
        self.view.set_viewport_position(taget_pt)


class _vi_z_minus(IrreversibleTextCommand):

    def run(self, count=1, mode=None):
        layout_coord = self.view.text_to_layout(first_sel(self.view).b)
        viewport_extent = self.view.viewport_extent()
        new_pos = (0.0, layout_coord[1] - viewport_extent[1])

        self.view.set_viewport_position(new_pos)


class _vi_zz(IrreversibleTextCommand):

    def run(self, count=1, mode=None):
        first_sel = self.view.sel()[0]
        current_position = self.view.text_to_layout(first_sel.b)
        viewport_dim = self.view.viewport_extent()
        new_pos = (0.0, current_position[1] - viewport_dim[1] / 2)

        self.view.set_viewport_position(new_pos)


class _vi_modify_numbers(ViTextCommandBase):

    DIGIT_PAT = re.compile('(\\D+?)?(-)?(\\d+)(\\D+)?')
    NUM_PAT = re.compile('\\d')

    def get_editable_data(self, pt):
        sign = -1 if (self.view.substr(pt - 1) == '-') else 1
        end = pt
        while self.view.substr(end).isdigit():
            end += 1
        return (sign, int(self.view.substr(Region(pt, end))),
                Region(end, self.view.line(pt).b))

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
        matches = [_vi_modify_numbers.NUM_PAT.search(text) for text in lines]
        if all(matches):
            return [(reg.b + ma.start()) for (reg, ma) in zip(regions, matches)]
        return []

    def run(self, edit, count=1, mode=None, subtract=False):
        # TODO Implement {Visual}CTRL-A
        # TODO Implement {Visual}CTRL-X
        if mode != INTERNAL_NORMAL:
            return

        # TODO Implement CTRL-A and CTRL-X  octal, hex, etc. numbers

        regs = list(self.view.sel())
        pts = self.find_next_num(regs)

        if not pts:
            return ui_blink()

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

    # Clears multiple selections and returns to normal mode. Should be more
    # convenient than having to reach for Esc.

    def run(self, mode=None, count=1):
        s = self.view.sel()[0]
        self.view.sel().clear()
        self.view.sel().add(s)
        self.view.run_command('_enter_normal_mode', {'mode': mode})


class _vi_big_j(ViTextCommandBase):
    WHITE_SPACE = ' \t'

    def run(self, edit, mode=None, count=1, dont_insert_or_remove_spaces=False):
        sels = self.view.sel()
        s = Region(sels[0].a, sels[-1].b)
        if mode == INTERNAL_NORMAL:
            end_pos = self.view.line(s.b).b
            start = end = s.b
            if count > 2:
                end = self.view.text_point(utils.row_at(self.view, s.b) + (count - 1), 0)
                end = self.view.line(end).b
            else:
                # Join current line and the next.
                end = self.view.text_point(utils.row_at(self.view, s.b) + 1, 0)
                end = self.view.line(end).b
        elif mode in [VISUAL, VISUAL_LINE, VISUAL_BLOCK]:
            if s.a < s.b:
                end_pos = self.view.line(s.a).b
                start = s.a
                if utils.row_at(self.view, s.b - 1) == utils.row_at(self.view, s.a):
                    end = self.view.text_point(utils.row_at(self.view, s.a) + 1, 0)
                else:
                    end = self.view.text_point(utils.row_at(self.view, s.b - 1), 0)
                end = self.view.line(end).b
            else:
                end_pos = self.view.line(s.b).b
                start = s.b
                if utils.row_at(self.view, s.b) == utils.row_at(self.view, s.a - 1):
                    end = self.view.text_point(utils.row_at(self.view, s.a - 1) + 1, 0)
                else:
                    end = self.view.text_point(utils.row_at(self.view, s.a - 1), 0)
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

        self.enter_normal_mode(mode=mode)


class _vi_gv(IrreversibleTextCommand):

    def run(self, mode=None, count=None):
        sels = self.view.get_regions('visual_sel')
        if not sels:
            return

        visual_sel_mode = self.view.settings().get('_nv_visual_sel_mode', mode)

        if visual_sel_mode == VISUAL:
            cmd = '_enter_visual_mode'
        elif visual_sel_mode == VISUAL_LINE:
            cmd = '_enter_visual_line_mode'
            for sel in sels:
                a = self.view.line(sel.a)
                b = self.view.line(sel.b)
                if a < b:
                    sel.a = a.begin()
                    sel.b = b.end()
                else:
                    sel.a = a.end()
                    sel.b = b.begin()
        elif visual_sel_mode == VISUAL_BLOCK:
            cmd = '_enter_visual_block_mode'
        else:
            raise RuntimeError('unexpected visual sel mode')

        self.view.window().run_command(cmd, {'mode': mode})
        self.view.sel().clear()
        self.view.sel().add_all(sels)


class _vi_gx(IrreversibleTextCommand):

    URL_REGEX = r"""(?x)
        .*(?P<url>
            https?://               # http:// or https://
            (?:www\.)?              # www.
            (?:[a-zA-Z0-9-]+\.)+    # domain
            [a-zA-Z]+               # tld
            /?[a-zA-Z0-9\-._?,!'(){}\[\]/+&@%$#=:"|~;]*     # url path
        )
    """

    def _url(regex, text):
        match = re.match(regex, text)
        if match:
            url = match.group('url')

            # Remove end of line full stop character.
            url = url.rstrip('.')

            # Remove closing tag markdown link e.g. `[title](url)`.
            url = url.rstrip(')')

            # Remove closing tag markdown image e.g. `![alt](url)]`.
            if url[-2:] == ')]':
                url = url[:-2]

            # Remove trailing quote marks e.g. `"url"`, `'url'`.
            url = url.rstrip('"\'')

            # Remove trailing quote-comma marks e.g. `"url",`, `'url',`.
            if url[-2:] == '",' or url[-2:] == '\',':
                url = url[:-2]

            return url

        return None

    def run(self, mode=None, count=None):
        if len(self.view.sel()) != 1:
            return

        sel = self.view.sel()[0]
        line = self.view.line(sel)
        text = self.view.substr(line)

        url = self.__class__._url(self.URL_REGEX, text)
        if url:
            webbrowser.open_new_tab(url)


class _vi_ctrl_e(ViTextCommandBase):

    def run(self, edit, mode=None, count=1):
        # TODO: Implement this motion properly; don't use built-in commands.
        # We're using an action because we don't care too much right now and we don't want the
        # motion to utils.blink every time we issue it (it does because the selections don't change and
        # NeoVintageous rightfully thinks it has failed.)
        if mode == VISUAL_LINE:
            return
        extend = True if mode == VISUAL else False

        self.view.run_command('scroll_lines', {'amount': -count, 'extend': extend})


class _vi_ctrl_g(ViWindowCommandBase):

    def run(self):
        do_ex_command(self.window, 'file')


class _vi_ctrl_y(ViTextCommandBase):

    def run(self, edit, mode=None, count=1):
        # TODO: Implement this motion properly; don't use built-in commands.
        # We're using an action because we don't care too much right now and we don't want the
        # motion to utils.blink every time we issue it (it does because the selections don't change and
        # NeoVintageous rightfully thinks it has failed.)
        if mode == VISUAL_LINE:
            return
        extend = True if mode == VISUAL else False

        self.view.run_command('scroll_lines', {'amount': count, 'extend': extend})


class _vi_ctrl_r_equal(ViTextCommandBase):

    def run(self, edit, insert=False, next_mode=None):
        def on_done(s):
            state = State(self.view)
            try:
                rv = [str(eval(s, None, None)), ]
                if not insert:
                    state.registers.set_expression(rv)
                else:
                    self.view.run_command('insert_snippet', {'contents': str(rv[0])})
                    state.reset()
            except Exception:
                status_message('invalid expression')
                on_cancel()

        def on_cancel():
            state = State(self.view)
            state.reset()

        self.view.window().show_input_panel('', '', on_done, None, on_cancel)


class _vi_q(IrreversibleTextCommand):

    _current = None

    def run(self, name=None, mode=None, count=1):
        state = State(self.view)

        try:
            if state.is_recording:
                State.macro_registers[self._current] = list(State.macro_steps)
                state.stop_recording()
                self.__class__._current = None
                return

            if name not in tuple('0123456789abcdefghijklmnopqrstuvwABCDEFGHIJKLMNOPQRSTUVW"'):
                return ui_blink("E354: Invalid register name: '" + name + "'")

            state.start_recording()
            self.__class__._current = name
        except (AttributeError, ValueError):
            state.stop_recording()
            self.__class__._current = None
            ui_blink()


class _vi_at(IrreversibleTextCommand):

    _last_used = None

    def run(self, name, mode=None, count=1):
        if name not in tuple('0123456789abcdefghijklmnopqrstuvwABCDEFGHIJKLMNOPQRSTUVW".=*+@'):
            return ui_blink("E354: Invalid register name: '" + name + "'")

        if name == '@':
            name = self._last_used

            if not name:
                return ui_blink('E748: No previously used register')

        try:
            cmds = State.macro_registers[name]
        except (KeyError, ValueError):
            return ui_blink()

        if not cmds:
            return ui_blink()

        self.__class__._last_used = name

        state = State(self.view)

        for i in range(count):
            for cmd, args in cmds:
                # TODO Is this robust enough?
                if 'xpos' in args:
                    state.update_xpos(force=True)
                    args['xpos'] = State(self.view).xpos
                elif args.get('motion') and 'xpos' in args.get('motion'):
                    state.update_xpos(force=True)
                    motion = args.get('motion')
                    motion['motion_args']['xpos'] = State(self.view).xpos
                    args['motion'] = motion

                self.view.run_command(cmd, args)


class _enter_visual_block_mode(ViTextCommandBase):

    def run(self, edit, mode=None):
        def f(view, s):
            return Region(s.b, s.b + 1)

        if mode in (VISUAL_LINE,):
            return

        if mode == VISUAL_BLOCK:
            self.enter_normal_mode(mode)
            return

        if mode == VISUAL:
            first = utils.first_sel(self.view)

            if self.view.line(first.end() - 1).empty():
                self.enter_normal_mode(mode)

                return ui_blink()

            self.view.sel().clear()
            lhs_edge = self.view.rowcol(first.b)[1]  # FIXME # noqa: F841
            regs = self.view.split_by_newlines(first)

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
            return

        # Handling multiple visual blocks seems quite hard, so ensure we only
        # have one.
        first = list(self.view.sel())[0]
        self.view.sel().clear()
        self.view.sel().add(first)

        state = State(self.view)
        state.enter_visual_block_mode()

        if not self.view.has_non_empty_selection_region():
            regions_transformer(self.view, f)

        state.display_status()


class _vi_select_j(ViWindowCommandBase):

    def run(self, count=1, mode=None):
        if mode != SELECT:
            raise ValueError('wrong mode')

        for i in range(count):
            self.window.run_command('find_under_expand')


class _vi_select_k(ViWindowCommandBase):

    def run(self, count=1, mode=None):
        if mode != SELECT:
            raise ValueError('wrong mode')

        for i in range(count):
            self.window.run_command('soft_undo')


class _vi_tilde(ViTextCommandBase):

    def run(self, edit, count=1, mode=None, motion=None):
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

        self.enter_normal_mode(mode)


class _vi_g_tilde(ViTextCommandBase):

    def run(self, edit, count=1, mode=None, motion=None):
        def f(view, s):
            return Region(s.end(), s.begin())

        sels = []
        for s in list(self.view.sel()):
            sels.append(s.a)

        if motion:
            self.save_sel()

            self.view.run_command(motion['motion'], motion['motion_args'])

            if not self.has_sel_changed():
                ui_blink()
                self.enter_normal_mode(mode)
                return

        self.view.run_command('swap_case')

        if motion:
            regions_transformer(self.view, f)

        self.view.sel().clear()
        self.view.sel().add_all(sels)
        self.enter_normal_mode(mode)


class _vi_visual_u(ViTextCommandBase):

    def run(self, edit, mode=None, count=1):
        for s in self.view.sel():
            self.view.replace(edit, s, self.view.substr(s).lower())

        def after(view, s):
            return Region(s.begin())

        regions_transformer(self.view, after)

        self.enter_normal_mode(mode)


class _vi_visual_big_u(ViTextCommandBase):

    def run(self, edit, mode=None, count=1):
        for s in self.view.sel():
            self.view.replace(edit, s, self.view.substr(s).upper())

        def after(view, s):
            return Region(s.begin())

        regions_transformer(self.view, after)

        self.enter_normal_mode(mode)


class _vi_g_tilde_g_tilde(ViTextCommandBase):

    def run(self, edit, count=1, mode=None):
        def select(view, s):
            line = view.line(s.b)

            return Region(line.end(), line.begin())

        if mode != INTERNAL_NORMAL:
            raise ValueError('wrong mode')

        regions_transformer(self.view, select)
        self.view.run_command('swap_case')
        # Ensure we leave the sel .b end where we want it.
        regions_transformer(self.view, select)

        self.enter_normal_mode(mode)


class _vi_g_big_u_big_u(ViTextCommandBase):

    def run(self, edit, mode=None, count=1):
        def select(view, s):
            return units.lines(view, s, count)

        def to_upper(view, s):
            view.replace(edit, s, view.substr(s).upper())
            return Region(next_non_blank(self.view, s.a))

        regions_transformer(self.view, select)
        regions_transformer(self.view, to_upper)
        self.enter_normal_mode(mode)


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
        self.enter_normal_mode(mode)


# Non-standard command. After a search has been performed via '/' or '?',
# selects all matches and enters select mode.
class _vi_g_big_h(ViWindowCommandBase):

    def run(self, mode=None, count=1):
        view = self.window.active_view()

        regs = view.get_regions('vi_search')
        if regs:
            view.sel().add_all(view.get_regions('vi_search'))

            self.state.enter_select_mode()
            self.state.display_status()
            return

        ui_blink()
        status_message('no available search matches')
        self.state.reset_command_data()


class _vi_ctrl_x_ctrl_l(ViTextCommandBase):
    MAX_MATCHES = 20

    def find_matches(self, prefix, end):
        escaped = re.escape(prefix)
        matches = []
        while end > 0:
            match = search.reverse_search(self.view,
                                          r'^\s*{0}'.format(escaped),
                                          0, end, flags=0)
            if (match is None) or (len(matches) == self.MAX_MATCHES):
                break
            line = self.view.line(match.begin())
            end = line.begin()
            text = self.view.substr(line).lstrip()
            if text not in matches:
                matches.append(text)
        return matches

    def run(self, edit, mode=None, register='"'):
        # TODO: Must exit to insert mode. As we're using a quick panel, the
        #       mode is being reset in init_state.
        assert mode == INSERT, 'bad mode'

        if (len(self.view.sel()) > 1 or not self.view.sel()[0].empty()):
            return ui_blink()

        s = self.view.sel()[0]
        line_begin = self.view.text_point(utils.row_at(self.view, s.b), 0)
        prefix = self.view.substr(Region(line_begin, s.b)).lstrip()
        self._matches = self.find_matches(prefix, end=self.view.line(s.b).a)
        if self._matches:
            self.show_matches(self._matches)
            state = State(self.view)
            state.reset_during_init = False
            state.reset_command_data()
            return

        ui_blink()

    def show_matches(self, items):
        self.view.window().show_quick_panel(items, self.replace, MONOSPACE_FONT)

    def replace(self, s):
        self.view.run_command('_nv_replace_line', {'with_what': self._matches[s]})
        del self.__dict__['_matches']
        pt = self.view.sel()[0].b
        self.view.sel().clear()
        self.view.sel().add(Region(pt))


class _vi_gc(ViTextCommandBase):

    def run(self, edit, mode=None, count=1, motion=None):
        def f(view, s):
            return Region(s.begin())

        if motion:
            self.view.run_command(motion['motion'], motion['motion_args'])
        elif mode not in (VISUAL, VISUAL_LINE):
            return ui_blink()

        self.view.run_command('toggle_comment', {'block': False})

        regions_transformer(self.view, f)

        line = self.view.line(self.view.sel()[0].begin())
        pt = line.begin()

        if line.size() > 0:
            line = self.view.find('^\\s*', line.begin())
            pt = line.end()

        self.view.sel().clear()
        self.view.sel().add(pt)

        self.enter_normal_mode(mode)


class _vi_g_big_c(ViTextCommandBase):

    def run(self, edit, mode=None, count=1, motion=None):
        def f(view, s):
            return Region(s.begin())

        if motion:
            self.view.run_command(motion['motion'], motion['motion_args'])
        elif mode not in (VISUAL, VISUAL_LINE):
            return ui_blink()

        self.view.run_command('toggle_comment', {'block': True})

        regions_transformer(self.view, f)
        self.enter_normal_mode(mode)


class _vi_gcc_action(ViTextCommandBase):

    def run(self, edit, mode=None, count=1):
        def f(view, s):
            if mode == INTERNAL_NORMAL:
                view.run_command('toggle_comment')
                if utils.row_at(self.view, s.a) != utils.row_at(self.view, self.view.size()):
                    pt = next_non_white_space_char(view, s.a, white_space=' \t')
                else:
                    pt = next_non_white_space_char(view,
                                                   self.view.line(s.a).a,
                                                   white_space=' \t')

                return Region(pt, pt)

            return s

        self.view.run_command('_vi_gcc_motion', {'mode': mode, 'count': count})

        line = self.view.line(self.view.sel()[0].begin())
        pt = line.begin()

        if line.size() > 0:
            line = self.view.find('^\\s*', line.begin())
            pt = line.end()

        regions_transformer_reversed(self.view, f)

        self.view.sel().clear()
        self.view.sel().add(pt)


class _vi_gcc_motion(ViTextCommandBase):

    def run(self, edit, mode=None, count=1):
        def f(view, s):
            if mode == INTERNAL_NORMAL:
                end = view.text_point(utils.row_at(self.view, s.b) + (count - 1), 0)
                begin = view.line(s.b).a

                row_at_end = utils.row_at(self.view, end)
                row_at_size = utils.row_at(self.view, view.size())

                if ((row_at_end == row_at_size) and (view.substr(begin - 1) == '\n')):
                    begin -= 1

                return Region(begin, view.full_line(end).b)

            return s

        regions_transformer(self.view, f)
