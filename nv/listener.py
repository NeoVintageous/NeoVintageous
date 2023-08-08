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

_listeners = {}


def register(name: str, listener) -> None:
    _listeners[name] = listener


# InsertEnter - Just before starting Insert mode.
def on_insert_enter(view, prev_mode: str) -> None:
    for listener in _listeners.values():
        listener.on_insert_enter(view, prev_mode)


# InsertLeave - Just after leaving Insert mode.
def on_insert_leave(view, new_mode: str) -> None:
    for listener in _listeners.values():
        listener.on_insert_leave(view, new_mode)
