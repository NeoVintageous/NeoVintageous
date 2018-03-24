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

from .tokens import TOKEN_COMMAND_NEW
from .tokens import TokenEof
from .tokens import TokenOfCommand


class TokenCommandNew(TokenOfCommand):
    def __init__(self, params, *args, **kwargs):
        super().__init__(params, TOKEN_COMMAND_NEW, 'new', *args, **kwargs)
        self.target_command = 'ex_new'


def scan_cmd_new(state):
    # TODO [refactor] params should used keys compatible with **kwargs, see do_ex_command(). Review other scanners too. # noqa: E501
    params = {'++': None, 'cmd': None}

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

        plus_plus_translations = {
            'ff': 'fileformat',
            'bin': 'binary',
            'enc': 'fileencoding',
            'nobin': 'nobinary'
        }

        params['++'] = plus_plus_translations.get(name, name)
        state.ignore()

        raise NotImplementedError(':new not fully implemented')

    m = state.match(r'.+$')
    if m:
        params['cmd'] = m.group(0).strip()
        raise NotImplementedError(':new not fully implemented')

    return None, [TokenCommandNew(params), TokenEof()]
