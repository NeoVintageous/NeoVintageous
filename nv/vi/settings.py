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

from collections import defaultdict
from collections import namedtuple
import json
import os

from sublime import active_window
from sublime import load_settings
from sublime import save_settings

from NeoVintageous.nv.vim import DIRECTION_DOWN
from NeoVintageous.nv.vim import DIRECTION_UP

_vi_user_setting = namedtuple('vi_editor_setting', 'scope values default parser action negatable')

_WINDOW_SETTINGS = [
    'last_buffer_search'
]

_SCOPE_WINDOW = 1
_SCOPE_VIEW = 2
_SCOPE_VI_VIEW = 3
_SCOPE_VI_WINDOW = 4


def volatile(f):
    _VintageSettings._volatile_settings.append(f.__name__)

    return f


def destroy(view):
    try:
        del _VintageSettings._volatile[view.id()]
    except KeyError:
        pass


def _set_generic_view_setting(view, name, value, opt, globally=False):
    if opt.scope == _SCOPE_VI_VIEW:
        name = 'vintageous_' + name

    if opt.parser:
        value = opt.parser(value)

    if not globally or (opt.scope not in (_SCOPE_VI_VIEW, _SCOPE_VI_WINDOW)):
        view.settings().set(name, value)
    else:
        prefs = load_settings('Preferences.sublime-settings')
        prefs.set(name, value)
        save_settings('Preferences.sublime-settings')


def _set_auto_indent(view, name, value, opt, globally=False):
    prefs = load_settings('Preferences.sublime-settings')
    prefs.set('auto_indent', opt.parser(value))
    save_settings('Preferences.sublime-settings')


def _set_minimap(view, name, value, opt, globally=False):
    view.window().run_command('toggle_minimap')


def _set_sidebar(view, name, value, opt, globally=False):
    view.window().run_command('toggle_side_bar')


def _set_list(view, name, value, opt, globally=False):
    value = _opt_bool_parser(value)
    if value:
        view.settings().set('draw_white_space', 'all')
    else:
        view.settings().set('draw_white_space', 'selection')


def _opt_bool_parser(value):
    if value.lower() in ('false', 'true', '0', '1', 'yes', 'no'):
        if value.lower() in ('true', '1', 'yes'):
            return True
        return False


def _opt_rulers_parser(value):
    try:
        converted = json.loads(value)
        if isinstance(converted, list):
            return converted
        else:
            raise ValueError
    except ValueError:
        raise
    except TypeError:
        raise ValueError


_VI_OPTIONS = {
    'autoindent': _vi_user_setting(scope=_SCOPE_VI_VIEW, values=(True, False, '0', '1'), default=True, parser=_opt_bool_parser, action=_set_auto_indent, negatable=True),  # noqa: E501
    'hlsearch': _vi_user_setting(scope=_SCOPE_VI_VIEW, values=(True, False, '0', '1'), default=True, parser=_opt_bool_parser, action=_set_generic_view_setting, negatable=True),  # FIXME # noqa: E501
    'ignorecase': _vi_user_setting(scope=_SCOPE_VI_VIEW, values=(True, False, '0', '1'), default=False, parser=_opt_bool_parser, action=_set_generic_view_setting, negatable=True),  # FIXME # noqa: E501
    'incsearch': _vi_user_setting(scope=_SCOPE_VI_VIEW, values=(True, False, '0', '1'), default=True, parser=_opt_bool_parser, action=_set_generic_view_setting, negatable=True),  # FIXME # noqa: E501
    'list': _vi_user_setting(scope=_SCOPE_VI_VIEW, values=(True, False, '0', '1'), default=False, parser=None, action=_set_list, negatable=True),  # FIXME # noqa: E501
    'magic': _vi_user_setting(scope=_SCOPE_VI_VIEW, values=(True, False, '0', '1'), default=True, parser=_opt_bool_parser, action=_set_generic_view_setting, negatable=True),  # FIXME # noqa: E501
    'visualbell': _vi_user_setting(scope=_SCOPE_VI_WINDOW, values=(True, False, '0', '1'), default=True, parser=_opt_bool_parser, action=_set_generic_view_setting, negatable=True),  # FIXME # noqa: E501
    'rulers': _vi_user_setting(scope=_SCOPE_VIEW, values=None, default=[], parser=_opt_rulers_parser, action=_set_generic_view_setting, negatable=False),  # FIXME # noqa: E501
    'showminimap': _vi_user_setting(scope=_SCOPE_WINDOW, values=(True, False, '0', '1'), default=True, parser=None, action=_set_minimap, negatable=True),  # FIXME # noqa: E501
    'showsidebar': _vi_user_setting(scope=_SCOPE_WINDOW, values=(True, False, '0', '1'), default=True, parser=None, action=_set_sidebar, negatable=True),  # FIXME # noqa: E501
}


_VI_OPTION_ALIASES = {
    'ai': 'autoindent',
    'hls': 'hlsearch',
    'ic': 'ignorecase',
}


def _resolve_option_alias(name):
    if name in _VI_OPTION_ALIASES:
        return _VI_OPTION_ALIASES[name]

    return name


