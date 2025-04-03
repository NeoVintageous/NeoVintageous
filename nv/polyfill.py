# Copyright (C) 2018-2023 The NeoVintageous Team (NeoVintageous).
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

from contextlib import contextmanager
import os
import re
import stat
import sys

from sublime import Region
from sublime import active_window as _active_window
from sublime import load_settings
from sublime import save_settings
from sublime import status_message as _status_message
from sublime import version
from sublime import windows as _windows


def _is_py38() -> bool:
    return sys.version_info >= (3, 8)


def status_message(msg: str, *args: str) -> None:
    _status_message(_format_message(msg, *args))


def _format_message(msg: str, *args) -> str:
    if args:
        msg = msg % args

    return msg


# There is no API to set a window status.
# https://github.com/SublimeTextIssues/Core/issues/627
def set_window_status(window, key: str, value) -> None:
    for view in window.views():
        view.set_status(key, value)


# There is no API to erase a window status.
# https://github.com/SublimeTextIssues/Core/issues/627
def erase_window_status(window, key: str) -> None:
    for view in window.views():
        view.erase_status(key)


# There is no API to set an application status.
# https://github.com/SublimeTextIssues/Core/issues/627
def set_status(key: str, value) -> None:
    for window in _windows():
        for view in window.views():
            view.set_status(key, value)


# There is no API to erase an application status.
# https://github.com/SublimeTextIssues/Core/issues/627
def erase_status(key: str) -> None:
    for window in _windows():
        for view in window.views():
            view.erase_status(key)


def run_window_command(cmd: str, args: dict = None, window=None) -> None:
    if not window:
        window = _active_window()

    window.run_command(cmd, args)


def has_dirty_buffers(window) -> bool:
    for v in window.views():
        if v.is_dirty():
            return True

    return False


def has_newline_at_eof(view) -> bool:
    return view.substr(view.size() - 1) == '\n'


def set_selection(view, sel) -> None:
    view.sel().clear()
    if isinstance(sel, list):
        view.sel().add_all(sel)
    else:
        view.sel().add(sel)


def is_view_read_only(view) -> bool:
    return view.is_read_only() or is_file_read_only(view.file_name())


def is_file_read_only(file_name: str) -> bool:
    if file_name:
        try:
            return (stat.S_IMODE(os.stat(file_name).st_mode) & stat.S_IWUSR != stat.S_IWUSR)
        except FileNotFoundError:
            return False

    return False


# A future compatable regular expression special character escaper. In Python
# 3.7 only characters that have special meaning in regex patterns are escaped.
if _is_py38():
    def re_escape(pattern: str):
        return re.escape(pattern)
else:
    def re_escape(pattern: str):
        return re.escape(pattern).replace(
            '\\<', '<').replace(
            '\\>', '>').replace(
            '\\\'', '\'').replace(
            '\\`', '`')


def merge_dicts(a: dict, b: dict) -> dict:
    x = a.copy()
    x.update(b)

    return x


# There's no Sublime API to show a corrections select list. The workaround is to
# mimic the mouse right button click which opens a corrections context menu.
# @see https://github.com/SublimeTextIssues/Core/issues/2539
def spell_select(view) -> None:
    x, y = view.text_to_window(view.sel()[0].b)
    view.run_command('context_menu', {'event': {'button': 2, 'x': x, 'y': y}})


def spell_add(view, word: str) -> None:
    view.run_command('add_word', {'word': word})


# There's no Sublime API to remove words from the added_words list.
# @see https://github.com/SublimeTextIssues/Core/issues/2539
def spell_undo(word: str) -> None:
    preferences = load_settings('Preferences.sublime-settings')
    added_words = preferences.get('added_words', [])

    try:
        if isinstance(added_words, list):
            added_words.remove(word)
        else:
            added_words = []
    except ValueError:
        return

    added_words.sort()
    preferences.set('added_words', added_words)
    save_settings('Preferences.sublime-settings')


# Returns the first region matching the pattern, starting from start_point, or
# None if no position in the string matches the pattern; note that this is
# different from finding a zero-length match at some point in the string.
#
# The optional flags parameter may be sublime.LITERAL, sublime.IGNORECASE, or
# the two ORed together.
#
# @see https://forum.sublimetext.com/t/find-pattern-returns-1-1-instead-of-none/43866
# @see https://github.com/SublimeTextIssues/Core/issues/534
def view_find(view, pattern: str, start_pt: int, flags: int = 0):
    match = view.find(pattern, start_pt, flags)
    if match is None or match.b == -1:
        return None

    return match


# There's no Sublime API to find patterns in reverse direction.
# @see https://github.com/SublimeTextIssues/Core/issues/245
def view_rfind_all(view, pattern: str, start_pt: int, flags: int = 0):
    matches = view.find_all(pattern, flags)
    for region in matches:
        if region.b > start_pt:
            return reversed(matches[:matches.index(region)])

    return reversed(matches)


