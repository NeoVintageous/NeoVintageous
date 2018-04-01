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

from collections import OrderedDict
import re

from .commands import scan_cmd_abbreviate
from .commands import scan_cmd_browse
from .commands import scan_cmd_buffers
from .commands import scan_cmd_cd
from .commands import scan_cmd_cdd
from .commands import scan_cmd_close
from .commands import scan_cmd_copy
from .commands import scan_cmd_cquit
from .commands import scan_cmd_delete
from .commands import scan_cmd_double_ampersand
from .commands import scan_cmd_edit
from .commands import scan_cmd_exit
from .commands import scan_cmd_file
from .commands import scan_cmd_global
from .commands import scan_cmd_help
from .commands import scan_cmd_let
from .commands import scan_cmd_move
from .commands import scan_cmd_new
from .commands import scan_cmd_nnoremap
from .commands import scan_cmd_noremap
from .commands import scan_cmd_nunmap
from .commands import scan_cmd_only
from .commands import scan_cmd_onoremap
from .commands import scan_cmd_ounmap
from .commands import scan_cmd_print
from .commands import scan_cmd_pwd
from .commands import scan_cmd_qall
from .commands import scan_cmd_quit
from .commands import scan_cmd_read
from .commands import scan_cmd_registers
from .commands import scan_cmd_set
from .commands import scan_cmd_setlocal
from .commands import scan_cmd_shell
from .commands import scan_cmd_shell_out
from .commands import scan_cmd_snoremap
from .commands import scan_cmd_split
from .commands import scan_cmd_substitute
from .commands import scan_cmd_tabfirst
from .commands import scan_cmd_tablast
from .commands import scan_cmd_tabnext
from .commands import scan_cmd_tabonly
from .commands import scan_cmd_tabprevious
from .commands import scan_cmd_unabbreviate
from .commands import scan_cmd_unmap
from .commands import scan_cmd_unvsplit
from .commands import scan_cmd_vnoremap
from .commands import scan_cmd_vsplit
from .commands import scan_cmd_vunmap
from .commands import scan_cmd_wall
from .commands import scan_cmd_wq
from .commands import scan_cmd_wqall
from .commands import scan_cmd_write
from .commands import scan_cmd_yank
from .tokens import TokenComma
from .tokens import TokenDigits
from .tokens import TokenDollar
from .tokens import TokenDot
from .tokens import TokenEof
from .tokens import TokenMark
from .tokens import TokenOffset
from .tokens import TokenPercent
from .tokens import TokenSearchBackward
from .tokens import TokenSearchForward
from .tokens import TokenSemicolon


class _ScannerState:

    EOF = '__EOF__'

    # Attributes:
    #   :source (str): The string to be scanned.
    #   :position (int): The current scan position. Default is 0.
    #   :start (int): The most recent scan start. Default is 0.

    def __init__(self, source):
        # type: (str) -> None
        self.source = source
        self.position = 0
        self.start = 0

    def consume(self):
        # type: () -> str
        # Returns one character or self.EOF constant ("__EOF__") if no
        # characters left in source.
        if self.position >= len(self.source):
            return self.EOF

        c = self.source[self.position]

        self.position += 1

        return c

    def backup(self):
        # type: () -> None
        # Backs up scanner position by one character.
        self.position -= 1

    def ignore(self):
        # type: () -> None
        # Discards characters up to the current poistion such that calls to
        # emit() will ignore those characters.
        self.start = self.position

    def emit(self):
        # type: () -> str
        # Returns source from start to current position, and advances start to
        # the current position.
        content = self.source[self.start:self.position]

        self.ignore()

        return content

    def skip(self, character):
        # type: (str) -> None
        # Consumes character while it matches.
        while True:
            c = self.consume()
            if c == self.EOF or c != character:
                break

        if c != self.EOF:
            self.backup()

    def skip_run(self, characters):
        # type: (str) -> None
        # Skips characters while there's a match.
        while True:
            c = self.consume()
            if c == self.EOF or c not in characters:
                break

        if c != self.EOF:
            self.backup()

    def expect(self, item, on_error=None):
        # type: (...) -> str
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

            # TODO Use domain specific exception.
            raise ValueError('expected {0}, got {1} instead'.format(item, c))

        return c

    def expect_eof(self, on_error=None):
        return self.expect(self.EOF, on_error)

    def expect_match(self, pattern, on_error=None):
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

    def peek(self, item):
        # type: (str) -> bool
        # Return True if item matches at the current position, False otherwise.
        return self.source[self.position:self.position + len(item)] == item

    def match(self, pattern):
        # Return the match obtained by searching pattern. The current `position`
        # will advance as many characters as the match's length.
        #
        # Args:
        #     pattern (str): A regular expression.
        m = re.compile(pattern).match(self.source, self.position)
        if m:
            self.position += m.end() - m.start()

            return m

        return


class Scanner:

    # Produce ex command-line tokens from a string.
    #
    # Attributes:
    #   :state (_ScannerState):
    #
    # TODO Make this class a function. We don't need a state object reference.

    def __init__(self, source):
        # type: (str) -> None
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


def _scan_range(state):
    # Produce tokens found in a command line range.
    # https://vimhelp.appspot.com/cmdline.txt.html#cmdline-ranges
    #
    # Args:
    #   :state (_ScannerState):
    #
    # Returns:
    #   tuple

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

    if c.isdigit():
        return _scan_digits(state)

    state.backup()

    return _scan_command, []


