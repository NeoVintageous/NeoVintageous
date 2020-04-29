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

import logging

from NeoVintageous.nv.ex.nodes import RangeNode
from NeoVintageous.nv.ex.scanner import Scanner
from NeoVintageous.nv.ex.tokens import TokenComma
from NeoVintageous.nv.ex.tokens import TokenCommand
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


_log = logging.getLogger(__name__)


class _ParsedCommandLine():

    def __init__(self, line_range, command):
        # Args:
        #   :line_range (RangeNode):
        #   :command (TokenCommand):
        self.line_range = line_range
        self.command = command

    def __str__(self) -> str:
        return '{}{}'.format(str(self.line_range), str(self.command) if self.command else '')

    def validate(self) -> None:
        if not (self.command and self.line_range):
            return

        if not self.command.addressable and not self.line_range.is_empty:
            raise Exception("E481: No range allowed")


class _ParserState:

    # Attributes:
    #   :scanner (Scanner):
    #   :is_range_start_line_parsed (bool): Default is false.
    #   :tokens:

    def __init__(self, source: str) -> None:
        self.scanner = Scanner(source)
        self.is_range_start_line_parsed = False
        self.tokens = self.scanner.scan()

    def next_token(self):
        return next(self.tokens)


def parse_command_line(source: str) -> _ParsedCommandLine:
    # The parser works its way through the command line by passing the current
    # state to the next parsing function. It stops when no parsing funcion is
    # returned from the previous one.
    _log.debug('parsing source >>>%s<<<', source)

    state = _ParserState(source)
    parse_func = _parse_line_ref
    command_line = _ParsedCommandLine(None, None)
    while True:
        parse_func, command_line = parse_func(state, command_line)
        if parse_func is None:
            command_line.validate()

            _log.debug('parsed %s', command_line)

            return command_line


def resolve_address(view, address: str):
    _log.debug('parsing address >>>%s<<<', address)
    return parse_command_line(address).line_range.resolve(view)


def _init_line_range(command_line: _ParsedCommandLine) -> None:
    if command_line.line_range:
        return

    command_line.line_range = RangeNode()


def _parse_line_ref(state: _ParserState, command_line: _ParsedCommandLine) -> tuple:
    token = state.next_token()

    if isinstance(token, TokenEof):
        return None, command_line

    if isinstance(token, TokenDot):
        _init_line_range(command_line)

        return _process_dot(state, command_line)

    if isinstance(token, TokenOffset):
        _init_line_range(command_line)

        return _process_offset(token, state, command_line)

    if isinstance(token, TokenSearchForward):
        _init_line_range(command_line)

        return _process_search_forward(token, state, command_line)

    if isinstance(token, TokenSearchBackward):
        _init_line_range(command_line)

        return _process_search_backward(token, state, command_line)

    if isinstance(token, TokenComma):
        _init_line_range(command_line)
        command_line.line_range.separator = TokenComma()
        # Vim resolves :1,2,3,4 to :3,4
        state.is_range_start_line_parsed = not state.is_range_start_line_parsed

        return _parse_line_ref, command_line

    if isinstance(token, TokenSemicolon):
        _init_line_range(command_line)
        command_line.line_range.separator = TokenSemicolon()
        # Vim resolves :1;2;3;4 to :3;4
        state.is_range_start_line_parsed = not state.is_range_start_line_parsed

        return _parse_line_ref, command_line

    if isinstance(token, TokenDigits):
        _init_line_range(command_line)

        return _process_digits(token, state, command_line)

    if isinstance(token, TokenDollar):
        _init_line_range(command_line)

        return _process_dollar(token, state, command_line)

    if isinstance(token, TokenPercent):
        _init_line_range(command_line)

        return _process_percent(token, state, command_line)

    if isinstance(token, TokenMark):
        _init_line_range(command_line)

        return _process_mark(token, state, command_line)

    if isinstance(token, TokenCommand):
        _init_line_range(command_line)
        command_line.command = token

        return None, command_line

    return None, command_line


def _process_mark(token: TokenMark, state: _ParserState, command_line: _ParsedCommandLine) -> tuple:
    if not state.is_range_start_line_parsed:
        command_line.line_range.start.append(token)
    else:
        command_line.line_range.end.append(token)

    return _parse_line_ref, command_line


