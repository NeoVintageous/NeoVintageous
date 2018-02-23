from .tokens import TOKEN_COMMAND_UNVSPLIT
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('unvsplit', 'unvsplit')
class TokenCommandUnvsplit(TokenOfCommand):
    def __init__(self, *args, **kwargs):
        super().__init__({}, TOKEN_COMMAND_UNVSPLIT, 'unvsplit', *args, **kwargs)
        self.target_command = 'ex_unvsplit'


def scan_cmd_unvsplit(state):
    state.expect_eof()

    return None, [TokenCommandUnvsplit(), TokenEof()]
