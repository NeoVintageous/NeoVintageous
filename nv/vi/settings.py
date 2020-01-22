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

from NeoVintageous.nv.vim import DIRECTION_DOWN


_cache = {}  # type: dict
_session = {}  # type: dict
_storage = {}  # type: dict
_views = defaultdict(dict)  # type: dict


def _get_session_value(name: str, default=None):
    try:
        return _session[name]
    except KeyError:
        return default


def _set_session_value(name: str, value) -> None:
    _session[name] = value


def get_cache_value(name: str, default=None):
    try:
        return _cache[name]
    except KeyError:
        return default


def set_cache_value(name: str, value) -> None:
    _cache[name] = value


def set_ex_substitute_last_pattern(pattern: str):
    return _set_session_value('ex_substitute_last_pattern', pattern)


def get_ex_substitute_last_pattern():
    return _get_session_value('ex_substitute_last_pattern')


def get_ex_substitute_last_replacement():
    return _get_session_value('ex_substitute_last_replacement')


def set_ex_substitute_last_replacement(replacement: str):
    return _set_session_value('ex_substitute_last_replacement', replacement)


def get_ex_shell_last_command():
    return _get_session_value('ex_shell_last_command')


def set_ex_shell_last_command(cmd: str):
    return _set_session_value('ex_shell_last_command', cmd)


def get_ex_global_last_pattern():
    return _get_session_value('ex_global_last_pattern')


def set_ex_global_last_pattern(pattern: str):
    return _set_session_value('ex_global_last_pattern', pattern)


def get_cmdline_cwd() -> str:
    if 'cmdline_cwd' in _storage:
        return _storage['cmdline_cwd']

    window = active_window()
    if window:
        variables = window.extract_variables()
        if 'folder' in variables:
            return str(variables['folder'])

    return os.getcwd()


def set_cmdline_cwd(path: str) -> None:
    _storage['cmdline_cwd'] = path


def get_visual_block_direction(view, default: int = DIRECTION_DOWN) -> int:
    return view.settings().get('_nv_visual_block_direction', default)


def set_visual_block_direction(view, direction: int) -> None:
    current_direction = get_visual_block_direction(view)
    if direction != current_direction:
        view.settings().set('_nv_visual_block_direction', direction)


# TODO remove assertions
def set_repeat_data(view, data: tuple) -> None:
    # Store data structure for repeat commands like "." to use.
    # Args:
    #   tuple (type, cmd_name_or_key_seq, mode): Type may be "vi" or
    #       "native" ("vi" commands are executed via _nv_process_notation,
    #       "while "native" commands are executed via sublime.run_command().
    assert isinstance(data, tuple) or isinstance(data, list), 'bad call'
    assert len(data) == 4, 'bad call'
    _views[view.id()]['repeat_data'] = data


def get_repeat_data(view):
    try:
        return _views[view.id()]['repeat_data']
    except KeyError:
        pass


def on_close(view) -> None:
    try:
        del _views[view.id()]
    except KeyError:
        pass


class _VintageSettings():

    def __init__(self, view):
        self.view = view
        if view is not None and not isinstance(view.settings().get('vintage'), dict):
            view.settings().set('vintage', dict())

    def __getitem__(self, key: str):
        return self.view.settings().get('vintage').get(key)

    def __setitem__(self, key: str, value) -> None:
        settings = self.view.settings().get('vintage')
        settings[key] = value
        self.view.settings().set('vintage', settings)


class SettingsManager():

    def __init__(self, view):
        self.vi = _VintageSettings(view)
