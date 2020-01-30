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

from sublime import CLASS_LINE_END
from sublime import CLASS_LINE_START
from sublime import CLASS_PUNCTUATION_END
from sublime import CLASS_PUNCTUATION_START
from sublime import CLASS_WORD_END
from sublime import CLASS_WORD_START
from sublime import Region

from NeoVintageous.nv.utils import last_row
from NeoVintageous.nv.utils import next_non_blank
from NeoVintageous.nv.utils import row_at


_WORD_PATTERN = re.compile('\\w')
# Places at which regular words start (for Vim).
_CLASS_VI_WORD_START = CLASS_WORD_START | CLASS_PUNCTUATION_START | CLASS_LINE_START
# Places at which *sometimes* words start. Called 'internal' because it's a
# notion Vim has; not obvious.
_CLASS_VI_INTERNAL_WORD_START = CLASS_WORD_START | CLASS_PUNCTUATION_START | CLASS_LINE_END
_CLASS_VI_WORD_END = CLASS_WORD_END | CLASS_PUNCTUATION_END
_CLASS_VI_INTERNAL_WORD_END = CLASS_WORD_END | CLASS_PUNCTUATION_END


def at_eol(view, pt: int) -> bool:
    return (view.classify(pt) & CLASS_LINE_END) == CLASS_LINE_END


def at_punctuation(view, pt: int) -> bool:
    is_at_eol = at_eol(view, pt)
    is_at_word = at_word(view, pt)
    is_white_space = view.substr(pt).isspace()
    is_at_eof = pt == view.size()

    return not any((is_at_eol, is_at_word, is_white_space, is_at_eof))


def at_word_start(view, pt: int) -> bool:
    return (view.classify(pt) & CLASS_WORD_START) == CLASS_WORD_START


def at_word_end(view, pt: int) -> bool:
    return (view.classify(pt) & CLASS_WORD_END) == CLASS_WORD_END


def at_punctuation_end(view, pt: int) -> bool:
    return (view.classify(pt) & CLASS_PUNCTUATION_END) == CLASS_PUNCTUATION_END


def at_word(view, pt: int):
    return at_word_start(view, pt) or _WORD_PATTERN.match(view.substr(pt))


def skip_word(view, pt: int) -> int:
    while True:
        if at_punctuation(view, pt):
            pt = view.find_by_class(pt, forward=True, classes=CLASS_PUNCTUATION_END)
        elif at_word(view, pt):
            pt = view.find_by_class(pt, forward=True, classes=CLASS_WORD_END)
        else:
            break

    return pt


def next_word_start(view, start: int, internal: bool = False) -> int:
    classes = _CLASS_VI_WORD_START if not internal else _CLASS_VI_INTERNAL_WORD_START
    pt = view.find_by_class(start, forward=True, classes=classes)
    if internal and at_eol(view, pt):
        # Unreachable?
        return pt

    return pt


def next_big_word_start(view, start: int, internal: bool = False) -> int:
    classes = _CLASS_VI_WORD_START if not internal else _CLASS_VI_INTERNAL_WORD_START
    pt = skip_word(view, start)
    seps = ''
    if internal and at_eol(view, pt):
        return pt

    pt = view.find_by_class(pt, forward=True, classes=classes, separators=seps)

    return pt


def next_word_end(view, start: int, internal: bool = False) -> int:
    classes = _CLASS_VI_WORD_END if not internal else _CLASS_VI_INTERNAL_WORD_END
    pt = view.find_by_class(start, forward=True, classes=classes)
    if internal and at_eol(view, pt):
        # Unreachable?
        return pt

    return pt


def word_starts(view, start: int, count: int = 1, internal: bool = False) -> int:
    assert start >= 0
    assert count > 0

    pt = start
    for i in range(count):
        # On the last motion iteration, we must do some special stuff if we are still on the
        # starting line of the motion.
        if (internal and (i == count - 1) and (view.line(start) == view.line(pt))):
            if view.substr(pt) == '\n':
                return pt + 1
            return next_word_start(view, pt, internal=True)

        pt = next_word_start(view, pt)
        if not internal or (i != count - 1):
            pt = next_non_blank(view, pt)
            while not (view.size() == pt or view.line(pt).empty() or view.substr(view.line(pt)).strip()):
                pt = next_word_start(view, pt)
                pt = next_non_blank(view, pt)

    if (internal and (view.line(start) != view.line(pt)) and (start != view.line(start).a and not view.substr(view.line(pt - 1)).isspace()) and at_eol(view, pt - 1)):  # FIXME # noqa: E501
        pt -= 1

    return pt


