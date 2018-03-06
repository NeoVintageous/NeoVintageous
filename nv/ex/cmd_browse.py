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

from .tokens import TOKEN_COMMAND_BROWSE
from .tokens import TokenEof
from .tokens import TokenOfCommand


class TokenCommandBrowse(TokenOfCommand):
    def __init__(self, params, *args, **kwargs):
        super().__init__(params, TOKEN_COMMAND_BROWSE, 'browse', *args, **kwargs)
        self.target_command = 'ex_browse'


def scan_cmd_browse(state):
    # TODO [review] "cmd" param looks unused.
    params = {'cmd': None}

    state.skip(' ')
    state.ignore()

    m = state.match(r'(?P<cmd>.*)$')

    params.update(m.groupdict())
    if params['cmd']:
        raise NotImplementedError('parameter not implemented')

    return None, [TokenCommandBrowse(params), TokenEof()]
