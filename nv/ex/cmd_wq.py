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

from .tokens import TOKEN_COMMAND_WQ
from .tokens import TokenEof
from .tokens import TokenOfCommand

_plus_plus_translations = {
    'ff': 'fileformat',
    'bin': 'binary',
    'enc': 'fileencoding',
    'nobin': 'nobinary',
}


class TokenCommandWq(TokenOfCommand):
    def __init__(self, params, *args, **kwargs):
        super().__init__(params, TOKEN_COMMAND_WQ, 'wq', *args, **kwargs)
        self.target_command = 'ex_wq'


def scan_cmd_wq(state):
    # TODO [review] None of the prams looks used
    params = {
        '++': None,
        'file': None,
    }

    c = state.consume()
    if c == state.EOF:
        return None, [TokenCommandWq(params), TokenEof()]

    bang = True if c == '!' else False
    if not bang:
        state.backup()

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
        params['++'] = _plus_plus_translations.get(name, name)

        state.ignore()
        raise NotImplementedError('param not implemented')

    if c == state.EOF:
        return None, [TokenCommandWq(params), TokenEof()]

    m = state.expect_match(r'.+$')
    params['file'] = m.group(0).strip()

    return None, [TokenCommandWq(params), TokenEof()]
