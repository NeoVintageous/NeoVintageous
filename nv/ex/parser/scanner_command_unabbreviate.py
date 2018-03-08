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
from .tokens_base import TOKEN_COMMAND_UNABBREVIATE
from .tokens_base import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('unabbreviate', 'una')
class TokenUnabbreviate(TokenOfCommand):
    def __init__(self, params, *args, **kwargs):
        super().__init__(params, TOKEN_COMMAND_UNABBREVIATE, 'unabbreviate', *args, **kwargs)
        self.target_command = 'ex_unabbreviate'

    @property
    def short(self):
        return self.params['lhs']


def scan_command_unabbreviate(state):
    params = {
        'lhs': None
    }
    m = state.expect_match(r'\s+(?P<lhs>.+?)\s*$')
    params.update(m.groupdict())
    return None, [TokenUnabbreviate(params), TokenEof()]
