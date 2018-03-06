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

"""Parsing for the Vim command line."""

# IMPORTANT! Some imports are at the bottom to avoid circular refs.

from .nodes import CommandLineNode
from .nodes import RangeNode
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
from .tokens_base import TokenOfCommand
from NeoVintageous.nv.vim import get_logger


_log = get_logger(__name__)


class ParserState():

    # Args:
    #   :source (str):
    #
    # Attributes:
    #   :scanner (Scanner):
    #   :is_range_start_line_parsed (bool): Default is false.
    #   :tokens:

    def __init__(self, source):
        self.scanner = Scanner(source)
        self.is_range_start_line_parsed = False
        self.tokens = self.scanner.scan()

    def next_token(self):
        return next(self.tokens)


def parse_command_line(source):
    # The parser works its way through the command line by passing the current
    # state to the next parsing function. It stops when no parsing funcion is
    # returned from the previous one.
    #
    # Args:
    #   :source (str):
    #
    # Returns:
    #   CommandLineNode

    state = ParserState(source)
    parse_func = parse_line_ref
    command_line = CommandLineNode(None, None)
    while True:
        parse_func, command_line = parse_func(state, command_line)
        if parse_func is None:
            command_line.validate()

            _log.debug('cmdline command {}'.format(command_line))

            return command_line


def init_line_range(command_line):
    if command_line.line_range:
        return

    command_line.line_range = RangeNode()


def parse_line_ref(state, command_line):
    token = state.next_token()

    if isinstance(token, TokenEof):
        return None, command_line

    if isinstance(token, TokenDot):
        init_line_range(command_line)

        return process_dot(state, command_line)

    if isinstance(token, TokenOffset):
        init_line_range(command_line)

        return process_offset(token, state, command_line)

    if isinstance(token, TokenSearchForward):
        init_line_range(command_line)

        return process_search_forward(token, state, command_line)

    if isinstance(token, TokenSearchBackward):
        init_line_range(command_line)

        return process_search_backward(token, state, command_line)

    if isinstance(token, TokenComma):
        init_line_range(command_line)
        command_line.line_range.separator = TokenComma()
        # Vim resolves :1,2,3,4 to :3,4
        state.is_range_start_line_parsed = not state.is_range_start_line_parsed

        return parse_line_ref, command_line

    if isinstance(token, TokenSemicolon):
        init_line_range(command_line)
        command_line.line_range.separator = TokenSemicolon()
        # Vim resolves :1;2;3;4 to :3;4
        state.is_range_start_line_parsed = not state.is_range_start_line_parsed

        return parse_line_ref, command_line

    if isinstance(token, TokenDigits):
        init_line_range(command_line)

        return process_digits(token, state, command_line)

    if isinstance(token, TokenDollar):
        init_line_range(command_line)

        return process_dollar(token, state, command_line)

    if isinstance(token, TokenPercent):
        init_line_range(command_line)

        return process_percent(token, state, command_line)

    if isinstance(token, TokenMark):
        init_line_range(command_line)

        return process_mark(token, state, command_line)

    if isinstance(token, TokenOfCommand):
        init_line_range(command_line)
        command_line.command = token

        return None, command_line

    return None, command_line


def process_mark(token, state, command_line):
    if not state.is_range_start_line_parsed:
        command_line.line_range.start.append(token)
    else:
        command_line.line_range.end.append(token)

    return parse_line_ref, command_line


def process_percent(token, state, command_line):
    if not state.is_range_start_line_parsed:
        if command_line.line_range.start:
            raise ValueError('bad range: {0}'.format(state.scanner.state.source))
        command_line.line_range.start.append(token)
    else:
        if command_line.line_range.end:
            raise ValueError('bad range: {0}'.format(state.scanner.state.source))
        command_line.line_range.end.append(token)

    return parse_line_ref, command_line


def process_dollar(token, state, command_line):
    if not state.is_range_start_line_parsed:
        if command_line.line_range.start:
            raise ValueError('bad range: {0}'.format(state.scanner.state.source))
        command_line.line_range.start.append(token)
    else:
        if command_line.line_range.end:
            raise ValueError('bad range: {0}'.format(state.scanner.state.source))
        command_line.line_range.end.append(token)

    return parse_line_ref, command_line


def process_digits(token, state, command_line):
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
    return parse_line_ref, command_line


def process_search_forward(token, state, command_line):
    if not state.is_range_start_line_parsed:
        if command_line.line_range.start:
            command_line.line_range.start_offset = []
        command_line.line_range.start.append(token)
    else:
        if command_line.line_range.end:
            command_line.line_range.end_offset = []
        command_line.line_range.end.append(token)

    return parse_line_ref, command_line


def process_search_backward(token, state, command_line):
    if not state.is_range_start_line_parsed:
        if command_line.line_range.start:
            command_line.line_range.start_offset = []
        command_line.line_range.start.append(token)
    else:
        if command_line.line_range.end:
            command_line.line_range.end_offset = []
        command_line.line_range.end.append(token)

    return parse_line_ref, command_line


def process_offset(token, state, command_line):
    if not state.is_range_start_line_parsed:
        if (command_line.line_range.start and command_line.line_range.start[-1] == TokenDollar()):
            raise ValueError('bad command line {}'.format(state.scanner.state.source))
        command_line.line_range.start.append(token)
    else:
        if (command_line.line_range.end and command_line.line_range.end[-1] == TokenDollar()):
            raise ValueError('bad command line {}'.format(state.scanner.state.source))
        command_line.line_range.end.append(token)

    return parse_line_ref, command_line


def process_dot(state, command_line):
        init_line_range(command_line)
        if not state.is_range_start_line_parsed:
            if command_line.line_range.start and isinstance(command_line.line_range.start[-1], TokenOffset):
                raise ValueError('bad range {0}'.format(state.scanner.state.source))
            command_line.line_range.start.append(TokenDot())
        else:
            if command_line.line_range.end and isinstance(command_line.line_range.end[-1], TokenOffset):
                raise ValueError('bad range {0}'.format(state.scanner.source))
            command_line.line_range.end.append(TokenDot())

        return parse_line_ref, command_line


# IMPORTANT! Avoid circular refs. Some subscanners import parse_command_line()
from .scanner import Scanner  # FIXME # noqa: E402
