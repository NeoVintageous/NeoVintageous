from .tokens import TOKEN_COMMAND_CQUIT
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('cquit', 'cq')
class TokenCquit(TokenOfCommand):
    def __init__(self, *args, **kwargs):
        super().__init__({}, TOKEN_COMMAND_CQUIT, 'cquit', *args, **kwargs)
        self.target_command = 'ex_cquit'


def scan_cmd_cquit(state):
    state.expect_eof()

    return None, [TokenCquit(), TokenEof()]
