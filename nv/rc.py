import builtins
import os
import re

import sublime

from NeoVintageous.nv.vim import get_logger
from NeoVintageous.nv.vim import message


_log = get_logger(__name__)

_parse_line_pattern = re.compile(
    '^(?::)?(?P<command_line>(?P<cmd>noremap|map|nnoremap|nmap|snoremap|smap|vnoremap|vmap|onoremap|omap|let) .*)$')

_recursive_mapping_alts = {
    'map': 'nnnoremap',
    'nmap': 'nnoremap',
    'smap': 'snoremap',
    'vmap': 'vnoremap',
    'omap': 'onoremap'
}


def _file_name():
    return os.path.join(sublime.packages_path(), 'User', '.vintageousrc')


def open(window):
    file = _file_name()

    if not os.path.exists(file):
        with builtins.open(file, 'w') as f:
            f.write('" Type :h vintageousrc for help.\n')

    window.open_file(file)


def load():
    _run()


def reload():
    _run()


def _run():
    _log.debug('run %s', _file_name())

    try:
        window = sublime.active_window()
        with builtins.open(_file_name(), 'r') as f:
            for line in f:
                cmd, args = _parse_line(line)
                if cmd:
                    _log.debug('run command %s %s', cmd, args)
                    window.run_command(cmd, args)

    except FileNotFoundError:
        _log.debug('rcfile not found')


def _parse_line(line):
    try:
        line = line.rstrip()
        if line:
            match = _parse_line_pattern.match(line)
            if match:
                cmd_line = match.group('command_line')
                cmd = match.group('cmd')

                if cmd in _recursive_mapping_alts:
                    raise Exception('Recursive mapping commands not allowed, use the "{}" command instead'
                                    .format(_recursive_mapping_alts[cmd]))

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
        msg = 'error detected while processing {} at line {}'.format(_file_name(), line.rstrip())
        message(msg)
        _log.exception(msg)

    return None, None
