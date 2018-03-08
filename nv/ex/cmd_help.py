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

from .tokens import TOKEN_COMMAND_HELP
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('help', 'h')
class TokenCommandHelp(TokenOfCommand):
    def __init__(self, params, *args, **kwargs):
        super().__init__(params, TOKEN_COMMAND_HELP, 'help', *args, **kwargs)
        self.target_command = 'ex_help'

    @property
    def subject(self):
        return self.params['subject']


def scan_cmd_help(state):
    match = state.expect_match(r'(?P<bang>!)?\s*(?P<subject>.+)?$').groupdict()
    params = {'subject': match['subject']}
    bang = bool(match['bang'])

    return None, [TokenCommandHelp(params, forced=bang), TokenEof()]
