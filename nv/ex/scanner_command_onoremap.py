from .tokens import TOKEN_COMMAND_ONOREMAP
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('onoremap', 'ono')
class TokenCommandOnoremap(TokenOfCommand):
    def __init__(self, params, *args, **kwargs):
        super().__init__(params, TOKEN_COMMAND_ONOREMAP, 'onoremap', *args, **kwargs)
        self.target_command = 'ex_onoremap'

    @property
    def keys(self):
        return self.params['keys']

    @property
    def command(self):
        return self.params['command']


def scan_command_onoremap(state):
    params = {
        'keys': None,
        'command': None,
    }

    m = state.match(r'\s*(?P<keys>.+?)\s+(?P<command>.+?)\s*$')

    if m:
        params.update(m.groupdict())

    return None, [TokenCommandOnoremap(params), TokenEof()]
