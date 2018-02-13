from .state import EOF
from .tokens import TOKEN_COMMAND_QUIT
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('quit', 'q')
class TokenQuit(TokenOfCommand):
    def __init__(self, *args, **kwargs):
        super().__init__({}, TOKEN_COMMAND_QUIT, 'quit', *args, **kwargs)
        self.target_command = 'ex_quit'


def scan_cmd_quit(state):
    c = state.consume()
    bang = c == '!'
    state.expect(EOF)

    return None, [TokenQuit(forced=bang), TokenEof()]
