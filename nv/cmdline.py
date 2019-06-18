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

from NeoVintageous.nv.ui import ui_cmdline_prompt
from NeoVintageous.nv.utils import hide_panel


class Cmdline():

    EX = ':'
    SEARCH_BACKWARD = '?'
    SEARCH_FORWARD = '/'

    _TYPES = (
        EX,
        SEARCH_BACKWARD,
        SEARCH_FORWARD,
    )

    def __init__(self, window, type, on_done=None, on_change=None, on_cancel=None):
        self._window = window

        if type not in self._TYPES:
            raise ValueError('invalid cmdline type')

        self._type = type

        self._callbacks = {
            'on_done': on_done,
            'on_change': on_change,
            'on_cancel': on_cancel,
        }

    def prompt(self, initial_text):
        ui_cmdline_prompt(
            self._window,
            initial_text=self._type + initial_text,
            on_done=self._on_done,
            on_change=self._on_change,
            on_cancel=self._on_cancel
        )

    def _callback(self, callback, *args):
        if self._callbacks and callback in self._callbacks:
            self._callbacks[callback](*args)

    def _is_valid_input(self, cmdline):
        return isinstance(cmdline, str) and len(cmdline) > 0 and cmdline[0] == self._type

    def _filter_input(self, inp):
        return inp[1:]

    def _on_done(self, inp):
        if not self._is_valid_input(inp):
            return self._on_cancel(force=True)

        self._callback('on_done', self._filter_input(inp))

    def _on_change(self, inp):
        if not self._is_valid_input(inp):
            return self._on_cancel(force=True)

        filtered_input = self._filter_input(inp)
        if filtered_input:
            self._callback('on_change', filtered_input)

    def _on_cancel(self, force=False):
        if force:
            hide_panel(self._window)

        self._callback('on_cancel')
