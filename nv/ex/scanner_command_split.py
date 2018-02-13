from .state import EOF
from .tokens import TOKEN_COMMAND_SPLIT
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('split', 'sp')
class TokenCommandSplit(TokenOfCommand):
    def __init__(self, params, *args, **kwargs):
        super().__init__(params, TOKEN_COMMAND_SPLIT, 'split', *args, **kwargs)
        self.target_command = 'ex_split'


def scan_command_split(state):
    state.skip(' ')
    state.ignore()

    params = {'file': None}

    if state.consume() == EOF:
        return None, [TokenCommandSplit(params), TokenEof()]

    state.backup()

    params['file'] = state.match(r'.+$').group(0).strip()

    return None, [TokenCommandSplit(params), TokenEof()]