# For completions.
def iter_settings(prefix=''):
    if prefix.startswith('no'):
        for item in (x for (x, y) in _VI_OPTIONS.items() if y.negatable):
            if ('no' + item).startswith(prefix):
                yield 'no' + item
    else:
        for k in sorted(_VI_OPTIONS.keys()):
            if (prefix == '') or k.startswith(prefix):
                yield k


def set_local(view, name, value):
    name = _resolve_option_alias(name)

    try:
        opt = _VI_OPTIONS[name]
        if not value and opt.negatable:
            opt.action(view, name, '1', opt)
            return
        opt.action(view, name, value, opt)
    except KeyError:
        if name.startswith('no'):
            try:
                name = _resolve_option_alias(name[2:])
                opt = _VI_OPTIONS[name]
                if opt.negatable:
                    opt.action(view, name, '0', opt)

                return
            except KeyError:
                pass
        raise


def set_global(view, name, value):
    name = _resolve_option_alias(name)

    try:
        opt = _VI_OPTIONS[name]
        if not value and opt.negatable:
            opt.action(view, name, '1', opt, globally=True)
            return
        opt.action(view, name, value, opt, globally=True)
    except KeyError:
        if name.startswith('no'):
            try:
                name = _resolve_option_alias(name[2:])
                opt = _VI_OPTIONS[name]
                if opt.negatable:
                    opt.action(view, name, '0', opt, globally=True)

                return
            except KeyError:
                pass
        raise


_storage = {}  # type: dict


def get_cmdline_cwd():
    if 'cmdline_cwd' in _storage:
        return _storage['cmdline_cwd']

    window = active_window()
    if window:
        variables = window.extract_variables()
        if 'folder' in variables:
            return variables['folder']

    return os.getcwd()


def set_cmdline_cwd(path):
    _storage['cmdline_cwd'] = path


def get_visual_block_direction(view):
    settings = view.settings().get('vintage')

    return settings['visual_block_direction'] if 'visual_block_direction' in settings else None


def _is_valid_direction(direction):
    return direction in (DIRECTION_DOWN, DIRECTION_UP)


def set_visual_block_direction(view, direction):
    if not _is_valid_direction(direction):
        raise ValueError('invalid direction')

    visual_block_direction = get_visual_block_direction(view)
    if visual_block_direction != direction:
        settings = view.settings().get('vintage')
        settings['visual_block_direction'] = direction
        view.settings().set('vintage', settings)


def _toggle_preference(name):
    preferences = load_settings('Preferences.sublime-settings')
    value = preferences.get(name)
    preferences.set(name, not value)
    save_settings('Preferences.sublime-settings')


def toggle_ctrl_keys():
    _toggle_preference('vintageous_use_ctrl_keys')


def toggle_super_keys():
    _toggle_preference('vintageous_use_super_keys')


def toggle_side_bar(window):
    window.run_command('toggle_side_bar')

    if window.is_sidebar_visible():
        window.run_command('focus_side_bar')
    else:
        window.focus_group(window.active_group())


def _get_option(view, name):
    name = _resolve_option_alias(name)

    try:
        option_data = _VI_OPTIONS[name]
    except KeyError:
        raise KeyError('not a vi editor option')

    if option_data.scope == _SCOPE_WINDOW:
        value = view.window().settings().get('vintageous_' + name)
    else:
        value = view.settings().get('vintageous_' + name)

    return value if (value in option_data.values) else option_data.default


class _SublimeSettings():
    def __init__(self, container=None):
        self.settings = container.settings()

    def __getitem__(self, key):
        return self.settings.get(key)

    def __setitem__(self, key, value):
        self.settings.set(key, value)


class _VintageSettings():

    _volatile_settings = []  # type: list

    _volatile = defaultdict(dict)  # type: dict

    def __init__(self, view):
        self.view = view

        if view is not None:
            if not isinstance(view.settings().get('vintage'), dict):
                view.settings().set('vintage', dict())

            window = view.window()
            if window is not None and not isinstance(window.settings().get('vintage'), dict):
                window.settings().set('vintage', dict())

    def __getitem__(self, key):
        try:
            return _get_option(self.view, key)
        except KeyError:
            pass

        try:
            if key not in _WINDOW_SETTINGS:
                try:
                    return self._get_volatile(key)
                except KeyError:
                    value = self.view.settings().get('vintage').get(key)
            else:
                value = self.view.window().settings().get('vintage').get(key)

        except (KeyError, AttributeError):
            value = None

        return value

    def __setitem__(self, key, value):
        if key not in _WINDOW_SETTINGS:
            if key in _VintageSettings._volatile_settings:
                self._set_volatile(key, value)
                return
            setts, target = self.view.settings().get('vintage'), self.view
        else:
            setts, target = self.view.window().settings().get('vintage'), self.view.window()

        setts[key] = value
        target.settings().set('vintage', setts)

    def _get_volatile(self, key):
        try:
            return _VintageSettings._volatile[self.view.id()][key]
        except KeyError:
            raise KeyError('error accessing volatile key: %s' % key)

    def _set_volatile(self, key, value):
        try:
            _VintageSettings._volatile[self.view.id()][key] = value
        except KeyError:
            raise KeyError('error while setting key "%s" to value "%s"' % (key, value))


class SettingsManager():

    def __init__(self, view):
        self.window = _SublimeSettings(view.window())
        self.view = _SublimeSettings(view)
        self.vi = _VintageSettings(view)
