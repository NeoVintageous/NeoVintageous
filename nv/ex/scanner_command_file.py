from .state import EOF
from .tokens import TOKEN_COMMAND_FILE
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('file', 'f')
class TokenCommandFile(TokenOfCommand):
    def __init__(self, *args, **kwargs):
        super().__init__({}, TOKEN_COMMAND_FILE, 'file', *args, **kwargs)
        self.target_command = 'ex_file'


def scan_command_file(state):
    bang = state.consume()

    if bang == EOF:
        return None, [TokenCommandFile(), TokenEof()]

    bang = bang == '!'
    if not bang:
        raise Exception("E488: Trailing characters")

    state.expect(EOF, on_error=lambda: Exception("E488: Trailing characters"))

    return None, [TokenCommandFile(forced=bang == '!'), TokenEof()]
