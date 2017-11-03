from .state import EOF
from .tokens import TokenEof
from .tokens_base import TOKEN_COMMAND_CLOSE
from .tokens_base import TokenOfCommand
from NeoVintageous.lib import ex


@ex.command('close', 'clo')
class TokenClose(TokenOfCommand):
    def __init__(self, *args, **kwargs):
        super().__init__({}, TOKEN_COMMAND_CLOSE, 'close', *args, **kwargs)
        self.target_command = 'ex_close'


def scan_command_close(state):
    c = state.consume()
    bang = c == '!'
    state.expect(EOF)

    return None, [TokenClose(forced=bang), TokenEof()]
