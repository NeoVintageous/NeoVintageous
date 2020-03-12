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

import os
import sys

from sublime import active_window

from NeoVintageous.nv.settings import get_setting


_session = {}  # type: dict


class Option():

    def __init__(self, name: str, default):
        self._name = name
        self._default = default

    def _filter_validate(self, value):
        return value

    def set(self, view, value):
        self._set(view, self._filter_validate(value))

    def _set(self, view, value):
        _session[self._name] = value

    def get(self, view):
        return self._get(view)

    def _get(self, view):
        try:
            value = _session[self._name]
        except KeyError:
            # DEPRECATED This is for backwards compatability only. All options
            # should be set by the .neovintageousrc configuration file.
            # See https://github.com/NeoVintageous/NeoVintageous/issues/404.
            value = get_setting(view, self._name, self._default)

        return value


class BooleanOption(Option):

    def _filter_validate(self, value):
        return bool(value)


class NumberOption(Option):

    def _filter_validate(self, value):
        return int(value)


class StringOption(Option):

    def __init__(self, name: str, default, select=()):
        super().__init__(name, default)
        self._select = select

    def _filter_validate(self, value):
        value = str(value)
        if self._select and value not in self._select:
            raise ValueError('invalid argument')

        return value


class BooleanViewOption(BooleanOption):

    def __init__(self, name: str, on=True, off=False):
        super().__init__(name, None)
        self._on = on
        self._off = off

    def _set(self, view, value):
        settings = view.settings()
        current_value = settings.get(self._name)

        # Note that the intent here is to avoid Sublime triggering a "setting
        # changed" event. Sublime triggers the event any time the settings set()
        # method is called, even if the actual value itself has not changed.
        if value:
            if current_value != self._on:
                settings.set(self._name, self._on)
        else:
            if current_value != self._off:
                settings.set(self._name, self._off)

    def _get(self, view):
        value = view.settings().get(self._name)

        if value == self._on:
            value = True
        elif value == self._off:
            value = False

        return value


class NumberViewOption(NumberOption):

    def __init__(self, name: str):
        super().__init__(name, None)

    def _set(self, view, value):
        settings = view.settings()
        current_value = settings.get(self._name)
        if value != current_value:
            settings.set(self._name, value)

    def _get(self, view):
        return view.settings().get(self._name)


def get_window_ui_element_visible(name: str, window=None) -> None:
    return getattr(active_window() if window is None else window, 'is_%s_visible' % name)()


def set_window_ui_element_visible(name: str, flag: bool = None, window=None) -> None:
    # The option is toggled when flag is None.
    window = active_window() if window is None else window
    is_visible = getattr(window, 'is_%s_visible' % name)()
    if flag is None:
        getattr(window, 'set_%s_visible' % name)(not is_visible)
    elif flag:
        if not is_visible:
            getattr(window, 'set_%s_visible' % name)(True)
    else:
        if is_visible:
            getattr(window, 'set_%s_visible' % name)(False)


class BooleanIsVisibleOption(BooleanOption):

    def _set(self, view, value):
        set_window_ui_element_visible(self._name, value, view.window() if view else None)

    def _get(self, view):
        return get_window_ui_element_visible(self._name, view.window() if view else None)


def _get_default_shell() -> str:
    if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
        return os.environ.get('SHELL', 'sh')
    elif sys.platform.startswith('win'):
        return 'cmd.exe'

    return ''


_options = {
    'autoindent': BooleanViewOption('auto_indent'),
    'belloff': StringOption('belloff', '', select=('', 'all')),
    'expandtabs': BooleanViewOption('translate_tabs_to_spaces', on=False, off=True),
    'hlsearch': BooleanOption('hlsearch', True),
    'ignorecase': BooleanOption('ignorecase', False),
    'incsearch': BooleanOption('incsearch', True),
    'list': BooleanViewOption('draw_white_space', on='all', off='selection'),
    'magic': BooleanOption('magic', True),
    'menu': BooleanIsVisibleOption('menu', True),  # {not in Vim}
    'minimap': BooleanIsVisibleOption('minimap', True),  # {not in Vim}
    'modeline': BooleanOption('modeline', True),
    'modelines': NumberOption('modelines', 5),
    'number': BooleanViewOption('line_numbers'),
    'scrolloff': NumberOption('scrolloff', 5),
    'shell': StringOption('shell', _get_default_shell()),
    'sidebar': BooleanIsVisibleOption('sidebar', True),  # {not in Vim}
    'sidescrolloff': NumberOption('sidescrolloff', 5),
    'smartcase': BooleanOption('smartcase', False),
    'spell': BooleanViewOption('spell_check'),
    'statusbar': BooleanIsVisibleOption('status_bar', True),  # {not in Vim}
    'tabstop': NumberViewOption('tab_size'),
    'textwidth': NumberViewOption('wrap_width'),
    'winaltkeys': StringOption('winaltkeys', 'menu', select=('no', 'yes', 'menu')),
    'wrap': BooleanViewOption('word_wrap'),
    'wrapscan': BooleanOption('wrapscan', True),
}

_OPTION_ALIASES = {
    'ai': 'autoindent',
    'bo': 'belloff',
    'et': 'expandtabs',
    'hls': 'hlsearch',
    'ic': 'ignorecase',
    'is': 'incsearch',
    'ml': 'modeline',
    'mls': 'modelines',
    'nu': 'number',
    'scs': 'smartcase',
    'siso': 'sidescrolloff',
    'so': 'scrolloff',
    'ts': 'tabstop',
    'tw': 'textwidth',
    'wak': 'winaltkeys',
    'ws': 'wrapscan',
}


def get_option_completions(prefix: str = ''):
    for name, option in sorted(_options.items()):
        if name.startswith(prefix):
            yield name

        if isinstance(option, BooleanOption):
            name = 'no' + name
            if name.startswith(prefix):
                yield name


def _resolve_aliases(name: str) -> str:
    try:
        return _OPTION_ALIASES[name]
    except KeyError:
        return name


def get_option(view, name: str):
    name = _resolve_aliases(name)
    option = _options[name]
    value = option.get(view)

    return value


def set_option_local(view, name: str, value=None) -> None:
    set_option(view, name, value)


def set_option(view, name: str, value=None) -> None:
    name = _resolve_aliases(name)

    try:
        _options[name].set(view, True if value is None else value)
    except KeyError:
        # If no option was found for name, try the leading "no" variant.
        if name.startswith('no'):
            name = _resolve_aliases(name[2:])

            try:
                _options[name].set(view, False if value is None else value)

                return
            except KeyError:
                # Intentional fallthrough because if there's a key error at this
                # point then it will be the key without the leading "no" part.
                pass

        raise


def toggle_option(view, name: str) -> None:
    value = get_option(view, name)
    if not isinstance(value, bool):
        raise ValueError('option cannot be toggled')

    set_option(view, name, not value)
