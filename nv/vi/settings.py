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

from NeoVintageous.nv.vim import DIRECTION_DOWN

_WINDOW_SETTINGS = [
    'last_buffer_search'
]

_SCOPE_VI_VIEW = 3
_SCOPE_VI_WINDOW = 4


_cache = {}  # type: dict
_session = {}  # type: dict
_storage = {}  # type: dict


def _get_session_value(name, default=None):
    try:
        return _session[name]
    except KeyError:
        return default


def _set_session_value(name, value):
    _session[name] = value


def get_cache_value(name, default=None):
    try:
        return _cache[name]
    except KeyError:
        return default


def set_cache_value(name, value):
    _cache[name] = value


def set_ex_substitute_last_pattern(pattern):
    return _set_session_value('ex_substitute_last_pattern', pattern)


def get_ex_substitute_last_pattern():
    return _get_session_value('ex_substitute_last_pattern')


def get_ex_substitute_last_replacement():
    return _get_session_value('ex_substitute_last_replacement')


def set_ex_substitute_last_replacement(replacement):
    return _set_session_value('ex_substitute_last_replacement', replacement)


def get_ex_shell_last_command():
    return _get_session_value('ex_shell_last_command')


def set_ex_shell_last_command(cmd):
    return _set_session_value('ex_shell_last_command', cmd)


def get_ex_global_last_pattern():
    return _get_session_value('ex_global_last_pattern')


def set_ex_global_last_pattern(pattern):
    return _set_session_value('ex_global_last_pattern', pattern)


def get_cmdline_cwd():
    if 'cmdline_cwd' in _storage:
        return _storage['cmdline_cwd']

    window = active_window()
    if window:
        variables = window.extract_variables()
        if 'folder' in variables:
            return variables['folder']

    return os.getcwd()


def set_cmdline_cwd(path):
    _storage['cmdline_cwd'] = path


def get_visual_block_direction(view, default=DIRECTION_DOWN):
    return view.settings().get('_nv_visual_block_direction', default)


def set_visual_block_direction(view, direction):
    current_direction = get_visual_block_direction(view)
    if direction != current_direction:
        view.settings().set('_nv_visual_block_direction', direction)


def _toggle_preference(name):
    preferences = load_settings('Preferences.sublime-settings')
    value = preferences.get(name)
    preferences.set(name, not value)
    save_settings('Preferences.sublime-settings')


def toggle_ctrl_keys():
    _toggle_preference('vintageous_use_ctrl_keys')


def toggle_super_keys():
    _toggle_preference('vintageous_use_super_keys')


def toggle_side_bar(window):
    window.run_command('toggle_side_bar')

    if window.is_sidebar_visible():
        window.run_command('focus_side_bar')
    else:
        window.focus_group(window.active_group())


class _SublimeSettings():
    def __init__(self, container=None):
        self.settings = container.settings()

    def __getitem__(self, key):
        return self.settings.get(key)

    def __setitem__(self, key, value):
        self.settings.set(key, value)


class _VintageSettings():

    # XXX Temporary hardcoded list until settings are completeley refactored.
    _volatile_settings = ['repeat_data']  # type: list
    _volatile = defaultdict(dict)  # type: dict

    def __init__(self, view):
        self.view = view

        if view is not None:
            if not isinstance(view.settings().get('vintage'), dict):
                view.settings().set('vintage', dict())

            window = view.window()
            if window is not None and not isinstance(window.settings().get('vintage'), dict):
                window.settings().set('vintage', dict())

    def __getitem__(self, key):
        try:
            if key not in _WINDOW_SETTINGS:
                try:
                    return self._get_volatile(key)
                except KeyError:
                    value = self.view.settings().get('vintage').get(key)
            else:
                value = self.view.window().settings().get('vintage').get(key)

        except (KeyError, AttributeError):
            value = None

        return value

    def __setitem__(self, key, value):
        if key not in _WINDOW_SETTINGS:
            if key in _VintageSettings._volatile_settings:
                self._set_volatile(key, value)
                return
            setts, target = self.view.settings().get('vintage'), self.view
        else:
            setts, target = self.view.window().settings().get('vintage'), self.view.window()

        setts[key] = value
        target.settings().set('vintage', setts)

    def _get_volatile(self, key):
        try:
            return _VintageSettings._volatile[self.view.id()][key]
        except KeyError:
            raise KeyError('error accessing volatile key: %s' % key)

    def _set_volatile(self, key, value):
        try:
            _VintageSettings._volatile[self.view.id()][key] = value
        except KeyError:
            raise KeyError('error while setting key "%s" to value "%s"' % (key, value))


def destroy(view):
    try:
        del _VintageSettings._volatile[view.id()]
    except KeyError:
        pass


class SettingsManager():

    def __init__(self, view):
        self.window = _SublimeSettings(view.window())
        self.view = _SublimeSettings(view)
        self.vi = _VintageSettings(view)
