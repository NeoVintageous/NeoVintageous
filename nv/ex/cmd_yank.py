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

from .tokens import TOKEN_COMMAND_YANK
from .tokens import TokenEof
from .tokens import TokenOfCommand


class TokenCommandYank(TokenOfCommand):
    def __init__(self, params, *args, **kwargs):
        super().__init__(params, TOKEN_COMMAND_YANK, 'yank', *args, **kwargs)
        self.addressable = True
        self.target_command = 'ex_yank'

    @property
    def register(self):
        return self.params['register']

    @property
    def count(self):
        return self.params['count']


def scan_cmd_yank(state):
    params = {'register': '"', 'count': None}

    state.skip(' ')
    state.ignore()

    c = state.consume()
    if c == state.EOF:
        return None, [TokenCommandYank(params), TokenEof()]

    state.backup()
    state.skip(' ')
    state.ignore()

    m = state.expect_match(r'(?P<register>[a-zA-Z0-9"])(?:\s+(?P<count>\d+))?\s*$')

    params.update(m.groupdict())
    if params['count']:
        raise NotImplementedError('parameter not implemented')

    return None, [TokenCommandYank(params), TokenEof()]
