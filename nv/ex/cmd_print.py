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

from .tokens import TOKEN_COMMAND_PRINT
from .tokens import TokenEof
from .tokens import TokenOfCommand


class TokenCommandPrint(TokenOfCommand):
    def __init__(self, params, *args, **kwargs):
        super().__init__(params, TOKEN_COMMAND_PRINT, 'print', *args, **kwargs)
        self.addressable = True
        self.cooperates_with_global = True
        self.target_command = 'ex_print'

    # TODO [review] This should be redundant. The base token str cast should be enough. NOTE: The exGlobal command has dep. on this.  # noqa: E501
    def __str__(self):
        return "{0} {1} {2}".format(self.content, ''.join(self.params['flags']), self.params['count']).strip()


def scan_cmd_print(state):
    # TODO [review] count param looks unused.
    params = {'count': '', 'flags': []}

    while True:
        c = state.consume()

        state.skip(' ')
        state.ignore()

        if c == state.EOF:
            return None, [TokenCommandPrint(params), TokenEof()]

        if c.isdigit():
            state.match(r'\d*')
            params['count'] = state.emit()
            continue

        m = state.expect_match(r'[l#p]+')
        params['flags'] = list(m.group(0))
        state.ignore()
        state.expect_eof()
        break

    return None, [TokenCommandPrint(params), TokenEof()]
