from .tokens import TOKEN_COMMAND_PRINT_WORKING_DIR
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('pwd', 'pwd')
class TokenCommandPrintWorkingDir(TokenOfCommand):
    def __init__(self, *args, **kwargs):
        super().__init__({}, TOKEN_COMMAND_PRINT_WORKING_DIR, 'pwd', *args, **kwargs)
        self.target_command = 'ex_print_working_dir'


def scan_cmd_print_working_dir(state):
    state.expect_eof()

    return None, [TokenCommandPrintWorkingDir(), TokenEof()]
