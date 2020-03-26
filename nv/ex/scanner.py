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

from NeoVintageous.nv.ex.tokens import TokenComma
from NeoVintageous.nv.ex.tokens import TokenDigits
from NeoVintageous.nv.ex.tokens import TokenDollar
from NeoVintageous.nv.ex.tokens import TokenDot
from NeoVintageous.nv.ex.tokens import TokenEof
from NeoVintageous.nv.ex.tokens import TokenMark
from NeoVintageous.nv.ex.tokens import TokenOffset
from NeoVintageous.nv.ex.tokens import TokenPercent
from NeoVintageous.nv.ex.tokens import TokenSearchBackward
from NeoVintageous.nv.ex.tokens import TokenSearchForward
from NeoVintageous.nv.ex.tokens import TokenSemicolon
from NeoVintageous.nv.ex_routes import ex_routes


class _ScannerState:

    EOF = '__EOF__'

    # Attributes:
    #   :source (str): The string to be scanned.
    #   :position (int): The current scan position. Default is 0.
    #   :start (int): The most recent scan start. Default is 0.

    def __init__(self, source: str) -> None:
        self.source = source
        self.position = 0
        self.start = 0

    def consume(self) -> str:
        # Returns one character or self.EOF constant ("__EOF__") if no
        # characters left in source.
        if self.position >= len(self.source):
            return self.EOF

        c = self.source[self.position]

        self.position += 1

        return c

    def backup(self) -> None:
        # Backs up scanner position by one character.
        self.position -= 1

    def ignore(self) -> None:
        # Discards characters up to the current poistion such that calls to
        # emit() will ignore those characters.
        self.start = self.position

    def emit(self) -> str:
        # Returns source from start to current position, and advances start to
        # the current position.
        content = self.source[self.start:self.position]

        self.ignore()

        return content

    def skip(self, character: str) -> None:
        # Consumes character while it matches.
        while True:
            c = self.consume()
            if c == self.EOF or c != character:
                break

        if c != self.EOF:
            self.backup()

    def skip_run(self, characters: str) -> None:
        # Skips characters while there's a match.
        while True:
            c = self.consume()
            if c == self.EOF or c not in characters:
                break

        if c != self.EOF:
            self.backup()

    def expect(self, item, on_error=None) -> str:
        # Expects item to match at the current position.
        #
        # Args:
        #   item (str): Expected character.
        #   on_error (callable): A function that returns an error. The error
        #       returned overrides the default ValueError.
        #
        # Raises:
        #   ValueError: If item does not match.
        #   on_error (callable): If item does not match.
        c = self.consume()
        if c != item:
            if on_error:
                raise on_error()

            raise ValueError('expected {0}, got {1} instead'.format(item, c))

        return c

    def expect_eof(self, on_error=None) -> str:
        return self.expect(self.EOF, on_error)

    def expect_match(self, pattern: str, on_error=None):
        # Expects item to match at the current position.
        #
        # Args:
        #     pattern (str): A regular expression.
        #     on_error (Callable): A function that returns an error. The error
        #         returned overrides the default ValueError.
        #
        # Raises:
        #   ValueError: If item does not match.
        #   on_error (callable): If item does not match.
        m = re.compile(pattern).match(self.source, self.position)
        if m:
            self.position += m.end() - m.start()

            return m

        if not on_error:
            raise ValueError('expected match with \'{0}\', at \'{1}\''.format(pattern, self.source[self.position:]))

        raise on_error()

    def peek(self, item: str) -> bool:
        # Return True if item matches at the current position, False otherwise.
        return self.source[self.position:self.position + len(item)] == item

    def match(self, pattern: str):
        # Return the match obtained by searching pattern. The current `position`
        # will advance as many characters as the match's length.
        #
        # Args:
        #     pattern (str): A regular expression.
        m = re.compile(pattern).match(self.source, self.position)
        if m:
            self.position += m.end() - m.start()

            return m


