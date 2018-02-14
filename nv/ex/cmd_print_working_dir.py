from .scanner_state import EOF
from .tokens import TOKEN_COMMAND_PRINT_WORKING_DIR
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('pwd', 'pwd')
class TokenPrintWorkingDir(TokenOfCommand):
    def __init__(self, *args, **kwargs):
        super().__init__({}, TOKEN_COMMAND_PRINT_WORKING_DIR, 'pwd', *args, **kwargs)
        self.target_command = 'ex_print_working_dir'


def scan_cmd_print_working_dir(state):
    state.expect(EOF)

    return None, [TokenPrintWorkingDir(), TokenEof()]
