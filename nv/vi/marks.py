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

# store: window, view, rowcol

_MARKS = {}


class Marks(object):

    def __get__(self, instance, owner):
        self.state = instance

        return self

    def add(self, name, view):
        # TODO: support multiple selections
        # TODO: Use id attribute; references might change.
        win, view, rowcol = view.window(), view, view.rowcol(view.sel()[0].b)
        _MARKS[name] = win, view, rowcol

    def get_as_encoded_address(self, name, exact=False):
        """
        Return an address for the mark @name.

        @name
          The name of the mark to be retrieved.
        @exact
          If `true`, the exact position of the mark is returned. Otherwise,
          the relevant row's 0 column is returned.
        """
        if name == "'":
            # Special case: '' motion
            return '<command _vi_double_single_quote>'

        win, view, rowcol = _MARKS.get(name, (None,) * 3)
        if win:
            if exact:
                rowcol_encoded = ':'.join(str(i) for i in rowcol)
            else:
                rowcol_encoded = ':'.join(str(i) for i in (rowcol[0], 0))

            fname = view.file_name()

            # Marks set in the same view as the current one are returned as regions. Marks in other
            # views are returned as encoded addresses that Sublime Text understands.
            if view and view.view_id == self.state.view.view_id:
                if not exact:
                    rowcol = (rowcol[0], 0)

                return Region(view.text_point(*rowcol))
            else:
                # FIXME: Remove buffers when they are closed.
                if fname:
                    return "{0}:{1}".format(fname, rowcol_encoded)
                else:
                    return "<untitled {0}>:{1}".format(view.buffer_id(), rowcol_encoded)
