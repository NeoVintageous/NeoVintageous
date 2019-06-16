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
import sys
import tempfile

# https://mypy.readthedocs.io/en/latest/common_issues.html#python-version-and-system-platform-checks
assert sys.platform.startswith('win')

try:
    import ctypes
except ImportError:
    from sublime import platform
    if platform() == 'windows':
        raise EnvironmentError('ctypes module missing for Windows.')

    ctypes = None


def get_startup_info():
    # Hide the child process window.
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    return startupinfo


def get_oem_cp():
    # type: (...) -> str
    return str(ctypes.windll.kernel32.GetOEMCP())


def run_and_wait(view, cmd):
    # type: (...) -> None
    subprocess.Popen(['cmd.exe', '/c', cmd + '&& pause']).wait()


def run_and_read(view, cmd):
    # type: (...) -> str
    out, err = subprocess.Popen(['cmd.exe', '/c', cmd],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=True,
                                startupinfo=get_startup_info()).communicate()

    try:
        return (out or err).decode(get_oem_cp()).replace('\r\n', '\n')
    except AttributeError:
        return ''


def filter_region(view, txt, command):
    # type: (...) -> str
    try:
        contents = tempfile.NamedTemporaryFile(suffix='.txt', delete=False)
        contents.write(txt.encode('utf-8'))
        contents.close()

        script = tempfile.NamedTemporaryFile(suffix='.bat', delete=False)
        script.write(('@echo off\ntype %s | %s' % (contents.name, command)).encode('utf-8'))
        script.close()

        p = subprocess.Popen([script.name],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             startupinfo=get_startup_info())

        out, err = p.communicate()

        return (out or err).decode(get_oem_cp()).replace('\r\n', '\n')[:-1].strip()
    finally:
        os.remove(script.name)
        os.remove(contents.name)
