# TODO refactor logging initialisation

import logging
from logging.handlers import RotatingFileHandler
import os


_DEBUG = bool(os.getenv('SUBLIME_NEOVINTAGEOUS_DEBUG'))


class _LogDir():
    """Locates the log dir for plugin logs."""

    @staticmethod
    def find():
        return _LogDir()._find_log_dir()

    def _test(self, a, b):
        if a == b:
            return 'folder'
        elif a == b + '.sublime-package':
            return 'sublime-package'

    def _find_path(self, start, package):
        while True:
            result = self._test(os.path.basename(start), package)

            if result == 'folder':
                if os.path.exists(os.path.join(os.path.dirname(start), 'User')):
                    return os.path.join(os.path.dirname(start), '.logs')

            elif result == 'sublime-package':
                parent = os.path.dirname(start)
                if os.path.exists(os.path.join(os.path.dirname(parent), 'Packages')):
                    return os.path.join(os.path.dirname(parent), 'Packages', '.logs')

            if os.path.dirname(start) == start:
                return

            start = os.path.dirname(start)

    def _find_log_dir(self):
        package = __name__.split('.')[0]

        if package == '__main__':
            return

        start = os.path.dirname(__file__)

        logs_path = self._find_path(start, package)

        if not logs_path:
            return

        if not os.path.exists(logs_path):
            os.mkdir(logs_path)

        return logs_path


class _Logger():
    """Logs events."""

    log_dir = _LogDir.find()

    def __init__(self, name):

        self.logger = logging.getLogger(name)
        default_level = logging.ERROR
        user_level = self._get_log_level_from_file()
        self.logger.setLevel(user_level if user_level is not None else default_level)

        f = logging.Formatter('%(asctime)s %(levelname)-5s %(name)s %(message)s')

        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(logging.WARNING)
        consoleHandler.setFormatter(f)
        self.logger.addHandler(consoleHandler)

        file_name = self._file_name()
        if file_name:
            fileHandler = RotatingFileHandler(file_name, maxBytes=1 << 10)
            fileHandler.setFormatter(f)
            self.logger.addHandler(fileHandler)
        else:
            print("NeoVintageous: cannot find log file path: %s" % file_name)

    def _get_path_to_log(self):
        package = __name__.split('.')[0]
        p = os.path.join(self.log_dir, package)
        return p

    def _get_log_level_from_file(self):
        p = self._get_path_to_log()
        if os.path.exists(p):
            with open(p, 'rt') as f:
                text = f.read().strip().upper()
                return getattr(logging, text, None)

    def _file_name(self):
        p = __name__.split('.')[0]
        return os.path.join(self.log_dir, '{}.log'.format(p))

    def debug(self, message, *args, **kwargs):
        self.logger.debug(message, *args, **kwargs)

    def info(self, message, *args, **kwargs):
        self.logger.info(message, *args, **kwargs)

    def warning(self, message, *args, **kwargs):
        self.logger.warning(message, *args, **kwargs)

    def error(self, message, *args, **kwargs):
        self.logger.error(message, *args, **kwargs)

    def critical(self, message, *args, **kwargs):
        self.logger.critical(message, *args, **kwargs)


class _NullLogger():
    """An implementation of the Logger API that does nothing."""

    def debug(self, message, *args, **kwargs):
        pass

    def info(self, message, *args, **kwargs):
        pass

    def warning(self, message, *args, **kwargs):
        pass

    def error(self, message, *args, **kwargs):
        pass

    def critical(self, message, *args, **kwargs):
        pass


if _DEBUG:
    def get_logger(name):
        return _Logger(name)
else:
    def get_logger(name):
        return _NullLogger()
