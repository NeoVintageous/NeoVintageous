from .tokens import TOKEN_COMMAND_CLOSE
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('close', 'clo')
class TokenCommandClose(TokenOfCommand):
    def __init__(self, *args, **kwargs):
        super().__init__({}, TOKEN_COMMAND_CLOSE, 'close', *args, **kwargs)
        self.target_command = 'ex_close'


def scan_cmd_close(state):
    bang = state.consume() == '!'

    # TODO [bug] ":command" followed by character that is not "!"  shouldn't be
    # valid e.g. the ":close" command should run when !:closex". There are a
    # bunch of commands that have this bug.

    state.expect_eof()

    return None, [TokenCommandClose(forced=bang), TokenEof()]
