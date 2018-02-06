from .state import EOF
from .tokens import TokenEof
from .tokens_base import TOKEN_COMMAND_VSPLIT
from .tokens_base import TokenOfCommand

from NeoVintageous.nv import ex


@ex.command('vsplit', 'vs')
class TokenCommandVsplit(TokenOfCommand):
    def __init__(self, params, *args, **kwargs):
        super().__init__(params, TOKEN_COMMAND_VSPLIT, 'vsplit', *args, **kwargs)
        self.target_command = 'ex_vsplit'


def scan_command_vsplit(state):
    state.skip(' ')
    state.ignore()

    params = {
        'file': None
    }

    if state.consume() == EOF:
        return None, [TokenCommandVsplit(params), TokenEof()]

    state.backup()

    params['file'] = state.match(r'.+$').group(0).strip()

    return None, [TokenCommandVsplit(params), TokenEof()]
