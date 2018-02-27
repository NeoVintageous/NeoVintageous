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

from .tokens import TOKEN_COMMAND_SET
from .tokens import TokenEof
from .tokens import TokenOfCommand


class TokenCommandSet(TokenOfCommand):
    def __init__(self, params, *args, **kwargs):
        super().__init__(params, TOKEN_COMMAND_SET, 'set', *args, **kwargs)
        self.target_command = 'ex_set'

    @property
    def value(self):
        return self.params['value']

    @property
    def option(self):
        return self.params['option']


def scan_cmd_set(state):
    params = {'option': None, 'value': None}

    state.skip(' ')
    state.ignore()

    m = state.expect_match(r'(?P<option>.+?)(?:[:=](?P<value>.+?))?$')
    params.update(m.groupdict())

    return None, [TokenCommandSet(params), TokenEof()]
