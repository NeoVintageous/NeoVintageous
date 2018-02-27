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

from .tokens import TOKEN_COMMAND_TABNEXT
from .tokens import TokenEof
from .tokens import TokenOfCommand


class TokenCommandTabNext(TokenOfCommand):
    def __init__(self, *args, **kwargs):
        super().__init__([], TOKEN_COMMAND_TABNEXT, 'tabnext', *args, **kwargs)
        self.target_command = 'ex_tabnext'


def scan_cmd_tabnext(state):
    c = state.consume()
    if c == state.EOF:
        return None, [TokenCommandTabNext(), TokenEof()]

    bang = c == '!'

    return None, [TokenCommandTabNext(forced=bang), TokenEof()]
