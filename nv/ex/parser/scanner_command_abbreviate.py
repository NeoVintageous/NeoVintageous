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
from .tokens_base import TOKEN_COMMAND_ABBREVIATE
from .tokens_base import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('abbreviate', 'ab')
class TokenCommandAbbreviate(TokenOfCommand):
    def __init__(self, params, *args, **kwargs):
        super().__init__(params, TOKEN_COMMAND_ABBREVIATE, 'write', *args, **kwargs)
        self.target_command = 'ex_abbreviate'

    @property
    def short(self):
        return self.params['short']

    @property
    def full(self):
        return self.params['full']


def scan_command_abbreviate(state):
    params = {
        'short': None,
        'full': None,
    }

    state.expect(' ')
    state.skip(' ')
    state.ignore()

    if state.consume() == EOF:
        return None, [TokenCommandAbbreviate({}), TokenEof()]

    state.backup()

    m = state.match(r'(?P<short>.+?)(?: +(?P<full>.+))?$')
    params.update(m.groupdict())

    return None, [TokenCommandAbbreviate(params), TokenEof()]