def _scan_mark(state):
    c = state.expect_match(r'[a-zA-Z\[\]()<>]')

    return _scan_range, [TokenMark(c.group(0))]


def _scan_digits(state):
    while True:
        c = state.consume()
        if not c.isdigit():
            if c == state.EOF:
                return None, [TokenDigits(state.emit()), TokenEof()]

            state.backup()
            break

    return _scan_range, [TokenDigits(state.emit())]


def _scan_search(state):
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


def _scan_offset(state):
    offsets = []

    def to_int(x):
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


# TODO: compile regexes. ??
_routes = OrderedDict()
_routes[r'!(?=.+)'] = scan_cmd_shell_out
_routes[r'&&?'] = scan_cmd_double_ampersand
_routes[r'ab(?:breviate)?'] = scan_cmd_abbreviate
_routes[r'bro(?:wse)?'] = scan_cmd_browse
_routes[r'clo(?:se)?'] = scan_cmd_close
_routes[r'co(?:py)?'] = scan_cmd_copy
_routes[r'cq(?:uit)?'] = scan_cmd_cquit
_routes[r'd(?:elete)?'] = scan_cmd_delete
_routes[r'exi(?:t)?'] = scan_cmd_exit
_routes[r'f(?:ile)?'] = scan_cmd_file
_routes[r'g(?:lobal)?(?=[^ ])'] = scan_cmd_global
_routes[r'h(?:elp)?'] = scan_cmd_help
_routes[r'(?:ls|files|buffers)!?'] = scan_cmd_buffers
_routes[r'vs(?:plit)?'] = scan_cmd_vsplit
_routes[r'x(?:it)?$'] = scan_cmd_exit
_routes[r'^cd(?=[^d]|$)'] = scan_cmd_cd
_routes[r'^cdd'] = scan_cmd_cdd
_routes[r'e(?:dit)?(?= |$)?'] = scan_cmd_edit
_routes[r'let\s'] = scan_cmd_let
_routes[r'm(?:ove)?(?=[^a]|$)'] = scan_cmd_move
_routes[r'no(?:remap)'] = scan_cmd_noremap
_routes[r'new'] = scan_cmd_new
_routes[r'nn(?:oremap)?'] = scan_cmd_nnoremap
_routes[r'nun(?:map)?'] = scan_cmd_nunmap
_routes[r'ono(?:remap)?'] = scan_cmd_onoremap
_routes[r'on(?:ly)?(?=!$|$)'] = scan_cmd_only
_routes[r'ounm(?:ap)?'] = scan_cmd_ounmap
_routes[r'p(?:rint)?$'] = scan_cmd_print
_routes[r'pwd?$'] = scan_cmd_pwd
_routes[r'q(?!a)(?:uit)?'] = scan_cmd_quit
_routes[r'qa(?:ll)?'] = scan_cmd_qall
_routes[r'r(?!eg)(?:ead)?'] = scan_cmd_read
_routes[r'reg(?:isters)?(?=\s+[a-z0-9]+$|$)'] = scan_cmd_registers
_routes[r's(?:ubstitute)?(?=[%&:/=]|$)'] = scan_cmd_substitute
_routes[r'se(?:t)?(?=$|\s)'] = scan_cmd_set
_routes[r'setl(?:ocal)?'] = scan_cmd_setlocal
_routes[r'sh(?:ell)?'] = scan_cmd_shell
_routes[r'snor(?:emap)?'] = scan_cmd_snoremap
_routes[r'sp(?:lit)?'] = scan_cmd_split
_routes[r'tabfir(?:st)?'] = scan_cmd_tabfirst
_routes[r'tabl(?:ast)?'] = scan_cmd_tablast
_routes[r'tabn(?:ext)?'] = scan_cmd_tabnext
_routes[r'tabo(?:nly)?'] = scan_cmd_tabonly
_routes[r'tabp(?:revious)?'] = scan_cmd_tabprevious
_routes[r'tabr(?:ewind)?'] = scan_cmd_tabfirst
_routes[r'una(?:bbreviate)?'] = scan_cmd_unabbreviate
_routes[r'unm(?:ap)?'] = scan_cmd_unmap
_routes[r'unvsplit$'] = scan_cmd_unvsplit
_routes[r'vn(?:oremap)?'] = scan_cmd_vnoremap
_routes[r'vu(?:nmap)?'] = scan_cmd_vunmap
_routes[r'w(?:rite)?(?=(?:!?(?:\+\+|>>| |$)))'] = scan_cmd_write
_routes[r'wqa(?:ll)?'] = scan_cmd_wqall
_routes[r'xa(?:ll)?'] = scan_cmd_wqall
_routes[r'wa(?:ll)?'] = scan_cmd_wall
_routes[r'wq(?=[^a-zA-Z]|$)?'] = scan_cmd_wq
_routes[r'y(?:ank)?'] = scan_cmd_yank


def _scan_command(state):
    # Args:
    #   :state (_ScannerState):
    #
    # Returns:
    #   Tuple[None, list(TokenEof)]
    for route, command in _routes.items():
        if state.match(route):
            state.ignore()

            return command(state)

    state.expect_eof(lambda: Exception("E492: Not an editor command"))

    return None, [TokenEof()]
