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

from .tokens import TOKEN_COMMAND_LET
from .tokens import TokenEof
from .tokens import TokenOfCommand


class TokenCommandLet(TokenOfCommand):
    def __init__(self, params, *args, **kwargs):
        super().__init__(params, TOKEN_COMMAND_LET, 'let', *args, **kwargs)
        self.target_command = 'ex_let'

    # All properties in command tokens are now deprecated and can eventually be removed.

    # TODO Looks unused now that ExLet uses params
    @property
    def variable_name(self):
        return self.params['name']

    # TODO Looks unused now that ExLet uses params
    @property
    def variable_value(self):
        return self.params['value']


def scan_cmd_let(state):
    params = {'name': None, 'value': None}

    m = state.expect_match(
        r'(?P<name>.+?)\s*=\s*(?P<value>.+?)\s*$',
        on_error=lambda: Exception("E121: Undefined variable"))

    params.update(m.groupdict())

    return None, [TokenCommandLet(params), TokenEof()]
