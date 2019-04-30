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

from NeoVintageous.nv.vi.settings import get_visual_block_direction
from NeoVintageous.nv.vi.settings import set_visual_block_direction
from NeoVintageous.nv.vi.utils import next_non_blank
from NeoVintageous.nv.vi.utils import regions_transformer
from NeoVintageous.nv.vim import DIRECTION_DOWN
from NeoVintageous.nv.vim import DIRECTION_UP
from NeoVintageous.nv.vim import INTERNAL_NORMAL
from NeoVintageous.nv.vim import NORMAL
from NeoVintageous.nv.vim import run_window_command


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
            # Remove trailing markdown punctuation e.g. ): int [title](url):
            if url[-2:] in (')]', '):'):
                url = url[:-2]

            # Remove trailing quote marks e.g. `"url"`, `'url'`.
            url = url.rstrip('"\'')

            # Remove trailing quote-comma marks e.g. ", and ,'
            if url[-2:] in ('",', '\','):
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
    # type: (Region, int) -> None
    if s.a < s.b:               # A --> B
        if target < s.a:        # TARGET < A --> B
            s.a += 1
            s.b = target
        else:
            s.b = target + 1
    elif s.a > s.b:             # B <-- A
        if target >= s.a:       # B <-- A <= TARGET
            s.a -= 1
            s.b = target + 1
        else:
            s.b = target
    else:                       # A === B

        # If A and B are equal, it means the Visual selection is not "well
        # formed". Instead of raising an error, or not resolving the selection,
        # the selection is coerced to be "well formed" and then resolved.

        if target == s.b:       # B === TARGET
            s.b = target + 1
        else:
            s.b = target


def resolve_visual_line_target(view, s, target):
    # type: (...) -> None
    if s.a < s.b:                               # A --> B
        if target < s.a:                        # TARGET < A --> B
            s.a = view.full_line(s.a).b
            s.b = view.line(target).a
        elif target > s.a:
            s.b = view.full_line(target).b
        elif target == s.a:
            s.b = s.a
            s.a = view.full_line(target).b
    elif s.a > s.b:                             # B <-- A
        if target > s.a:                        # B <-- A < TARGET
            s.a = view.line(s.a - 1).a
            s.b = view.full_line(target).b
        elif target < s.a:                      # TARGET < B <-- TARGET < A
            s.b = view.line(target).a
        elif target == s.a:                     # A === TARGET
            s.a = view.line(s.a - 1).a
            s.b = view.full_line(target).b
    elif s.a == s.b:                            # A === B

        # If A and B are equal, it means the Visual selection is not "well
        # formed". Instead of raising an error, or not resolving the selection,
        # the selection is coerced to be "well formed" and then resolved.

        if target > s.a:
            s.a = view.line(s.a).a
            s.b = view.full_line(target).b
        elif target < s.a:
            s.a = view.full_line(s.a).b
            s.b = view.line(target).a
        elif target == s.a:
            s.a = view.line(target).a
            s.b = view.full_line(target).b


