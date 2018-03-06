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

import os
from collections import Counter

from sublime import active_window
from sublime import Region

from NeoVintageous.nv import plugin
from NeoVintageous.nv import rcfile
from NeoVintageous.nv.vi import cmd_defs
from NeoVintageous.nv.vi import settings
from NeoVintageous.nv.vi import utils
from NeoVintageous.nv.vi.cmd_base import ViCommandDefBase
from NeoVintageous.nv.vi.cmd_base import ViMotionDef
from NeoVintageous.nv.vi.cmd_base import ViOperatorDef
from NeoVintageous.nv.vi.macros import MacroRegisters
from NeoVintageous.nv.vi.marks import Marks
from NeoVintageous.nv.vi.registers import Registers
from NeoVintageous.nv.vi.settings import SettingsManager
from NeoVintageous.nv.vi.utils import first_sel
from NeoVintageous.nv.vi.utils import is_ignored_but_command_mode
from NeoVintageous.nv.vi.utils import is_view
from NeoVintageous.nv.vi.variables import Variables
from NeoVintageous.nv.vim import console_message
from NeoVintageous.nv.vim import DIRECTION_DOWN
from NeoVintageous.nv.vim import get_logger
from NeoVintageous.nv.vim import INPUT_AFTER_MOTION
from NeoVintageous.nv.vim import INPUT_INMEDIATE
from NeoVintageous.nv.vim import INPUT_VIA_PANEL
from NeoVintageous.nv.vim import INSERT
from NeoVintageous.nv.vim import INTERNAL_NORMAL
from NeoVintageous.nv.vim import mode_to_friendly_name
from NeoVintageous.nv.vim import NORMAL
from NeoVintageous.nv.vim import OPERATOR_PENDING
from NeoVintageous.nv.vim import REPLACE
from NeoVintageous.nv.vim import SELECT
from NeoVintageous.nv.vim import UNKNOWN
from NeoVintageous.nv.vim import VISUAL
from NeoVintageous.nv.vim import VISUAL_BLOCK
from NeoVintageous.nv.vim import VISUAL_LINE


_log = get_logger(__name__)


