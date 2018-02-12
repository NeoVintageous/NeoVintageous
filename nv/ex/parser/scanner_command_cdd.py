from .state import EOF
from .tokens import TOKEN_COMMAND_CDD
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('cdd', 'cdd')
class TokenCdd(TokenOfCommand):
    def __init__(self, *args, **kwargs):
        super().__init__({}, TOKEN_COMMAND_CDD, 'cdd', *args, **kwargs)
        self.target_command = 'ex_cdd'


def scan_command_cdd(state):
    c = state.consume()

    if c == EOF:
        return None, [TokenCdd(), TokenEof()]

    bang = c == '!'
    if not bang:
        state.backup()

    state.expect(EOF)

    return None, [TokenCdd(forced=bang), TokenEof()]
