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

from sublime import active_window

from NeoVintageous.nv import macros
from NeoVintageous.nv import plugin
from NeoVintageous.nv.settings import get_count
from NeoVintageous.nv.settings import get_mode
from NeoVintageous.nv.settings import get_partial_sequence
from NeoVintageous.nv.settings import get_reset_during_init
from NeoVintageous.nv.settings import get_setting
from NeoVintageous.nv.settings import is_non_interactive
from NeoVintageous.nv.settings import is_processing_notation
from NeoVintageous.nv.settings import set_action_count
from NeoVintageous.nv.settings import set_mode
from NeoVintageous.nv.settings import set_motion_count
from NeoVintageous.nv.settings import set_must_capture_register_name
from NeoVintageous.nv.settings import set_partial_sequence
from NeoVintageous.nv.settings import set_register
from NeoVintageous.nv.settings import set_repeat_data
from NeoVintageous.nv.settings import set_reset_during_init
from NeoVintageous.nv.utils import get_visual_repeat_data
from NeoVintageous.nv.utils import is_view
from NeoVintageous.nv.utils import save_previous_selection
from NeoVintageous.nv.utils import scroll_into_view
from NeoVintageous.nv.utils import update_xpos
from NeoVintageous.nv.vi import cmd_defs
from NeoVintageous.nv.vi.cmd_base import ViMotionDef
from NeoVintageous.nv.vi.cmd_base import ViOperatorDef
from NeoVintageous.nv.vi.cmd_defs import ViToggleMacroRecorder
from NeoVintageous.nv.vi.settings import SettingsManager
from NeoVintageous.nv.vim import INSERT
from NeoVintageous.nv.vim import INTERNAL_NORMAL
from NeoVintageous.nv.vim import NORMAL
from NeoVintageous.nv.vim import OPERATOR_PENDING
from NeoVintageous.nv.vim import REPLACE
from NeoVintageous.nv.vim import UNKNOWN
from NeoVintageous.nv.vim import VISUAL
from NeoVintageous.nv.vim import VISUAL_BLOCK
from NeoVintageous.nv.vim import VISUAL_LINE
from NeoVintageous.nv.vim import clean_view
from NeoVintageous.nv.vim import enter_insert_mode
from NeoVintageous.nv.vim import is_visual_mode
from NeoVintageous.nv.vim import mode_to_name
from NeoVintageous.nv.vim import reset_status_line
from NeoVintageous.nv.vim import run_action
from NeoVintageous.nv.vim import run_motion
from NeoVintageous.nv.vim import run_window_command


_log = logging.getLogger(__name__)


def _must_scroll_into_view(motion: ViMotionDef, action: ViOperatorDef) -> bool:
    if motion and motion.scroll_into_view:
        return True

    if action and action.scroll_into_view:
        return True

    return False


def _must_update_xpos(motion: ViMotionDef, action: ViOperatorDef) -> bool:
    if motion and motion.updates_xpos:
        return True

    if action and action.updates_xpos:
        return True

    return False


