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


def scan_cmd_cd(state):
    command = TokenCommand('cd')

    # TODO [refactor] Should params should used keys compatible with **kwargs? (review other commands too) # noqa: E501
    params = {'path': None, '-': None}
    bang = False

    c = state.consume()
    if c == state.EOF:
        command.params = params
        command.forced = bang

        return None, [command, TokenEof()]

    bang = c == '!'
    if not bang:
        state.backup()

    state.skip(' ')
    state.ignore()

    c = state.consume()
    if c == state.EOF:
        command.params = params
        command.forced = bang

        return None, [command, TokenEof()]

    if c == '-':
        raise NotImplementedError('parameter not implemented')

    state.backup()
    m = state.match(r'(?P<path>.+?)\s*$')
    params.update(m.groupdict())

    command.params = params
    command.forced = bang

    return None, [command, TokenEof()]
