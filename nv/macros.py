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

from NeoVintageous.nv.polyfill import erase_window_status
from NeoVintageous.nv.polyfill import set_window_status
from NeoVintageous.nv.settings import get_glue_until_normal_mode

_data = {}  # type: dict


def _get(window, key: str = None, default=None):
    try:
        macro = _data[window.id()]
    except KeyError:
        macro = _data[window.id()] = {}

    if key is None:
        return macro

    try:
        return macro[key]
    except KeyError:
        return default


def is_valid_writable_register(name: str) -> bool:
    return name in tuple('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"')


def is_valid_readable_register(name: str) -> bool:
    return name in tuple('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ".=*+@')


def is_recording(window) -> bool:
    return _get(window, 'recording', False)


def start_recording(window, register_name: str) -> None:
    macro = _get(window)
    macro['recording'] = True
    macro['recording_steps'] = []
    macro['recording_register_name'] = register_name

    set_window_status(window, 'vim-recorder', 'recording @%s' % register_name)


def stop_recording(window) -> None:
    macro = _get(window)

    name = _get(window, 'recording_register_name')
    if name:
        if 'recorded' not in macro:
            macro['recorded'] = {}

        macro['recorded'][name] = _get_steps(window)

    macro['recording'] = False
    macro['recording_steps'] = []
    macro['recording_register_name'] = None

    erase_window_status(window, 'vim-recorder')


def get_recorded(window, name: str):
    macro = _get(window)

    try:
        return macro['recorded'][name]
    except KeyError:
        return None


def get_last_used_register_name(window) -> str:
    return _get(window, 'last_used_register_name')


def set_last_used_register_name(window, name: str) -> None:
    macro = _get(window)
    macro['last_used_register_name'] = name


def add_macro_step(view, cmd: str, args: dict) -> None:
    window = view.window()

    if is_recording(window):
        # don't store the ending macro step
        if cmd == 'nv_vi_q':
            return

        if not get_glue_until_normal_mode(view):
            macro = _get(window)

            if 'recording_steps' not in macro:
                macro['recording_steps'] = []

            macro['recording_steps'].append((cmd, args))


def _get_steps(window) -> list:
    return list(_get(window, 'recording_steps', []))