class VisualBlockSelection():

    # There are two "pivot" points: the direction of the Visual block, and the
    # direction of selections (forward/reverse) within the Visual block.
    #
    # The reason for selections "within" the Visual block, is because Sublime
    # doesn't support real block selections, to work around that limitation,
    # normal selections grouped together are used to emulate a block selection.
    #
    # The direction of the Visual block is indicated as DOWN or UP.
    #
    # The "pivot" for the direction of the selections is the column at point A.
    # Point B determines if the selections are REVERSED or FORWARD, if point B
    # is to the LEFT of COL-A, then the selections are REVERSED, otherwise not.
    #
    # Here are some examples:
    #
    # (when the number of lines is equal to one, then ab==b and a==ba)
    #
    # Visual block is DOWN and contains FORWARD selections:
    #
    #   a     DOWN FORWARD  a----ab
    #    \                  |     |
    #     \                 | --> |
    #      \                |     |
    #       b               ba----b
    #
    # Visual block is DOWN and contains REVERSED selections:
    #
    #       a DOWN REVERSE  ab----a
    #      /                |     |
    #     /                 | <-- |
    #    /                  |     |
    #   b                   b----ba
    #
    # Visual block is UP and contains FORWARD selections:
    #
    #       b UP FORWARD    ba----b
    #      /                |     |
    #     /                 | --> |
    #    /                  |     |
    #   a                   a----ab
    #
    # Visual block is UP and contains REVERSED selections:
    #
    #   b     UP REVERSE    b----ba
    #    \                  |     |
    #     \                 | <-- |
    #      \                |     |
    #       a               ab----a

    def __init__(self, view, direction=DIRECTION_DOWN):
        self.view = view
        self._set_direction(get_visual_block_direction(view, direction))

    def _set_direction(self, direction):
        # type: (int) -> None
        set_visual_block_direction(self.view, direction)
        self._direction = direction

    def _a(self):
        # type: () -> Region
        index = 0 if self.is_direction_down() else -1
        return self.view.sel()[index]

    def _b(self):
        # type: () -> Region
        index = -1 if self.is_direction_down() else 0
        return self.view.sel()[index]

    def begin(self):
        # type: () -> int
        a = self._a()
        b = self._b()

        if a < b:
            begin = a.begin()
        else:
            begin = b.begin()

        return begin

    def end(self):
        # type: () -> int
        a = self._a()
        b = self._b()

        if a < b:
            end = b.end()
        else:
            end = a.end()

        return end

    @property
    def a(self):
        # type: () -> int
        return self._a().a

    @property
    def ab(self):
        # type: () -> int
        return self._a().b

    @property
    def b(self):
        # type: () -> int
        return self._b().b

    @property
    def ba(self):
        # type: () -> int
        return self._b().a

    def rowcolb(self):
        # type: () -> tuple
        return self.view.rowcol(self.insertion_point_b())

    def to_visual(self):
        if self.is_direction_down():
            a = self.begin()
            b = self.end()
        else:
            a = self.end()
            b = self.begin()

        return Region(a, b)

    def to_visual_line(self):
        a = self.view.full_line(self.begin()).a
        b = self.view.full_line(self.end()).b

        return Region(a, b)

    def insertion_point_b(self):
        # type: () -> int
        b = self.b
        ba = self.ba

        return b - 1 if b > ba else b

    def insertion_point_a(self):
        # type: () -> int
        a = self.a
        ab = self.ab

        return a - 1 if a > ab else a

    def _is_direction(self, direction):
        # type: (int) -> bool
        return self._direction == direction

    def is_direction_down(self):
        # type: () -> bool
        return self._is_direction(DIRECTION_DOWN)

    def is_direction_up(self):
        # type: () -> bool
        return self._is_direction(DIRECTION_UP)

    def resolve_target(self, target):
        # type: (int) -> list

        # When the TARGET is to the RIGHT of COL-A, then the Visual block will
        # have FORWARD selections. When the TARGET is to the LEFT of COL-A, then
        # the Visual block will have REVERSED selections.
        #
        # When the TARGET is to the LEFT of COL-A, the new Visual block will
        # have REVERSED selections, when it's to the RIGHT of COL-A, the new
        # Visual block will have FORWARD selections.
        #
        # When the TARGET is on the same side as the current column COL-B (the
        # TARGET is changing point B, and thus COL-B), then the direction of the
        # selections is inverted, for example:
        #
        #          a DOWN REVERSE
        #         /|
        #        / |
        #       /  |
        #      b   |
        #          |
        #          | T

        a = self.a
        ab = self.ab

        begin = self.begin()
        end = self.end()

        col_a = self.view.rowcol(a - 1 if a > ab else a)[1]
        col_t = self.view.rowcol(target)[1]

        is_direction_down = self.is_direction_down()

        block = []

        if is_direction_down:
            if target >= begin:
                lines = self.view.lines(Region(begin, target + 1))
            else:
                lines = self.view.lines(Region(a + 1, target))
        else:
            if target >= end:
                lines = self.view.lines(Region(a, target + 1))
            else:
                lines = self.view.lines(Region(a + 1, target))

        if col_t >= col_a:
            for line in lines:
                # If the line size is less than COL-A (selection direction
                # "pivot" point), the line is ommited from FORWARD Visual block.
                if line.size() >= col_a:
                    new_line = Region(
                        min(line.a + col_a, line.b + 1),
                        min(line.a + col_t + 1, line.b + 1)
                    )

                    block.append(new_line)
        else:
            for line in lines:
                # If the line size is less than COL-T, in a REVERSE selection,
                # then the line is ommited from a REVERSE Visual block.
                if line.size() >= col_t:
                    new_line = Region(
                        min(line.a + col_a + 1, line.b + 1),
                        min(line.a + col_t, line.b + 1)
                    )

                    block.append(new_line)

        if is_direction_down:
            if target < begin:
                self._set_direction(DIRECTION_UP)
        else:
            if target >= end:
                self._set_direction(DIRECTION_DOWN)

        return block

    def transform_target(self, target):
        # type: (int) -> None
        visual_block = self.resolve_target(target)
        if visual_block:
            self.view.sel().clear()
            self.view.sel().add_all(visual_block)
            self.view.show(target, False)

    def _transform(self, region):
        self.view.sel().clear()
        self.view.sel().add(region)

    def transform_to_visual(self):
        self._transform(self.to_visual())

    def transform_to_visual_line(self):
        self._transform(self.to_visual_line())


