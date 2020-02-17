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

from collections import defaultdict
import os

from sublime import active_window
from sublime import load_settings
from sublime import save_settings

from NeoVintageous.nv.polyfill import save_preferences
from NeoVintageous.nv.session import get_session_value
from NeoVintageous.nv.session import set_session_value
from NeoVintageous.nv.vim import DIRECTION_DOWN

# TODO Refactor into .session
_views = defaultdict(dict)  # type: dict


# TODO Refactor to .session
def get_session_view_value(view, name: str):
    try:
        return _views[view.id()][name]
    except KeyError:
        pass


# TODO Refactor to .session
def set_session_view_value(view, name: str, value) -> None:
    _views[view.id()][name] = value


def on_close(view) -> None:
    try:
        del _views[view.id()]
    except KeyError:
        pass


def get_setting(view, name: str, default=None):
    return view.settings().get('vintageous_%s' % name, default)


def set_setting(view, name: str, value) -> None:
    view.settings().set('vintageous_%s' % name)


def reset_setting(view, name: str) -> None:
    view.settings().erase('vintageous_%s' % name)


def _get_private(obj, name: str, default=None):
    return obj.settings().get('_vintageous_%s' % name, default)


def _set_private(obj, name: str, value) -> None:
    obj.settings().set('_vintageous_%s' % name, value)


# DEPRECATED TODO Refactor to use get_setting() instead
def get_setting_neo(view, name: str):
    return view.settings().get('neovintageous_%s' % name)


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
    return _get_private(view.window(), 'last_buffer_search_command', 'vi_slash')


def set_last_buffer_search(view, value: str) -> None:
    _set_private(view.window(), 'last_buffer_search', value)


def set_last_buffer_search_command(view, value: str) -> None:
    _set_private(view.window(), 'last_buffer_search_command', value)


def set_repeat_data(view, data: tuple) -> None:
    # The structure of {data}:
    #
    #   [{type}, {command}, {mode}, {visual}]
    #
    # Type can be "vi" or "native".
    #
    # Command can be a string key sequence or a ST command with args.
    #
    # Visual is a tuple (start_pt, end_pt, mode).
    #
    # Examples:
    #
    # ('native', ('insert', {'characters': 'fizz'}), 'mode_insert', None)
    # ('native', ('sequence', {'commands': [['insert', {'characters': 'fizz'}], ['left_delete', None]]}), 'mode_insert', None])  # noqa: E501
    # ('vi', 'x', 'mode_normal', (0, 4, 'mode_visual'))
    # TODO remove assertions
    assert isinstance(data, tuple) or isinstance(data, list), 'bad call'
    assert len(data) == 4, 'bad call'
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
