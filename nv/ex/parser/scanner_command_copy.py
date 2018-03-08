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

from .tokens import TokenEof
from .tokens_base import TOKEN_COMMAND_COPY
from .tokens_base import TokenOfCommand
from .parser import parse_command_line
from NeoVintageous.nv import ex


@ex.command('copy', 'co')
class TokenCopy(TokenOfCommand):
    def __init__(self, params, *args, **kwargs):
        super().__init__(params, TOKEN_COMMAND_COPY, 'copy', *args, **kwargs)
        self.addressable = True
        self.target_command = 'ex_copy'

    @property
    def address(self):
        return self.params['address']

    def calculate_address(self):
        # TODO: must calc only the first line ref?
        calculated = parse_command_line(self.address)
        if calculated is None:
            return None

        assert calculated.command is None, 'bad address'
        assert calculated.line_range.separator is None, 'bad address'

        return calculated.line_range


def scan_command_copy(state):
    params = {
        'address': None
    }

    m = state.expect_match(r'\s*(?P<address>.+?)\s*$')
    params.update(m.groupdict())

    return None, [TokenCopy(params), TokenEof()]
