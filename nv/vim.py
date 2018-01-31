from logging.handlers import RotatingFileHandler
import logging
import os

from sublime import status_message as _status_message


# TODO [review] Some of these modes appear unused or not needed
# XXX The modes Use strings because we need to pass modes as arguments in
# Default.sublime-keymap and it's more readable.
COMMAND_LINE = 'mode_command_line'
CTRL_X = 'mode_control_x'
INSERT = 'mode_insert'
# NeoVintageous always runs actions based on selections. Some Vim commands,
# however, behave differently depending on whether the current mode is NORMAL or
# VISUAL. To differentiate NORMAL mode operations (involving only an action, or
# a motion plus an action) from VISUAL mode, we need to add an additional mode
# for handling selections that won't interfere with the actual VISUAL mode.
# This is INTERNAL_NORMAL's job. We consider INTERNAL_NORMAL a pseudomode,
# because global state's .mode property should never set to it, yet it's set in
# vi_cmd_data often.
# Note that for pure motions we still use plain NORMAL mode.
INTERNAL_NORMAL = 'mode_internal_normal'
NORMAL = 'mode_normal'
NORMAL_INSERT = 'mode_normal_insert'  # The mode you enter when giving i a count
OPERATOR_PENDING = 'mode_operator_pending'
REPLACE = 'mode_replace'
SELECT = 'mode_select'
UNKNOWN = 'mode_unknown'
VISUAL = 'mode_visual'
VISUAL_BLOCK = 'mode_visual_block'
VISUAL_LINE = 'mode_visual_line'


def mode_to_friendly_name(mode):
    # type: (int) -> str
    if mode == INSERT:
        return 'INSERT'
    if mode == INTERNAL_NORMAL:
        return ''
    if mode == NORMAL:
        return ''
    if mode == OPERATOR_PENDING:
        return ''
    if mode == VISUAL:
        return 'VISUAL'
    if mode == VISUAL_BLOCK:
        return 'VISUAL BLOCK'
    if mode == VISUAL_LINE:
        return 'VISUAL LINE'
    if mode == UNKNOWN:
        return 'UNKNOWN'
    if mode == REPLACE:
        return 'REPLACE'
    if mode == NORMAL_INSERT:
        return 'INSERT'
    if mode == SELECT:
        return 'SELECT'
    if mode == CTRL_X:
        return 'Mode ^X'

    return 'REALLY UNKNOWN'


# TODO [refactor] I assume "INMEDIATE" is a typo, should be "IMMEDIATE"?
INPUT_INMEDIATE = 1
INPUT_VIA_PANEL = 2
INPUT_AFTER_MOTION = 3


DIRECTION_NONE = 0
DIRECTION_UP = 1
DIRECTION_DOWN = 2
DIRECTION_LEFT = 3
DIRECTION_RIGHT = 4


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
if bool(os.getenv('SUBLIME_NEOVINTAGEOUS_DEBUG')):

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