class State(object):

    def __init__(self, view):
        self.view = view
        self.settings = SettingsManager(self.view)

    @property
    def glue_until_normal_mode(self) -> bool:
        """
        Indicate that editing commands should be grouped together.

        They should be grouped together in a single undo step after the user
        requested `_enter_normal_mode` next.

        This property is *VOLATILE*; it shouldn't be persisted between
        sessions.
        """
        return self.settings.vi['_vintageous_glue_until_normal_mode'] or False

    @glue_until_normal_mode.setter
    def glue_until_normal_mode(self, value: bool) -> None:
        self.settings.vi['_vintageous_glue_until_normal_mode'] = value

    @property
    def sequence(self) -> str:
        # Sequence of keys provided by the user.
        return self.settings.vi['sequence'] or ''

    @sequence.setter
    def sequence(self, value: str) -> None:
        _log.debug('set sequence >>>%s<<<', value)
        self.settings.vi['sequence'] = value

    @property  # DEPRECATED
    def partial_sequence(self) -> str:
        return get_partial_sequence(self.view)

    @partial_sequence.setter  # DEPRECATED
    def partial_sequence(self, value: str) -> None:
        set_partial_sequence(self.view, value)

    @property  # DEPRECATED
    def mode(self) -> str:
        return get_mode(self.view)

    @mode.setter  # DEPRECATED
    def mode(self, value: str) -> None:
        set_mode(self.view, value)

    @property
    def action(self):
        action = self.settings.vi['action'] or None
        if action:
            cls = getattr(cmd_defs, action['name'], None)
            if cls is None:
                cls = plugin.classes.get(action['name'], None)
            if cls is None:
                ValueError('unknown action: %s' % action)
            return cls.from_json(action['data'])

    @action.setter
    def action(self, value) -> None:
        serialized = value.serialize() if value else None
        self.settings.vi['action'] = serialized

    @property
    def motion(self):
        motion = self.settings.vi['motion'] or None

        if motion:
            cls = getattr(cmd_defs, motion['name'])

            return cls.from_json(motion['data'])

    @motion.setter
    def motion(self, value) -> None:
        serialized = value.serialize() if value else None
        self.settings.vi['motion'] = serialized

    @property
    def count(self) -> int:
        return get_count(self.view, default=1)

    @property
    def count_default_zero(self) -> int:
        # TODO Refactor: method was required because count() defaults to 1
        return get_count(self.view, default=0)

    def must_collect_input(self, view, motion: ViMotionDef, action: ViOperatorDef) -> bool:
        if motion and action:
            if motion.accept_input:
                return True

            return (action.accept_input and action.input_parser is not None and action.input_parser.is_after_motion())

        # Special case: `q` should stop the macro recorder if it's running and
        # not request further input from the user.
        if (isinstance(action, ViToggleMacroRecorder) and macros.is_recording(view.window())):
            return False

        if (action and action.accept_input and action.input_parser and action.input_parser.is_immediate()):
            return True

        if motion:
            return motion.accept_input

        return False

    def display_status(self) -> None:
        mode_name = mode_to_name(self.mode)
        if mode_name:
            self.view.set_status('vim-mode', '-- {} --'.format(mode_name) if mode_name else '')

        self.view.set_status('vim-seq', self.sequence)

    def reset_command_data(self) -> None:
        # Resets all temp data needed to build a command or partial command.
        motion = self.motion
        action = self.action

        if _must_update_xpos(motion, action):
            update_xpos(self.view)

        if _must_scroll_into_view(motion, action):
            # Intentionally using the active view because the previous command
            # may have switched views and self.view would be the previous one.
            scroll_into_view(active_window().active_view(), self.mode)

        action and action.reset()
        self.action = None
        motion and motion.reset()
        self.motion = None
        set_action_count(self.view, '')
        set_motion_count(self.view, '')

        self.sequence = ''
        self.partial_sequence = ''
        set_register(self.view, '"')
        set_must_capture_register_name(self.view, False)
        reset_status_line(self.view, self.mode)

    def runnable(self) -> bool:
        # Returns:
        #   True if motion and/or action is in a runnable state, False otherwise.
        # Raises:
        #   ValueError: Invlid mode.
        action = self.action
        motion = self.motion

        if self.must_collect_input(self.view, motion, action):
            return False

        mode = self.mode

        if action and motion:
            if mode != NORMAL:
                raise ValueError('invalid mode')

            return True

        if (action and (not action.motion_required or is_visual_mode(mode))):
            if mode == OPERATOR_PENDING:
                raise ValueError('action has invalid mode')

            return True

        if motion:
            if mode == OPERATOR_PENDING:
                raise ValueError('motion has invalid mode')

            return True

        return False

    def eval(self) -> None:
        _log.debug('evaluating...')
        if not self.runnable():
            _log.debug('not runnable!')
            return

        if self.action and self.motion:

            # Evaluate action with motion: runs the action with the motion as an
            # argument. The motion's mode is set to INTERNAL_NORMAL and is run
            # by the action internally to make the selection it operates on. For
            # example the motion commands can be used after an operator command,
            # to have the command operate on the text that was moved over.

            action_cmd = self.action.translate(self)
            motion_cmd = self.motion.translate(self)

            _log.debug('action: %s', action_cmd)
            _log.debug('motion: %s', motion_cmd)

            self.mode = INTERNAL_NORMAL

            if 'mode' in action_cmd['action_args']:
                action_cmd['action_args']['mode'] = INTERNAL_NORMAL

            if 'mode' in motion_cmd['motion_args']:
                motion_cmd['motion_args']['mode'] = INTERNAL_NORMAL

            args = action_cmd['action_args']

            args['count'] = 1

            # Let the action run the motion within its edit object so that we
            # don't need to worry about grouping edits to the buffer.
            args['motion'] = motion_cmd

            if self.glue_until_normal_mode and not is_processing_notation(self.view):
                run_window_command('mark_undo_groups_for_gluing')

            macros.add_step(self, action_cmd['action'], args)

            run_window_command(action_cmd['action'], args)

            if not is_non_interactive(self.view) and self.action.repeatable:
                set_repeat_data(self.view, ('vi', str(self.sequence), self.mode, None))

            self.reset_command_data()

            return  # Nothing more to do.

        if self.motion:

            # Evaluate motion: Run it.

            motion_cmd = self.motion.translate(self)

            _log.debug('motion: %s', motion_cmd)

            macros.add_step(self, motion_cmd['motion'], motion_cmd['motion_args'])

            run_motion(self.view, motion_cmd)

        if self.action:

            # Evaluate action. Run it.

            action_cmd = self.action.translate(self)

            _log.debug('action: %s', action_cmd)

            if self.mode == NORMAL:
                self.mode = INTERNAL_NORMAL

                if 'mode' in action_cmd['action_args']:
                    action_cmd['action_args']['mode'] = INTERNAL_NORMAL

            elif is_visual_mode(self.mode):
                # Special-case exclusion: saving the previous selection would
                # overwrite the previous selection needed e.g. gv in a VISUAL
                # mode needs to expand or contract to previous selection.
                if action_cmd['action'] != '_vi_gv':
                    save_previous_selection(self.view, self.mode)

            # Some commands, like 'i' or 'a', open a series of edits that need
            # to be grouped together unless we are gluing a larger sequence
            # through _nv_process_notation. For example, aFOOBAR<Esc> should be
            # grouped atomically, but not inside a sequence like
            # iXXX<Esc>llaYYY<Esc>, where we want to group the whole sequence
            # instead.
            if self.glue_until_normal_mode and not is_processing_notation(self.view):
                run_window_command('mark_undo_groups_for_gluing')

            sequence = self.sequence
            visual_repeat_data = get_visual_repeat_data(self.view, self.mode)
            action = self.action

            macros.add_step(self, action_cmd['action'], action_cmd['action_args'])

            run_action(active_window(), action_cmd)

            if not (is_processing_notation(self.view) and self.glue_until_normal_mode) and action.repeatable:
                set_repeat_data(self.view, ('vi', sequence, self.mode, visual_repeat_data))

        if self.mode == INTERNAL_NORMAL:
            self.mode = NORMAL

        self.reset_command_data()


