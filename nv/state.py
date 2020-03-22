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

from collections import Counter
import logging

from sublime import active_window
from sublime import Region

from NeoVintageous.nv import macros
from NeoVintageous.nv import plugin
from NeoVintageous.nv.settings import get_mode
from NeoVintageous.nv.settings import get_reset_during_init
from NeoVintageous.nv.settings import get_setting
from NeoVintageous.nv.settings import set_repeat_data
from NeoVintageous.nv.settings import set_reset_during_init
from NeoVintageous.nv.settings import set_xpos
from NeoVintageous.nv.utils import col_at
from NeoVintageous.nv.utils import is_view
from NeoVintageous.nv.utils import row_at
from NeoVintageous.nv.utils import save_previous_selection
from NeoVintageous.nv.vi import cmd_defs
from NeoVintageous.nv.vi.cmd_base import ViCommandDefBase
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
from NeoVintageous.nv.vim import reset_status
from NeoVintageous.nv.vim import run_action
from NeoVintageous.nv.vim import run_motion
from NeoVintageous.nv.vim import run_window_command


_log = logging.getLogger(__name__)


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
    def processing_notation(self) -> bool:
        # Indicate whether _nv_process_notation is running.
        #
        # Indicates whether _nv_process_notation is running a command and is
        # grouping all edits in one single undo step. That is, we are running a
        # non- interactive sequence of commands.
        #
        # This property is *VOLATILE*; it shouldn't be persisted between
        # sessions.
        return self.settings.vi['_vintageous_processing_notation'] or False

    @processing_notation.setter
    def processing_notation(self, value: bool) -> None:
        self.settings.vi['_vintageous_processing_notation'] = value

    # FIXME: This property seems to do the same as processing_notation.
    @property
    def non_interactive(self) -> bool:
        # Indicate whether _nv_process_notation is running.
        #
        # Indicates whether _nv_process_notation is running a command and no
        # interactive prompts should be used (for example, by the '/' motion.)
        #
        # This property is *VOLATILE*; it shouldn't be persisted between
        # sessions.
        return self.settings.vi['_vintageous_non_interactive'] or False

    @non_interactive.setter
    def non_interactive(self, value: bool) -> None:
        assert isinstance(value, bool), 'bool expected'
        self.settings.vi['_vintageous_non_interactive'] = value

    @property
    def must_capture_register_name(self) -> bool:
        # Returns:
        #   True if State is expecting a register name next, False otherwise.
        return self.settings.vi['must_capture_register_name'] or False

    @must_capture_register_name.setter
    def must_capture_register_name(self, value: bool) -> None:
        self.settings.vi['must_capture_register_name'] = value

    # This property isn't reset automatically. _enter_normal_mode mode must
    # take care of that so it can repeat the commands issued while in
    # insert mode.
    @property
    def normal_insert_count(self) -> str:
        """
        Count issued to 'i' or 'a', etc.

        These commands enter insert mode. If passed a count, they must repeat
        the commands run while in insert mode.
        """
        return self.settings.vi['normal_insert_count'] or '1'

    @normal_insert_count.setter
    def normal_insert_count(self, value: str) -> None:
        self.settings.vi['normal_insert_count'] = value

    @property
    def sequence(self) -> str:
        # Sequence of keys provided by the user.
        return self.settings.vi['sequence'] or ''

    @sequence.setter
    def sequence(self, value: str) -> None:
        _log.debug('set sequence >>>%s<<<', value)
        self.settings.vi['sequence'] = value

    @property
    def partial_sequence(self) -> str:
        # Sometimes we need to store a partial sequence to obtain the commands'
        # full name. Such is the case of `gD`, for example.
        return self.settings.vi['partial_sequence'] or ''

    @partial_sequence.setter
    def partial_sequence(self, value: str) -> None:
        _log.debug('set partial sequence >>>%s<<<', value)
        self.settings.vi['partial_sequence'] = value

    @property
    def mode(self) -> str:
        # State of current mode.
        #
        # It isn't guaranteed that the underlying view's .sel() will be in a
        # consistent state (for example, that it will at least have one non-
        # empty region in visual mode.
        return self.settings.vi['mode'] or UNKNOWN

    @mode.setter
    def mode(self, value: str) -> None:
        self.settings.vi['mode'] = value

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
    def motion_count(self) -> str:
        return self.settings.vi['motion_count'] or ''

    @motion_count.setter
    def motion_count(self, value: str) -> None:
        assert value == '' or value.isdigit(), 'bad call'
        self.settings.vi['motion_count'] = value

    @property
    def action_count(self) -> str:
        return self.settings.vi['action_count'] or ''

    @action_count.setter
    def action_count(self, value: str) -> None:
        assert value == '' or value.isdigit(), 'bad call'
        self.settings.vi['action_count'] = value

    def _get_count(self, default: int) -> int:
        c = default

        if self.action_count:
            c = int(self.action_count) or 1

        if self.motion_count:
            c *= int(self.motion_count) or 1

        if c < 0:
            raise ValueError('count must be greater than zero')

        return c

    @property
    def count(self) -> int:
        return self._get_count(default=1)

    @property
    def count_default_zero(self) -> int:
        # TODO Refactor: method was required because count() defaults to 1
        return self._get_count(default=0)

    @property
    def register(self) -> str:
        # Accessor for the current open register (as requested by the user).
        # Returns:
        #   str: Default is '"'.
        return self.settings.vi['register'] or '"'

    @register.setter
    def register(self, value: str) -> None:
        assert len(str(value)) == 1, '`value` must be a character'
        self.settings.vi['register'] = value
        self.must_capture_register_name = False

    @property
    def must_collect_input(self) -> bool:
        # Returns:
        #   True if the current status should collect input, False otherwise.
        motion = self.motion
        action = self.action

        if motion and action:
            if motion.accept_input:
                return True

            return (action.accept_input and action.input_parser and action.input_parser.is_after_motion())

        # Special case: `q` should stop the macro recorder if it's running and
        # not request further input from the user.
        if (isinstance(action, ViToggleMacroRecorder) and macros.is_recording(self.view.window())):
            return False

        if (action and action.accept_input and action.input_parser and action.input_parser.is_immediate()):
            return True

        if motion:
            return (motion and motion.accept_input)

        return False

    @property
    def must_update_xpos(self) -> bool:
        # Returns:
        #   True if motion/action should update xpos, False otherwise.
        motion = self.motion
        if motion and motion.updates_xpos:
            return True

        action = self.action
        if action and action.updates_xpos:
            return True

        return False

    def reset_register_data(self) -> None:
        self.register = '"'
        self.must_capture_register_name = False

    def display_status(self) -> None:
        mode_name = mode_to_name(self.mode)
        if mode_name:
            self.view.set_status('vim-mode', '-- {} --'.format(mode_name) if mode_name else '')

        self.view.set_status('vim-seq', self.sequence)

    def must_scroll_into_view(self) -> bool:
        # Returns:
        #   True if motion/action should scroll into view, False otherwise.
        motion = self.motion
        if motion and motion.scroll_into_view:
            return True

        action = self.action
        if action and action.scroll_into_view:
            return True

        return False

    def scroll_into_view(self) -> None:
        view = active_window().active_view()
        if view:
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
            if is_visual_mode(self.mode):
                if sel.b > sel.a:
                    if view.substr(sel.b - 1) == '\n':
                        target_pt = max(0, target_pt - 1)
                        # Use the start point of the target line to avoid
                        # horizontal scrolling. For example, this can happen in
                        # VISUAL LINE mode when the EOL is off-screen.
                        target_pt = max(0, view.line(target_pt).a)

            view.show(target_pt, False)

    def reset_command_data(self) -> None:
        # Resets all temp data needed to build a command or partial command.
        self.update_xpos()
        if self.must_scroll_into_view():
            self.scroll_into_view()

        self.action and self.action.reset()
        self.action = None
        self.motion and self.motion.reset()
        self.motion = None
        self.action_count = ''
        self.motion_count = ''

        self.sequence = ''
        self.partial_sequence = ''
        self.reset_register_data()
        reset_status(self.view, self.mode)

    def reset_volatile_data(self) -> None:
        # Reset window or application wide data to their default values.
        # Use when starting a new session.
        self.glue_until_normal_mode = False
        self.view.run_command('unmark_undo_groups_for_gluing')
        self.processing_notation = False
        self.non_interactive = False
        set_reset_during_init(self.view, True)

    def update_xpos(self, force: bool = False) -> None:
        if force or self.must_update_xpos:
            try:
                # TODO: we should check the current mode instead. ============
                sel = self.view.sel()[0]
                pos = sel.b
                if not sel.empty():
                    if sel.a < sel.b:
                        pos -= 1

                counter = Counter(self.view.substr(Region(self.view.line(pos).a, pos)))  # type: dict
                tab_size = self.view.settings().get('tab_size')
                set_xpos(self.view, (self.view.rowcol(pos)[1] + ((counter['\t'] * tab_size) - counter['\t'])))
            except Exception:
                # TODO [review] Exception handling
                _log.debug('error updating xpos; default to 0')
                set_xpos(self.view, 0)

    def set_command(self, command: ViCommandDefBase) -> None:
        # Set the current command.
        #
        # Args:
        #   command (ViCommandDefBase): A command definition.
        #
        # Raises:
        #   ValueError: If too many motions.
        #   ValueError: If too many actions.
        #   ValueError: Unexpected command type.
        assert isinstance(command, ViCommandDefBase), 'ViCommandDefBase expected, got {}'.format(type(command))

        is_runnable = self.runnable()

        if isinstance(command, ViMotionDef):
            if is_runnable:
                raise ValueError('too many motions')

            self.motion = command

            if self.mode == OPERATOR_PENDING:
                self.mode = NORMAL

        elif isinstance(command, ViOperatorDef):
            if is_runnable:
                raise ValueError('too many actions')

            self.action = command

            if command.motion_required and not is_visual_mode(self.mode):
                self.mode = OPERATOR_PENDING

        else:
            raise ValueError('unexpected command type')

        if not self.non_interactive:
            if command.accept_input and command.input_parser and command.input_parser.is_panel():
                command.input_parser.run_command()

    def get_visual_repeat_data(self):
        # Return the data needed to restore visual selections.
        #
        # Before repeating a visual mode command in normal mode.
        #
        # Returns:
        #   3-tuple (lines, chars, mode)
        if self.mode not in (VISUAL, VISUAL_LINE):
            return

        first = self.view.sel()[0]
        lines = (row_at(self.view, first.end()) -
                 row_at(self.view, first.begin()))

        if lines > 0:
            chars = col_at(self.view, first.end())
        else:
            chars = first.size()

        return (lines, chars, self.mode)

    def restore_visual_data(self, data):
        rows, chars, old_mode = data
        first = self.view.sel()[0]

        if old_mode == VISUAL:
            if rows > 0:
                end = self.view.text_point(row_at(self.view, first.b) + rows, chars)
            else:
                end = first.b + chars

            self.view.sel().add(Region(first.b, end))
            self.mode = VISUAL

        elif old_mode == VISUAL_LINE:
            rows, _, old_mode = data
            begin = self.view.line(first.b).a
            end = self.view.text_point(row_at(self.view, begin) +
                                       (rows - 1), 0)
            end = self.view.full_line(end).b
            self.view.sel().add(Region(begin, end))
            self.mode = VISUAL_LINE

    def runnable(self) -> bool:
        # Returns:
        #   True if motion and/or action is in a runnable state, False otherwise.
        # Raises:
        #   ValueError: Invlid mode.
        if self.must_collect_input:
            return False

        action = self.action
        motion = self.motion
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

            if self.glue_until_normal_mode and not self.processing_notation:
                run_window_command('mark_undo_groups_for_gluing')

            macros.add_step(self, action_cmd['action'], args)

            run_window_command(action_cmd['action'], args)

            if not self.non_interactive and self.action.repeatable:
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
            if self.glue_until_normal_mode and not self.processing_notation:
                run_window_command('mark_undo_groups_for_gluing')

            sequence = self.sequence
            visual_repeat_data = self.get_visual_repeat_data()
            action = self.action

            macros.add_step(self, action_cmd['action'], action_cmd['action_args'])

            run_action(active_window(), action_cmd)

            if not (self.processing_notation and self.glue_until_normal_mode) and action.repeatable:
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
