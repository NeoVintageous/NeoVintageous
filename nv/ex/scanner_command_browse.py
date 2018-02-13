from .tokens import TOKEN_COMMAND_BROWSE
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('browse', 'bro')
class TokenBrowse(TokenOfCommand):
    def __init__(self, params, *args, **kwargs):
        super().__init__(params, TOKEN_COMMAND_BROWSE, 'browse', *args, **kwargs)
        self.target_command = 'ex_browse'


def scan_command_browse(state):
    params = {
        'cmd': None,
    }

    state.skip(' ')
    state.ignore()

    m = state.match(r'(?P<cmd>.*)$')
    params.update(m.groupdict())

    if params['cmd']:
        raise NotImplementedError('parameter not implemented')

    return None, [TokenBrowse(params), TokenEof()]
