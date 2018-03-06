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

from .parser import parse_command_line
from .tokens import TokenEof
from .tokens_base import TOKEN_COMMAND_MOVE
from .tokens_base import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('move', 'm')
class TokenMove(TokenOfCommand):
    def __init__(self, params, *args, **kwargs):
        super().__init__(params, TOKEN_COMMAND_MOVE, 'move', *args, **kwargs)
        self.addressable = True
        self.target_command = 'ex_move'

    @property
    def address(self):
        return self.params['address']


def scan_command_move(state):
    params = {
        'address': None
    }

    state.skip(' ')
    state.ignore()

    m = state.match(r'(?P<address>.*$)')
    if m:
        address_command_line = m.group(0).strip() or '.'
        params['address'] = parse_command_line(address_command_line).line_range

    return None, [TokenMove(params), TokenEof()]
