from .state import EOF
from .tokens import TokenEof
from .tokens_base import TOKEN_COMMAND_QUIT
from .tokens_base import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('quit', 'q')
class TokenQuit(TokenOfCommand):
    def __init__(self, *args, **kwargs):
        super().__init__({}, TOKEN_COMMAND_QUIT, 'quit', *args, **kwargs)
        self.target_command = 'ex_quit'


def scan_command_quit(state):
    c = state.consume()
    bang = c == '!'
    state.expect(EOF)

    return None, [TokenQuit(forced=bang), TokenEof()]
