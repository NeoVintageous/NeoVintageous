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

import os

from sublime import active_window

from NeoVintageous.nv.polyfill import toggle_preference
from NeoVintageous.nv.session import get_session_value
from NeoVintageous.nv.session import get_session_view_value
from NeoVintageous.nv.session import set_session_value
from NeoVintageous.nv.session import set_session_view_value
from NeoVintageous.nv.vim import DIRECTION_DOWN
from NeoVintageous.nv.vim import UNKNOWN
from NeoVintageous.nv.events_user import on_mode_change


def get_setting(view, name: str, default=None):
    return view.settings().get('vintageous_%s' % name, default)


def set_setting(view, name: str, value) -> None:
    view.settings().set('vintageous_%s' % name, value)


def reset_setting(view, name: str) -> None:
    view.settings().erase('vintageous_%s' % name)


def _get_private(obj, name: str, default=None):
    return obj.settings().get('_vintageous_%s' % name, default)


def _set_private(obj, name: str, value) -> None:
    obj.settings().set('_vintageous_%s' % name, value)


def get_internal_setting(obj, name: str, default=None):
    return _get_private(obj, name, default)


def set_internal_setting(obj, name: str, value) -> None:
    _set_private(obj, name, value)


# DEPRECATED TODO Refactor to use get_setting() instead
def get_setting_neo(view, name: str):
    return view.settings().get('neovintageous_%s' % name)


def get_action_count(view) -> str:
    return get_session_view_value(view, 'action_count', '')


def set_action_count(view, value) -> None:
    set_session_view_value(view, 'action_count', str(value))


def get_cmdline_cwd() -> str:
    # 1. Return session cwd e.g. set via ":cd {path}".
    cwd = get_session_value('cmdline_cwd')
    if cwd:
        return cwd

    window = active_window()
    if window:

        # 2. Return first window folder.
        variables = window.extract_variables()
        if 'folder' in variables:
            return str(variables['folder'])

        # 3. Return first view file name dirname.
        for view in window.views():
            if view:
                file_name = view.file_name()
                if file_name:
                    return os.path.dirname(file_name)

    # 4. Default to the cwd set by ST.
    return os.getcwd()


def set_cmdline_cwd(path: str) -> None:
    set_session_value('cmdline_cwd', path)


def get_count(view, default: int = 1) -> int:
    c = default

    acount = get_action_count(view)
    if acount:
        c = int(acount) or 1

    mcount = get_motion_count(view)
    if mcount:
        # If the operator count is 0 and the motion has count, the operator
        # count needs to be adjusted to 1 because the two counts need to be
        # multiplied and multiplying by 0 is always 0. For example: "gc7G"
        if c == 0:
            c = 1

        # If the motion includes a count and the operator also has a
        # count, the two counts are multiplied.  For example: "2d3w"
        # deletes six words.
        c *= int(mcount) or 1

    if c < 0:
        raise ValueError('count must be greater than zero')

    return c


def get_ex_global_last_pattern() -> str:
    return get_session_value('ex_global_last_pattern')


def set_ex_global_last_pattern(pattern: str) -> None:
    set_session_value('ex_global_last_pattern', pattern)


def get_ex_shell_last_command() -> str:
    return get_session_value('ex_shell_last_command')


def set_ex_shell_last_command(cmd: str) -> None:
    set_session_value('ex_shell_last_command', cmd)


def get_last_substitute_search_pattern() -> str:
    return get_session_value('last_substitute_search_pattern')


def set_last_substitute_search_pattern(pattern: str) -> None:
    set_session_value('last_substitute_search_pattern', pattern, persist=True)


def get_last_substitute_string() -> str:
    return get_session_value('last_substitute_string')


def set_last_substitute_string(replacement: str) -> None:
    set_session_value('last_substitute_string', replacement, persist=True)


def get_exit_when_quiting_last_window(view) -> bool:
    return get_setting(view, 'exit_when_quiting_last_window')


# Supports repeating the last search commands. For example the command ";"
# (semi-colon) repeats the latest f, t, F or T [count] times and ","
# (comma) repeats the latest f, t, F or T in opposite direction.
def get_last_char_search_command(view) -> str:
    return _get_private(view.window(), 'last_char_search_command', 'vi_f')


# The last character used for searches such as "f" and "t".
def get_last_char_search_character(view) -> str:
    return _get_private(view.window(), 'last_char_search_character', '')


def set_last_char_search(view, command: str, character: str) -> None:
    set_last_char_search_command(view, command)
    set_last_char_search_character(view, character)


def set_last_char_search_command(view, value: str) -> None:
    _set_private(view.window(), 'last_char_search_command', value)


def set_last_char_search_character(view, value: str) -> None:
    _set_private(view.window(), 'last_char_search_character', value)


# The last characte used for searches such as "/" and "?".
def get_last_search_pattern(view) -> str:
    return get_session_value('last_search_pattern', '')


# Supports repeating the last search commands. For example the command "n".
def get_last_search_pattern_command(view) -> str:
    return get_session_value('last_search_pattern_command', 'nv_vi_slash')


def set_last_search_pattern(view, pattern: str, command: str) -> None:
    set_session_value('last_search_pattern', pattern)
    set_session_value('last_search_pattern_command', command)


# State of current mode. It isn't guaranteed that the underlying view's
# .sel() will be in a consistent state (for example, that it will at least
# have one non- empty region in visual mode.
def get_mode(view) -> str:
    return get_session_view_value(view, 'mode', UNKNOWN)


def set_mode(view, value: str) -> None:
    current_mode = get_mode(view)
    if not current_mode == value: # mode changes
       set_session_view_value(view, f'is_{current_mode}', False) # unset old mode
       set_session_view_value(view, f'is_{value}'       , True ) #   set new mode
       on_mode_change(view, current_mode, value)
    set_session_view_value(view, 'mode', value)


