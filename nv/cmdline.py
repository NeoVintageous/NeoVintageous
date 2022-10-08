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

from NeoVintageous.nv.options import get_option
from NeoVintageous.nv.utils import hide_panel


def _init_common_panel_settings(panel) -> None:
    _set = panel.settings().set

    _set('auto_complete', False)
    _set('auto_indent', False)
    _set('auto_match_enabled', False)
    _set('draw_centered', False)
    _set('draw_indent_guides', False)
    _set('gutter', False)
    _set('is_widget', True)
    _set('line_numbers', False)
    _set('match_selection', False)
    _set('rulers', [])
    _set('scroll_past_end', False)
    _set('smart_indent', False)
    _set('translate_tabs_to_spaces', False)
    _set('word_wrap', False)


class Cmdline():

    EX = ':'
    SEARCH_BACKWARD = '?'
    SEARCH_FORWARD = '/'

    _TYPES = (
        EX,
        SEARCH_BACKWARD,
        SEARCH_FORWARD,
    )

    def __init__(self, view, type: str, on_done=None, on_change=None, on_cancel=None):
        self._window = view.window()

        if type not in self._TYPES:
            raise ValueError('invalid cmdline type')

        self._type = type

        if type in (self.SEARCH_FORWARD, self.SEARCH_BACKWARD) and not get_option(view, 'incsearch'):
            on_change = None

        self._callbacks = {
            'on_done': on_done,
            'on_change': on_change,
            'on_cancel': on_cancel,
        }

    def prompt(self, initial_text: str) -> None:
        input_panel = self._window.show_input_panel(
            caption='',
            initial_text=self._type + initial_text,
            on_done=self._on_done,
            on_change=self._on_change,
            on_cancel=self._on_cancel
        )

        input_panel.set_name('Command-line mode')
        input_panel.settings().set('_nv_ex_mode', True)

        _init_common_panel_settings(input_panel)

    def _callback(self, callback, *args) -> None:
        if self._callbacks and callback in self._callbacks:
            self._callbacks[callback](*args)

    def _is_valid_input(self, cmdline: str) -> bool:
        return isinstance(cmdline, str) and len(cmdline) > 0 and cmdline[0] == self._type

    def _filter_input(self, inp: str) -> str:
        return inp[1:]

    def _on_done(self, inp: str) -> None:
        if not self._is_valid_input(inp):
            return self._on_cancel(force=True)

        self._callback('on_done', self._filter_input(inp))

    def _on_change(self, inp: str) -> None:
        if not self._is_valid_input(inp):
            return self._on_cancel(force=True)

        filtered_input = self._filter_input(inp)
        if filtered_input:
            self._callback('on_change', filtered_input)

    def _on_cancel(self, force: bool = False) -> None:
        if force:
            hide_panel(self._window)

        self._callback('on_cancel')


class CmdlineOutput():

    def __init__(self, window):
        self._window = window
        self._name = 'Command-line'
        self._output = self._window.create_output_panel(self._name)
        self._output.assign_syntax('Packages/NeoVintageous/res/Command-line output.sublime-syntax')

        _init_common_panel_settings(self._output)

    def show(self) -> None:
        self._window.run_command('show_panel', {'panel': 'output.' + self._name})
        self._output.settings().set('nv_cmdline_output', True)
        self.write('\nPress ENTER to continue')
        self._window.focus_view(self._window.find_output_panel(self._name))

    def write(self, text: str) -> None:
        self._output.set_read_only(False)
        self._output.run_command('insert', {'characters': text})
        self._output.set_read_only(True)
