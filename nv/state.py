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
from NeoVintageous.nv.macros import add_macro_step
from NeoVintageous.nv.polyfill import run_window_command
from NeoVintageous.nv.session import get_session_view_value
from NeoVintageous.nv.session import set_session_view_value
from NeoVintageous.nv.settings import get_glue_until_normal_mode
from NeoVintageous.nv.settings import get_mode
from NeoVintageous.nv.settings import get_reset_during_init
from NeoVintageous.nv.settings import get_sequence
from NeoVintageous.nv.settings import get_setting
from NeoVintageous.nv.settings import is_interactive
from NeoVintageous.nv.settings import is_processing_notation
from NeoVintageous.nv.settings import set_action_count
from NeoVintageous.nv.settings import set_mode
from NeoVintageous.nv.settings import set_motion_count
from NeoVintageous.nv.settings import set_must_capture_register_name
from NeoVintageous.nv.settings import set_partial_sequence
from NeoVintageous.nv.settings import set_register
from NeoVintageous.nv.settings import set_repeat_data
from NeoVintageous.nv.settings import set_reset_during_init
from NeoVintageous.nv.settings import set_sequence
from NeoVintageous.nv.utils import get_visual_repeat_data
from NeoVintageous.nv.utils import is_view
from NeoVintageous.nv.utils import save_previous_selection
from NeoVintageous.nv.utils import update_xpos
from NeoVintageous.nv.vi import cmd_defs
from NeoVintageous.nv.vi.cmd_base import ViMotionDef
from NeoVintageous.nv.vi.cmd_base import ViOperatorDef
from NeoVintageous.nv.vi.cmd_defs import ViToggleMacroRecorder
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


_log = logging.getLogger(__name__)


def update_status_line(view) -> None:
    mode_name = mode_to_name(get_mode(view))
    if mode_name:
        view.set_status('vim-mode', '-- {} --'.format(mode_name) if mode_name else '')

    view.set_status('vim-seq', get_sequence(view))


def must_collect_input(view, motion: ViMotionDef, action: ViOperatorDef) -> bool:
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


def _scroll_into_view(view, mode: str) -> None:
    sels = view.sel()
    if len(sels) < 1:
        return

    # Show the *last* cursor on screen. There is currently no way to
    # identify the "active" cursor of a multiple cursor selection.
    sel = sels[-1]

    target_pt = sel.b

    # In VISUAL mode we need to make sure that any newline at the end of
    # the selection is NOT included in the target, because otherwise an
    # extra line after the target line will also be scrolled into view.
    if is_visual_mode(mode):
        if sel.b > sel.a:
            if view.substr(sel.b - 1) == '\n':
                target_pt = max(0, target_pt - 1)
                # Use the start point of the target line to avoid
                # horizontal scrolling. For example, this can happen in
                # VISUAL LINE mode when the EOL is off-screen.
                target_pt = max(0, view.line(target_pt).a)

    view.show(target_pt, False)


def _create_definition(view, name: str):
    cmd = get_session_view_value(view, name)
    if cmd:
        cls = getattr(cmd_defs, cmd['name'], None)

        if cls is None:
            cls = plugin.classes.get(cmd['name'], None)

        if cls is None:
            ValueError('unknown %s: %s' % (name, cmd))

        return cls.from_json(cmd['data'])


def get_action(view):
    return _create_definition(view, 'action')


def set_action(view, value) -> None:
    serialized = value.serialize() if value else None
    set_session_view_value(view, 'action', serialized)


def get_motion(view):
    return _create_definition(view, 'motion')


def set_motion(view, value) -> None:
    serialized = value.serialize() if value else None
    set_session_view_value(view, 'motion', serialized)


def reset_command_data(view) -> None:
    # Resets all temp data needed to build a command or partial command.
    motion = get_motion(view)
    action = get_action(view)

    if _must_update_xpos(motion, action):
        update_xpos(view)

    if _must_scroll_into_view(motion, action):
        # Intentionally using the active view because the previous command
        # may have switched views and view would be the previous one.
        active_view = active_window().active_view()
        if active_view:
            _scroll_into_view(active_view, get_mode(active_view))

    action and action.reset()
    set_action(view, None)
    motion and motion.reset()
    set_motion(view, None)
    set_action_count(view, '')
    set_motion_count(view, '')
    set_sequence(view, '')
    set_partial_sequence(view, '')
    set_register(view, '"')
    set_must_capture_register_name(view, False)
    reset_status_line(view, get_mode(view))


def is_runnable(view) -> bool:
    # Returns:
    #   True if motion and/or action is in a runnable state, False otherwise.
    # Raises:
    #   ValueError: Invlid mode.
    action = get_action(view)
    motion = get_motion(view)

    if must_collect_input(view, motion, action):
        return False

    mode = get_mode(view)

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


