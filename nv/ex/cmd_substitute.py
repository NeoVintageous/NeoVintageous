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

from .tokens import TOKEN_COMMAND_SUBSTITUTE
from .tokens import TokenEof
from .tokens import TokenOfCommand


class TokenCommandSubstitute(TokenOfCommand):
    def __init__(self, params, *args, **kwargs):
        super().__init__(params, TOKEN_COMMAND_SUBSTITUTE, 'substitute', *args, **kwargs)
        self.addressable = True
        self.target_command = 'ex_substitute'


def _scan_cmd_substitute_params(state):
    state.backup()
    delim = state.consume()
    # TODO [refactor] Rename search_term -> pattern
    params = {
        "search_term": None,
        "replacement": None,
        "count": 1,
        "flags": [],
    }

    while True:
        c = state.consume()

        if c == delim:
            state.start += 1
            state.backup()
            params['search_term'] = state.emit()
            state.consume()
            break

        if c == state.EOF:
            raise ValueError("bad command: {0}".format(state.source))

    while True:
        c = state.consume()
        if c == delim:
            state.start += 1
            state.backup()
            params['replacement'] = state.emit()
            state.consume()
            state.ignore()
            break

        if c == state.EOF:
            state.start += 1
            params['replacement'] = state.emit()
            state.consume()
            state.ignore()
            break

    if state.match(r'\s*[&cegiInp#lr]+'):
        params['flags'] = list(state.emit().strip())
        if '&' in params['flags'] and params['flags'][0] != '&':
            raise ValueError("bad command: {}".format(state.source))

    if state.peek(' '):
        state.skip(' ')
        state.ignore()
        if state.match(r'\d+'):
            params['count'] = int(state.emit())

    state.skip(' ')
    state.ignore()
    state.expect_eof()

    return None, [TokenCommandSubstitute(params), TokenEof()]


def scan_cmd_substitute(state):
    delim = state.consume()

    if delim == state.EOF:
        return None, [TokenCommandSubstitute(None), TokenEof()]

    return _scan_cmd_substitute_params(state)
