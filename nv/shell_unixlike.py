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

import os
import subprocess

from NeoVintageous.nv.options import get_option
from NeoVintageous.nv.settings import get_setting


def open(view) -> None:
    term = get_setting(view, 'terminal', os.environ.get('TERM'))
    if term:
        subprocess.Popen([term, '-e', 'bash'], cwd=os.getcwd())


def read(view, cmd: str) -> str:
    p = subprocess.Popen([get_option(view, 'shell'), '-c', cmd],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)

    out, err = p.communicate()

    if out:
        return out.decode('utf-8')

    if err:
        return err.decode('utf-8')

    return ''


def filter_region(view, text: str, cmd: str) -> str:
    # Redirect STDERR to STDOUT to capture both.
    # This seems to be the behavior of vim as well.
    p = subprocess.Popen([get_option(view, 'shell'), '-c', cmd],
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)

    # Pass in text as input: saves having to deal with quoting stuff.
    out, _ = p.communicate(text.encode('utf-8'))

    return out.decode('utf-8', errors='backslashreplace')
