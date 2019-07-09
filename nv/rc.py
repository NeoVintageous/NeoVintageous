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

import builtins
import logging
import os
import re

import sublime

from NeoVintageous.nv.vim import message


_log = logging.getLogger(__name__)


def _file_name():
    return '.neovintageousrc'


def _file_path():
    return os.path.join(sublime.packages_path(), 'User', _file_name())


def open(window):
    file = _file_path()

    if not os.path.exists(file):
        with builtins.open(file, 'w') as f:
            f.write('" Type :h neovintageousrc for help.\n')

    window.open_file(file)


def load():
    _log.debug('load %s', _file_path())
    _load()


def reload():
    _log.debug('reload %s', _file_path())
    _unload()
    _load()


def _unload():
    from NeoVintageous.nv.mappings import mappings_clear
    from NeoVintageous.nv.variables import variables_clear

    variables_clear()
    mappings_clear()


def _load():
    try:
        from NeoVintageous.nv.ex_cmds import do_ex_cmdline
        window = sublime.active_window()
        with builtins.open(_file_path(), 'r') as f:
            for line in f:
                ex_cmdline = _parse_line(line)
                if ex_cmdline:
                    do_ex_cmdline(window, ex_cmdline)

        print('%s file loaded' % _file_name())
    except FileNotFoundError:
        _log.info('%s file not found', _file_name())


# Recursive mappings (:map, :nmap, :omap, :smap, :vmap) are not supported. They
# were removed in version 1.5.0. They were removed because they were they were
# implemented as non-recursive mappings.
_PARSE_LINE_PATTERN = re.compile(
    '^(?::)?(?P<cmdline>(?P<cmd>noremap|nnoremap|snoremap|vnoremap|onoremap|let) .*)$')


def _parse_line(line):
    try:
        line = line.rstrip()
        if line:
            match = _PARSE_LINE_PATTERN.match(line)
            if match:
                cmdline = match.group('cmdline')
                # Ensure there is leading colon, because the parser pattern omits it.
                if cmdline:
                    cmdline = ':' + cmdline

                # Since the '|' character is used to separate a map command from
                # the next command, you will have to do something special to
                # include a '|' in {rhs}. You can use '<bar>' or escape with a
                # slash '\|'. See :h map-bar. TODO Refactor logic for
                # translating escaped bar to <bar> into mapping internals.
                cmdline = cmdline.replace('\\|', '<bar>')

                if '|' in cmdline:
                    # Using '|' to separate map commands is currently not supported.
                    raise Exception('E488: Trailing characters: {}'.format(line.rstrip()))

                return cmdline
    except Exception as e:
        message('error detected while processing {} at line "{}":\n{}'.format(_file_name(), line.rstrip(), str(e)))

    return None
