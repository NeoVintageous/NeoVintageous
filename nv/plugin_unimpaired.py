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
from NeoVintageous.nv.options import set_window_ui_element_visible
from NeoVintageous.nv.options import toggle_option
from NeoVintageous.nv.plugin import register
from NeoVintageous.nv.polyfill import view_find
from NeoVintageous.nv.polyfill import view_rfind
from NeoVintageous.nv.settings import get_count
from NeoVintageous.nv.settings import get_mode
from NeoVintageous.nv.utils import InputParser
from NeoVintageous.nv.utils import regions_transformer
from NeoVintageous.nv.utils import set_selection
from NeoVintageous.nv.utils import translate_char
from NeoVintageous.nv.vi import seqs
from NeoVintageous.nv.vi.cmd_base import ViOperatorDef
from NeoVintageous.nv.vim import NORMAL
from NeoVintageous.nv.vim import VISUAL
from NeoVintageous.nv.window import window_buffer_control
from NeoVintageous.nv.window import window_tab_control


__all__ = [
    'nv_unimpaired_command'
]


@register(seqs.LEFT_SQUARE_BRACKET_L, (NORMAL, VISUAL))
class UnimpairedContextPrevious(ViOperatorDef):
    def translate(self, view):
        return {
            'action': 'nv_unimpaired',
            'action_args': {
                'mode': get_mode(view),
                'count': get_count(view),
                'action': 'context_previous'
            }
        }


@register(seqs.RIGHT_SQUARE_BRACKET_L, (NORMAL, VISUAL))
class UnimpairedContextNext(ViOperatorDef):
    def translate(self, view):
        return {
            'action': 'nv_unimpaired',
            'action_args': {
                'mode': get_mode(view),
                'count': get_count(view),
                'action': 'context_next'
            }
        }


@register(seqs.LEFT_SQUARE_BRACKET_N, (NORMAL,))
class UnimpairedGotoPrevConflictMarker(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, view):
        return {
            'action': 'nv_unimpaired',
            'action_args': {
                'mode': get_mode(view),
                'count': get_count(view),
                'action': 'goto_prev_conflict_marker'
            }
        }


