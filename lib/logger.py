from logging.handlers import RotatingFileHandler
import logging
import os


_DEBUG = bool(os.getenv('SUBLIME_NEOVINTAGEOUS_DEBUG'))


def _log_file():
    # TODO Why arn't we using sublime.packages_path() ?
    module_relative_file = __name__.replace('.', os.sep) + '.py'
    if __file__.endswith(module_relative_file):
        return os.path.join(
            __file__[:-(len(module_relative_file) + len(os.sep))],
            'User',
            'NeoVintageous.log'
        )


def _init_logger():
    logger = logging.getLogger(__name__.split('.')[0])
    logger.setLevel(logging.DEBUG)

    handler_formatter = logging.Formatter('%(asctime)s %(levelname)-5s %(name)-30s %(message)s')

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(handler_formatter)
    logger.addHandler(console_handler)

    log_file = _log_file()
    if log_file:
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10000000,  # 10000000 = 10MB
            backupCount=3
        )
        file_handler.setFormatter(handler_formatter)
        logger.addHandler(file_handler)
    else:
        print('NeoVintageous: could not create log file "%s"' % log_file)


class _NullLogger():
    """An implementation of the Logger API that does nothing."""

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
        return logging.getLogger(name)
else:
    def get_logger(name):
        return _NullLogger()
