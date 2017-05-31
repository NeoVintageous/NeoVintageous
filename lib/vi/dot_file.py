import os

import sublime

from NeoVintageous.lib import nvim


_logger = nvim.get_logger(__name__)


class DotFile(object):
    def __init__(self, path):
        self.path = path

    @staticmethod
    def from_user():
        path = os.path.join(sublime.packages_path(), 'User', '.vintageousrc')
        return DotFile(path)

    def run(self):
        try:
            with open(self.path, 'r') as f:
                for line in f:
                    cmd, args = self.parse(line)
                    if cmd:
                        _logger.info('[DotFile] running: {0} {1}'.format(cmd, args))
                        sublime.active_window().run_command(cmd, args)
        except FileNotFoundError:
            pass

    def parse(self, line):
        try:
            _logger.info('[DotFile] parsing line: {0}'.format(line.rstrip()))

            if line.startswith((':map ')):
                line = line[1:]
                return ('ex_map', {'command_line': line.rstrip()})

            if line.startswith((':nmap ')):
                line = line[1:]
                return ('ex_nmap', {'command_line': line.rstrip()})

            if line.startswith((':omap ')):
                line = line[1:]
                return ('ex_omap', {'command_line': line.rstrip()})

            if line.startswith((':vmap ')):
                line = line[1:]
                return ('ex_vmap', {'command_line': line.rstrip()})

            if line.startswith((':let ')):
                line = line[1:]
                return ('ex_let', {'command_line': line.strip()})

        except Exception:
            _logger.debug('bad config in dotfile: \'%s\'', line.rstrip())
            nvim.console_message('bad config in dotfile: \'%s\'' % line.rstrip())

        return None, None