@register(seqs.RIGHT_SQUARE_BRACKET_N, (NORMAL,))
class UnimpairedGotoNextConflictMarker(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates_xpos = True
        self.scroll_into_view = True

    def translate(self, view):
        return {
            'action': 'nv_unimpaired',
            'action_args': {
                'mode': get_mode(view),
                'count': get_count(view),
                'action': 'goto_next_conflict_marker'
            }
        }


@register(seqs.LEFT_SQUARE_BRACKET_SPACE, (NORMAL,))
class UnimpairedBlankUp(ViOperatorDef):
    def translate(self, view):
        return {
            'action': 'nv_unimpaired',
            'action_args': {
                'mode': get_mode(view),
                'count': get_count(view),
                'action': 'blank_up'
            }
        }


@register(seqs.RIGHT_SQUARE_BRACKET_SPACE, (NORMAL,))
class UnimpairedBlankDown(ViOperatorDef):
    def translate(self, view):
        return {
            'action': 'nv_unimpaired',
            'action_args': {
                'mode': get_mode(view),
                'count': get_count(view),
                'action': 'blank_down'
            }
        }


@register(seqs.LEFT_SQUARE_BRACKET_B, (NORMAL,))
class UnimpairedBprevious(ViOperatorDef):
    def translate(self, view):
        return {
            'action': 'nv_unimpaired',
            'action_args': {
                'mode': get_mode(view),
                'count': get_count(view),
                'action': 'bprevious'
            }
        }


@register(seqs.RIGHT_SQUARE_BRACKET_B, (NORMAL,))
class UnimpairedBnext(ViOperatorDef):
    def translate(self, view):
        return {
            'action': 'nv_unimpaired',
            'action_args': {
                'mode': get_mode(view),
                'count': get_count(view),
                'action': 'bnext'
            }
        }


@register(seqs.LEFT_SQUARE_BRACKET_BIG_B, (NORMAL,))
class UnimpairedBfirst(ViOperatorDef):
    def translate(self, view):
        return {
            'action': 'nv_unimpaired',
            'action_args': {
                'mode': get_mode(view),
                'count': get_count(view),
                'action': 'bfirst'
            }
        }


@register(seqs.RIGHT_SQUARE_BRACKET_BIG_B, (NORMAL,))
class UnimpairedBlast(ViOperatorDef):
    def translate(self, view):
        return {
            'action': 'nv_unimpaired',
            'action_args': {
                'mode': get_mode(view),
                'count': get_count(view),
                'action': 'blast'
            }
        }


@register(seqs.LEFT_SQUARE_BRACKET_E, (NORMAL,))
class UnimpairedMoveUp(ViOperatorDef):
    def translate(self, view):
        return {
            'action': 'nv_unimpaired',
            'action_args': {
                'mode': get_mode(view),
                'count': get_count(view),
                'action': 'move_up'
            }
        }


@register(seqs.RIGHT_SQUARE_BRACKET_E, (NORMAL,))
class UnimpairedMoveDown(ViOperatorDef):
    def translate(self, view):
        return {
            'action': 'nv_unimpaired',
            'action_args': {
                'mode': get_mode(view),
                'count': get_count(view),
                'action': 'move_down'
            }
        }


@register(seqs.LEFT_SQUARE_BRACKET_T, (NORMAL,))
class UnimpairedTabprevious(ViOperatorDef):
    def translate(self, view):
        return {
            'action': 'nv_unimpaired',
            'action_args': {
                'mode': get_mode(view),
                'count': get_count(view),
                'action': 'tabprevious'
            }
        }


@register(seqs.RIGHT_SQUARE_BRACKET_T, (NORMAL,))
class UnimpairedTabnext(ViOperatorDef):
    def translate(self, view):
        return {
            'action': 'nv_unimpaired',
            'action_args': {
                'mode': get_mode(view),
                'count': get_count(view),
                'action': 'tabnext'
            }
        }


@register(seqs.LEFT_SQUARE_BRACKET_BIG_T, (NORMAL,))
class UnimpairedTabfirst(ViOperatorDef):
    def translate(self, view):
        return {
            'action': 'nv_unimpaired',
            'action_args': {
                'mode': get_mode(view),
                'count': get_count(view),
                'action': 'tabfirst'
            }
        }


@register(seqs.RIGHT_SQUARE_BRACKET_BIG_T, (NORMAL,))
class UnimpairedTablast(ViOperatorDef):
    def translate(self, view):
        return {
            'action': 'nv_unimpaired',
            'action_args': {
                'mode': get_mode(view),
                'count': get_count(view),
                'action': 'tablast'
            }
        }


class OptionMixin(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = True
        self.input_parser = InputParser(InputParser.IMMEDIATE)

    @property
    def accept_input(self) -> bool:
        return self.inp == ''

    def accept(self, key: str) -> bool:
        self.inp += translate_char(key)

        return True


@register(seqs.CO, (NORMAL,))
@register(seqs.YO, (NORMAL,))
class UnimpairedToggle(OptionMixin):
    def translate(self, view):
        return {
            'action': 'nv_unimpaired',
            'action_args': {
                'action': 'toggle_option',
                'name': self.inp
            }
        }


@register(seqs.LEFT_SQUARE_BRACKET_O, (NORMAL,))
class UnimpairedToggleOn(OptionMixin):
    def translate(self, view):
        return {
            'action': 'nv_unimpaired',
            'action_args': {
                'action': 'enable_option',
                'name': self.inp
            }
        }


@register(seqs.RIGHT_SQUARE_BRACKET_O, (NORMAL,))
class UnimpairedToggleOff(OptionMixin):
    def translate(self, view):
        return {
            'action': 'nv_unimpaired',
            'action_args': {
                'action': 'disable_option',
                'name': self.inp
            }
        }


_CONFLICT_MARKER_REGEX = '^(<<<<<<< |=======$|>>>>>>> )'


def _goto_prev_conflict_marker(view, count: int) -> None:
    def f(view, s):
        for i in range(0, count):
            match = view_rfind(view, _CONFLICT_MARKER_REGEX, s.b)
            if not match:
                break

            s.a = s.b = match.begin()

        return s

    regions_transformer(view, f)


def _goto_next_conflict_marker(view, count: int) -> None:
    def f(view, s):
        for i in range(0, count):
            match = view_find(view, _CONFLICT_MARKER_REGEX, s.b + 1)
            if not match:
                break

            s.a = s.b = match.begin()

        return s

    regions_transformer(view, f)


# Go to the previous [count] lint error.
def _context_previous(window, count: int) -> None:
    window.run_command('sublime_linter_goto_error', {
        'direction': 'previous',
        'count': count
    })


# Go to the next [count] lint error.
def _context_next(window, count: int) -> None:
    window.run_command('sublime_linter_goto_error', {
        'direction': 'next',
        'count': count
    })


# Exchange the current line with [count] lines below it.
def _move_down(view, count: int) -> None:
    for i in range(count):
        view.run_command('swap_line_down')


# Exchange the current line with [count] lines above it.
def _move_up(view, count: int) -> None:
    for i in range(count):
        view.run_command('swap_line_up')


# Add [count] blank lines below the cursor.
def _blank_down(view, edit, count: int) -> None:
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
def _blank_up(view, edit, count: int) -> None:
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


def _set_bool_option(view, key: str, flag: bool = None) -> None:
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


def _do_toggle_option(view, name: str, flag: bool = None) -> None:
    if flag is None:
        toggle_option(view, name)
    else:
        set_option(view, name, flag)


def _list_option(view, flag: bool) -> None:
    _do_toggle_option(view, 'list', flag)


def _hlsearch_option(view, flag: bool) -> None:
    _do_toggle_option(view, 'hlsearch', flag)


def _ignorecase_option(view, flag: bool) -> None:
    _do_toggle_option(view, 'ignorecase', flag)


def _menu_option(view, flag: bool = None) -> None:
    set_window_ui_element_visible('menu', flag, view.window())


def _minimap_option(view, flag: bool = None) -> None:
    set_window_ui_element_visible('minimap', flag, view.window())


def _sidebar_option(view, flag: bool = None) -> None:
    set_window_ui_element_visible('sidebar', flag, view.window())


def _statusbar_option(view, flag: bool = None) -> None:
    set_window_ui_element_visible('status_bar', flag, view.window())


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
    'relativenumber': 'relative_line_numbers',
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


def _toggle_option(view, key, value=None) -> None:
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


class nv_unimpaired_command(TextCommand):
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
            window_buffer_control(self.view.window(), action[1:], count)
        elif action in ('tabnext', 'tabprevious', 'tabfirst', 'tablast'):
            window_tab_control(self.view.window(), action[3:], count)
        elif action == 'goto_next_conflict_marker':
            _goto_next_conflict_marker(self.view, count)
        elif action == 'goto_prev_conflict_marker':
            _goto_prev_conflict_marker(self.view, count)
        elif action == 'context_next':
            _context_next(self.view.window(), count)
        elif action == 'context_previous':
            _context_previous(self.view.window(), count)
        elif action == 'toggle_option':
            _toggle_option(self.view, kwargs.get('name'))
        elif action == 'enable_option':
            _toggle_option(self.view, kwargs.get('name'), True)
        elif action == 'disable_option':
            _toggle_option(self.view, kwargs.get('name'), False)
        else:
            raise ValueError('unknown action')
