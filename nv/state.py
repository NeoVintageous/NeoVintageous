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
from NeoVintageous.nv.settings import get_setting
from NeoVintageous.nv.settings import get_reset_during_init
from NeoVintageous.nv.settings import set_reset_during_init
from NeoVintageous.nv.utils import col_at
from NeoVintageous.nv.utils import is_ignored_but_command_mode
from NeoVintageous.nv.utils import is_view
from NeoVintageous.nv.utils import row_at
from NeoVintageous.nv.utils import save_previous_selection
from NeoVintageous.nv.vi import cmd_defs
from NeoVintageous.nv.vi.cmd_base import ViCommandDefBase
from NeoVintageous.nv.vi.cmd_base import ViMotionDef
from NeoVintageous.nv.vi.cmd_base import ViOperatorDef
from NeoVintageous.nv.vi.cmd_defs import ViToggleMacroRecorder
from NeoVintageous.nv.vi.settings import set_repeat_data
from NeoVintageous.nv.vi.settings import SettingsManager
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
from NeoVintageous.nv.vim import is_visual_mode
from NeoVintageous.nv.vim import mode_to_name
from NeoVintageous.nv.vim import run_action
from NeoVintageous.nv.vim import run_motion
from NeoVintageous.nv.vim import run_window_command


_log = logging.getLogger(__name__)