def get_motion_count(view) -> str:
    return get_session_view_value(view, 'motion_count', '')


def set_motion_count(view, value) -> None:
    set_session_view_value(view, 'motion_count', str(value))


# This setting isn't reset automatically. nv_enter_normal_mode mode must take care
# of that so it can repeat the commands issued while in insert mode.
# Count issued to 'i' or 'a', etc. These commands enter insert mode. If
# passed a count, they must repeat the commands run while in insert mode.
def get_normal_insert_count(view) -> int:
    return int(get_session_view_value(view, 'normal_insert_count', 1))


def set_normal_insert_count(view, value: int) -> None:
    set_session_view_value(view, 'normal_insert_count', value)


# See set_interactive().
def is_interactive(view) -> bool:
    return get_session_view_value(view, 'interactive', True)


# Indicate if prompts should be interactive or suppressed (non-interactive).
# For example, cmdline and search input collecting: :ls<CR> and /foo<CR>.
def set_interactive(view, value: bool) -> None:
    set_session_view_value(view, 'interactive', value)


# Sometimes we need to store a partial sequence to obtain the commands' full
# name. Such is the case of `gD`, for example.
def get_partial_sequence(view) -> str:
    return get_session_view_value(view, 'partial_sequence', '')


def set_partial_sequence(view, value: str) -> None:
    set_session_view_value(view, 'partial_sequence', value)


# Indicate whether nv_process_notation is running.
#
# Indicates whether nv_process_notation is running a command and is
# grouping all edits in one single undo step. That is, we are running a non-
# interactive sequence of commands.
#
# This property is *VOLATILE*; it shouldn't be persisted between sessions.
def is_processing_notation(view) -> bool:
    return get_session_view_value(view, 'processing_notation', False)


def set_processing_notation(view, value: bool) -> None:
    return set_session_view_value(view, 'processing_notation', value)


def get_register(view) -> str:
    return get_session_view_value(view, 'register', '"')


def set_register(view, value: str) -> None:
    set_session_view_value(view, 'register', value)
    set_capture_register(view, False)


def get_capture_register(view) -> bool:
    return get_session_view_value(view, 'capture_register', False)


def set_capture_register(view, value: bool) -> None:
    set_session_view_value(view, 'capture_register', value)


def get_xpos(view) -> int:
    return get_session_view_value(view, 'xpos', 0)


def set_xpos(view, value: int) -> None:
    set_session_view_value(view, 'xpos', value)


def set_repeat_data(view, data) -> None:
    # :param data:
    #   The repeat data.
    #   A tuple or list.
    #
    # The structure of {data}:
    #
    #   (
    #       {type},
    #       {command_data},
    #       {mode},
    #       {visual_data}
    #   )
    #
    # arg            | type          | description
    # ---------------|---------------|------------
    # {type}         | str           | "vi" or "native".
    # {command_data} | str or tuple  | e.g. "x" or ("insert", {"characters": "hello"})
    # {mode}         | str           | e.g. "mode_insert"
    # {visual_data}  | None or tuple | e.g. (0, 4, "mode_visual")
    #
    # * {command_data} can be a string key sequence or a command with args.
    # * {visual_data} can be a tuple ({start_pt}, {end_pt}, {mode}).
    #
    # Examples:
    #
    #   ( "native", ("insert", {"characters": "fizz"}), "mode_insert", None )
    #   ( "vi", "x", "mode_normal", (0, 4, "mode_visual") )
    #   ( "native", ("sequence", {"commands": [["insert", {"characters": "fizz"}], ["left_delete", None]]}), "mode_insert", None )  # noqa: 501
    #
    set_session_view_value(view, 'repeat_data', data)


def get_repeat_data(view):
    return get_session_view_value(view, 'repeat_data')


# Some commands gather input through input panels. An input panel is a view,
# but when it's closed, the previous view gets activated and init code runs.
# This setting can be used to inhibit running the init code when activated.
def get_reset_during_init(view) -> bool:
    return _get_private(view.window(), 'reset_during_init', True)


def set_reset_during_init(view, value: bool) -> None:
    _set_private(view.window(), 'reset_during_init', value)


def get_sequence(view) -> str:
    return get_session_view_value(view, 'sequence', '')


def set_sequence(view, value: str) -> None:
    set_session_view_value(view, 'sequence', value)


def append_sequence(view, value: str) -> None:
    set_sequence(view, get_sequence(view) + value)


# Indicate that editing commands should be grouped together. They should be
# grouped together in a single undo step after the user requested
# `nv_enter_normal_mode` next. This property is *VOLATILE*; it shouldn't be
# persisted between sessions.
def get_glue_until_normal_mode(view) -> bool:
    return get_session_view_value(view, 'glue_until_normal_mode', False)


def set_glue_until_normal_mode(view, value: bool) -> None:
    set_session_view_value(view, 'glue_until_normal_mode', value)


def get_visual_block_direction(view, default: int = DIRECTION_DOWN) -> int:
    return view.settings().get('_nv_visual_block_direction', default)


def set_visual_block_direction(view, direction: int) -> None:
    current_direction = get_visual_block_direction(view)
    if direction != current_direction:
        view.settings().set('_nv_visual_block_direction', direction)


def toggle_ctrl_keys() -> None:
    toggle_preference('vintageous_use_ctrl_keys')


def toggle_super_keys() -> None:
    toggle_preference('vintageous_use_super_keys')


def is_plugin_enabled(view, plugin: object) -> bool:
    return get_setting(view, 'enable_%s' % plugin.__class__.__module__[24:])
