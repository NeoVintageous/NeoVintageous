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

from NeoVintageous.nv.ex.plat import unixlike


def run_and_wait(view, cmd):
    unixlike.run_and_wait(view, cmd, 'VintageousEx_linux_terminal')


def run_and_read(view, cmd):
    return unixlike.run_and_read(view, cmd)


def filter_region(view, text, command):
    return unixlike.filter_region(
        view, text, command, 'VintageousEx_linux_shell')
