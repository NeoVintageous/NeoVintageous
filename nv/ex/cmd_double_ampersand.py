from .tokens import TOKEN_COMMAND_DOUBLE_AMPERSAND
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('&&', '&&')
class TokenDoubleAmpersand(TokenOfCommand):
    def __init__(self, params, *args, **kwargs):
        super().__init__(params, TOKEN_COMMAND_DOUBLE_AMPERSAND, '&&', *args, **kwargs)
        self.addressable = True
        self.target_command = 'ex_double_ampersand'


def scan_cmd_double_ampersand(state):
    params = {
        'flags': [],
        'count': '',
    }

    m = state.match(r'\s*([cgr])*\s*(\d*)\s*$')
    params['flags'] = list(m.group(1)) if m.group(1) else []
    params['count'] = m.group(2) or ''

    state.expect_eof()

    return None, [TokenDoubleAmpersand(params), TokenEof()]