def big_word_starts(view, start: int, count: int = 1, internal: bool = False) -> int:
    assert start >= 0
    assert count > 0

    pt = start
    for i in range(count):
        if internal and i == count - 1 and view.line(start) == view.line(pt):
            if view.substr(pt) == '\n':
                return pt + 1
            return next_big_word_start(view, pt, internal=True)

        pt = next_big_word_start(view, pt)
        if not internal or i != count - 1:
            pt = next_non_blank(view, pt)
            while not (view.size() == pt or
                       view.line(pt).empty() or
                       view.substr(view.line(pt)).strip()):
                pt = next_big_word_start(view, pt)
                pt = next_non_blank(view, pt)

    if (internal and (view.line(start) != view.line(pt)) and (start != view.line(start).a and not view.substr(view.line(pt - 1)).isspace()) and at_eol(view, pt - 1)):  # FIXME # noqa: E501
        pt -= 1

    return pt


def word_ends(view, start: int, count: int = 1, big: bool = False) -> int:
    assert start >= 0 and count > 0, 'bad call'

    pt = start
    if not view.substr(start).isspace():
        pt = start + 1

    for i in range(count):
        if big:
            while True:
                pt = next_word_end(view, pt)
                if pt >= view.size() or view.substr(pt).isspace():
                    if pt > view.size():
                        pt = view.size()
                    break
        else:
            pt = next_word_end(view, pt)

    return pt


def big_word_ends(view, start: int, count: int = 1) -> int:
    return word_ends(view, start, count, big=True)


def lines(view, s: Region, count: int = 1) -> Region:
    """
    Return a region spanning @count full lines.

    Assumes we're operating in INTERNAL_NORMAL mode.

    @view
      Target view.
    @s
      Selection in @view taken as starting point.
    @count
      Number of lines to include in returned region.
    """
    # assumes INTERNAL_NORMAL mode.
    a = view.line(s.b).a
    b = view.text_point(row_at(view, s.b) + (count - 1), 0)
    # make sure we remove the last line if needed
    if ((row_at(view, b) == last_row(view)) and (view.substr(a - 1) == '\n')):
        a -= 1

    return Region(a, view.full_line(b).b)


def inner_lines(view, s: Region, count: int = 1) -> Region:
    """
    Return a region spanning @count inner lines.

    Inner lines are lines excluding leading/trailing whitespace at outer ends.

    Assumes we're operating in INTERNAL_NORMAL mode.

    @view
      Target view.
    @s
      Selection in @view taken as starting point.
    @count
      Number of lines to include in returned region.
    """
    end = view.text_point(row_at(view, s.b) + (count - 1), 0)
    begin = view.line(s.b).a
    begin = next_non_blank(view, begin)

    return Region(begin, view.line(end).b)


def next_paragraph_start(view, pt: int, count: int = 1) -> int:
    skip_empty = count > 1

    if row_at(view, pt) == last_row(view):
        if not view.line(view.size()).empty():
            return view.size() - 1

        return view.size()

    # skip empty rows before moving for the first time
    current_row = row_at(view, pt)
    if (view.line(view.text_point(current_row + 1, 0)).empty() and view.line(pt).empty()):
        pt, _ = _next_non_empty_row(view, pt)

    for i in range(count):
        pt, eof = _next_empty_row(view, pt)
        if eof:
            if view.line(pt).empty():
                return pt

            return pt - 1

        if skip_empty and (i != (count - 1)):
            pt, eof = _next_non_empty_row(view, pt)
            if eof:
                if not view.line(pt).empty():
                    return pt - 1

                return pt

    return pt


def _next_empty_row(view, pt: int) -> tuple:
    r = row_at(view, pt)
    while True:
        r += 1
        pt = view.text_point(r, 0)
        if row_at(view, pt) == last_row(view):
            return view.size(), True

        if view.line(pt).empty():
            return pt, False


def _next_non_empty_row(view, pt: int) -> tuple:
    r = row_at(view, pt)
    while True:
        r += 1
        reg = view.line(view.text_point(r, 0))
        if r >= last_row(view):
            return view.size(), True

        if not reg.empty():
            return reg.a, False


def prev_paragraph_start(view, pt: int, count: int = 1, skip_empty: bool = True) -> int:
    # first row?
    if row_at(view, pt) == 0:
        return 0

    current_row = row_at(view, pt)
    if (view.line(view.text_point(current_row - 1, 0)).empty() and view.line(view.text_point(current_row, 0)).empty()):
        pt, bof = _prev_non_empty_row(view, pt)
        if bof:
            return 0

    for i in range(count):
        pt, bof = _prev_empty_row(view, pt)
        if bof:
            return 0

        if skip_empty and (count > 1) and (i != count - 1):
            pt, bof = _prev_non_empty_row(view, pt)
            if bof:
                return pt

    return view.text_point(row_at(view, pt), 0)


def _prev_empty_row(view, pt: int) -> tuple:
    r = row_at(view, pt)
    while True:
        r -= 1
        if r == 0:
            return 0, True

        pt = view.text_point(r, 0)
        if view.line(pt).empty():
            return pt, False


def _prev_non_empty_row(view, pt: int) -> tuple:
    r = row_at(view, pt)
    while True:
        r -= 1
        reg = view.line(view.text_point(r, 0))
        # stop if we hit the first row
        if r <= 0:
            return 0, True

        if not reg.empty():
            return reg.a, False
