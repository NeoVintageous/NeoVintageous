from .tokens import TOKEN_COMMAND_CDD
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('cdd', 'cdd')
class TokenCommandCdd(TokenOfCommand):
    def __init__(self, *args, **kwargs):
        super().__init__({}, TOKEN_COMMAND_CDD, 'cdd', *args, **kwargs)
        self.target_command = 'ex_cdd'


def scan_cmd_cdd(state):
    c = state.consume()
    if c == state.EOF:
        return None, [TokenCommandCdd(), TokenEof()]

    bang = c == '!'
    if not bang:
        state.backup()

    state.expect_eof()

    return None, [TokenCommandCdd(forced=bang), TokenEof()]
