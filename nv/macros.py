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

from NeoVintageous.nv.polyfill import erase_status
from NeoVintageous.nv.polyfill import set_status
from NeoVintageous.nv.session import get_session_value
from NeoVintageous.nv.session import set_session_value
from NeoVintageous.nv.settings import get_glue_until_normal_mode

_data = {}  # type: dict


def is_readable(name: str) -> bool:
    return name in tuple('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ".=*+@')


def is_writable(name: str) -> bool:
    return name in tuple('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"')


def is_recording() -> bool:
    try:
        return _data['recording']
    except KeyError:
        return False


def start_recording(name: str) -> None:
    _data['recording'] = True
    _data['recording_steps'] = []
    _data['recording_register'] = name

    set_status('vim-recorder', 'recording @%s' % name)


def stop_recording() -> None:
    name = _data['recording_register']
    if name:
        if 'recorded' not in _data:
            _data['recorded'] = {}

        _data['recorded'][name] = _get_steps()

    _data['recording'] = False
    _data['recording_steps'] = []
    _data['recording_register'] = None

    erase_status('vim-recorder')


def _get_steps() -> list:
    try:
        return _data['recording_steps']
    except KeyError:
        return []


def get_recorded(name: str):
    try:
        return _data['recorded'][name]
    except KeyError:
        return None


def get_last_used_register_name() -> str:
    return get_session_value('last_used_register_name')


def set_last_used_register_name(name: str) -> None:
    set_session_value('last_used_register_name', name)


def add_macro_step(view, cmd: str, args: dict) -> None:
    if is_recording():
        # don't store the ending macro step
        if cmd == 'nv_vi_q':
            return

        if not get_glue_until_normal_mode(view):
            if 'recording_steps' not in _data:
                _data['recording_steps'] = []

            _data['recording_steps'].append((cmd, args))
