from .tokens import TOKEN_COMMAND_ONLY
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('only', 'on')
class TokenCommandOnly(TokenOfCommand):
    def __init__(self, *args, **kwargs):
        super().__init__({}, TOKEN_COMMAND_ONLY, 'only', *args, **kwargs)
        self.target_command = 'ex_only'


def scan_cmd_only(state):
    bang = state.consume()
    if bang == '!':
        state.ignore()
        state.expect_eof()

        return None, [TokenCommandOnly(forced=True), TokenEof()]

    assert bang == state.EOF, 'trailing characters'

    return None, [TokenCommandOnly(), TokenEof()]
