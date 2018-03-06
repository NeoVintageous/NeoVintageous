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

from .state import EOF
from .tokens import TokenEof
from .tokens_base import TOKEN_COMMAND_DOUBLE_AMPERSAND
from .tokens_base import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('&&', '&&')
class TokenDoubleAmpersand(TokenOfCommand):
    def __init__(self, params, *args, **kwargs):
        super().__init__(params, TOKEN_COMMAND_DOUBLE_AMPERSAND, '&&', *args, **kwargs)
        self.addressable = True
        self.target_command = 'ex_double_ampersand'


def scan_command_double_ampersand(state):
    params = {
        'flags': [],
        'count': '',
    }

    m = state.match(r'\s*([cgr])*\s*(\d*)\s*$')
    params['flags'] = list(m.group(1)) if m.group(1) else []
    params['count'] = m.group(2) or ''

    state.expect(EOF)

    return None, [TokenDoubleAmpersand(params), TokenEof()]
