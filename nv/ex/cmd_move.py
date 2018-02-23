from .tokens import TOKEN_COMMAND_MOVE
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('move', 'm')
class TokenCommandMove(TokenOfCommand):
    def __init__(self, params, *args, **kwargs):
        super().__init__(params, TOKEN_COMMAND_MOVE, 'move', *args, **kwargs)
        self.addressable = True
        self.target_command = 'ex_move'

    @property
    def address(self):
        return self.params['address']


def scan_cmd_move(state):
    params = {'address': None}

    state.skip(' ')
    state.ignore()

    m = state.match(r'(?P<address>.*$)')
    if m:
        address_command_line = m.group(0).strip() or '.'
        params['address'] = address_command_line

    return None, [TokenCommandMove(params), TokenEof()]