class State(object):

    def __init__(self, view):
        self.view = view
        self.settings = SettingsManager(self.view)

    @property
    def glue_until_normal_mode(self):
        """
        Indicate that editing commands should be grouped together.

        They should be grouped together in a single undo step after the user
        requested `_enter_normal_mode` next.

        This property is *VOLATILE*; it shouldn't be persisted between
        sessions.
        """
        return self.settings.vi['_vintageous_glue_until_normal_mode'] or False

    @glue_until_normal_mode.setter
    def glue_until_normal_mode(self, value):
        self.settings.vi['_vintageous_glue_until_normal_mode'] = value

    @property
    def processing_notation(self):
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
    def processing_notation(self, value):
        self.settings.vi['_vintageous_processing_notation'] = value

    # FIXME: This property seems to do the same as processing_notation.
    @property
    def non_interactive(self):
        # Indicate whether _nv_process_notation is running.
        #
        # Indicates whether _nv_process_notation is running a command and no
        # interactive prompts should be used (for example, by the '/' motion.)
        #
        # This property is *VOLATILE*; it shouldn't be persisted between
        # sessions.
        return self.settings.vi['_vintageous_non_interactive'] or False

    @non_interactive.setter
    def non_interactive(self, value):
        assert isinstance(value, bool), 'bool expected'
        self.settings.vi['_vintageous_non_interactive'] = value

    @property
    def must_capture_register_name(self):
        # type: () -> bool
        # Returns:
        #   True if State is expecting a register name next, False otherwise.
        return self.settings.vi['must_capture_register_name'] or False

    @must_capture_register_name.setter
    def must_capture_register_name(self, value):
        # type: (bool) -> None
        self.settings.vi['must_capture_register_name'] = value

    # This property isn't reset automatically. _enter_normal_mode mode must
    # take care of that so it can repeat the commands issued while in
    # insert mode.
    @property
    def normal_insert_count(self):
        """
        Count issued to 'i' or 'a', etc.

        These commands enter insert mode. If passed a count, they must repeat
        the commands run while in insert mode.
        """
        return self.settings.vi['normal_insert_count'] or '1'

    @normal_insert_count.setter
    def normal_insert_count(self, value):
        self.settings.vi['normal_insert_count'] = value

    @property
    def sequence(self):
        # type: () -> str
        # Sequence of keys provided by the user.
        return self.settings.vi['sequence'] or ''

    @sequence.setter
    def sequence(self, value):
        # type: (str) -> None
        _log.debug('sequence >>>%s<<<', value)
        self.settings.vi['sequence'] = value

    @property
    def partial_sequence(self):
        # type: () -> str
        # Sometimes we need to store a partial sequence to obtain the commands'
        # full name. Such is the case of `gD`, for example.
        return self.settings.vi['partial_sequence'] or ''

    @partial_sequence.setter
    def partial_sequence(self, value):
        # type: (str) -> None
        _log.debug('partial sequence >>>%s<<<', value)
        self.settings.vi['partial_sequence'] = value

    @property
    def mode(self):
        # type: () -> str
        # State of current mode.
        #
        # It isn't guaranteed that the underlying view's .sel() will be in a
        # consistent state (for example, that it will at least have one non-
        # empty region in visual mode.
        return self.settings.vi['mode'] or UNKNOWN

    @mode.setter
    def mode(self, value):
        # type: (str) -> None
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
    def action(self, value):
        serialized = value.serialize() if value else None
        self.settings.vi['action'] = serialized

    @property
    def motion(self):
        motion = self.settings.vi['motion'] or None

        if motion:
            cls = getattr(cmd_defs, motion['name'])

            return cls.from_json(motion['data'])

    @motion.setter
    def motion(self, value):
        serialized = value.serialize() if value else None
        self.settings.vi['motion'] = serialized

    @property
    def motion_count(self):
        return self.settings.vi['motion_count'] or ''

    @motion_count.setter
    def motion_count(self, value):
        assert value == '' or value.isdigit(), 'bad call'
        self.settings.vi['motion_count'] = value

    @property
    def action_count(self):
        return self.settings.vi['action_count'] or ''

    @action_count.setter
    def action_count(self, value):
        assert value == '' or value.isdigit(), 'bad call'
        self.settings.vi['action_count'] = value

    @property
    def count(self):
        # type: () -> int
        # Calculate the count for the current command.
        #
        # Returns:
        #   int: Default is 0.
        c = 1

        if self.action_count:
            c = int(self.action_count) or 1

        if self.motion_count:
            c *= (int(self.motion_count) or 1)

        if c < 1:
            raise ValueError('count must be positive')

        return c

    @property
    def count_default_zero(self):
        # type: () -> int
        # Calculate the count for the current command.
        #
        # Returns:
        #   int: Default is 0.
        #
        # TODO [refactor] This method was required because count() defaults to
        #   0. Both methods should be merged allowing to pass a default as a
        #   parameter.
        c = 0

        if self.action_count:
            c = int(self.action_count) or 0

        if self.motion_count:
            c *= (int(self.motion_count) or 0)

        if c < 0:
            raise ValueError('count must be zero or positive')

        return c

    @property
    def xpos(self):
        # type: () -> int
        # Accessor for the current xpos for carets.
        # Returns:
        #   int: Default is 0.
        return self.settings.vi['xpos'] or 0

    @xpos.setter
    def xpos(self, value):
        # type: (int) -> None
        assert isinstance(value, int), '`value` must be an int'
        self.settings.vi['xpos'] = value

    @property
    def register(self):
        # type: () -> str
        # Accessor for the current open register (as requested by the user).
        # Returns:
        #   str: Default is '"'.
        return self.settings.vi['register'] or '"'

    @register.setter
    def register(self, value):
        assert len(str(value)) == 1, '`value` must be a character'
        self.settings.vi['register'] = value
        self.must_capture_register_name = False

    @property
    def must_collect_input(self):
        # type: () -> bool
        # Returns:
        #   True if the current status should collect input, False otherwise.
        motion = self.motion
        action = self.action

        if motion and action:
            if motion.accept_input:
                return True

            return (action.accept_input and action.input_parser and action.input_parser.is_type_after_motion())

        # Special case: `q` should stop the macro recorder if it's running and
        # not request further input from the user.
        if (isinstance(action, ViToggleMacroRecorder) and macros.is_recording(self.view.window())):
            return False

        if (action and action.accept_input and action.input_parser and action.input_parser.is_type_immediate()):
            return True

        if motion:
            return (motion and motion.accept_input)

        return False

    @property
    def must_update_xpos(self):
        # type: () -> bool
        # Returns:
        #   True if motion/action should update xpos, False otherwise.
        motion = self.motion
        if motion and motion.updates_xpos:
            return True

        action = self.action
        if action and action.updates_xpos:
            return True

        return False

    def enter_normal_mode(self):
        self.mode = NORMAL

    def enter_visual_mode(self):
        self.mode = VISUAL

    def enter_visual_line_mode(self):
        self.mode = VISUAL_LINE

    def enter_insert_mode(self):
        self.mode = INSERT

    def enter_replace_mode(self):
        self.mode = REPLACE

    def enter_select_mode(self):
        self.mode = SELECT

    def enter_visual_block_mode(self):
        self.mode = VISUAL_BLOCK

    def reset_sequence(self):
        # TODO When is_recording, we could store the .sequence
        # and replay that, but we can't easily translate key presses in insert
        # mode to a NeoVintageous-friendly notation. A hybrid approach may work:
        # use a plain string for any command-mode-based mode, and native ST
        # commands for insert mode. That should make editing macros easier.
        self.sequence = ''

    def reset_partial_sequence(self):
        # type: () -> None
        self.partial_sequence = ''

    def reset_register_data(self):
        # type: () -> None
        self.register = '"'
        self.must_capture_register_name = False

    def reset_status(self):
        # type: () -> None
        self.view.erase_status('vim-seq')
        if self.mode == NORMAL:
            self.view.erase_status('vim-mode')

    def display_status(self):
        # type: () -> None
        mode_name = mode_to_name(self.mode)
        if mode_name:
            self.view.set_status('vim-mode', '-- {} --'.format(mode_name) if mode_name else '')

        self.view.set_status('vim-seq', self.sequence)

    def must_scroll_into_view(self):
        # type: () -> bool
        # Returns:
        #   True if motion/action should scroll into view, False otherwise.
        motion = self.motion
        if motion and motion.scroll_into_view:
            return True

        action = self.action
        if action and action.scroll_into_view:
            return True

        return False

    def scroll_into_view(self):
        # type: () -> None
        view = active_window().active_view()
        if view:
            # Show the *last* cursor on screen. There is currently no way to
            # identify the "active" cursor of a multiple cursor selection.
            sel = view.sel()[-1]

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

    def reset(self):
        # type: () -> None
        # TODO Remove this when we've ported all commands. This is here for retrocompatibility.
        self.reset_command_data()

    def reset_command_data(self):
        # type: () -> None
        # Resets all temporary data needed to build a command or partial
        # command.
        self.update_xpos()
        if self.must_scroll_into_view():
            self.scroll_into_view()

        self.action and self.action.reset()
        self.action = None
        self.motion and self.motion.reset()
        self.motion = None
        self.action_count = ''
        self.motion_count = ''

        self.reset_sequence()
        self.reset_partial_sequence()
        self.reset_register_data()
        self.reset_status()

    def reset_volatile_data(self):
        # type: () -> None
        # Reset window or application wide data to their default values.
        # Use when starting a new session.
        self.glue_until_normal_mode = False
        self.view.run_command('unmark_undo_groups_for_gluing')
        self.processing_notation = False
        self.non_interactive = False
        set_reset_during_init(self.view.window(), True)

    def update_xpos(self, force=False):
        if force or self.must_update_xpos:
            try:
                # TODO: we should check the current mode instead. ============
                sel = self.view.sel()[0]
                pos = sel.b
                if not sel.empty():
                    if sel.a < sel.b:
                        pos -= 1

                counter = Counter(self.view.substr(Region(self.view.line(pos).a, pos)))
                tab_size = self.view.settings().get('tab_size')
                self.xpos = (self.view.rowcol(pos)[1] + ((counter['\t'] * tab_size) - counter['\t']))
            except Exception:
                # TODO [review] Exception handling
                _log.debug('error updating xpos; default to 0')
                self.xpos = 0

    def process_input(self, key):
        # type: (str) -> bool
        _log.info('process input key %s', key)

        motion = self.motion
        if motion and motion.accept_input:
            motion_accepted = motion.accept(key)

            # Motion, with processed key, needs to reserialised and stored.
            self.motion = motion

            return motion_accepted

        # We can just default to whatever the action' accept methods returns,
        # because it will return False by default.

        action = self.action
        action_accepted = action.accept(key)

        # Action, with processed key, needs to reserialised and stored.
        self.action = action

        return action_accepted

    def set_command(self, command):
        # type: (ViCommandDefBase) -> None
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
            if command.accept_input and command.input_parser and command.input_parser.is_type_via_panel():
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

    def runnable(self):
        # type: () -> bool
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

    def eval(self):
        # type: () -> None
        if not self.runnable():
            return

        if self.action and self.motion:
            action_cmd = self.action.translate(self)
            _log.debug('action_cmd = %s', action_cmd)
            motion_cmd = self.motion.translate(self)
            _log.debug('motion_cmd = %s', motion_cmd)

            _log.debug('changing to INTERNAL_NORMAL...')
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
                # Tell Sublime Text that it should group all the next edits
                # until we enter normal mode again.
                run_window_command('mark_undo_groups_for_gluing')

            macros.add_step(self, action_cmd['action'], args)
            run_window_command(action_cmd['action'], args)

            if not self.non_interactive:
                if self.action.repeatable:
                    _log.debug('action is repeatable, setting repeat data...')
                    set_repeat_data(self.view, ('vi', str(self.sequence), self.mode, None))

            self.reset_command_data()

            return

        if self.motion:
            motion_cmd = self.motion.translate(self)

            macros.add_step(self, motion_cmd['motion'], motion_cmd['motion_args'])

            # All motions are subclasses of ViTextCommandBase, so it's safe to
            # run the command via the current view.
            run_motion(self.view, motion_cmd)

        if self.action:
            action_cmd = self.action.translate(self)

            if self.mode == NORMAL:
                _log.debug('is NORMAL, changing to INTERNAL_NORMAL...')
                self.mode = INTERNAL_NORMAL

                if 'mode' in action_cmd['action_args']:
                    _log.debug('action has a mode, changing to INTERNAL_NORMAL...')
                    action_cmd['action_args']['mode'] = INTERNAL_NORMAL

            elif is_visual_mode(self.mode):
                # Special-case exclusion: saving the previous selection would
                # overwrite the previous selection needed e.g. gv in a VISUAL
                # mode needs to expand or contract to previous selection.
                if action_cmd['action'] != '_vi_gv':
                    _log.debug('is VISUAL, saving selection...')
                    save_previous_selection(self.view, self.mode)

            # Some commands, like 'i' or 'a', open a series of edits that need
            # to be grouped together unless we are gluing a larger sequence
            # through _nv_process_notation. For example, aFOOBAR<Esc> should be
            # grouped atomically, but not inside a sequence like
            # iXXX<Esc>llaYYY<Esc>, where we want to group the whole sequence
            # instead.
            if self.glue_until_normal_mode and not self.processing_notation:
                # Tell Sublime Text that it should group all the next edits
                # until we enter normal mode again.
                run_window_command('mark_undo_groups_for_gluing')

            seq = self.sequence
            visual_repeat_data = self.get_visual_repeat_data()
            action = self.action

            macros.add_step(self, action_cmd['action'], action_cmd['action_args'])
            run_action(active_window(), action_cmd)

            if not (self.processing_notation and self.glue_until_normal_mode):
                if action.repeatable:
                    _log.debug('action is repeatable, setting repeat data...')
                    set_repeat_data(self.view, ('vi', seq, self.mode, visual_repeat_data))

        if self.mode == INTERNAL_NORMAL:
            _log.debug('is INTERNAL_NORMAL, changing to NORMAL...')
            self.enter_normal_mode()

        self.reset_command_data()


