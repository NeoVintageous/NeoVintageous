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

_state = {}  # type: dict


def _get(window, key=None, default=None):
    try:
        state = _state[window.id()]
    except KeyError:
        state = _state[window.id()] = {}

    if key is None:
        return state

    try:
        return state[key]
    except KeyError:
        return default


def is_valid_writable_register(name):
    return name in tuple('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"')


def is_valid_readable_register(name):
    return name in tuple('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ".=*+@')


def is_recording(window):
    return _get(window, 'recording', False)


def start_recording(window, register_name):
    state = _get(window)
    state['recording'] = True
    state['recording_steps'] = []
    state['recording_register_name'] = register_name

    set_window_status(window, 'vim-recorder', 'recording @%s' % register_name)


def stop_recording(window):
    state = _get(window)

    name = _get(window, 'recording_register_name')
    if name:
        if 'recorded' not in state:
            state['recorded'] = {}

        state['recorded'][name] = _get_steps(window)

    state['recording'] = False
    state['recording_steps'] = []
    state['recording_register_name'] = None

    erase_window_status(window, 'vim-recorder')


def get_recorded(window, name):
    state = _get(window)

    try:
        return state['recorded'][name]
    except KeyError:
        return None


def get_last_used_register_name(window):
    return _get(window, 'last_used_register_name')


def set_last_used_register_name(window, name):
    state = _get(window)
    state['last_used_register_name'] = name


# TODO Refactor to remove State dependency
def add_step(state, cmd, args):
    window = state.view.window()

    if is_recording(window):
        # don't store the ending macro step
        if cmd == '_vi_q':
            return

        if state.runnable and not state.glue_until_normal_mode:
            state = _get(window)

            if 'recording_steps' not in state:
                state['recording_steps'] = []

            state['recording_steps'].append((cmd, args))


def _get_steps(window):
    return list(_get(window, 'recording_steps', []))