class InputParser():

    IMMEDIATE = 1
    VIA_PANEL = 2
    AFTER_MOTION = 3

    def __init__(self, type=None, command=None, interactive_command=None, param=None):
        self._type = type
        self._command = command
        self._interactive_command = interactive_command
        self._param = param

    def is_interactive(self):
        # type: () -> bool
        return bool(self._interactive_command)

    def is_type_after_motion(self):
        return self._type == self.AFTER_MOTION

    def is_type_immediate(self):
        return self._type == self.IMMEDIATE

    def is_type_via_panel(self):
        return self._type == self.VIA_PANEL

    def run_interactive_command(self, window, param_value):
        # type: (...) -> None
        cmd = self._interactive_command
        args = {self._param: param_value}

        window.run_command(cmd, args)

    def run_command(self):
        run_window_command(self._command)


def folded_rows(view, pt):
    # type: (...) -> int
    folds = view.folded_regions()
    try:
        fold = [f for f in folds if f.contains(pt)][0]
        fold_row_a = view.rowcol(fold.a)[0]
        fold_row_b = view.rowcol(fold.b - 1)[0]
        # Return no. of hidden lines.
        return (fold_row_b - fold_row_a)
    except IndexError:
        return 0


# FIXME If we have two contiguous folds, this method will fail. Handle folded regions
def previous_non_folded_pt(view, pt):
    # type: (...) -> int
    folds = view.folded_regions()
    try:
        fold = [f for f in folds if f.contains(pt)][0]
        non_folded_row = view.rowcol(fold.a - 1)[0]
        pt = view.text_point(non_folded_row, 0)
    except IndexError:
        pass

    return pt


# FIXME: If we have two contiguous folds, this method will fail. Handle folded regions
def next_non_folded_pt(view, pt):
    # type: (...) -> int
    folds = view.folded_regions()
    try:
        fold = [f for f in folds if f.contains(pt)][0]
        non_folded_row = view.rowcol(view.full_line(fold.b).b)[0]
        pt = view.text_point(non_folded_row, 0)
    except IndexError:
        pass

    return pt


def calculate_xpos(view, start, xpos):
    # type: (...) -> tuple
    if view.line(start).empty():
        return start, 0

    size = view.settings().get('tab_size')
    eol = view.line(start).b - 1
    pt = 0
    chars = 0
    while (pt < xpos):
        if view.substr(start + chars) == '\t':
            pt += size
        else:
            pt += 1

        chars += 1

    pt = min(eol, start + chars)

    return (pt, chars)
