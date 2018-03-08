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

from .tokens import TOKEN_COMMAND_SHELL_OUT
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('!', '!')
class TokenCommandShellOut(TokenOfCommand):
    def __init__(self, params, *args, **kwargs):
        super().__init__(params, TOKEN_COMMAND_SHELL_OUT, '!', *args, **kwargs)
        self.addressable = True
        self.target_command = 'ex_shell_out'

    @property
    def command(self):
        return self.params['cmd']


def scan_cmd_shell_out(state):
    params = {'cmd': None}

    m = state.expect_match(r'(?P<cmd>.+)$')
    params.update(m.groupdict())

    return None, [TokenCommandShellOut(params), TokenEof()]
