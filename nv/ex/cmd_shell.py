from .state import EOF
from .tokens import TOKEN_COMMAND_SHELL
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('shell', 'shell')
class TokenShell(TokenOfCommand):
    def __init__(self, *args, **kwargs):
        super().__init__({}, TOKEN_COMMAND_SHELL, 'shell', *args, **kwargs)
        self.target_command = 'ex_shell'


def scan_cmd_shell(state):
    state.expect(EOF)

    return None, [TokenShell(), TokenEof()]
