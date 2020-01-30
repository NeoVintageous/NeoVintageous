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

import re

from sublime import load_settings
from sublime import save_settings


# There's no Sublime API to set a window status.
# https://github.com/SublimeTextIssues/Core/issues/627
def set_window_status(window, key: str, value) -> None:
    for view in window.views():
        view.set_status(key, value)


# There's no Sublime API to erase a window status.
# https://github.com/SublimeTextIssues/Core/issues/627
def erase_window_status(window, key: str) -> None:
    for view in window.views():
        view.erase_status(key)


# A future compatable regular expression special character escaper. In Python
# 3.7 only characters that have special meaning in regex patterns are escaped.
def re_escape(pattern: str):
    return re.escape(pattern).replace(
        '\\<', '<').replace(
        '\\>', '>')


# There's no Sublime API to show a corrections select list. The workaround is to
# mimic the mouse right button click which opens a corrections context menu.
# See: https://github.com/SublimeTextIssues/Core/issues/2539.
def spell_select(view) -> None:
    x, y = view.text_to_window(view.sel()[0].b)
    view.run_command('context_menu', {'event': {'button': 2, 'x': x, 'y': y}})


def spell_add(view, word: str) -> None:
    view.run_command('add_word', {'word': word})


# There's no Sublime API to remove words from the added_words list.
# See: https://github.com/SublimeTextIssues/Core/issues/2539.
def spell_undo(word: str) -> None:
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
def view_find(view, pattern: str, start_pt: int, flags: int = 0):
    match = view.find(pattern, start_pt, flags)
    if match is None or match.b == -1:
        return None

    return match


# There's no Sublime API to find patterns in reverse direction.
# See: https://github.com/SublimeTextIssues/Core/issues/245.
def view_rfind_all(view, pattern: str, start_pt: int, flags: int = 0):
    matches = view.find_all(pattern)
    for region in matches:
        if region.b > start_pt:
            return reversed(matches[:matches.index(region)])

    return reversed(matches)


# There's no Sublime API to find a pattern in reverse direction.
# See: https://github.com/SublimeTextIssues/Core/issues/245.
def view_rfind(view, pattern: str, start_pt: int, flags: int = 0):
    matches = view_rfind_all(view, pattern, start_pt, flags)
    if matches:
        try:
            return next(matches)
        except StopIteration:
            pass


# There's no Sublime API to find a pattern within a start-end range.
# Note that this returns zero-length matches. Also see view_find().
# Returns None if nothing is found instead of returning Region(-1).
# See: https://forum.sublimetext.com/t/find-pattern-returns-1-1-instead-of-none/43866.
# See: https://github.com/SublimeTextIssues/Core/issues/534.
def view_find_in_range(view, pattern: str, pos: int, endpos: int, flags: int = 0):
    match = view_find(view, pattern, pos, flags)
    if match is not None and match.b <= endpos:
        return match


# There's no Sublime API to find all matching pattern within a range.
# Note that this returns zero-length matches. Also see view_find().
# Returns None if nothing is found instead of returning Region(-1).
# See: https://forum.sublimetext.com/t/find-pattern-returns-1-1-instead-of-none/43866.
# See: https://github.com/SublimeTextIssues/Core/issues/534.
# TODO Refactor to generator
def view_find_all_in_range(view, pattern: str, pos: int, endpos: int, flags: int = 0):
    matches = []
    while pos <= endpos:
        match = view.find(pattern, pos, flags)
        if match is None or match.b == -1:
            break

        pos = match.b
        if match.size() == 0:
            pos += 1

        if match.b <= endpos:
            matches.append(match)

    return matches


# Polyfill to work around bug in internal APIs.
# See: https://github.com/SublimeTextIssues/Core/issues/2879.
def view_indentation_level(view, pt: int):
    return view.indentation_level(pt)


# Polyfill to allow specifying an inclusive flag to include or exclude leading
# and trailing whitespace. By default excludes leading and trailing whitespace.
def view_indented_region(view, pt: int, inclusive: bool = False):
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


# Polyfill fix for Sublime Text 4. In Sublime Text 4 split_by_newlines includes
# full lines, previously the lines were constrianed to given region start and
# end points. See https://github.com/NeoVintageous/NeoVintageous/issues/647.
def split_by_newlines(view, region) -> list:
    regions = view.split_by_newlines(region)

    if len(regions) > 0:
        regions[0].a = min(region.a, region.b)

    return regions
