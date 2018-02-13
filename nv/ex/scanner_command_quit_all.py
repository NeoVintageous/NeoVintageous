from .state import EOF
from .tokens import TOKEN_COMMAND_QUIT_ALL
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('quall', 'qa')
class TokenQuitAll(TokenOfCommand):
    def __init__(self, *args, **kwargs):
        super().__init__({}, TOKEN_COMMAND_QUIT_ALL, 'qall', *args, **kwargs)
        self.target_command = 'ex_quit_all'


def scan_command_quit_all(state):
    c = state.consume()

    bang = c == '!'

    state.expect(EOF)

    return None, [TokenQuitAll(forced=bang), TokenEof()]
