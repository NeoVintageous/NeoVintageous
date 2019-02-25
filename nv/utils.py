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
