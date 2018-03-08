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

from .tokens import TOKEN_COMMAND_GLOBAL
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('global', 'g')
class TokenCommandGlobal(TokenOfCommand):
    def __init__(self, params, *args, **kwargs):
        super().__init__(params, TOKEN_COMMAND_GLOBAL, 'global', *args, **kwargs)
        self.addressable = True
        self.target_command = 'ex_global'

    @property
    def pattern(self):
        return self.params['pattern']

    @property
    def subcommand(self):
        return self.params['subcommand']


def scan_cmd_global(state):
    params = {'pattern': None, 'subcommand': None}

    c = state.consume()

    bang = c == '!'
    sep = c if not bang else c.consume()

    # TODO: we're probably missing legal separators.
    assert c in '!:?/\\&$', 'bad separator'

    state.ignore()

    while True:
        c = state.consume()

        if c == state.EOF:
            raise ValueError('unexpected EOF in: ' + state.source)

        if c == sep:
            state.backup()

            params['pattern'] = state.emit()

            state.consume()
            state.ignore()
            break

    command = state.match(r'.*$').group(0).strip()
    if command:
        params['subcommand'] = command

    return None, [TokenCommandGlobal(params, forced=bang), TokenEof()]