def evaluate_state(view) -> None:
    _log.debug('evaluating...')
    if not is_runnable(view):
        _log.debug('not runnable!')
        return

    action = get_action(view)
    motion = get_motion(view)

    if action and motion:

        # Evaluate action with motion: runs the action with the motion as an
        # argument. The motion's mode is set to INTERNAL_NORMAL and is run
        # by the action internally to make the selection it operates on. For
        # example the motion commands can be used after an operator command,
        # to have the command operate on the text that was moved over.

        action_cmd = action.translate(view)
        motion_cmd = motion.translate(view)

        _log.debug('action: %s', action_cmd)
        _log.debug('motion: %s', motion_cmd)

        set_mode(view, INTERNAL_NORMAL)

        if 'mode' in action_cmd['action_args']:
            action_cmd['action_args']['mode'] = INTERNAL_NORMAL

        if 'mode' in motion_cmd['motion_args']:
            motion_cmd['motion_args']['mode'] = INTERNAL_NORMAL

        args = action_cmd['action_args']

        args['count'] = 1

        # Let the action run the motion within its edit object so that we
        # don't need to worry about grouping edits to the buffer.
        args['motion'] = motion_cmd

        if get_glue_until_normal_mode(view) and not is_processing_notation(view):
            run_window_command('mark_undo_groups_for_gluing')

        add_macro_step(view, action_cmd['action'], args)

        run_window_command(action_cmd['action'], args)

        if is_interactive(view) and get_action(view).repeatable:
            set_repeat_data(view, ('vi', str(get_sequence(view)), get_mode(view), None))

        reset_command_data(view)

        return  # Nothing more to do.

    if motion:

        # Evaluate motion: Run it.

        motion_cmd = motion.translate(view)

        _log.debug('motion: %s', motion_cmd)

        add_macro_step(view, motion_cmd['motion'], motion_cmd['motion_args'])

        run_motion(view, motion_cmd)

    if action:
        action_cmd = action.translate(view)

        _log.debug('action: %s', action_cmd)

        if get_mode(view) == NORMAL:
            set_mode(view, INTERNAL_NORMAL)

            if 'mode' in action_cmd['action_args']:
                action_cmd['action_args']['mode'] = INTERNAL_NORMAL

        elif is_visual_mode(get_mode(view)):
            # Special-case exclusion: saving the previous selection would
            # overwrite the previous selection needed e.g. gv in a VISUAL
            # mode needs to expand or contract to previous selection.
            if action_cmd['action'] != 'nv_vi_gv':
                save_previous_selection(view, get_mode(view))

        # Some commands, like 'i' or 'a', open a series of edits that need
        # to be grouped together unless we are gluing a larger sequence
        # through nv_process_notation. For example, aFOOBAR<Esc> should be
        # grouped atomically, but not inside a sequence like
        # iXXX<Esc>llaYYY<Esc>, where we want to group the whole sequence
        # instead.
        if get_glue_until_normal_mode(view) and not is_processing_notation(view):
            run_window_command('mark_undo_groups_for_gluing')

        sequence = get_sequence(view)
        visual_repeat_data = get_visual_repeat_data(view, get_mode(view))
        action = get_action(view)

        add_macro_step(view, action_cmd['action'], action_cmd['action_args'])

        run_action(active_window(), action_cmd)

        if not (is_processing_notation(view) and get_glue_until_normal_mode(view)) and action.repeatable:
            set_repeat_data(view, ('vi', sequence, get_mode(view), visual_repeat_data))

    if get_mode(view) == INTERNAL_NORMAL:
        set_mode(view, NORMAL)

    reset_command_data(view)


def _should_reset_mode(view, current_mode: str) -> bool:
    return current_mode == UNKNOWN or get_setting(view, 'reset_mode_when_switching_tabs')


def init_state(view) -> None:
    # If the view not a regular vim capable view (e.g. console, widget, panel),
    # skip the state initialisation and perform a clean routine on the view.
    # TODO is a clean routine really necessary on non-vim capable views?
    if not is_view(view):
        clean_view(view)
        return

    if not get_reset_during_init(view):
        # Probably exiting from an input panel, like when using '/'. Don't reset
        # the global state, as it may contain data needed to complete the
        # command that's being built.
        set_reset_during_init(view, True)
        return

    mode = get_mode(view)

    if not _should_reset_mode(view, mode):
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
        view.window().run_command('nv_enter_normal_mode', {'from_init': True})
    elif mode != VISUAL and view.has_non_empty_selection_region():
        # Try to fixup a malformed visual state. For example, apparently this
        # can happen when a search is performed via a search panel and "Find
        # All" is pressed. In that case, multiple selections may need fixing.
        view.window().run_command('nv_enter_visual_mode', {'mode': mode})
    else:
        # This may be run when we're coming from cmdline mode.
        mode = VISUAL if view.has_non_empty_selection_region() else mode
        view.window().run_command('nv_enter_normal_mode', {'mode': mode, 'from_init': True})

    reset_command_data(view)
