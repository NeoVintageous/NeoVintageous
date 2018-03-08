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

from NeoVintageous.nv.ex.tokens import TokenDigits
from NeoVintageous.nv.ex.tokens import TokenDollar
from NeoVintageous.nv.ex.tokens import TokenDot
from NeoVintageous.nv.ex.tokens import TokenMark
from NeoVintageous.nv.ex.tokens import TokenOffset
from NeoVintageous.nv.ex.tokens import TokenOfSearch
from NeoVintageous.nv.ex.tokens import TokenPercent
from NeoVintageous.nv.ex.tokens import TokenSearchBackward
from NeoVintageous.nv.ex.tokens import TokenSearchForward
from NeoVintageous.nv.vi.search import reverse_search_by_pt
from NeoVintageous.nv.vi.utils import first_sel
from NeoVintageous.nv.vi.utils import row_at


class Node:
    pass


class RangeNode(Node):
    """Represents a Vim line range."""

    def __init__(self, start=None, end=None, separator=None):
        # Args:
        #   start (list):
        #   end (list):
        #   separator (str):
        self.start = start or []
        self.end = end or []
        self.separator = separator

    def __str__(self):
        return '{0}{1}{2}'.format(
            ''.join(str(x) for x in self.start),
            str(self.separator) if self.separator else '',
            ''.join(str(x) for x in self.end),
        )

    def __rpr__(self):
        return ('RangeNode<{0}(start:{1}, end:{2}, separator:{3}]>'
                .format(self.__class__.__name__, self.start, self.end, self.separator))

    def __eq__(self, other):
        if not isinstance(other, RangeNode):
            return False

        return (self.start == other.start and
                self.end == other.end and
                self.separator == other.separator)

    @property
    def is_empty(self):
        """
        Indicate whether this range has ever been defined.

        For example, in interactive mode, if `true`, it means that the user
        hasn't provided any line range on the command line.
        """
        return not any((self.start, self.end, self.separator))

    def _resolve_line_number(self, view, token, current):
        # type: (...) -> int
        if isinstance(token, TokenDot):
            return row_at(view, view.text_point(current, 0))

        if isinstance(token, TokenDigits):
            return max(int(str(token)) - 1, -1)

        if isinstance(token, TokenPercent):
            return row_at(view, view.size())

        if isinstance(token, TokenDollar):
            return row_at(view, view.size())

        if isinstance(token, TokenOffset):
            return current + sum(token.content)

        if isinstance(token, TokenSearchForward):
            match = view.find(str(token)[1:-1], view.text_point(current, 0))
            if not match:
                raise ValueError('pattern not found')

            return row_at(view, match.a)

        if isinstance(token, TokenSearchBackward):
            match = reverse_search_by_pt(view, str(token)[1:-1], 0, view.text_point(current, 0))
            if not match:
                raise ValueError('pattern not found')

            return row_at(view, match.a)

        if isinstance(token, TokenMark):
            return self._resolve_mark(view, token)

        raise NotImplementedError()

    def _resolve_mark(self, view, token):
        # type: (...) -> int
        if token.content == '<':
            sel = list(view.sel())[0]
            view.sel().clear()
            view.sel().add(sel)
            if sel.a < sel.b:
                return row_at(view, sel.a)
            else:
                return row_at(view, sel.a - 1)

        if token.content == '>':
            sel = list(view.sel())[0]
            view.sel().clear()
            view.sel().add(sel)
            if sel.a < sel.b:
                return row_at(view, sel.b - 1)
            else:
                return row_at(view, sel.b)

        raise NotImplementedError()

    def _resolve_line_reference(self, view, line_reference, current=0):
        """
        Calculate the line offset determined by @line_reference.

        @view
          The view where the calculation is made.
        @line_reference
          The sequence of tokens defining the line range to be calculated.
        @current
          Line number where we are now.
        """
        last_token = None
        # XXX: what happens if there is no selection in the view?
        current = row_at(view, first_sel(view).b)
        for token in line_reference:
            # Make sure a search forward doesn't overlap with a match obtained
            # right before this search.
            if isinstance(last_token, TokenOfSearch) and isinstance(token, TokenOfSearch):
                if isinstance(token, TokenSearchForward):
                    current += 1

            current = self._resolve_line_number(view, token, current)

            last_token = token

        return current

    def resolve(self, view):
        """Return a representing the Vim line range that the ex command should operate on."""
        start = self._resolve_line_reference(view, self.start or [TokenDot()])

        if not self.separator:
            if start == -1:
                return Region(-1, -1)

            if len(self.start) == 1 and isinstance(self.start[0], TokenPercent):
                return Region(0, view.size())

            return view.full_line(view.text_point(start, 0))

        new_start = start if self.separator == ';' else 0
        end = self._resolve_line_reference(view, self.end or [TokenDot()], current=new_start)

        return view.full_line(Region(view.text_point(start, 0), view.text_point(end, 0)))


class CommandLineNode(Node):

    def __init__(self, line_range, command):
        # Args:
        #   :line_range (RangeNode):
        #   :command (TokenOfCommand):
        self.line_range = line_range
        self.command = command

    def __str__(self):
        # TODO return '{0}{1}' because if there's no range then it returns ", command*" which looks mangled
        return '{0}, {1}'.format(str(self.line_range), str(self.command))

    def validate(self):
        # type: () -> None
        # Raise an error for known conditions.
        if not (self.command and self.line_range):
            return

        if not self.command.addressable and not self.line_range.is_empty:
            raise Exception("E481: No range allowed")
