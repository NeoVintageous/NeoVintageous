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

from .tokens import TOKEN_COMMAND_CD
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('cd', 'cd')
class TokenCommandCd(TokenOfCommand):
    def __init__(self, params, *args, **kwargs):
        super().__init__(params, TOKEN_COMMAND_CD, 'cd', *args, **kwargs)
        self.target_command = 'ex_cd'

    @property
    def path(self):
        return self.params['path']

    @property
    def must_go_back(self):
        return self.params['-']


def scan_cmd_cd(state):
    params = {'path': None, '-': None}

    bang = state.consume() == '!'
    if not bang:
        state.backup()

    state.skip(' ')
    state.ignore()

    c = state.consume()
    if c == '-':
        params['-'] = '-'
        state.expect_eof()
        raise NotImplementedError('parameter not implemented')
    elif c != state.EOF:
        state.backup()
        m = state.match(r'(?P<path>.+?)\s*$')
        params.update(m.groupdict())

    return None, [TokenCommandCd(params, forced=bang), TokenEof()]
