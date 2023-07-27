# Copyright (C) 2018-2023 The NeoVintageous Team (NeoVintageous).
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


def _file_name() -> str:
    return '.neovintageousrc'


def _file_path() -> str:
    return os.path.join(sublime.packages_path(), 'User', _file_name())


def open_rc(window) -> None:
    file = _file_path()

    if not os.path.exists(file):
        with builtins.open(file, 'w', encoding='utf-8') as f:
            f.write('" Type :help nv for help.\n')

    window.open_file(file)


def load_rc() -> None:
    _log.debug('load %s', _file_path())
    _load()


def reload_rc() -> None:
    _log.debug('reload %s', _file_path())
    _unload()
    _load()


def _unload() -> None:
    from NeoVintageous.nv.mappings import mappings_clear
    from NeoVintageous.nv.variables import variables_clear

    variables_clear()
    mappings_clear()
    _unload_cfgU()


def _load() -> None:
    try:
        from NeoVintageous.nv.ex_cmds import do_ex_cmdline
        window = sublime.active_window()
        with builtins.open(_file_path(), 'r', encoding='utf-8', errors='replace') as f:
            for line in f:
                ex_cmdline = _parse_line(line)
                if ex_cmdline:
                    do_ex_cmdline(window, ex_cmdline)

        print('%s file loaded' % _file_name())
    except FileNotFoundError:
        _log.info('%s file not found', _file_name())
    load_cfgU()


# Recursive mappings (:map, :nmap, :omap, :smap, :vmap) are not supported. They
# were removed in version 1.5.0. They were removed because they were they were
# implemented as non-recursive mappings.
_PARSE_LINE_PATTERN = re.compile(
    '^\\s*(?::)?(?P<cmdline>(?P<cmd>(?:[nsviox])?noremap|let|set|(?:[nsviox])?unmap) .*)$')


def _parse_line(line: str):
    try:
        line = line.rstrip()
        if line:
            match = _PARSE_LINE_PATTERN.match(line)
            if match:
                cmdline = match.group('cmdline')
                # Ensure there is leading colon, because the parser pattern omits it.
                if cmdline:
                    cmdline = ':' + cmdline

                # The '|' character is used to chain commands. Users should
                # escape it with a slash or use '<bar>'. See :h map-bar. It's
                # translated to <bar> internally (implementation detail).
                # See https://github.com/NeoVintageous/NeoVintageous/issues/615.
                cmdline = cmdline.replace('\\|', '<bar>')

                if '|' in cmdline:
                    # Using '|' to separate map commands is currently not supported.
                    raise Exception('E488: Trailing characters: {}'.format(line.rstrip()))

                return cmdline
    except Exception as e:
        message('error detected while processing {} at line "{}":\n{}'.format(_file_name(), line.rstrip(), str(e)))

    return None


from NeoVintageous.plugin import PACKAGE_NAME
from NeoVintageous.nv.vim import INSERT, INTERNAL_NORMAL, NORMAL, OPERATOR_PENDING, REPLACE, SELECT, UNKNOWN, VISUAL, VISUAL_BLOCK, VISUAL_LINE

cfgU_settings = (f'{PACKAGE_NAME}.sublime-settings')
class cfgU():

    @staticmethod
    def load():
        global user_settings

        win = sublime.active_window()

        cfgU.user_settings = user_settings

        cfgU.surround   = user_settings.get('surround'  , None)
        if not (surrT := type(cfgU.surround)) is dict:
            _log.warn(f"⚠️‘surround’ in ‘{cfgU_settings}’ should be a dictionary, not {surrT}")
            cfgU.surround = None


def load_cfgU() -> None: # load alternative user config file to a global class and add a watcher event to track changes
    # load user config file to a global class and add a watcher event to track changes
    global cfgU
    global user_settings

    try:
        user_settings = sublime.load_settings(cfgU_settings)
        cfgU.load();
        user_settings.clear_on_change(PACKAGE_NAME)
        user_settings.add_on_change  (PACKAGE_NAME, lambda: cfgU.load())
    except FileNotFoundError:
        _log.info(f'‘{cfgU_settings}’ file not found')

def _unload_cfgU() -> None: # clear config change watcher
    global cfgU
    global user_settings

    user_settings.clear_on_change(PACKAGE_NAME)
