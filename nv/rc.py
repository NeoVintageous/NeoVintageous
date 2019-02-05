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
    return os.path.join(sublime.packages_path(), 'User', '.vintageousrc')


def open(window):
    file = _file_name()

    if not os.path.exists(file):
        with builtins.open(file, 'w') as f:
            f.write('" Type :h vintageousrc for help.\n')

    window.open_file(file)


def load():
    _log.debug('load %s', _file_name())
    _load()


def reload():
    _log.debug('reload %s', _file_name())
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
        with builtins.open(_file_name(), 'r') as f:
            for line in f:
                ex_cmdline = _parse_line(line)
                if ex_cmdline:
                    do_ex_cmdline(window, ex_cmdline)

        print('vintageousrc file loaded')
    except FileNotFoundError:
        _log.info('vintageousrc file not found')


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

                # By default, mapping the character '|' (bar) should be escaped
                # with a slash or '<Bar>' used instead. Neovintageous currently
                # doesn't support '<Bar>' and internally doesn't require the bar
                # character to be escaped, but in order not to break backwards
                # compatibility in the future, this piece of code checks that
                # the mapping escapes the bar character correctly. This piece of
                # code can be removed when this is fixed in the core. See :help
                # map_bar for more details.
                if '|' in cmdline:
                    if '|' in cmdline.replace('\\|', ''):
                        raise Exception('E488: Trailing characters: {}'.format(line.rstrip()))

                    cmdline = cmdline.replace('\\|', '|')

                return cmdline
    except Exception:
        message('error detected while processing vintageousrc at line "{}"'.format(line.rstrip()))

    return None
