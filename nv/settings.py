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

from sublime import active_window

from NeoVintageous.nv.polyfill import save_preferences
from NeoVintageous.nv.session import get_session_value
from NeoVintageous.nv.session import get_session_view_value
from NeoVintageous.nv.session import set_session_value
from NeoVintageous.nv.session import set_session_view_value
from NeoVintageous.nv.vim import DIRECTION_DOWN
from NeoVintageous.nv.vim import UNKNOWN


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


def set_action_count(view, value: str) -> None:
    # TODO Is this check necessary; this was an assertion which are disabled in <4000 which is good
    if value != '' and not value.isdigit():
        raise ValueError()
    set_session_view_value(view, 'action_count', value)


def get_cmdline_cwd() -> str:
    cwd = get_session_value('cmdline_cwd')
    if cwd:
        return cwd

    window = active_window()
    if window:
        variables = window.extract_variables()
        if 'folder' in variables:
            return str(variables['folder'])

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


def get_ex_substitute_last_pattern() -> str:
    return get_session_value('ex_substitute_last_pattern')


def set_ex_substitute_last_pattern(pattern: str) -> None:
    set_session_value('ex_substitute_last_pattern', pattern, persist=True)


def get_ex_substitute_last_replacement() -> str:
    return get_session_value('ex_substitute_last_replacement')


def set_ex_substitute_last_replacement(replacement: str) -> None:
    set_session_value('ex_substitute_last_replacement', replacement, persist=True)


def get_last_char_search(view) -> str:
    # The last characte used for searches such as "f" and "t".
    return _get_private(view.window(), 'last_char_search', '')


def get_last_char_search_command(view) -> str:
    # Supports repeating the last search commands. For example the command ";"
    # (semi-colon) repeats the latest f, t, F or T [count] times and "," (comma)
    # repeats the latest f, t, F or T in opposite direction [count] times.
    return _get_private(view.window(), 'last_char_search_command', 'vi_f')


def set_last_char_search(view, value: str) -> None:
    _set_private(view.window(), 'last_char_search', value)


def set_last_char_search_command(view, value: str) -> None:
    _set_private(view.window(), 'last_char_search_command', value)


def get_last_buffer_search(view) -> str:
    # The last characte used for searches such as "/" and "?".
    return _get_private(view.window(), 'last_buffer_search', '')


def get_last_buffer_search_command(view) -> str:
    # Supports repeating the last search commands. For example the command "n".
    return _get_private(view.window(), 'last_buffer_search_command', 'nv_vi_slash')


def set_last_buffer_search(view, value: str) -> None:
    _set_private(view.window(), 'last_buffer_search', value)


def set_last_buffer_search_command(view, value: str) -> None:
    _set_private(view.window(), 'last_buffer_search_command', value)


def get_mode(view) -> str:
    # State of current mode. It isn't guaranteed that the underlying view's
    # .sel() will be in a consistent state (for example, that it will at least
    # have one non- empty region in visual mode.
    return get_session_view_value(view, 'mode', UNKNOWN)


def set_mode(view, value: str) -> None:
    set_session_view_value(view, 'mode', value)


def get_motion_count(view) -> str:
    return get_session_view_value(view, 'motion_count', '')


def set_motion_count(view, value: str) -> None:
    # TODO Is this check necessary; this was an assertion which are disabled in <4000 which is good
    if value != '' and not value.isdigit():
        raise ValueError()

    set_session_view_value(view, 'motion_count', value)


# This setting isn't reset automatically. nv_enter_normal_mode mode must take care
# of that so it can repeat the commands issued while in insert mode.
def get_normal_insert_count(view) -> int:
    # Count issued to 'i' or 'a', etc. These commands enter insert mode. If
    # passed a count, they must repeat the commands run while in insert mode.
    return int(get_session_view_value(view, 'normal_insert_count', 1))


def set_normal_insert_count(view, value: int) -> None:
    set_session_view_value(view, 'normal_insert_count', value)


def is_interactive(view) -> bool:
    # See set_interactive().
    return get_session_view_value(view, 'interactive', True)


