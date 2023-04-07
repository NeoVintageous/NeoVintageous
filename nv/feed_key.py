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

from NeoVintageous.nv.ex_cmds import do_ex_user_cmdline
from NeoVintageous.nv.mappings import IncompleteMapping
from NeoVintageous.nv.mappings import Mapping
from NeoVintageous.nv.mappings import mappings_can_resolve
from NeoVintageous.nv.mappings import mappings_resolve
from NeoVintageous.nv.settings import append_sequence
from NeoVintageous.nv.settings import get_action_count
from NeoVintageous.nv.settings import get_capture_register
from NeoVintageous.nv.settings import get_mode
from NeoVintageous.nv.settings import get_motion_count
from NeoVintageous.nv.settings import get_partial_sequence
from NeoVintageous.nv.settings import get_register
from NeoVintageous.nv.settings import get_sequence
from NeoVintageous.nv.settings import get_setting
from NeoVintageous.nv.settings import is_interactive
from NeoVintageous.nv.settings import set_action_count
from NeoVintageous.nv.settings import set_capture_register
from NeoVintageous.nv.settings import set_mode
from NeoVintageous.nv.settings import set_motion_count
from NeoVintageous.nv.settings import set_partial_sequence
from NeoVintageous.nv.settings import set_register
from NeoVintageous.nv.state import evaluate_state
from NeoVintageous.nv.state import get_action
from NeoVintageous.nv.state import get_motion
from NeoVintageous.nv.state import init_view
from NeoVintageous.nv.state import is_runnable
from NeoVintageous.nv.state import must_collect_input
from NeoVintageous.nv.state import reset_command_data
from NeoVintageous.nv.state import set_action
from NeoVintageous.nv.state import set_motion
from NeoVintageous.nv.state import update_status_line
from NeoVintageous.nv.ui import ui_bell
from NeoVintageous.nv.vi.cmd_base import CommandNotFound
from NeoVintageous.nv.vi.cmd_base import ViCommandDefBase
from NeoVintageous.nv.vi.cmd_base import ViMotionDef
from NeoVintageous.nv.vi.cmd_base import ViOperatorDef
from NeoVintageous.nv.vi.cmd_defs import ViOpenNameSpace
from NeoVintageous.nv.vi.cmd_defs import ViOpenRegister
from NeoVintageous.nv.vi.keys import to_bare_command_name
from NeoVintageous.nv.vim import INSERT
from NeoVintageous.nv.vim import NORMAL
from NeoVintageous.nv.vim import OPERATOR_PENDING
from NeoVintageous.nv.vim import SELECT
from NeoVintageous.nv.vim import VISUAL
from NeoVintageous.nv.vim import VISUAL_BLOCK
from NeoVintageous.nv.vim import VISUAL_LINE
from NeoVintageous.nv.vim import enter_normal_mode
from NeoVintageous.nv.vim import is_visual_mode


_log = logging.getLogger(__name__)


