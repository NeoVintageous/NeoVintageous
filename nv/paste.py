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

from sublime import Region


def pad_visual_block_paste_contents(view, sels: list, contents: list, before_cursor: bool) -> tuple:
    sel = sels[0]
    row, col = view.rowcol(sel.a)
    view_size = view.size()

    # When the selection line is empty the insertion point is always as
    # if before_cursor was true i.e. column zero of the empty line.
    before_cursor = True if view.line(sel.a).empty() else before_cursor

    for index in range(1, len(contents)):
        content = contents[index]
        sel_row = row + index
        line = view.line(view.text_point(sel_row, 0))
        pad_size = col - line.size()

        # When the paste column is greater than the line size then the
        # selection content needs to be left-padded with whitespace.
        if pad_size >= 0:
            pt = line.begin() + line.size()
            if pad_size > 0:
                content = (' ' * pad_size) + content

            if not before_cursor:
                content = ' ' + content
                if line.size() > 0:
                    pt -= 1

            contents[index] = content
        else:
            pt = view.text_point(sel_row, col)

        if view.rowcol(pt)[0] < sel_row:
            lead = '\n'
            if pt >= view_size and pad_size < 0:
                lead += (' ' * col)
                if not before_cursor:
                    lead += ' '
                    pt -= 1

            contents[index] = lead + contents[index]

        sels.append(Region(pt))

    # Cursor needs to reset to start of pasted text.
    resolve_to_specific_pt = sels[0].begin()
    if not before_cursor:
        resolve_to_specific_pt += 1

    return sels, contents, before_cursor, resolve_to_specific_pt


def resolve_paste_items_with_view_sel(view, contents: list) -> list:
    sels_count = len(view.sel())
    contents_len = len(contents)

    if sels_count == contents_len:
        return contents

    if sels_count > 1:
        # If the number of items in the paste register exceeds the number of
        # selections then slice the paste items up to the number of sels.
        if contents_len > sels_count:
            return contents[:sels_count]

        # If the paste items are all the same then fill the paste items up the
        # number of selections.
        if len(set(contents)) == 1:
            for x in range(sels_count - contents_len):
                contents.append(contents[0])

            return contents[:sels_count]

        # The cpaste contents is not compatible with the number of selections.
        return []

    return contents
