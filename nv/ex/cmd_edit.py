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

from .tokens import TOKEN_COMMAND_EDIT
from .tokens import TokenEof
from .tokens import TokenOfCommand

_plus_plus_translations = {
    'ff': 'fileformat',
    'bin': 'binary',
    'enc': 'fileencoding',
    'nobin': 'nobinary',
}


class TokenCommandEdit(TokenOfCommand):
    def __init__(self, params, *args, **kwargs):
        super().__init__(params, TOKEN_COMMAND_EDIT, 'edit', *args, **kwargs)
        self.target_command = 'ex_edit'


def scan_cmd_edit(state):
    # TODO [refactor] params should used keys compatible with **kwargs, see do_ex_command(). Review other scanners too. # noqa: E501
    params = {
        '++': None,
        'cmd': None,
        'file_name': None,
        'count': None,
    }

    c = state.consume()
    if c == state.EOF:
        return None, [TokenCommandEdit(params), TokenEof()]

    bang = c == '!'
    if not bang:
        state.backup()

    while True:
        c = state.consume()

        if c == state.EOF:
            return None, [TokenCommandEdit(params, forced=bang), TokenEof()]

        if c == '+':
            k = state.consume()
            if k == '+':
                state.ignore()
                # TODO: expect_match should work with emit()
                # https://vimhelp.appspot.com/editing.txt.html#[++opt]
                m = state.expect_match(
                    r'(?:f(?:ile)?f(?:ormat)?|(?:file)?enc(?:oding)?|(?:no)?bin(?:ary)?|bad|edit)(?=\s|$)',
                    lambda: Exception("E474: Invalid argument"))

                name = m.group(0)
                params['++'] = _plus_plus_translations.get(name, name)

                state.ignore()

                raise NotImplementedError('param not implemented')
                continue

            state.backup()
            state.ignore()
            state.expect_match(r'.+$')

            params['cmd'] = state.emit()

            raise NotImplementedError('param not implemented')
            continue

        if c != ' ':
            state.match(r'.*')
            params['file_name'] = state.emit().strip()

            state.skip(' ')
            state.ignore()
            continue

        if c == '#':
            state.ignore()
            m = state.expect_match(r'\d+')
            params['count'] = m.group(0)

            raise NotImplementedError('param not implemented')
            continue

    return None, [TokenCommandEdit(params, forced=bang), TokenEof()]
