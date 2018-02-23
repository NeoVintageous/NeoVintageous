from .tokens import TOKEN_COMMAND_SNOREMAP
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('snoremap', 'snor')
class TokenCommandSnoremap(TokenOfCommand):
    def __init__(self, params, *args, **kwargs):
        super().__init__(params, TOKEN_COMMAND_SNOREMAP, 'snoremap', *args, **kwargs)
        self.target_command = 'ex_snoremap'

    @property
    def keys(self):
        return self.params['keys']

    @property
    def command(self):
        return self.params['command']


def scan_cmd_snoremap(state):
    params = {'keys': None, 'command': None}

    m = state.match(r'\s*(?P<keys>.+?)\s+(?P<command>.+?)\s*$')
    if m:
        params.update(m.groupdict())

    return None, [TokenCommandSnoremap(params), TokenEof()]
