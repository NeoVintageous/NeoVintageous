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

from .tokens import TOKEN_COMMAND_MOVE
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('move', 'm')
class TokenCommandMove(TokenOfCommand):
    def __init__(self, params, *args, **kwargs):
        super().__init__(params, TOKEN_COMMAND_MOVE, 'move', *args, **kwargs)
        self.addressable = True
        self.target_command = 'ex_move'

    @property
    def address(self):
        return self.params['address']


def scan_cmd_move(state):
    params = {'address': None}

    state.skip(' ')
    state.ignore()

    m = state.match(r'(?P<address>.*$)')
    if m:
        address_command_line = m.group(0).strip() or '.'
        params['address'] = address_command_line

    return None, [TokenCommandMove(params), TokenEof()]