def _process_percent(token: TokenPercent, state: _ParserState, command_line: _ParsedCommandLine) -> tuple:
    if not state.is_range_start_line_parsed:
        if command_line.line_range.start:
            raise ValueError('bad range: {0}'.format(state.scanner.state.source))
        command_line.line_range.start.append(token)
    else:
        if command_line.line_range.end:
            raise ValueError('bad range: {0}'.format(state.scanner.state.source))
        command_line.line_range.end.append(token)

    return _parse_line_ref, command_line


def _process_dollar(token: TokenDollar, state: _ParserState, command_line: _ParsedCommandLine) -> tuple:
    if not state.is_range_start_line_parsed:
        if command_line.line_range.start:
            raise ValueError('bad range: {0}'.format(state.scanner.state.source))
        command_line.line_range.start.append(token)
    else:
        if command_line.line_range.end:
            raise ValueError('bad range: {0}'.format(state.scanner.state.source))
        command_line.line_range.end.append(token)

    return _parse_line_ref, command_line


def _process_digits(token: TokenDigits, state: _ParserState, command_line: _ParsedCommandLine) -> tuple:
    if not state.is_range_start_line_parsed:
        if (command_line.line_range.start and command_line.line_range.start[-1]) == TokenDot():
            raise ValueError('bad range: {0}'.format(state.scanner.state.source))
        elif (command_line.line_range.start and isinstance(command_line.line_range.start[-1], TokenDigits)):
            command_line.line_range.start = [token]
        else:
            command_line.line_range.start.append(token)
    else:
        if (command_line.line_range.end and command_line.line_range.end[-1] == TokenDot()):
            raise ValueError('bad range: {0}'.format(state.scanner.state.source))
        elif (command_line.line_range.end and isinstance(command_line.line_range.end[-1], TokenDigits)):
            command_line.line_range.end = [token]
        else:
            command_line.line_range.end.append(token)

    return _parse_line_ref, command_line


def _process_search_forward(token: TokenSearchForward, state: _ParserState, command_line: _ParsedCommandLine) -> tuple:
    if not state.is_range_start_line_parsed:
        if command_line.line_range.start:
            # TODO Review start_offset looks unused
            command_line.line_range.start_offset = []
        command_line.line_range.start.append(token)
    else:
        if command_line.line_range.end:
            # TODO Review end_offset looks unused
            command_line.line_range.end_offset = []
        command_line.line_range.end.append(token)

    return _parse_line_ref, command_line


def _process_search_backward(token: TokenSearchBackward, state: _ParserState, command_line: _ParsedCommandLine) -> tuple:  # noqa: E501
    if not state.is_range_start_line_parsed:
        if command_line.line_range.start:
            # TODO Review start_offset looks unused
            command_line.line_range.start_offset = []
        command_line.line_range.start.append(token)
    else:
        if command_line.line_range.end:
            # TODO Review end_offset looks unused
            command_line.line_range.end_offset = []
        command_line.line_range.end.append(token)

    return _parse_line_ref, command_line


def _process_offset(token: TokenOffset, state: _ParserState, command_line: _ParsedCommandLine) -> tuple:
    if not state.is_range_start_line_parsed:
        if (command_line.line_range.start and command_line.line_range.start[-1] == TokenDollar()):
            raise ValueError('bad command line {}'.format(state.scanner.state.source))
        command_line.line_range.start.append(token)
    else:
        if (command_line.line_range.end and command_line.line_range.end[-1] == TokenDollar()):
            raise ValueError('bad command line {}'.format(state.scanner.state.source))
        command_line.line_range.end.append(token)

    return _parse_line_ref, command_line


def _process_dot(state: _ParserState, command_line: _ParsedCommandLine) -> tuple:
    if not state.is_range_start_line_parsed:
        if command_line.line_range.start and isinstance(command_line.line_range.start[-1], TokenOffset):
            raise ValueError('bad range {0}'.format(state.scanner.state.source))
        command_line.line_range.start.append(TokenDot())
    else:
        if command_line.line_range.end and isinstance(command_line.line_range.end[-1], TokenOffset):
            raise ValueError('bad range {0}'.format(state.scanner.state.source))
        command_line.line_range.end.append(TokenDot())

    return _parse_line_ref, command_line
