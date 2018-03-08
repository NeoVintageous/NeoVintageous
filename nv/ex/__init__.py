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


command_names = []  # Used to provide completions on the ex command line.


def command(name, abbrev):
    # Register the name of an ex command with command_names.
    #
    # Meant to be imported like this:
    #
    #     from NeoVintageous.nv import ex
    #     ...
    #     @ex.command('foo', 'f')
    #     class ExFooCommand(...): ...

    command_names.append((name, abbrev))

    def inner(f):
        return f

    return inner
