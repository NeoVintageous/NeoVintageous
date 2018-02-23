from .tokens import TOKEN_COMMAND_QUIT
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('quit', 'q')
class TokenCommandQuit(TokenOfCommand):
    def __init__(self, *args, **kwargs):
        super().__init__({}, TOKEN_COMMAND_QUIT, 'quit', *args, **kwargs)
        self.target_command = 'ex_quit'


def scan_cmd_quit(state):
    bang = state.consume() == '!'

    # TODO [bug] ":command" followed by character that is not "!"  shouldn't be
    # valid e.g. the ":close" command should run when !:closex". There are a
    # bunch of commands that have this bug.

    state.expect_eof()

    return None, [TokenCommandQuit(forced=bang), TokenEof()]
