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

from .tokens import TOKEN_COMMAND_QUIT_ALL
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('quall', 'qa')
class TokenCommandQuitAll(TokenOfCommand):
    def __init__(self, *args, **kwargs):
        super().__init__({}, TOKEN_COMMAND_QUIT_ALL, 'qall', *args, **kwargs)
        self.target_command = 'ex_quit_all'


def scan_cmd_quit_all(state):
    bang = state.consume() == '!'

    # TODO [bug] ":command" followed by character that is not "!"  shouldn't be
    # valid e.g. the ":close" command should run when !:closex". There are a
    # bunch of commands that have this bug.

    state.expect_eof()

    return None, [TokenCommandQuitAll(forced=bang), TokenEof()]
