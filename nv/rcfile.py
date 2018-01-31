import os
import re

import sublime

from NeoVintageous.nv.nvim import get_logger
from NeoVintageous.nv.nvim import message


_log = get_logger(__name__)

# Why is the builtin open function being aliased? In a nutshell: so that this
# module can provide a succinct and concise api for opening the rcfile e.g.
# from lib import rcfile; rcfile.open(window). The builtin open function is used
# within the module so an open function definition would conflict with the
# builtin so the builtin is aliased for later use before the module level open
# function is defined.
_open = __builtins__['open']


def file_name():
    return os.path.join(sublime.packages_path(), 'User', '.vintageousrc')


def open(window):
    file = file_name()

    if not os.path.exists(file):
        with _open(file, 'w'):
            pass

    window.open_file(file)


def load():
    _run()


def reload():
    _run()


def _run():
    _log.debug('run \'%s\'', file_name())

    try:
        window = sublime.active_window()
        with _open(file_name(), 'r') as f:
            for line in f:
                cmd, args = _parse_line(line)
                if cmd:
                    _log.debug('run command \'%s\' with args %s', cmd, args)
                    window.run_command(cmd, args)

    except FileNotFoundError:
        _log.debug('rcfile not found')


_PARSE_LINE_PATTERN = re.compile(
    '^(?::)?(?P<command_line>(?P<cmd>noremap|map|nnoremap|nmap|snoremap|smap|vnoremap|vmap|onoremap|omap|let) .*)$')


# TODO Properly implement map, nmap, vmap and omap
# Currently map, nmap, vmap, and omap work the same as
# noremap, nnoremap, vnoremap, and onoremap.
_TMP_CMD_ALIASES = {
    'noremap': 'map',
    'nnoremap': 'nmap',
    'onoremap': 'omap',
    'snoremap': 'smap',
    'vnoremap': 'vmap'
}


def _parse_line(line):
    try:
        line = line.rstrip()
        if line:
            match = _PARSE_LINE_PATTERN.match(line)
            if match:
                cmd_line = match.group('command_line')
                cmd = match.group('cmd')

                if cmd in _TMP_CMD_ALIASES:
                    cmd_line = cmd_line.replace(cmd, _TMP_CMD_ALIASES[cmd])
                    cmd = _TMP_CMD_ALIASES[cmd]

                # By default, mapping the character '|' (bar) should be escaped
                # with a slash or '<Bar>' used instead. Neovintageous currently
                # doesn't support '<Bar>' and internally doesn't require the bar
                # character to be escaped, but in order not to break backwards
                # compatibility in the future, this piece of code checks that
                # the mapping escapes the bar character correctly. This piece of
                # code can be removed when this is fixed in the core. See :help
                # map_bar for more details.
                if '|' in cmd_line:
                    if '|' in cmd_line.replace('\\|', ''):
                        raise Exception('E488: Trailing characters: {}'.format(line.rstrip()))
                    cmd_line = cmd_line.replace('\\|', '|')

                return ('ex_' + cmd, {'command_line': cmd_line})
    except Exception:
        msg = 'error detected while processing \'{}\' at line \'{}\''.format(file_name(), line.rstrip())
        message(msg)
        _log.exception(msg)

    return None, None
