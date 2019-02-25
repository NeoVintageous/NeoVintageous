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


def extract_file_name(view):
    sel = view.sel()[0]

    line = view.substr(view.line(sel))
    pos = len(line) - len(line.strip()) + 1
    col = view.rowcol(sel.b)[1]

    if pos > col:
        return

    matches = re.findall('[^\\s]+', line)
    if not matches:
        return

    for match in matches:
        pos += len(match)
        if pos >= col:
            if not re.match('^[a-zA-Z0-9\\._/-]+$', match):
                return

            return match


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
