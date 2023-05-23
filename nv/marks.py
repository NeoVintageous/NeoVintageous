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

from string import ascii_letters

from sublime import Region

from NeoVintageous.nv.jumplist import jumplist_back
from NeoVintageous.nv.utils import get_insertion_point_at_b


def set_mark(view, name: str) -> None:
    if not _is_valid(name):
        raise KeyError()

    pt = get_insertion_point_at_b(view.sel()[0])
    view.add_regions(_get_key(name), [Region(pt)])


def get_mark(view, name: str):
    if not _is_valid(name):
        raise KeyError()

    # Returns None, list[Region], or tuple[sublime.View, list[Region]]
    if name in ('\'', '`'):
        marks_view, marks = jumplist_back(view)
        if len(marks) > 0:
            if marks_view != view:
                return marks_view, marks[0]

            return marks[0]
    else:
        marks = _get_regions(view, name)
        if marks:
            return marks[0]


def _is_valid(name: str) -> bool:
    return name in ascii_letters


def _get_key(name: str) -> str:
    return '_nv_mark' + name


def _get_regions(view, name: str) -> list:
    return view.get_regions(_get_key(name))