def init_state(view):
    # type: (...) -> None
    # Initialise view state.
    #
    # Runs at startup and every time a view gets activated, loaded, etc.
    #
    # Args:
    #   :view (sublime.View):
    if not is_view(view):
        # Abort if we got a console, widget, panel...
        try:
            # XXX: All this seems to be necessary here.
            if not is_ignored_but_command_mode(view):
                view.settings().set('command_mode', False)
                view.settings().set('inverse_caret_state', False)

            view.settings().erase('vintage')
        except Exception:
            # TODO [review] Exception handling
            _log.debug('error initialising irregular view i.e. console, widget, panel, etc.')
        finally:
            return

    state = State(view)

    if not get_reset_during_init(view.window()):
        # Probably exiting from an input panel, like when using '/'. Don't
        # reset the global state, as it may contain data needed to complete
        # the command that's being built.
        set_reset_during_init(view.window(), True)
        return

    mode = state.mode

    # Non-standard user setting.
    reset = state.settings.view['vintageous_reset_mode_when_switching_tabs']
    # XXX: If the view was already in normal mode, we still need to run the
    # init code. I believe this is due to Sublime Text (intentionally) not
    # serializing the inverted caret state and the command_mode setting when
    # first loading a file.
    # If the mode is unknown, it might be a new file. Let normal mode setup
    # continue.
    if not reset and (mode not in (NORMAL, UNKNOWN)):
        return

    # If we have no selections, add one.
    if len(view.sel()) == 0:
        view.sel().add(0)

    default_mode = get_setting(view, 'default_mode')
    if default_mode == 'insert':
        if mode in (NORMAL, UNKNOWN):
            enter_insert_mode(view, mode)
    elif mode in (VISUAL, VISUAL_LINE):
        # This was commented out to fix the issue of visual selections being
        # lost because some keys, like the super key, cause Sublime to lose
        # focus, and when focus comes back it triggers the on_activated() event,
        # which then initializes state, which then causes visual mode to enter
        # normal mode. Note that there may be regressions as a side effect.
        # See nv/events.py#NeoVintageousEvents::on_activated().
        # See https://github.com/NeoVintageous/NeoVintageous/issues/547
        # view.window().run_command('_enter_normal_mode', {'from_init': True})
        _log.debug('initializing %s state', mode)
    elif mode in (INSERT, REPLACE):
        # TODO: Don't we need to pass a mode here?
        view.window().run_command('_enter_normal_mode', {'from_init': True})

    elif view.has_non_empty_selection_region() and mode != VISUAL:
        # Runs, for example, when we've performed a search via ST3 search panel
        # and we've pressed 'Find All'. In this case, we want to ensure a
        # consistent state for multiple selections.
        # TODO We could end up with multiple selections in other ways that bypass init_state.
        state.mode = VISUAL
    else:
        # This may be run when we're coming from cmdline mode.
        mode = VISUAL if view.has_non_empty_selection_region() else mode
        state.enter_normal_mode()
        view.window().run_command('_enter_normal_mode', {'mode': mode, 'from_init': True})

    state.reset_command_data()