class Scanner:

    # Produce ex command-line tokens from a string.
    #
    # Attributes:
    #   :state (_ScannerState):

    def __init__(self, source: str) -> None:
        self.state = _ScannerState(source)

    def scan(self):
        # Generate ex command-line tokens for source. The scanner works its way
        # through the source string by passing the current state to the next
        # scanning function.
        next_func = _scan_range
        while True:
            # We return multiple tokens so that we can work around cyclic
            # imports: functions that need to, return TokenEof without having to
            # call a function in this module from a separate module. Keep
            # scanning while we get a scanning function.
            (next_func, items) = next_func(self.state)
            yield from items
            if not next_func:
                break


def _scan_range(state) -> tuple:
    # Produce tokens found in a command line range.
    # https://vimhelp.appspot.com/cmdline.txt.html#cmdline-ranges
    #
    # Args:
    #   :state (_ScannerState):
    c = state.consume()

    if c == state.EOF:
        return None, [TokenEof()]

    if c == '.':
        state.emit()

        return _scan_range, [TokenDot()]

    if c == '$':
        state.emit()

        return _scan_range, [TokenDollar()]

    if c == ',':
        state.emit()

        return _scan_range, [TokenComma()]

    if c in ';':
        state.emit()

        return _scan_range, [TokenSemicolon()]

    if c == "'":
        return _scan_mark(state)

    if c in '/?':
        return _scan_search(state)

    if c in '+-':
        return _scan_offset(state)

    if c == '%':
        state.emit()

        return _scan_range, [TokenPercent()]

    if c in '\t ':
        state.skip_run(' \t')
        state.ignore()

        return _scan_range, []

    if c.isdigit():
        return _scan_digits(state)

    state.backup()

    return _scan_command, []


def _scan_mark(state) -> tuple:
    c = state.expect_match(r'[a-zA-Z\[\]()<>]')

    return _scan_range, [TokenMark(c.group(0))]


def _scan_digits(state) -> tuple:
    while True:
        c = state.consume()
        if not c.isdigit():
            if c == state.EOF:
                return None, [TokenDigits(state.emit()), TokenEof()]

            state.backup()
            break

    return _scan_range, [TokenDigits(state.emit())]


def _scan_search(state) -> tuple:
    delim = state.source[state.position - 1]
    while True:
        c = state.consume()

        if c == delim:
            state.start += 1
            state.backup()
            content = state.emit()
            state.consume()
            token = TokenSearchForward if c == '/' else TokenSearchBackward

            return _scan_range, [token(content)]

        elif c == state.EOF:
            raise ValueError('unclosed search pattern: {0}'.format(state.source))


def _scan_offset(state) -> tuple:
    offsets = []

    def to_int(x: str) -> int:
        return int(x, 10)

    sign = '-' if state.source[state.position - 1] == '-' else ''

    digits = state.expect_match(r'\s*(\d+)')
    offsets.append(sign + digits.group(1))

    while True:
        c = state.consume()

        if c == state.EOF:
            state.ignore()

            return None, [TokenOffset(list(map(to_int, offsets))), TokenEof()]

        if c == '+' or c == '-':
            digits = state.expect_match(r'\s*(\d+)')
            sign = '-' if state.source[state.position - 1] == '-' else ''
            offsets.append(sign + digits.group(1))
            continue

        if not c.isdigit():
            state.backup()
            state.ignore()

            return _scan_range, [TokenOffset(list(map(to_int, offsets)))]


def _scan_command(state) -> tuple:
    # Args:
    #   :state (_ScannerState):
    #
    # Returns:
    #   Tuple[None, list(TokenEof)]
    for route, command in ex_routes.items():
        if state.match(route):
            state.ignore()

            cmd = command(state)

            state.expect_eof(lambda: Exception("E492: Not an editor command: %s" % state.source))

            return None, [cmd, TokenEof()]

    raise Exception("E492: Not an editor command: %s" % state.source)
