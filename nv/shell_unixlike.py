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


def run_and_wait(view, cmd, terminal_setting_name) -> None:
    term = view.settings().get(terminal_setting_name)
    term = term or os.path.expandvars("$COLORTERM") or os.path.expandvars("$TERM")
    subprocess.Popen([
        term,
        '-e',
        "bash -c \"%s; read -p 'Press RETURN to exit.'\"" % (cmd)
    ]).wait()


def run_and_read(view, cmd) -> str:
    out, err = subprocess.Popen([cmd],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=True).communicate()

    try:
        return (out or err).decode('utf-8')
    except AttributeError:
        return ''


def filter_region(view, text, command, shell_setting_name) -> str:
    shell = view.settings().get(shell_setting_name)
    shell = shell or os.path.expandvars("$SHELL")

    # Redirect STDERR to STDOUT to capture both.
    # This seems to be the behavior of vim as well.
    p = subprocess.Popen([shell, '-c', command],
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)

    # Pass in text as input: saves having to deal with quoting stuff.
    out, _ = p.communicate(text.encode('utf-8'))

    return out.decode('utf-8', errors='backslashreplace')
