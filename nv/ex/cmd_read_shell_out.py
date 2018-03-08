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

from .tokens import TOKEN_COMMAND_READ_SHELL_OUT
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


plus_plus_translations = {
    'ff': 'fileformat',
    'bin': 'binary',
    'enc': 'fileencoding',
    'nobin': 'nobinary',
}


@ex.command('read', 'r')
class TokenCommandReadShellOut(TokenOfCommand):
    def __init__(self, params, *args, **kwargs):
        super().__init__(params, TOKEN_COMMAND_READ_SHELL_OUT, 'read', *args, **kwargs)
        self.target_command = 'ex_read_shell_out'

    @property
    def command(self):
        return self.params['cmd']

    @property
    def file_name(self):
        return self.params['file_name']

    @property
    def plusplus(self):
        return self.params['++']


def scan_cmd_read_shell_out(state):
    params = {
        'cmd': None,
        '++': [],
        'file_name': None,
    }

    state.skip(' ')
    state.ignore()

    c = state.consume()

    if c == '+':
        state.expect('+')
        state.ignore()
        # TODO: expect_match should work with emit()
        # https://vimhelp.appspot.com/editing.txt.html#[++opt]
        m = state.expect_match(
            r'(?:f(?:ile)?f(?:ormat)?|(?:file)?enc(?:oding)?|(?:no)?bin(?:ary)?|bad|edit)(?=\s|$)',
            lambda: Exception("E474: Invalid argument"))
        name = m.group(0)
        params['++'] = plus_plus_translations.get(name, name)
        state.ignore()
        raise NotImplementedError('++opt not implemented')

    elif c == '!':
        m = state.match(r'(?P<cmd>.+)')
        params.update(m.groupdict())

    else:
        state.backup()
        m = state.match(r'(?P<file_name>.+)$')
        params.update(m.groupdict())

    state.expect_eof()

    return None, [TokenCommandReadShellOut(params), TokenEof()]
