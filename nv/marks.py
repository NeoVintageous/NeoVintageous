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

from collections import OrderedDict
from string import ascii_letters

from sublime import HIDDEN
from sublime import PERSISTENT
from sublime import Region

from NeoVintageous.nv.jumplist import jumplist_back
from NeoVintageous.nv.session import get_session_value
from NeoVintageous.nv.settings import get_setting
from NeoVintageous.nv.utils import get_insertion_point_at_b


def set_mark(view, name: str) -> None:
    if not _is_writable(name):
        raise KeyError()

    if name.isupper():
        if not view.file_name():
            return

        _get_session_marks()[name] = view.file_name()

    regions = [Region(get_insertion_point_at_b(view.sel()[0]))]

    view.add_regions(
        _get_key(name),
        regions,
        flags=HIDDEN | PERSISTENT,
        scope='region.cyanish neovintageous_mark',
        icon=_get_icon(view, name))


def _get_icon(view, name: str) -> str:
    if not get_setting(view, 'show_marks_in_gutter'):
        return ''

    return 'Packages/NeoVintageous/res/icons/%s_%s.png' % (
        'lower' if name.islower() else 'upper',
        name.lower())


def get_mark(view, name: str):
    if not _is_readable(name):
        raise KeyError()

    if name in ('\'', '`'):
        marks_view, marks = jumplist_back(view)
        if len(marks) > 0:
            if marks_view != view:
                return marks_view, marks[0]

            return marks[0]
    else:
        if name.isupper():
            view = _get_uppercase_mark_view(view, name)
            if not view:
                return

        marks = _get_regions(view, name)
        if marks:
            if name.isupper():
                return view, marks[0]

            return marks[0]


def get_marks(view) -> OrderedDict:
    marks = OrderedDict()
    for name in ascii_letters:
        mark = get_mark(view, name)
        if mark is None:
            continue

        if isinstance(mark, tuple):
            view, mark = mark

        marks[name] = _get_mark_info(view, mark)

    return marks


def _get_mark_info(view, region: Region) -> dict:
    line_number, col = view.rowcol(region.b)
    line_number += 1

    if view.file_name():
        file_or_text = view.file_name()
    else:
        file_or_text = view.substr(view.line(region.b))

    return {
        'line_number': line_number,
        'col': col,
        'file_or_text': file_or_text
    }


def _is_writable(name: str) -> bool:
    return name in ascii_letters


def _is_readable(name: str) -> bool:
    return name in ascii_letters + '\'`'


def _get_key(name: str) -> str:
    return '_nv_mark' + name


def _get_regions(view, name: str) -> list:
    return view.get_regions(_get_key(name))


def _get_session_marks() -> dict:
    return get_session_value('marks', {})


def _get_uppercase_mark_view(view, name: str):
    try:
        file_name = _get_session_marks()[name]
    except KeyError:
        return

    window = view.window()
    if not window:
        return

    return window.find_open_file(file_name)
