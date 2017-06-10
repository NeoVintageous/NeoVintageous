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
    try:
        with _open(file_name(), 'r') as f:
            for line in f:
                cmd, args = _parse_line(line)
                if cmd:
                    _logger.debug('running: {0} {1}'.format(cmd, args))
                    sublime.active_window().run_command(cmd, args)
    except FileNotFoundError:
        pass


_PARSE_LINE_PATTERN = re.compile('^(?::)?(?P<command_line>(?P<cmd>map|nmap|omap|vmap|let) .*)$')


def _parse_line(line):
    try:
        line = line.rstrip()
        _logger.debug('parse line: \'%s\'', line)
        match = _PARSE_LINE_PATTERN.match(line)
        if match:
            return ('ex_' + match.group('cmd'), {'command_line': match.group('command_line')})
    except Exception:
        _logger.debug('bad command in rcfile: \'%s\'', line.rstrip())
        nvim.console_message('bad command in rcfile: \'%s\'' % line.rstrip())

    return None, None
