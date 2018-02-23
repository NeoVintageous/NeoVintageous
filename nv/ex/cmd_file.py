from .tokens import TOKEN_COMMAND_FILE
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('file', 'f')
class TokenCommandFile(TokenOfCommand):
    def __init__(self, *args, **kwargs):
        super().__init__({}, TOKEN_COMMAND_FILE, 'file', *args, **kwargs)
        self.target_command = 'ex_file'


def scan_cmd_file(state):
    bang = state.consume()
    if bang == state.EOF:
        return None, [TokenCommandFile(), TokenEof()]

    bang = bang == '!'
    if not bang:
        raise Exception("E488: Trailing characters")

    state.expect_eof(on_error=lambda: Exception("E488: Trailing characters"))

    return None, [TokenCommandFile(forced=bang == '!'), TokenEof()]
