from .tokens import TOKEN_COMMAND_YANK
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('yank', 'y')
class TokenCommandYank(TokenOfCommand):
    def __init__(self, params, *args, **kwargs):
        super().__init__(params, TOKEN_COMMAND_YANK, 'yank', *args, **kwargs)
        self.addressable = True
        self.target_command = 'ex_yank'

    @property
    def register(self):
        return self.params['register']

    @property
    def count(self):
        return self.params['count']


def scan_cmd_yank(state):
    params = {
        'register': '"',
        'count': None,
    }

    state.skip(' ')
    state.ignore()

    c = state.consume()
    if c == state.EOF:
        return None, [TokenCommandYank(params), TokenEof()]

    state.backup()
    state.skip(' ')
    state.ignore()

    m = state.expect_match(r'(?P<register>[a-zA-Z0-9"])(?:\s+(?P<count>\d+))?\s*$')

    params.update(m.groupdict())
    if params['count']:
        raise NotImplementedError('parameter not implemented')

    return None, [TokenCommandYank(params), TokenEof()]
