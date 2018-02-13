from .tokens import TOKEN_COMMAND_OUNMAP
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('ounmap', 'ounm')
class TokenCommandOunmap(TokenOfCommand):
    def __init__(self, params, *args, **kwargs):
        super().__init__(params, TOKEN_COMMAND_OUNMAP, 'ounmap', *args, **kwargs)
        self.target_command = 'ex_ounmap'

    @property
    def keys(self):
        return self.params['keys']


def scan_cmd_ounmap(state):
    params = {
        'keys': None,
    }

    m = state.match(r'\s*(?P<keys>.+?)\s*$')
    if m:
        params.update(m.groupdict())

    return None, [TokenCommandOunmap(params), TokenEof()]
