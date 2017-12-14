from logging.handlers import RotatingFileHandler
import logging
import os

from sublime import status_message as _status_message


_DEBUG = bool(os.getenv('SUBLIME_NEOVINTAGEOUS_DEBUG'))


E_ADDRESS_REQUIRED = 14
E_CANT_FIND_DIR_IN_CDPATH = 344
E_CANT_MOVE_LINES_ONTO_THEMSELVES = 134
E_CANT_WRITE_FILE = 212
E_EMPTY_BUFFER = 749
E_FILE_EXISTS = 13
E_INVALID_ADDRESS = 14
E_INVALID_ARGUMENT = 474
E_INVALID_RANGE = 16
E_NO_BANG_ALLOWED = 477
E_NO_FILE_NAME = 32
E_NO_RANGE_ALLOWED = 481
E_OTHER_BUFFER_HAS_CHANGES = 445
E_READONLY_FILE = 45
E_TRAILING_CHARS = 488
E_UNDEFINED_VARIABLE = 121
E_UNKNOWN_COMMAND = 492
E_UNSAVED_CHANGES = 37


class Error(Exception):

    _MESSAGES = {
        E_FILE_EXISTS: 'File exists (add ! to override).',
        E_ADDRESS_REQUIRED: 'Invalid address.',
        E_INVALID_ADDRESS: 'Invalid address.',
        E_INVALID_RANGE: 'Invalid range.',
        E_NO_FILE_NAME: 'No file name.',
        E_UNSAVED_CHANGES: 'There are unsaved changes.',
        E_READONLY_FILE: "'readonly' option is set (add ! to override)",
        # TODO: Should pass the name of the variable to this message:
        E_UNDEFINED_VARIABLE: "Undefined variable.",
        E_CANT_MOVE_LINES_ONTO_THEMSELVES: "Move lines into themselves.",
        E_CANT_WRITE_FILE: "Can't open file for writing.",
        E_CANT_FIND_DIR_IN_CDPATH: "Can't fin directory in 'cdpath'.",
        E_OTHER_BUFFER_HAS_CHANGES: "Other buffer contains changes.",
        E_INVALID_ARGUMENT: "Invalid argument.",
        E_NO_BANG_ALLOWED: 'No ! allowed.',
        E_NO_RANGE_ALLOWED: 'No range allowed.',
        E_TRAILING_CHARS: 'Traling characters.',
        E_UNKNOWN_COMMAND: 'Not an editor command.',
        E_EMPTY_BUFFER: 'Empty buffer.',
    }

    def __init__(self, code, *args, **kwargs):
        self.code = code
        self.message = self._MESSAGES.get(code, '')
        super().__init__(*args, **kwargs)

    def __str__(self):
        return 'E{0} {1}'.format(self.code, self.message)


def console_message(msg):
    print('NeoVintageous: ' + str(msg))


def status_message(msg):
    _status_message(str(msg))


def message(msg):
    status_message(msg)
    console_message(msg)


def exception_message(exception):
    message(exception)


def not_implemented_message(msg):
    message(msg)


def _log_file():
    # Why is sublime.packages_path() not used to build the path?
    # > At importing time, plugins may not call any API functions, with the
    # > exception of sublime.version(), sublime.platform(),
    # > sublime.architecture() and sublime.channel().
    # > - https://www.sublimetext.com/docs/3/api_reference.html.
    module_relative_file = __name__.replace('.', os.sep) + '.py'
    current_file = __file__.replace('NeoVintageous.sublime-package', 'NeoVintageous')
    if current_file.endswith(module_relative_file):
        path = current_file.replace('/Installed Packages/NeoVintageous/', '/Packages/NeoVintageous/')
        return os.path.join(
            path[:-(len(module_relative_file) + len(os.sep))],
            'User',
            'NeoVintageous.log'
        )


class _LogFormatter(logging.Formatter):

    def format(self, record):
        if not record.msg.startswith(' '):
            pad_count = 60 - (len(record.name) + len(record.funcName) + len(str(record.lineno)))
            if pad_count > 0:
                record.msg = (' ' * pad_count) + record.msg

        return super().format(record)


def _init_logger():
    formatter = _LogFormatter('%(asctime)s %(levelname)-5s %(name)s@%(funcName)s:%(lineno)d %(message)s')

    logger = logging.getLogger('NeoVintageous')
    logger.setLevel(logging.DEBUG)

    # Stream handler
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # File handler
    log_file = _log_file()
    if log_file:
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10000000,  # 10000000 = 10MB
            backupCount=2
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        logger.debug('debug log file: \'{}\''.format(log_file))
    else:
        console_message('could not create log file \'{}\''.format(log_file))


class _NullLogger():

    def debug(self, msg, *args, **kwargs):
        pass

    def info(self, msg, *args, **kwargs):
        pass

    def warning(self, msg, *args, **kwargs):
        pass

    def error(self, msg, *args, **kwargs):
        pass

    def critical(self, msg, *args, **kwargs):
        pass

    def exception(self, msg, *args, **kwargs):
        pass


if _DEBUG:
    _init_logger()

    def get_logger(name):
        logger = logging.getLogger(name)
        logger.debug('logger name: %s', name)

        return logger
else:
    def get_logger(name):
        return _NullLogger()