def init_state(view) -> None:
    # Initialise view state.
    #
    # Runs every time a view is activated, loaded, etc.

    # Don't initialise if we get a console, widget, panel, or any other view
    # where Vim modes are not relevant. Some related initialised settings that
    # may cause unexpected behaviours if they exist are erased "cleaned" too.
    if not is_view(view):
        try:
            # TODO "cleaning" views that are not initialised shouldn't be necessary?
            clean_view(view)
        except Exception:
            _log.debug('could not clean an object: console, widget, panel, etc.')
        finally:
            return

    if not get_reset_during_init(view):
        # Probably exiting from an input panel, like when using '/'. Don't reset
        # the global state, as it may contain data needed to complete the
        # command that's being built.
        set_reset_during_init(view, True)
        return

    state = State(view)

    mode = get_mode(view)

    # Does user want to reset mode (to normal mode) when initialising state?
    if mode not in (NORMAL, UNKNOWN) and not get_setting(view, 'reset_mode_when_switching_tabs'):
        return

    # Fix malformed selection: if we have no selections, add one.
    if len(view.sel()) == 0:
        view.sel().add(0)

    if get_setting(view, 'default_mode') == 'insert':
        if mode in (NORMAL, UNKNOWN):
            enter_insert_mode(view, mode)
    elif mode in (VISUAL, VISUAL_LINE, VISUAL_BLOCK):
        # Visual modes are not reset (to normal mode), because actions like
        # pressing the super key or opening a command-palette/overlay will cause
        # the active view to lose focus and when focus is received again it
        # triggers the on_activated() event, this in turn initialises the view'
        # state, which would reset the visual mode to normal mode, therefore,
        # for example, any command run from the command palette that expects to
        # operate on a visual selection wouldn't work because the visual
        # selection is reset to normal mode before the command has time to run.
        # See https://github.com/NeoVintageous/NeoVintageous/issues/547
        pass
    elif mode in (INSERT, REPLACE):
        # NOTE that the mode is not passed as an argument because it causes the
        # cursor to move back one point from it's current position, for example
        # when pressing i<Esc>i<Esc>i<Esc> the cursor moves one point each time,
        # which is expected, but not expected when initialising state. But not
        # passing the mode may also be causing some other hidden bugs too.
        view.window().run_command('_enter_normal_mode', {'from_init': True})
    elif mode != VISUAL and view.has_non_empty_selection_region():
        # Try to fixup a malformed visual state. For example, apparently this
        # can happen when a search is performed via a search panel and "Find
        # All" is pressed. In that case, multiple selections may need fixing.
        view.window().run_command('_enter_visual_mode', {'mode': mode})
    else:
        # This may be run when we're coming from cmdline mode.
        mode = VISUAL if view.has_non_empty_selection_region() else mode
        view.window().run_command('_enter_normal_mode', {'mode': mode, 'from_init': True})

    state.reset_command_data()