def set_interactive(view, value: bool) -> None:
    # Indicate if prompts should be interactive or suppressed (non-interactive).
    # For example, cmdline and search input collecting: :ls<CR> and /foo<CR>.
    set_session_view_value(view, 'interactive', value)


def get_partial_sequence(view) -> str:
    # Sometimes we need to store a partial sequence to obtain the commands' full
    # name. Such is the case of `gD`, for example.
    return get_session_view_value(view, 'partial_sequence', '')


def set_partial_sequence(view, value: str) -> None:
    set_session_view_value(view, 'partial_sequence', value)


def is_processing_notation(view) -> bool:
    # Indicate whether nv_process_notation is running.
    #
    # Indicates whether nv_process_notation is running a command and is
    # grouping all edits in one single undo step. That is, we are running a non-
    # interactive sequence of commands.
    #
    # This property is *VOLATILE*; it shouldn't be persisted between sessions.
    return get_session_view_value(view, 'processing_notation', False)


def set_processing_notation(view, value: bool) -> None:
    return set_session_view_value(view, 'processing_notation', value)


def get_register(view) -> str:
    return get_session_view_value(view, 'register', '"')


def set_register(view, value: str) -> None:
    assert len(str(value)) == 1, '`value` must be a character'  # TODO Remove assertion
    set_session_view_value(view, 'register', value)
    set_must_capture_register_name(view, False)


def get_xpos(view) -> int:
    return get_session_view_value(view, 'xpos', 0)


def set_xpos(view, value: int) -> None:
    assert isinstance(value, int), '`value` must be an int'  # TODO Remove assertion
    set_session_view_value(view, 'xpos', value)


def is_must_capture_register_name(view) -> bool:
    return get_session_view_value(view, 'must_capture_register_name', False)


def set_must_capture_register_name(view, value: bool) -> None:
    set_session_view_value(view, 'must_capture_register_name', value)


def set_repeat_data(view, data: tuple) -> None:
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
    assert isinstance(data, tuple) or isinstance(data, list), 'bad call'  # TODO remove assertion
    assert len(data) == 4, 'bad call'  # TODO remove assertion
    set_session_view_value(view, 'repeat_data', data)


def get_repeat_data(view):
    return get_session_view_value(view, 'repeat_data')


def get_reset_during_init(view) -> bool:
    # Some commands gather input through input panels. An input panel is a view,
    # but when it's closed, the previous view gets activated and init code runs.
    # This setting can be used to inhibit running the init code when activated.
    return _get_private(view.window(), 'reset_during_init', True)


def set_reset_during_init(view, value: bool) -> None:
    _set_private(view.window(), 'reset_during_init', value)


def get_sequence(view) -> str:
    return get_session_view_value(view, 'sequence', '')


def set_sequence(view, value: str) -> None:
    set_session_view_value(view, 'sequence', value)


def append_sequence(view, value: str) -> None:
    set_sequence(view, get_sequence(view) + value)


def get_glue_until_normal_mode(view) -> bool:
    # Indicate that editing commands should be grouped together. They should be
    # grouped together in a single undo step after the user requested
    # `nv_enter_normal_mode` next. This property is *VOLATILE*; it shouldn't be
    # persisted between sessions.
    return get_session_view_value(view, 'glue_until_normal_mode', False)


def set_glue_until_normal_mode(view, value: bool) -> None:
    set_session_view_value(view, 'glue_until_normal_mode', value)


def get_visual_block_direction(view, default: int = DIRECTION_DOWN) -> int:
    return view.settings().get('_nv_visual_block_direction', default)


def set_visual_block_direction(view, direction: int) -> None:
    current_direction = get_visual_block_direction(view)
    if direction != current_direction:
        view.settings().set('_nv_visual_block_direction', direction)


def _toggle_preference(name: str) -> None:
    with save_preferences() as preferences:
        preferences.set(name, not preferences.get(name))


def toggle_ctrl_keys() -> None:
    _toggle_preference('vintageous_use_ctrl_keys')


def toggle_super_keys() -> None:
    _toggle_preference('vintageous_use_super_keys')
