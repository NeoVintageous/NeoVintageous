from .tokens import TokenEof
from .tokens_base import TOKEN_COMMAND_NOREMAP
from .tokens_base import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('noremap', 'no')
class TokenCommandNoremap(TokenOfCommand):
    def __init__(self, params, *args, **kwargs):
        super().__init__(params, TOKEN_COMMAND_NOREMAP, 'noremap', *args, **kwargs)
        self.target_command = 'ex_noremap'

    @property
    def keys(self):
        return self.params['keys']

    @property
    def command(self):
        return self.params['command']


def scan_command_noremap(state):
    params = {
        'keys': None,
        'command': None,
    }

    m = state.match(r'\s*(?P<keys>.+?)\s+(?P<command>.+?)\s*$')

    if m:
        params.update(m.groupdict())

    return None, [TokenCommandNoremap(params), TokenEof()]
