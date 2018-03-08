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

from .tokens import TOKEN_COMMAND_BUFFERS
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('buffers', 'buffers')
@ex.command('files', 'files')
@ex.command('ls', 'ls')
class TokenCommandBuffers(TokenOfCommand):
    def __init__(self, *args, **kwargs):
        super().__init__({}, TOKEN_COMMAND_BUFFERS, 'buffers', *args, **kwargs)
        self.target_command = 'ex_prompt_select_open_file'


def scan_cmd_buffers(state):
    try:
        state.expect_eof()
    except ValueError:
        # TODO Use a special domain exception for exceptions raised in scans.
        raise Exception("E488: Trailing characters")

    return None, [TokenCommandBuffers(), TokenEof()]
