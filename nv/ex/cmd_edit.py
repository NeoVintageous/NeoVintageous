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
from .tokens import TokenCommand


def scan_cmd_edit(state):
    command = TokenCommand('edit')
    # TODO [refactor] Should params should used keys compatible with **kwargs? (review other commands too) # noqa: E501
    params = {
        '++': None,
        'cmd': None,
        'file_name': None,
        'count': None,
    }

    c = state.consume()
    if c == state.EOF:
        command.params = params

        return None, [command, TokenEof()]

    bang = c == '!'
    if not bang:
        state.backup()

    plus_plus_translations = {
        'ff': 'fileformat',
        'bin': 'binary',
        'enc': 'fileencoding',
        'nobin': 'nobinary'
    }

    while True:
        c = state.consume()

        if c == state.EOF:
            command.params = params
            command.forced = bang

            return None, [command, TokenEof()]

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
                params['++'] = plus_plus_translations.get(name, name)

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

    command.params = params
    command.forced = bang

    return None, [command, TokenEof()]
