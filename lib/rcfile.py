import os
import re

import sublime

from NeoVintageous.lib import nvim


_logger = nvim.get_logger(__name__)

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
        with open(file, 'w'):
            pass

    window.open_file(file)


def load():
    _run()


def reload():
    _run()


def _run():
    _logger.debug('file=\'%s\'', file_name())
    try:
        with _open(file_name(), 'r') as f:
            for line in f:
                cmd, args = _parse_line(line)
                if cmd:
                    _logger.debug('run command \'%s\' with args %s', cmd, args)
                    sublime.active_window().run_command(cmd, args)
    except FileNotFoundError:
        pass


_PARSE_LINE_PATTERN = re.compile('^(?::)?(?P<command_line>(?P<cmd>noremap|map|nnoremap|nmap|vnoremap|vmap|onoremap|omap|let) .*)$')  # FIXME # noqa: E501


# TODO Properly implement map, nmap, vmap and omap
# Currently map, nmap, vmap, and omap work the same as
# noremap, nnoremap, vnoremap, and onoremap.
_TMP_CMD_ALIASES = {
    'noremap': 'map',
    'nnoremap': 'nmap',
    'vnoremap': 'vmap',
    'onoremap': 'omap'
}


def _parse_line(line):
    try:
        line = line.rstrip()
        if line:
            _logger.debug('\'%s\'', line)
            match = _PARSE_LINE_PATTERN.match(line)
            if match:
                cmd_line = match.group('command_line')
                cmd = match.group('cmd')

                if cmd in _TMP_CMD_ALIASES:
                    cmd_line = cmd_line.replace(cmd, _TMP_CMD_ALIASES[cmd])
                    cmd = _TMP_CMD_ALIASES[cmd]

                return ('ex_' + cmd, {'command_line': cmd_line})
    except Exception:
        _logger.exception('bad command in rcfile: \'%s\'', line.rstrip())
        nvim.console_message('bad command in rcfile: \'%s\'' % line.rstrip())

    return None, None
