from .tokens import TOKEN_COMMAND_QUIT_ALL
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('quall', 'qa')
class TokenCommandQuitAll(TokenOfCommand):
    def __init__(self, *args, **kwargs):
        super().__init__({}, TOKEN_COMMAND_QUIT_ALL, 'qall', *args, **kwargs)
        self.target_command = 'ex_quit_all'


def scan_cmd_quit_all(state):
    bang = state.consume() == '!'

    # TODO [bug] ":command" followed by character that is not "!"  shouldn't be
    # valid e.g. the ":close" command should run when !:closex". There are a
    # bunch of commands that have this bug.

    state.expect_eof()

    return None, [TokenCommandQuitAll(forced=bang), TokenEof()]
