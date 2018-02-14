from .scanner_state import EOF
from .tokens import TOKEN_COMMAND_UNVSPLIT
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('unvsplit', 'unvsplit')
class TokenCommandUnvsplit(TokenOfCommand):
    def __init__(self, *args, **kwargs):
        super().__init__({}, TOKEN_COMMAND_UNVSPLIT, 'vsplit', *args, **kwargs)
        self.target_command = 'ex_unvsplit'


def scan_cmd_unvsplit(state):
    state.expect(EOF)

    return None, [TokenCommandUnvsplit(), TokenEof()]
