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

# A port of https://github.com/tpope/vim-unimpaired.

from sublime_plugin import TextCommand

from NeoVintageous.nv.options import set_option
from NeoVintageous.nv.options import toggle_option
from NeoVintageous.nv.options import window_visible_option
from NeoVintageous.nv.plugin import register
from NeoVintageous.nv.utils import InputParser
from NeoVintageous.nv.utils import set_selection
from NeoVintageous.nv.utils import translate_char
from NeoVintageous.nv.vi.cmd_base import ViOperatorDef
from NeoVintageous.nv.vim import NORMAL
from NeoVintageous.nv.vim import VISUAL
from NeoVintageous.nv.window import window_buffer_control
from NeoVintageous.nv.window import window_tab_control


__all__ = [
    '_nv_unimpaired_command'
]


@register(seq='[l', modes=(NORMAL, VISUAL))
class _UnimpairedContextPrevious(ViOperatorDef):
    def translate(self, state):
        return {
            'action': '_nv_unimpaired',
            'action_args': {
                'mode': state.mode,
                'count': state.count,
                'action': 'context_previous'
            }
        }


@register(seq=']l', modes=(NORMAL, VISUAL))
class _UnimpairedContextNext(ViOperatorDef):
    def translate(self, state):
        return {
            'action': '_nv_unimpaired',
            'action_args': {
                'mode': state.mode,
                'count': state.count,
                'action': 'context_next'
            }
        }


@register(seq='[<space>', modes=(NORMAL,))
class _UnimpairedBlankUp(ViOperatorDef):
    def translate(self, state):
        return {
            'action': '_nv_unimpaired',
            'action_args': {
                'mode': state.mode,
                'count': state.count,
                'action': 'blank_up'
            }
        }


@register(seq=']<space>', modes=(NORMAL,))
class _UnimpairedBlankDown(ViOperatorDef):
    def translate(self, state):
        return {
            'action': '_nv_unimpaired',
            'action_args': {
                'mode': state.mode,
                'count': state.count,
                'action': 'blank_down'
            }
        }


@register(seq='[b', modes=(NORMAL,))
class _UnimpairedBprevious(ViOperatorDef):
    def translate(self, state):
        return {
            'action': '_nv_unimpaired',
            'action_args': {
                'mode': state.mode,
                'count': state.count,
                'action': 'bprevious'
            }
        }


@register(seq=']b', modes=(NORMAL,))
class _UnimpairedBnext(ViOperatorDef):
    def translate(self, state):
        return {
            'action': '_nv_unimpaired',
            'action_args': {
                'mode': state.mode,
                'count': state.count,
                'action': 'bnext'
            }
        }


@register(seq='[B', modes=(NORMAL,))
class _UnimpairedBfirst(ViOperatorDef):
    def translate(self, state):
        return {
            'action': '_nv_unimpaired',
            'action_args': {
                'mode': state.mode,
                'count': state.count,
                'action': 'bfirst'
            }
        }


@register(seq=']B', modes=(NORMAL,))
class _UnimpairedBlast(ViOperatorDef):
    def translate(self, state):
        return {
            'action': '_nv_unimpaired',
            'action_args': {
                'mode': state.mode,
                'count': state.count,
                'action': 'blast'
            }
        }


@register(seq='[e', modes=(NORMAL,))
class _UnimpairedMoveUp(ViOperatorDef):
    def translate(self, state):
        return {
            'action': '_nv_unimpaired',
            'action_args': {
                'mode': state.mode,
                'count': state.count,
                'action': 'move_up'
            }
        }


@register(seq=']e', modes=(NORMAL,))
class _UnimpairedMoveDown(ViOperatorDef):
    def translate(self, state):
        return {
            'action': '_nv_unimpaired',
            'action_args': {
                'mode': state.mode,
                'count': state.count,
                'action': 'move_down'
            }
        }


@register(seq='[t', modes=(NORMAL,))
class _UnimpairedTabprevious(ViOperatorDef):
    def translate(self, state):
        return {
            'action': '_nv_unimpaired',
            'action_args': {
                'mode': state.mode,
                'count': state.count,
                'action': 'tabprevious'
            }
        }