# There's no Sublime API to find a pattern in reverse direction.
# @see https://github.com/SublimeTextIssues/Core/issues/245
def view_rfind(view, pattern: str, start_pt: int, flags: int = 0):
    matches = view_rfind_all(view, pattern, start_pt, flags)
    if matches:
        try:
            return next(matches)
        except StopIteration:
            pass


# Returns the first region matching the pattern, between indexes pos and endpos,
# or None if no position in the string matches the pattern; note that this is
# different from finding a zero-length match at some point in the string.
#
# The parameter pos is an index in the string where the search is to start.
#
# The parameter endpos limits how far the string will be searched; it will be as
# if the string is endpos characters long, so only the characters from pos to
# endpos - 1 will be searched for a match.
#
# The optional flags parameter may be sublime.LITERAL, sublime.IGNORECASE, or
# the two ORed together.
#
# @see https://forum.sublimetext.com/t/find-pattern-returns-1-1-instead-of-none/43866
# @see https://github.com/sublimehq/sublime_text/issues/2797
# @see https://github.com/SublimeTextIssues/Core/issues/534
def view_find_in_range(view, pattern: str, pos: int, endpos: int, flags: int = 0):
    match = view_find(view, pattern, pos, flags)
    if match is not None and match.b <= endpos:
        return match


# There's no Sublime API to find all matching pattern within a range.
# Note that this returns zero-length matches. Also see view_find().
# Returns None if nothing is found instead of returning Region(-1).
# @see https://forum.sublimetext.com/t/find-pattern-returns-1-1-instead-of-none/43866
# @see https://github.com/sublimehq/sublime_text/issues/2797
# @see https://github.com/SublimeTextIssues/Core/issues/534
# @todo Refactor to generator
def view_find_all_in_range(view, pattern: str, pos: int, endpos: int, flags: int = 0) -> list:
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
# @see https://github.com/SublimeTextIssues/Core/issues/2879
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


def view_to_region(view) -> Region:
    return Region(0, view.size())


def view_to_str(view) -> str:
    return view.substr(view_to_region(view))


# In ST4 split_by_newlines includes full lines, previously the lines were
# constrained to given region start and end points. This function emulates the
# previous behaviour and constrains to the given region start and end points.
# @see https://github.com/NeoVintageous/NeoVintageous/issues/647
def split_by_newlines(view, region: Region) -> list:
    regions = view.split_by_newlines(region)

    if len(regions) > 0:
        regions[0].a = min(region.a, region.b)

    return regions


def toggle_side_bar(window) -> None:
    window.run_command('toggle_side_bar')

    # Ensure that the focus is put on the side bar if it's now visible,
    # otherwise ensure that the focus returns to active group view.
    if window.is_sidebar_visible():
        window.run_command('focus_side_bar')
    else:
        window.focus_group(window.active_group())


def reveal_side_bar(window) -> None:
    if not window.is_sidebar_visible():
        toggle_side_bar(window)

    window.run_command('reveal_side_bar')
    window.run_command('focus_side_bar')


@contextmanager
def save_preferences():
    yield load_settings('Preferences.sublime-settings')
    save_settings('Preferences.sublime-settings')


def toggle_preference(name: str) -> None:
    with save_preferences() as preferences:
        preferences.set(name, not preferences.get(name))


if int(version()) >= 4081:
    from sublime import find_syntax_for_file

    def reload_syntax(view) -> None:
        view.assign_syntax(find_syntax_for_file(view.file_name()))
else:
    def reload_syntax(view) -> None:
        pass


def goto_definition_side_by_side(window) -> None:
    window.run_command('goto_definition', {'side_by_side': True})
    window.run_command('carry_file_to_pane', {'direction': 'right'})


def truncate(string: str, truncate_at: int) -> str:
    if len(string) > truncate_at:
        return string[0:truncate_at] + ' ...'

    return string


def make_all_groups_same_size(window) -> None:
    return window.set_layout(_get_layout_groups_same_size(window.layout()))


def _get_layout_groups_same_size(layout: dict) -> dict:
    cell_count = len(layout['cells'])
    col_count = len(layout['cols'])
    row_count = len(layout['rows'])

    if col_count == 2 and row_count == 2:
        return layout

    if cell_count == 4 and col_count == 3 and row_count == 3:
        # Special case for 4-grid. Works around some complicated layout issues.
        return {
            'cells': [[0, 0, 1, 1], [1, 0, 2, 1], [0, 1, 1, 2], [1, 1, 2, 2]],
            'cols': [0.0, 0.5, 1.0],
            'rows': [0.0, 0.5, 1.0]
        }

    def equalise(count: int) -> list:
        size = round(1.0 / (count - 1), 2)
        vals = [0.0]
        for i in range(1, count - 1):
            vals.append(round(size * i, 2))
        vals.append(1.0)
        return vals

    if col_count > 2:
        layout['cols'] = equalise(col_count)

    if row_count > 2:
        layout['rows'] = equalise(row_count)

    return layout


def close_pane_if_empty(window) -> bool:
    views_in_group = window.views_in_group(window.active_group())
    if len(views_in_group) == 0:
        window.run_command('close_pane')
        return True

    return False
