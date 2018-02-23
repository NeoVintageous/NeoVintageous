from .tokens import TOKEN_COMMAND_WRITE_ALL
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('wall', 'wa')
class TokenCommandWriteAllCommand(TokenOfCommand):
    def __init__(self, *args, **kwargs):
        super().__init__({}, TOKEN_COMMAND_WRITE_ALL, 'write_all', *args, **kwargs)
        self.target_command = 'ex_write_all'


def scan_cmd_write_all(state):
    bang = state.consume() == '!'

    # TODO [bug] ":command" followed by character that is not "!"  shouldn't be
    # valid e.g. the ":close" command should run when !:closex". There are a
    # bunch of commands that have this bug.

    state.expect_eof()

    return None, [TokenCommandWriteAllCommand(forced=bang), TokenEof()]
