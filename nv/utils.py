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

from sublime import Region

from NeoVintageous.nv.vi.utils import next_non_blank
from NeoVintageous.nv.vi.utils import regions_transformer
from NeoVintageous.nv.vim import INTERNAL_NORMAL
from NeoVintageous.nv.vim import NORMAL


def extract_file_name(view):
    sel = view.sel()[0]
    line = view.substr(view.line(sel))
    pos = len(line) - len(line.strip()) + 1
    col = view.rowcol(sel.b)[1]

    if pos > col:
        return

    matches = re.findall('[^\\s]+', line)
    if matches:
        for match in matches:
            pos += len(match)
            if pos >= col:
                if not re.match('^[a-zA-Z0-9\\._/-]+$', match):
                    return

                return match


def extract_url(view):
    _URL_REGEX = r"""(?x)
        .*(?P<url>
            https?://               # http:// or https://
            (?:www\.)?              # www.
            (?:[a-zA-Z0-9-]+\.)+    # domain
            [a-zA-Z]+               # tld
            /?[a-zA-Z0-9\-._?,!'(){}\[\]/+&@%$#=:"|~;]*     # url path
        )
    """

    def _extract_url_from_text(regex, text):
        match = re.match(regex, text)
        if match:
            url = match.group('url')

            # Remove end of line full stop character.
            url = url.rstrip('.')

            # Remove closing tag markdown link e.g. `[title](url)`.
            url = url.rstrip(')')

            # Remove closing tag markdown image e.g. `![alt](url)]`.
            if url[-2:] == ')]':
                url = url[:-2]

            # Remove trailing quote marks e.g. `"url"`, `'url'`.
            url = url.rstrip('"\'')

            # Remove trailing quote-comma marks e.g. `"url",`, `'url',`.
            if url[-2:] == '",' or url[-2:] == '\',':
                url = url[:-2]

            return url

        return None

    sel = view.sel()[0]
    line = view.line(sel)
    text = view.substr(line)

    return _extract_url_from_text(_URL_REGEX, text)


# Tries to workaround some of the Sublime Text issues where the cursor caret is
# positioned, off-by-one, at the end of line i.e. the caret positions itself at
# >>>eol| |<<< instead of >>>eo|l|<<<. In some cases, the cursor positions
# itself at >>>eol| |<<<, and then a second later,  moves to the correct
# position >>>eo|l|<<< e.g. a left mouse click after the end of a line. Some of
# these issues can't be worked-around e.g. the mouse click issue described
# above. See https://github.com/SublimeTextIssues/Core/issues/2121.
def fix_eol_cursor(view, mode):
    def f(view, s):
        b = s.b

        if ((view.substr(b) == '\n' or b == view.size()) and not view.line(b).empty()):
            return Region(b - 1)

        return s

    if mode in (NORMAL, INTERNAL_NORMAL):
        regions_transformer(view, f)


def highlow_visible_rows(view):
    visible_region = view.visible_region()
    highest_visible_row = view.rowcol(visible_region.a)[0]
    lowest_visible_row = view.rowcol(visible_region.b - 1)[0]

    # To avoid scrolling when we move to the highest visible row, we need to
    # check if the row is fully visible or only partially visible. If the row is
    # only partially visible we will move to next one.

    line_height = view.line_height()
    view_position = view.viewport_position()
    viewport_extent = view.viewport_extent()

    # The extent y position needs an additional "1.0" to its height. It's not
    # clear why Sublime needs to add it, but it always adds it.

    highest_position = (highest_visible_row * line_height) + 1.0
    if highest_position < view_position[1]:
        highest_visible_row += 1

    lowest_position = ((lowest_visible_row + 1) * line_height) + 1.0
    if lowest_position > (view_position[1] + viewport_extent[1]):
        lowest_visible_row -= 1

    return (highest_visible_row, lowest_visible_row)


def highest_visible_pt(view):
    return view.text_point(highlow_visible_rows(view)[0], 0)


def lowest_visible_pt(view):
    return view.text_point(highlow_visible_rows(view)[1], 0)


def scroll_horizontally(view, edit, amount, half_screen=False):
    if view.settings().get('word_wrap'):
        return

    if half_screen:
        half_extent = view.viewport_extent()[0] / 2
        half_extent_amount = int(half_extent / view.em_width())
        amount = half_extent_amount * int(amount)

    position = view.viewport_position()
    delta = int(amount) * view.em_width()
    pos_x = (position[0] - (position[0] % view.em_width())) + delta
    if pos_x < 0:
        pos_x = 0

    view.set_viewport_position((pos_x, position[1]))


def scroll_viewport_position(view, number_of_scroll_lines, forward=True):
    x, y = view.viewport_position()

    y_addend = ((number_of_scroll_lines) * view.line_height())

    if forward:
        viewport_position = (x, y + y_addend)
    else:
        viewport_position = (x, y - y_addend)

    view.set_viewport_position(viewport_position, animate=False)


def get_option_scroll(view):
    line_height = view.line_height()
    viewport_extent = view.viewport_extent()
    line_count = viewport_extent[1] / line_height
    number_of_scroll_lines = line_count / 2

    return int(number_of_scroll_lines)


def _get_scroll_target(view, number_of_scroll_lines, forward=True):
    s = view.sel()[0]

    if forward:
        if s.b > s.a and view.substr(s.b - 1) == '\n':
            sel_row, sel_col = view.rowcol(s.b - 1)
        else:
            sel_row, sel_col = view.rowcol(s.b)

        target_row = sel_row + number_of_scroll_lines

        # Ignore the last line if it's a blank line. In Sublime the last
        # character is a NULL character point ('\x00'). We don't need to check
        # that it's NULL, just backup one point and retrieve that row and col.
        last_line_row, last_line_col = view.rowcol(view.size() - 1)

        # Ensure the target does not overflow the bottom of the buffer.
        if target_row >= last_line_row:
            target_row = last_line_row
    else:
        if s.b > s.a and view.substr(s.b - 1) == '\n':
            sel_row, sel_col = view.rowcol(s.b - 1)
        else:
            sel_row, sel_col = view.rowcol(s.b)

        target_row = sel_row - number_of_scroll_lines

        # Ensure the target does not overflow the top of the buffer.
        if target_row <= 0:
            target_row = 0

    # Return nothing to indicate there no need to scroll.
    if sel_row == target_row:
        return

    target_pt = next_non_blank(view, view.text_point(target_row, 0))

    return target_pt


def get_scroll_up_target_pt(view, number_of_scroll_lines):
    return _get_scroll_target(view, number_of_scroll_lines, forward=False)


def get_scroll_down_target_pt(view, number_of_scroll_lines):
    return _get_scroll_target(view, number_of_scroll_lines, forward=True)


def resolve_visual_target(s, target):
    # type: (Region, int) -> Region
    if s.a < s.b:               # A --> B
        if target < s.a:        # TARGET < A --> B
            s.a += 1
            s.b = target
        else:
            s.b = target + 1
    elif s.a > s.b:             # B <-- A
        if target > s.a:        # B <-- A < TARGET
            s.a -= 1
            s.b = target + 1
        elif target == s.a:     # B <-- A = TARGET
            s.a -= 1
            s.b = target + 1
        else:
            s.b = target
    elif s.a == s.b:            # A === B
        if target == s.b:       # A === B = TARGET
            s.b = target + 1
        else:
            s.b = target

    return s
