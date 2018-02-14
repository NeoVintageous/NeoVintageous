from .scanner_state import EOF
from .tokens import TOKEN_COMMAND_BUFFERS
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('buffers', 'buffers')
@ex.command('files', 'files')
@ex.command('ls', 'ls')
class TokenCommandBuffers(TokenOfCommand):
    def __init__(self, *args, **kwargs):
        super().__init__({}, TOKEN_COMMAND_BUFFERS, 'write', *args, **kwargs)
        self.target_command = 'ex_prompt_select_open_file'


def scan_cmd_buffers(state):
    try:
        state.expect(EOF)
    except ValueError:
        raise Exception("E488: Trailing characters")

    return None, [TokenCommandBuffers(), TokenEof()]