class State(object):
    """
    Manage global Vim state. Accumulates command data, etc.

    Usage:
      Always instantiate passing it the view that commands are going to
      target.

      Example:

          state = State(view)

    Note: `State` internally uses view.settings() and window.settings() to persist data.
    """

    registers = Registers()
    macro_registers = MacroRegisters()
    marks = Marks()
    variables = Variables()
    macro_steps = []

    def __init__(self, view):
        self.view = view
        # We use several types of settings:
        #   - vi-specific (settings.vi),
        #   - regular ST view settings (settings.view) and
        #   - window settings (settings.window).
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
        """
        Indicate whether `ProcessNotation` is running.

        Indicates whether `ProcessNotation` is running a command and is grouping
        all edits in one single undo step. That is, we are running a non-
        interactive sequence of commands.

        This property is *VOLATILE*; it shouldn't be persisted between
        sessions.
        """
        # TODO Rename self.settings.vi to self.settings.local
        return self.settings.vi['_vintageous_processing_notation'] or False

    @processing_notation.setter
    def processing_notation(self, value):
        self.settings.vi['_vintageous_processing_notation'] = value

    # FIXME: This property seems to do the same as processing_notation.
    @property
    def non_interactive(self):
        """
        Indicate whether `ProcessNotation` is running.

        Indicates whether `ProcessNotation` is running a command and no
        interactive prompts should be used (for example, by the '/' motion.)

        This property is *VOLATILE*; it shouldn't be persisted between
        sessions.
        """
        return self.settings.vi['_vintageous_non_interactive'] or False

    @non_interactive.setter
    def non_interactive(self, value):
        assert isinstance(value, bool), 'bool expected'
        self.settings.vi['_vintageous_non_interactive'] = value

    @property
    def last_character_search(self):
        """Last character used as input for 'f' or 't'."""
        return self.settings.window['_vintageous_last_character_search'] or ''

    @last_character_search.setter
    def last_character_search(self, value):
        assert isinstance(value, str), 'bad call'
        assert len(value) == 1, 'bad call'
        self.settings.window['_vintageous_last_character_search'] = value

    @property
    def last_char_search_command(self):
        # type: () -> str
        # ',' and ';' change directions depending on which of 'f' or 't' was the previous command.
        #
        # Returns:
        #   str: The name of the last character search command, namely: 'vi_f',
        #       'vi_t', 'vi_big_f' or 'vi_big_t'.
        name = self.settings.window['_vintageous_last_char_search_command']

        return name or 'vi_f'

    @last_char_search_command.setter
    def last_char_search_command(self, value):
        # type: (str) -> None
        self.settings.window['_vintageous_last_char_search_command'] = value

    @property
    def last_buffer_search_command(self):
        # type: () -> str
        # 'n' and 'N' change directions depending on which of '/' or '?' was the previous command.
        # Returns:
        #   str: The name of the last character search command, namely:
        #       'vi_slash', 'vi_question_mark', 'vi_star', 'vi_octothorp'.
        name = self.settings.window['_vintageous_last_buffer_search_command']

        return name or 'vi_slash'

    @last_buffer_search_command.setter
    def last_buffer_search_command(self, value):
        # type: (str) -> None
        self.settings.window['_vintageous_last_buffer_search_command'] = value

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

    @property
    def last_buffer_search(self):
        # type: () -> str
        # Returns:
        #   The last string used by buffer search commands '/' or '?'.
        return self.settings.window['_vintageous_last_buffer_search'] or ''

    @last_buffer_search.setter
    def last_buffer_search(self, value):
        # type: (str) -> None
        self.settings.window['_vintageous_last_buffer_search'] = value

    @property
    def reset_during_init(self):
        # Some commands gather user input through input panels. An input panel
        # is just a view, so when it's closed, the previous view gets activated
        # and Vintageous init code runs. In this case, however, we most likely
        # want the global state to remain unchanged. This variable helps to
        # signal this. For an example, see the '_vi_slash' command.
        value = self.settings.window['_vintageous_reset_during_init']
        if not isinstance(value, bool):
            return True

        return value

    @reset_during_init.setter
    def reset_during_init(self, value):
        assert isinstance(value, bool), 'expected a bool'
        self.settings.window['_vintageous_reset_during_init'] = value

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
        _log.debug('sequence %s', value)
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
        _log.debug('partial sequence %s', value)
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
    @settings.volatile
    def repeat_data(self):
        return self.settings.vi['repeat_data'] or None

    @repeat_data.setter
    def repeat_data(self, value):
        # Store data structure for repeat ('.') to use.
        #
        # Args:
        #   tuple (type, cmd_name_or_key_seq, mode): Type may be "vi" or
        #       "native" ("vi" commands are executed via ProcessNotation, while
        #       "native" commands are executed via sublime.run_command().
        assert isinstance(value, tuple) or isinstance(value, list), 'bad call'
        assert len(value) == 4, 'bad call'
        _log.debug('set repeat data: %s', value)
        self.settings.vi['repeat_data'] = value

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
    def visual_block_direction(self):
        # type: () -> int
        # Accessor for the visual block direction for current selection.
        # Returns:
        #   int: Representing direction, default is DOWN.
        return self.settings.vi['visual_block_direction'] or DIRECTION_DOWN

    @visual_block_direction.setter
    def visual_block_direction(self, value):
        # type: (int) -> None
        assert isinstance(value, int), '`value` must be an int'
        self.settings.vi['visual_block_direction'] = value

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
        _log.debug('register %s', value)
        self.settings.vi['register'] = value
        self.must_capture_register_name = False

    @property
    def must_collect_input(self):
        # type: () -> bool
        # Returns:
        #   True if the current status must collect input, False otherwise.
        motion = self.motion
        action = self.action

        if motion and action:
            if motion.accept_input:
                return True

            return (action.accept_input and action.input_parser.type == INPUT_AFTER_MOTION)

        # Special case: `q` should stop the macro recorder if it's running and
        # not request further input from the user.
        if (isinstance(action, cmd_defs.ViToggleMacroRecorder) and self.is_recording):
            return False

        if (action and action.accept_input and action.input_parser.type == INPUT_INMEDIATE):
            return True

        if motion:
            return (motion and motion.accept_input)

        return False

    @property
    def must_update_xpos(self):
        # Returns:
        #   bool|None: True if motion or action requires xpos update, None
        #       otherwise.
        # TODO State.must_update_xpos) should return False by default rather
        #   than None.
        motion = self.motion
        if motion and motion.updates_xpos:
            return True

        action = self.action
        if action and action.updates_xpos:
            return True

    @property
    def is_recording(self):
        # type: () -> bool
        return self.settings.vi['recording'] or False

    @is_recording.setter
    def is_recording(self, value):
        assert isinstance(value, bool), 'bad call'
        self.settings.vi['recording'] = value

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
        _log.debug('reset partial sequence')
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
        mode_name = mode_to_friendly_name(self.mode)
        if mode_name:
            mode_name = '-- {} --'.format(mode_name) if mode_name else ''
            self.view.set_status('vim-mode', mode_name)

        self.view.set_status('vim-seq', self.sequence)

    def must_scroll_into_view(self):
        # type: () -> bool
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
            # Make sure we show the first caret on the screen, but don't show
            # its surroundings.
            # TODO Maybe some commands should show their surroundings too?
            view.show(view.sel()[0], False)

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
        self.reset_during_init = True

    def update_xpos(self, force=False):
        if self.must_update_xpos or force:
            try:
                # TODO: we should check the current mode instead. ============
                sel = self.view.sel()[0]
                pos = sel.b
                if not sel.empty():
                    if sel.a < sel.b:
                        pos -= 1
                # ============================================================
                r = Region(self.view.line(pos).a, pos)
                counter = Counter(self.view.substr(r))
                tab_size = self.view.settings().get('tab_size')
                xpos = (self.view.rowcol(pos)[1] +
                        ((counter['\t'] * tab_size) - counter['\t']))
            except Exception as e:
                console_message(str(e))
                _log.exception('error setting xpos; default to 0')
                self.xpos = 0
                return
            else:
                self.xpos = xpos

    def _set_parsers(self, command):
        # type: (ViCommandDefBase) -> None
        if command.accept_input:
            if command.input_parser.type == INPUT_VIA_PANEL:
                if self.non_interactive:
                    return

                active_window().run_command(command.input_parser.command)

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
        assert isinstance(command, ViCommandDefBase), 'ViCommandDefBase expected, got {}'.format(type(command))  # FIXME # noqa: E501

        if isinstance(command, ViMotionDef):
            if self.runnable():
                # We already have a motion, so this looks like an error.
                raise ValueError('too many motions')
            self.motion = command

            if self.mode == OPERATOR_PENDING:
                self.mode = NORMAL

            self._set_parsers(command)

        elif isinstance(command, ViOperatorDef):
            if self.runnable():
                # We already have an action, so this looks like an error.
                raise ValueError('too many actions')
            self.action = command

            if (self.action.motion_required and not self.in_any_visual_mode()):
                self.mode = OPERATOR_PENDING

            self._set_parsers(command)

        else:
            raise ValueError('unexpected command type')

    def in_any_visual_mode(self):
        return (self.mode in (VISUAL, VISUAL_LINE, VISUAL_BLOCK))

    def can_run_action(self):
        action = self.action
        if (action and (not action['motion_required'] or self.in_any_visual_mode())):
            return True

    def get_visual_repeat_data(self):
        # Return the data needed to restore visual selections.
        #
        # Before repeating a visual mode command in normal mode.
        #
        # Returns:
        #   3-tuple (lines, chars, mode)
        if self.mode not in (VISUAL, VISUAL_LINE):
            return

        first = first_sel(self.view)
        lines = (utils.row_at(self.view, first.end()) -
                 utils.row_at(self.view, first.begin()))

        if lines > 0:
            chars = utils.col_at(self.view, first.end())
        else:
            chars = first.size()

        return (lines, chars, self.mode)

    def restore_visual_data(self, data):
        rows, chars, old_mode = data
        first = first_sel(self.view)

        if old_mode == VISUAL:
            if rows > 0:
                end = self.view.text_point(utils.row_at(self.view, first.b) + rows, chars)
            else:
                end = first.b + chars

            self.view.sel().add(Region(first.b, end))
            self.mode = VISUAL

        elif old_mode == VISUAL_LINE:
            rows, _, old_mode = data
            begin = self.view.line(first.b).a
            end = self.view.text_point(utils.row_at(self.view, begin) +
                                       (rows - 1), 0)
            end = self.view.full_line(end).b
            self.view.sel().add(Region(begin, end))
            self.mode = VISUAL_LINE

    def start_recording(self):
        self.is_recording = True
        State.macro_steps = []
        self.view.set_status('vim-recorder', 'Recording...')

    def stop_recording(self):
        self.is_recording = False
        self.view.erase_status('vim-recorder')

    def add_macro_step(self, cmd_name, args):
        if self.is_recording:
            if cmd_name == '_vi_q':
                # don't store the ending macro step
                return

            if self.runnable and not self.glue_until_normal_mode:
                State.macro_steps.append((cmd_name, args))

    def runnable(self):
        # type: () -> bool
        # Returns:
        #   bool: True if we can run the state data as it is, False otherwise.
        #
        # Raises:
        #   ValueError: Wrong mode.
        if self.must_collect_input:
            return False

        if self.action and self.motion:
            if self.mode != NORMAL:
                raise ValueError('wrong mode')

            return True

        if self.can_run_action():
            if self.mode == OPERATOR_PENDING:
                raise ValueError('wrong mode')

            return True

        if self.motion:
            if self.mode == OPERATOR_PENDING:
                raise ValueError('wrong mode')

            return True

        return False

    def eval(self):
        # type: () -> None
        # Run data as a command if possible.
        if not self.runnable():
            return

        if self.action and self.motion:
            action_cmd = self.action.translate(self)
            motion_cmd = self.motion.translate(self)
            _log.debug('full command, switching to internal normal mode...')
            self.mode = INTERNAL_NORMAL

            # TODO: Make a requirement that motions and actions take a
            # 'mode' param.
            if 'mode' in action_cmd['action_args']:
                action_cmd['action_args']['mode'] = INTERNAL_NORMAL

            if 'mode' in motion_cmd['motion_args']:
                motion_cmd['motion_args']['mode'] = INTERNAL_NORMAL

            args = action_cmd['action_args']
            args['count'] = 1
            # let the action run the motion within its edit object so that
            # we don't need to worry about grouping edits to the buffer.
            args['motion'] = motion_cmd
            _log.debug('motion cmd %s, action cmd %s', motion_cmd, action_cmd)

            if self.glue_until_normal_mode and not self.processing_notation:
                # We need to tell Sublime Text now that it should group
                # all the next edits until we enter normal mode again.
                active_window().run_command('mark_undo_groups_for_gluing')

            self.add_macro_step(action_cmd['action'], args)

            _log.info('run command (action + motion) %s %s', action_cmd['action'], args)
            active_window().run_command(action_cmd['action'], args)
            if not self.non_interactive:
                if self.action.repeatable:
                    self.repeat_data = ('vi', str(self.sequence), self.mode, None)

            self.reset_command_data()

            return

        if self.motion:
            motion_cmd = self.motion.translate(self)
            _log.debug('lone motion cmd %s', motion_cmd)

            self.add_macro_step(motion_cmd['motion'], motion_cmd['motion_args'])

            # We know that all motions are subclasses of ViTextCommandBase,
            # so it's safe to call them from the current view.
            _log.info('run command (motion) %s %s', motion_cmd['motion'], motion_cmd['motion_args'])
            self.view.run_command(motion_cmd['motion'], motion_cmd['motion_args'])

        if self.action:
            action_cmd = self.action.translate(self)
            _log.debug('lone action cmd %s', action_cmd)
            if self.mode == NORMAL:
                _log.debug('switch to internal normal mode')
                self.mode = INTERNAL_NORMAL

                if 'mode' in action_cmd['action_args']:
                    action_cmd['action_args']['mode'] = INTERNAL_NORMAL

            elif self.mode in (VISUAL, VISUAL_LINE, VISUAL_BLOCK):
                self.view.add_regions('visual_sel', list(self.view.sel()))

            # Some commands, like 'i' or 'a', open a series of edits that
            # need to be grouped together unless we are gluing a larger
            # sequence through ProcessNotation. For example, aFOOBAR<Esc> should
            # be grouped atomically, but not inside a sequence like
            # iXXX<Esc>llaYYY<Esc>, where we want to group the whole
            # sequence instead.
            if self.glue_until_normal_mode and not self.processing_notation:
                active_window().run_command('mark_undo_groups_for_gluing')

            seq = self.sequence
            visual_repeat_data = self.get_visual_repeat_data()
            action = self.action

            self.add_macro_step(action_cmd['action'], action_cmd['action_args'])

            _log.info('run command (action) %s %s', action_cmd['action'], action_cmd['action_args'])
            active_window().run_command(action_cmd['action'], action_cmd['action_args'])

            if not (self.processing_notation and self.glue_until_normal_mode):
                if action.repeatable:
                    self.repeat_data = ('vi', seq, self.mode, visual_repeat_data)

        if self.mode == INTERNAL_NORMAL:
            self.enter_normal_mode()

        self.reset_command_data()


