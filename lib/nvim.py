from logging.handlers import RotatingFileHandler
import logging
import os

from sublime import status_message as _status_message


_DEBUG = bool(os.getenv('SUBLIME_NEOVINTAGEOUS_DEBUG'))


def console_message(msg):
    # type: (str) -> None
    print('NeoVintageous:', msg)


def status_message(msg):
    # type: (str) -> None
    _status_message(msg)


def message(msg):
    # type: (str) -> None
    status_message(msg)
    console_message(msg)


# If the debug environment variable is set then the debug message logging is
# initialised, otherwise a null logger used. This avoids needless overhead of
# dbeug logging functioanility, which 80% of users will never need.
if _DEBUG:

    class _LogFormatter(logging.Formatter):

        def format(self, record):
            if not record.msg.startswith(' '):
                pad_count = 60 - (len(record.name) + len(record.funcName) + len(str(record.lineno)))
                if pad_count > 0:
                    record.msg = (' ' * pad_count) + record.msg

            return super().format(record)

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

    def _init_logger():
        level = logging.DEBUG
        formatter = _LogFormatter('%(asctime)s %(levelname)-5s %(name)s@%(funcName)s:%(lineno)d %(message)s')
        file = _log_file()

        logger = logging.getLogger('NeoVintageous')
        logger.setLevel(level)

        # Stream handler
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        # File handler
        if file:
            file_handler = RotatingFileHandler(
                file,
                maxBytes=10000000,  # 10000000 = 10MB
                backupCount=2
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

            logger.debug('debug log file: \'{}\''.format(file))
        else:
            console_message('could not create log file \'{}\''.format(file))

        logger.debug('logger initialised')

    _init_logger()

    def get_logger(name):
        logger = logging.getLogger(name)
        logger.debug('logger name: %s', name)

        return logger

else:

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

    def get_logger(name):
        return _NullLogger()
