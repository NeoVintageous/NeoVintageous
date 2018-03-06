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

from .tokens import TOKEN_COMMAND_WRITE
from .tokens import TokenEof
from .tokens import TokenOfCommand

_plus_plus_translations = {
    'ff': 'fileformat',
    'bin': 'binary',
    'enc': 'fileencoding',
    'nobin': 'nobinary',
}


class TokenCommandWrite(TokenOfCommand):
    def __init__(self, params, *args, **kwargs):
        super().__init__(params, TOKEN_COMMAND_WRITE, 'write', *args, **kwargs)
        self.addressable = True
        self.target_command = 'ex_write'

    @property
    def options(self):
        return self.params['++']

    @property
    def target_file(self):
        return self.params['file_name']

    @property
    def appends(self):
        return self.params['>>']

    @property
    def command(self):
        return self.params['cmd']


def scan_cmd_write(state):
    # TODO [refactor] params should used keys compatible with **kwargs, see do_ex_command(). Review other scanners too. # noqa: E501
    params = {
        '++': '',
        'file_name': '',
        '>>': False,
        'cmd': '',
    }

    bang = state.consume()
    if bang == state.EOF:
        return None, [TokenCommandWrite(params), TokenEof()]

    if bang != '!':
        bang = False
        state.backup()

    state.skip(' ')
    state.ignore()

    while True:
        c = state.consume()
        if c == state.EOF:
            # TODO: forced?
            return None, [TokenCommandWrite(params, forced=bang), TokenEof()]

        if c == '+':
            state.expect('+')
            state.ignore()
            # TODO: expect_match should work with emit()
            # https://vimhelp.appspot.com/editing.txt.html#[++opt]
            m = state.expect_match(
                r'(?:f(?:ile)?f(?:ormat)?|(?:file)?enc(?:oding)?|(?:no)?bin(?:ary)?|bad|edit)(?=\s|$)',
                lambda: Exception("E474: Invalid argument"))

            name = m.group(0)
            params['++'] = _plus_plus_translations.get(name, name)
            state.ignore()
            continue

        if c == '>':
            state.expect('>')
            state.ignore()
            params['>>'] = True
            state.match(r'.*$')
            params['file_name'] = state.emit().strip()
            continue

        if c == '!':
            state.ignore()
            state.match(r'.*$')
            params['cmd'] = state.emit()
            continue

        if c != ' ':
            state.match(r'.*')
            params['file_name'] = state.emit().strip()
            state.skip(' ')
            state.ignore()

    state.expect_eof()

    return None, [TokenCommandWrite(params, forced=bang == '!'), TokenEof()]