def init_state(view, new_session=False):
    # type: (...) -> None
    # Initialise view state.
    #
    # Runs at startup and every time a view gets activated, loaded, etc.
    #
    # Args:
    #   :view (sublime.View):
    #   :new_session (bool): Whether we're starting up Sublime Text. If so,
    #       volatile data must be wiped, and vintageousrc file must be loaded.

    if not is_view(view):
        # Abort if we got a console, widget, panel...
        try:
            # XXX: All this seems to be necessary here.
            if not is_ignored_but_command_mode(view):
                view.settings().set('command_mode', False)
                view.settings().set('inverse_caret_state', False)

            view.settings().erase('vintage')
        except Exception:
            _log.exception('error initialising irregular view i.e. console, widget, panel, etc.')
        finally:
            return

    state = State(view)

    if not state.reset_during_init:
        # Probably exiting from an input panel, like when using '/'. Don't
        # reset the global state, as it may contain data needed to complete
        # the command that's being built.
        state.reset_during_init = True
        return

    # Non-standard user setting.
    reset = state.settings.view['vintageous_reset_mode_when_switching_tabs']
    # XXX: If the view was already in normal mode, we still need to run the
    # init code. I believe this is due to Sublime Text (intentionally) not
    # serializing the inverted caret state and the command_mode setting when
    # first loading a file.
    # If the mode is unknown, it might be a new file. Let normal mode setup
    # continue.
    if not reset and (state.mode not in (NORMAL, UNKNOWN)):
        return

    # If we have no selections, add one.
    if len(state.view.sel()) == 0:
        state.view.sel().add(Region(0))

    if state.mode in (VISUAL, VISUAL_LINE):
        # TODO: Don't we need to pass a mode here?
        view.window().run_command('_enter_normal_mode', {'from_init': True})

    elif state.mode in (INSERT, REPLACE):
        # TODO: Don't we need to pass a mode here?
        view.window().run_command('_enter_normal_mode', {'from_init': True})

    elif (view.has_non_empty_selection_region() and
          state.mode != VISUAL):
            # Runs, for example, when we've performed a search via ST3 search
            # panel and we've pressed 'Find All'. In this case, we want to
            # ensure a consistent state for multiple selections.
            # TODO: We could end up with multiple selections in other ways
            #       that bypass init_state.
            state.mode = VISUAL

    else:
        # This may be run when we're coming from cmdline mode.
        pseudo_visual = view.has_non_empty_selection_region()
        mode = VISUAL if pseudo_visual else state.mode
        # TODO: Maybe the above should be handled by State?
        state.enter_normal_mode()
        view.window().run_command('_enter_normal_mode', {'mode': mode, 'from_init': True})

    state.reset_command_data()

    if new_session:
        state.reset_volatile_data()
        rcfile.load()

        # TODO is setting the cwd for cmdline necessary?
        cmdline_cd = os.path.dirname(view.file_name()) if view.file_name() else os.getcwd()
        state.settings.vi['_cmdline_cd'] = cmdline_cd