@register(seq=']t', modes=(NORMAL,))
class _UnimpairedTabnext(ViOperatorDef):
    def translate(self, state):
        return {
            'action': '_nv_unimpaired',
            'action_args': {
                'mode': state.mode,
                'count': state.count,
                'action': 'tabnext'
            }
        }


@register(seq='[T', modes=(NORMAL,))
class _UnimpairedTabfirst(ViOperatorDef):
    def translate(self, state):
        return {
            'action': '_nv_unimpaired',
            'action_args': {
                'mode': state.mode,
                'count': state.count,
                'action': 'tabfirst'
            }
        }


@register(seq=']T', modes=(NORMAL,))
class _UnimpairedTablast(ViOperatorDef):
    def translate(self, state):
        return {
            'action': '_nv_unimpaired',
            'action_args': {
                'mode': state.mode,
                'count': state.count,
                'action': 'tablast'
            }
        }


class _BaseToggleDef(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = True
        self.input_parser = InputParser(InputParser.IMMEDIATE)

    @property
    def accept_input(self):
        return self.inp == ''

    def accept(self, key: str) -> bool:
        self.inp += translate_char(key)

        return True


@register(seq='co', modes=(NORMAL,))
@register(seq='yo', modes=(NORMAL,))
class _UnimpairedToggle(_BaseToggleDef):
    def translate(self, state):
        return {
            'action': '_nv_unimpaired',
            'action_args': {
                'action': 'toggle_option',
                'value': self.inp
            }
        }


@register(seq='[o', modes=(NORMAL,))
class _UnimpairedToggleOn(_BaseToggleDef):
    def translate(self, state):
        return {
            'action': '_nv_unimpaired',
            'action_args': {
                'action': 'enable_option',
                'value': self.inp
            }
        }


@register(seq=']o', modes=(NORMAL,))
class _UnimpairedToggleOff(_BaseToggleDef):
    def translate(self, state):
        return {
            'action': '_nv_unimpaired',
            'action_args': {
                'action': 'disable_option',
                'value': self.inp
            }
        }


# Go to the previous [count] SCM conflict marker or diff/patch hunk.
def _context_previous(view, count):
    window = view.window()
    if window:
        window.run_command('sublime_linter_goto_error', {
            'direction': 'previous',
            'count': count
        })


# Go to the next [count] SCM conflict marker or diff/patch hunk.
def _context_next(view, count):
    window = view.window()
    if window:
        window.run_command('sublime_linter_goto_error', {
            'direction': 'next',
            'count': count
        })


# Exchange the current line with [count] lines below it.
def _move_down(view, count):
    for i in range(count):
        view.run_command('swap_line_down')


# Exchange the current line with [count] lines above it.
def _move_up(view, count):
    for i in range(count):
        view.run_command('swap_line_up')


# Add [count] blank lines below the cursor.
def _blank_down(view, edit, count):
    end_point = view.size()
    new_sels = []
    for sel in view.sel():
        line = view.line(sel)

        if line.empty():
            new_sels.append(line.b)
        else:
            new_sels.append(view.find('[^\\s]', line.begin()).begin())

        view.insert(
            edit,
            line.end() + 1 if line.end() < end_point else end_point,
            '\n' * count
        )

    if new_sels:
        set_selection(view, new_sels)


# Add [count] blank lines above the cursor.
def _blank_up(view, edit, count):
    new_sels = []
    for sel in view.sel():
        line = view.line(sel)
        if line.empty():
            new_sels.append(line.b + count)
        else:
            new_sels.append(view.find('[^\\s]', line.begin()).begin() + count)

        view.insert(
            edit,
            line.begin() - 1 if line.begin() > 0 else 0,
            '\n' * count
        )

    if new_sels:
        set_selection(view, new_sels)


def _set_bool_option(view, key, flag=None):
    settings = view.settings()
    value = settings.get(key)

    if flag is None:
        settings.set(key, not value)
    elif flag:
        if not value:
            settings.set(key, True)
    else:
        if value:
            settings.set(key, False)


def _do_toggle_option(view, key, flag=None):
    if flag is None:
        toggle_option(view, key)
    else:
        set_option(view, key, flag)


def _list_option(view, flag):
    _do_toggle_option(view, 'list', flag)


def _hlsearch_option(view, flag):
    _do_toggle_option(view, 'hlsearch', flag)


def _ignorecase_option(view, flag):
    _do_toggle_option(view, 'ignorecase', flag)


def _menu_option(view, flag=None):
    window_visible_option(view, 'menu', flag)


def _minimap_option(view, flag=None):
    window_visible_option(view, 'minimap', flag)


def _sidebar_option(view, flag=None):
    window_visible_option(view, 'sidebar', flag)


def _statusbar_option(view, flag=None):
    window_visible_option(view, 'status_bar', flag)


# Used by the _toggle_option() function.
# * None: means the option is not implemented.
# * str: means the option is a boolean option.
# * function: means it is a complex option.
_OPTIONS = {
    'background': None,
    'crosshairs': None,
    'cursorcolumn': None,
    'cursorline': 'highlight_line',
    'diff': None,
    'hlsearch': _hlsearch_option,
    'ignorecase': _ignorecase_option,
    'list': _list_option,
    'menu': _menu_option,  # non standard i.e. not in the original Unimpaired plugin
    'minimap': _minimap_option,  # non standard i.e. not in the original Unimpaired plugin
    'number': 'line_numbers',
    'relativenumber': None,
    'sidebar': _sidebar_option,  # non standard i.e. not in the original Unimpaired plugin
    'spell': 'spell_check',
    'statusbar': _statusbar_option,  # non standard i.e. not in the original Unimpaired plugin
    'virtualedit': None,
    'wrap': 'word_wrap'
}


# These aliases are mapped to _OPTIONS.
_OPTION_ALIASES = {
    'a': 'menu',  # non standard i.e. not in the original Unimpaired plugin
    'b': 'background',
    'c': 'cursorline',
    'd': 'diff',
    'e': 'statusbar',  # non standard i.e. not in the original Unimpaired plugin
    'h': 'hlsearch',
    'i': 'ignorecase',
    'l': 'list',
    'm': 'minimap',  # non standard i.e. not in the original Unimpaired plugin
    'n': 'number',
    'r': 'relativenumber',
    's': 'spell',
    't': 'sidebar',  # non standard i.e. not in the original Unimpaired plugin
    'u': 'cursorcolumn',
    'v': 'virtualedit',
    'w': 'wrap',
    'x': 'crosshairs'
}


def _toggle_option(view, key, value=None):
    if key in _OPTION_ALIASES:
        key = _OPTION_ALIASES[key]

    if key not in _OPTIONS:
        raise ValueError('unknown toggle')

    option = _OPTIONS[key]

    if not option:
        raise ValueError('option is not implemented')

    if isinstance(option, str):
        _set_bool_option(view, option, value)
    elif callable(option):
        option(view, value)
    else:
        raise ValueError('unknown option type')


class _nv_unimpaired_command(TextCommand):
    def run(self, edit, action, mode=None, count=1, **kwargs):
        if action == 'move_down':
            _move_down(self.view, count)
        elif action == 'move_up':
            _move_up(self.view, count)
        elif action == 'blank_down':
            _blank_down(self.view, edit, count)
        elif action == 'blank_up':
            _blank_up(self.view, edit, count)
        elif action in ('bnext', 'bprevious', 'bfirst', 'blast'):
            window_buffer_control(self.view.window(), action[1:], count=count)
        elif action in ('tabnext', 'tabprevious', 'tabfirst', 'tablast'):
            window_tab_control(self.view.window(), action[3:], count=count)
        elif action == 'context_next':
            _context_next(self.view, count)
        elif action == 'context_previous':
            _context_previous(self.view, count)
        elif action == 'toggle_option':
            _toggle_option(self.view, kwargs.get('value'))
        elif action == 'enable_option':
            _toggle_option(self.view, kwargs.get('value'), True)
        elif action == 'disable_option':
            _toggle_option(self.view, kwargs.get('value'), False)
        else:
            raise ValueError('unknown action')
