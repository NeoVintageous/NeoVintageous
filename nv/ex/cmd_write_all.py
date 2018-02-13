from .state import EOF
from .tokens import TOKEN_COMMAND_WRITE_ALL
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('wall', 'wa')
class TokenWriteAllCommand(TokenOfCommand):
    def __init__(self, *args, **kwargs):
        super().__init__({}, TOKEN_COMMAND_WRITE_ALL, 'write_all', *args, **kwargs)
        self.target_command = 'ex_write_all'


def scan_cmd_write_all(state):
    c = state.consume()
    bang = c == '!'
    state.expect(EOF)

    return None, [TokenWriteAllCommand(forced=bang), TokenEof()]
