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

from NeoVintageous.nv.plugin import INPUT_IMMEDIATE
from NeoVintageous.nv.plugin import inputs
from NeoVintageous.nv.plugin import NORMAL
from NeoVintageous.nv.plugin import register
from NeoVintageous.nv.plugin import ViOperatorDef
from NeoVintageous.nv.plugin import VISUAL
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
        self.input_parser = inputs.parser_def(
            command=inputs.one_char,
            interactive_command=None,
            input_param=None,
            on_done=None,
            type=INPUT_IMMEDIATE
        )

    @property
    def accept_input(self):
        return self.inp == ''

    def accept(self, key):
        self._inp = key

        return True


@register(seq='co', modes=(NORMAL,))
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


def _context_previous(view, count):
    window = view.window()
    if window:
        window.run_command('sublime_linter_goto_error', {
            'direction': 'previous',
            'count': count
        })


def _context_next(view, count):
    window = view.window()
    if window:
        window.run_command('sublime_linter_goto_error', {
            'direction': 'next',
            'count': count
        })


def _move_down(view, count):
    for i in range(count):
        view.run_command('swap_line_down')


def _move_up(view, count):
    for i in range(count):
        view.run_command('swap_line_up')


def _blank_down(view, edit, count):
    end_point = view.size()
    new_sels = []
    for sel in view.sel():
        line = view.line(sel)
        new_sels.append(view.find('[^\\s]', line.begin()).begin())
        view.insert(
            edit,
            line.end() + 1 if line.end() < end_point else end_point,
            '\n' * count
        )

    if new_sels:
        view.sel().clear()
        view.sel().add_all(new_sels)


def _blank_up(view, edit, count):
    new_sels = []
    for sel in view.sel():
        line = view.line(sel)
        new_sels.append(view.find('[^\\s]', line.begin()).begin() + count)
        view.insert(
            edit,
            line.begin() - 1 if line.begin() > 0 else 0,
            '\n' * count
        )

    if new_sels:
        view.sel().clear()
        view.sel().add_all(new_sels)


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


def _set_value_option(view, key, on_value, off_value, flag=None):
    settings = view.settings()
    value = settings.get(key)

    if flag is None:
        settings.set(key, off_value if value == on_value else on_value)
    elif flag:
        if value != on_value:
            settings.set(key, on_value)
    else:
        if value != off_value:
            settings.set(key, off_value)


def _list_option(view, flag=None):
    # TODO [enhancement] Add option to set default for "off". i.e. instead of
    # toggling between "all" (on) and "selection" (off), which is the current
    # behaviour, toggle between "all" (on) and whatever the user default for
    # "off" is. For example the user might have "off" set to "none" or
    # "selection" (the default in sublime). "selection" means that whitespace
    # characters are visible in selected text, "none" means whitespace
    # characters are never visible.
    _set_value_option(view, 'draw_white_space', 'all', 'selection', flag)


def _menu_option(view, flag=None):
    window = view.window()
    is_visible = window.is_menu_visible()
    if flag is None:
        window.set_menu_visible(not is_visible)
    elif flag:
        if not is_visible:
            window.set_menu_visible(True)
    else:
        if is_visible:
            window.set_menu_visible(False)


def _minimap_option(view, flag=None):
    window = view.window()
    is_visible = window.is_minimap_visible()
    if flag is None:
        window.set_minimap_visible(not is_visible)
    elif flag:
        if not is_visible:
            window.set_minimap_visible(True)
    else:
        if is_visible:
            window.set_minimap_visible(False)


def _sidebar_option(view, flag=None):
    window = view.window()
    is_visible = window.is_sidebar_visible()
    if flag is None:
        window.set_sidebar_visible(not is_visible)
    elif flag:
        if not is_visible:
            window.set_sidebar_visible(True)
    else:
        if is_visible:
            window.set_sidebar_visible(False)


def _statusbar_option(view, flag=None):
    window = view.window()
    is_visible = window.is_status_bar_visible()
    if flag is None:
        window.set_status_bar_visible(not is_visible)
    elif flag:
        if not is_visible:
            window.set_status_bar_visible(True)
    else:
        if is_visible:
            window.set_status_bar_visible(False)


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
    'hlsearch': None,
    'ignorecase': None,
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
    'e': 'statusbar',  # non standard i.e. not in the original Unimpaired plugin
    'd': 'diff',
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
    else:
        option(view, value)


class _nv_unimpaired_command(TextCommand):
    def run(self, edit, action, mode=None, count=1, **kwargs):
        if action == 'move_down':
            # Exchange the current line with [count] lines below it
            _move_down(self.view, count)
        elif action == 'move_up':
            # Exchange the current line with [count] lines above it
            _move_up(self.view, count)
        elif action == 'blank_down':
            # Add [count] blank lines below the cursor
            _blank_down(self.view, edit, count)
        elif action == 'blank_up':
            # Add [count] blank lines above the cursor
            _blank_up(self.view, edit, count)
        elif action in ('bnext', 'bprevious', 'bfirst', 'blast'):
            window_buffer_control(self.view.window(), action[1:], count=count)
        elif action in ('tabnext', 'tabprevious', 'tabfirst', 'tablast'):
            window_tab_control(self.view.window(), action[3:], count=count)
        elif action == 'context_next':
            # Go to the next [count]  SCM conflict marker or diff/patch hunk
            _context_next(self.view, count)
        elif action == 'context_previous':
            # Go to the previous [count] SCM conflict marker or diff/patch hunk
            _context_previous(self.view, count)
        elif action == 'toggle_option':
            _toggle_option(self.view, kwargs.get('value'))
        elif action == 'enable_option':
            _toggle_option(self.view, kwargs.get('value'), True)
        elif action == 'disable_option':
            _toggle_option(self.view, kwargs.get('value'), False)
        else:
            raise ValueError('unknown action')
