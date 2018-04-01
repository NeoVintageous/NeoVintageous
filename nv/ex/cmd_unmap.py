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


# TODO [refactor] All the map related scan functions can probably be consolidated into one scanner. They either parse one key (unmap commands), or command and key.  # noqa: E501
def scan_cmd_unmap(state):
    command = TokenCommand('unmap')
    params = {'keys': None}

    # TODO [refactor] Some commands require certain arguments e.g "keys" is a
    # required argument for the unmap ex command. Currently the do_ex_command
    # (may have  been refactored into another name), passes params to the ex
    # commands, and None is valid argument, but in the case of this command
    # it's a required argument, so rather than the ex command deal with the
    # invalid argument, it should be dealt with a) either here, or b) by the
    # command runner.

    m = state.match(r'\s*(?P<keys>.+?)\s*$')
    if m:
        params.update(m.groupdict())

    command.params = params

    return None, [command, TokenEof()]
