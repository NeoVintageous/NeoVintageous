from .scanner_state import EOF
from .tokens import TOKEN_COMMAND_CLOSE
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('close', 'clo')
class TokenClose(TokenOfCommand):
    def __init__(self, *args, **kwargs):
        super().__init__({}, TOKEN_COMMAND_CLOSE, 'close', *args, **kwargs)
        self.target_command = 'ex_close'


def scan_cmd_close(state):
    c = state.consume()
    bang = c == '!'
    state.expect(EOF)

    return None, [TokenClose(forced=bang), TokenEof()]