class FeedKeyHandler():

    def __init__(self, view, key: str, repeat_count: int, do_eval: bool, check_user_mappings: bool):
        self.view = view
        self.window = self.view.window()
        self.key = key
        self.repeat_count = repeat_count
        self.do_eval = do_eval
        self.check_user_mappings = check_user_mappings
        self.mode = get_mode(self.view)
        _log.info(
            'key evt: %s %s count=%s eval=%s mappings=%s',
            key,
            self.mode,
            repeat_count,
            do_eval,
            check_user_mappings)

    def handle(self) -> None:
        self._handle_bad_selection()

        if self._handle_escape():
            return

        self._append_sequence()

        if self._handle_register():
            return

        if self._collect_input():
            return

        self._handle()

    def _handle_bad_selection(self) -> None:
        if _is_selection_malformed(self.view, self.mode):
            self.mode = _fix_malformed_selection(self.view, self.mode)

    def _handle_escape(self) -> bool:
        if self.key.lower() == '<esc>':
            if (self.mode == INSERT and
                    self.view.is_auto_complete_visible() and
                    not get_setting(self.view, 'auto_complete_exit_from_insert_mode')):
                self.view.window().run_command('hide_auto_complete')
            elif self.mode == SELECT:
                self.view.run_command('nv_vi_select_big_j', {'mode': self.mode})
            else:
                enter_normal_mode(self.window, self.mode)
                reset_command_data(self.view)

            return True

        return False

    def _append_sequence(self) -> None:
        append_sequence(self.view, self.key)
        update_status_line(self.view)

    def _handle_register(self) -> bool:
        if get_capture_register(self.view):
            set_register(self.view, self.key)
            set_partial_sequence(self.view, '')

            return True

        return False

    def _collect_input(self) -> bool:
        motion = get_motion(self.view)
        action = get_action(self.view)

        if must_collect_input(self.view, motion, action):
            if motion and motion.accept_input:
                motion.accept(self.key)
                set_motion(self.view, motion)  # Processed motion needs to reserialised and stored.
            else:
                action.accept(self.key)
                set_action(self.view, action)  # Processed action needs to reserialised and stored.

            if is_runnable(self.view) and self.do_eval:
                evaluate_state(self.view)
                reset_command_data(self.view)

            return True

        return False

    def _handle_count(self) -> bool:
        # NOTE motion/action counts need to be cast to strings because they need
        # to be "joined" to the previous key press, not added. For example when
        # you press the digit 1 followed by 2, it's a count of 12, not 3.

        if self.repeat_count:
            set_action_count(self.view, str(self.repeat_count))

        if not get_action(self.view) and self.key.isdigit():
            if not self.repeat_count and (self.key != '0' or get_action_count(self.view)):
                set_action_count(self.view, str(get_action_count(self.view)) + self.key)
                return True

        if (get_action(self.view) and (get_mode(self.view) == OPERATOR_PENDING) and self.key.isdigit()):
            if not self.repeat_count and (self.key != '0' or get_motion_count(self.view)):
                set_motion_count(self.view, str(get_motion_count(self.view)) + self.key)
                return True

        return False

    def _handle(self) -> None:
        # If the user has defined a mapping that starts with a number i.e. count
        # then the count handler has to be skipped otherwise it won't resolve.
        # See https://github.com/NeoVintageous/NeoVintageous/issues/434.
        if not mappings_can_resolve(self.view, self.key):
            if self._handle_count():
                return

        set_partial_sequence(self.view, get_partial_sequence(self.view) + self.key)

        command = mappings_resolve(self.view, check_user_mappings=self.check_user_mappings)

        if isinstance(command, IncompleteMapping):
            return

        if isinstance(command, ViOpenNameSpace):
            return

        if isinstance(command, ViOpenRegister):
            set_capture_register(self.view, True)
            return

        if isinstance(command, Mapping):
            self._handle_mapping(command)
            return

        if isinstance(command, CommandNotFound):

            # TODO We shouldn't need to try resolve the command again. The
            # resolver should handle commands correctly the first time. The
            # reason this logic is still needed is because we might be looking
            # at a command like 'dd', which currently doesn't resolve properly.
            # The first 'd' is mapped for NORMAL mode, but 'dd' is not mapped in
            # OPERATOR PENDING mode, so we get a missing command, and here we
            # try to fix that (user mappings are excluded, since they've already
            # been given a chance to evaluate).

            if get_mode(self.view) == OPERATOR_PENDING:
                command = mappings_resolve(self.view, sequence=to_bare_command_name(get_sequence(self.view)),
                                           mode=NORMAL, check_user_mappings=False)
            else:
                command = mappings_resolve(self.view, sequence=to_bare_command_name(get_sequence(self.view)))

            if self._handle_command_not_found(command):
                return

        if (isinstance(command, ViOperatorDef) and get_mode(self.view) == OPERATOR_PENDING):

            # TODO This should be unreachable code. The mapping resolver should
            # handle anything that can still reach this point (the first time).
            # We're expecting a motion, but we could still get an action. For
            # example, dd, g~g~ or g~~ remove counts. It looks like it might
            # only be the '>>' command that needs this code.

            command = mappings_resolve(self.view, sequence=to_bare_command_name(get_sequence(self.view)), mode=NORMAL)
            if self._handle_command_not_found(command):
                return

            if not command.motion_required:
                set_mode(self.view, NORMAL)

        self._handle_command(command, self.do_eval)

    def _handle_mapping(self, command) -> None:
        # TODO Review What happens if Mapping + do_eval=False
        if self.do_eval:
            _log.debug('evaluating user mapping...')

            # TODO Review Why does rhs of mapping need to be resequenced in OPERATOR PENDING mode?
            rhs = command.rhs
            if get_mode(self.view) == OPERATOR_PENDING:
                rhs = get_sequence(self.view)[:-len(get_partial_sequence(self.view))] + command.rhs

            # TODO Review Why does state need to be reset before running user mapping?
            reg = get_register(self.view)
            acount = get_action_count(self.view)
            mcount = get_motion_count(self.view)
            reset_command_data(self.view)
            set_register(self.view, reg)
            set_motion_count(self.view, mcount)
            set_action_count(self.view, acount)

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
                    # Example :reg
                    command = rhs
                    trailing = ''

                _log.debug('parsed user mapping before="%s", cmd="%s", after="%s"', leading, command, trailing)

                if leading:
                    self.window.run_command('nv_process_notation', {
                        'keys': leading,
                        'check_user_mappings': False,
                    })

                do_ex_user_cmdline(self.window, command)

                if trailing:
                    self.window.run_command('nv_process_notation', {
                        'keys': trailing,
                        'check_user_mappings': False,
                    })

            else:
                self.window.run_command('nv_process_notation', {
                    'keys': rhs,
                    'check_user_mappings': False,
                })

    def _handle_command(self, command: ViCommandDefBase, do_eval: bool) -> None:
        # Raises:
        #   ValueError: If too many motions.
        #   ValueError: If too many actions.
        #   ValueError: Unexpected command type.
        _is_runnable = is_runnable(self.view)

        if isinstance(command, ViMotionDef):
            if _is_runnable:
                raise ValueError('too many motions')

            set_motion(self.view, command)

            if get_mode(self.view) == OPERATOR_PENDING:
                set_mode(self.view, NORMAL)

        elif isinstance(command, ViOperatorDef):
            if _is_runnable:
                raise ValueError('too many actions')

            set_action(self.view, command)

            if command.motion_required and not is_visual_mode(get_mode(self.view)):
                set_mode(self.view, OPERATOR_PENDING)

        else:
            raise ValueError('unexpected command type')

        if is_interactive(self.view):
            if command.accept_input and command.input_parser and command.input_parser.is_panel():
                command.input_parser.run_command(self.view.window())

        if get_mode(self.view) == OPERATOR_PENDING:
            set_partial_sequence(self.view, '')

        if do_eval:
            evaluate_state(self.view)

    def _handle_command_not_found(self, command) -> bool:
        if isinstance(command, CommandNotFound):
            if get_mode(self.view) == OPERATOR_PENDING:
                set_mode(self.view, NORMAL)

            reset_command_data(self.view)
            ui_bell()

            return True

        return False


def _is_selection_malformed(view, mode) -> bool:
    return mode not in (VISUAL, VISUAL_LINE, VISUAL_BLOCK, SELECT) and view.has_non_empty_selection_region()


def _fix_malformed_selection(view, mode: str) -> str:
    # If a selection was made via the mouse or a built-in ST command the
    # selection may be in an inconsistent state e.g. incorrect mode.
    # https://github.com/NeoVintageous/NeoVintageous/issues/742
    if mode == NORMAL and len(view.sel()) > 1:
        mode = VISUAL
        set_mode(view, mode)
    elif mode != VISUAL and view.has_non_empty_selection_region():
        # Try to fixup a malformed visual state. For example, apparently this
        # can happen when a search is performed via a search panel and "Find
        # All" is pressed. In that case, multiple selections may need fixing.
        view.window().run_command('nv_enter_visual_mode', {'mode': mode})

    # TODO Extract fix malformed selections specific logic from init_view()
    init_view(view)

    return mode
