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

from sublime import load_settings
from sublime import save_settings


def get_setting(view, name, default=None):
    return view.settings().get('vintageous_%s' % name, default)


def set_setting(view, name, value):
    view.settings().set('vintageous_%s' % name)


def reset_setting(view, name):
    view.settings().erase('vintageous_%s' % name)


# DEPRECATED Refactor and use get_setting() instead
def get_setting_neo(view, name):
    return view.settings().get('neovintageous_%s' % name)


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
