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


# There's no Sublime API to set a window status.
# https://github.com/SublimeTextIssues/Core/issues/627
def set_window_status(window, key, value):
    for view in window.views():
        view.set_status(key, value)


# There's no Sublime API to erase a window status.
# https://github.com/SublimeTextIssues/Core/issues/627
def erase_window_status(window, key):
    for view in window.views():
        view.erase_status(key)


# There's no Sublime API to show a corrections select list. The workaround is to
# mimic the mouse right button click which opens a corrections context menu.
# See: https://github.com/SublimeTextIssues/Core/issues/2539.
def spell_select(view):
    x, y = view.text_to_window(view.sel()[0].b)
    view.run_command('context_menu', {'event': {'button': 2, 'x': x, 'y': y}})


def spell_add(view, word):
    view.run_command('add_word', {'word': word})


# There's no Sublime API to remove words from the added_words list.
# See: https://github.com/SublimeTextIssues/Core/issues/2539.
def spell_undo(word):
    preferences = load_settings('Preferences.sublime-settings')
    added_words = preferences.get('added_words', [])

    try:
        added_words.remove(word)
    except ValueError:
        return

    added_words.sort()
    preferences.set('added_words', added_words)
    save_settings('Preferences.sublime-settings')


# Polyfill to workaround Sublime's view.find() return value issues.
# Returns None if nothing is found instead of returning Region(-1).
# See: https://forum.sublimetext.com/t/find-pattern-returns-1-1-instead-of-none/43866.
# See: https://github.com/SublimeTextIssues/Core/issues/534.
def view_find(view, pattern, start_pt, flags=0):
    match = view.find(pattern, start_pt, flags)
    if match is None or match.b == -1:
        return None

    return match


# Polyfill to work around bug in internal APIs.
# See: https://github.com/SublimeTextIssues/Core/issues/2879.
def view_indentation_level(view, pt):
    return view.indentation_level(pt)


# Polyfill to allow specifying an inclusive flag to include or exclude leading
# and trailing whitespace. By default excludes leading and trailing whitespace.
def view_indented_region(view, pt, inclusive=False):
    indented_region = view.indented_region(pt)

    if not inclusive:
        ws = view_find(view, '\\s*', indented_region.begin())
        if ws is not None:
            indented_region.a = view.line(ws.b).a
    else:
        ws = view_find(view, '\\s*', indented_region.end())
        if ws is not None:
            indented_region.b = view.line(ws.b).a

    return indented_region
