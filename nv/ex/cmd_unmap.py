from .tokens import TOKEN_COMMAND_UNMAP
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('unmap', 'unm')
class TokenCommandUnmap(TokenOfCommand):
    def __init__(self, params, *args, **kwargs):
        super().__init__(params, TOKEN_COMMAND_UNMAP, 'unmap', *args, **kwargs)
        self.target_command = 'ex_unmap'

    @property
    def keys(self):
        return self.params['keys']

    @property
    def command(self):
        return self.params['command']


def scan_cmd_unmap(state):
    params = {
        'keys': None,
    }

    m = state.match(r'\s*(?P<keys>.+?)\s*$')
    if m:
        params.update(m.groupdict())

    return None, [TokenCommandUnmap(params), TokenEof()]
