from .scanner_state import EOF
from .tokens import TOKEN_COMMAND_ABBREVIATE
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('abbreviate', 'ab')
class TokenCommandAbbreviate(TokenOfCommand):
    def __init__(self, params, *args, **kwargs):
        super().__init__(params, TOKEN_COMMAND_ABBREVIATE, 'abbreviate', *args, **kwargs)
        self.target_command = 'ex_abbreviate'

    @property
    def short(self):
        return self.params['short']

    @property
    def full(self):
        return self.params['full']


def scan_cmd_abbreviate(state):
    params = {
        'short': None,
        'full': None,
    }

    state.expect(' ')
    state.skip(' ')
    state.ignore()
    if state.consume() == EOF:
        return None, [TokenCommandAbbreviate({}), TokenEof()]

    state.backup()

    m = state.match(r'(?P<short>.+?)(?: +(?P<full>.+))?$')
    params.update(m.groupdict())

    return None, [TokenCommandAbbreviate(params), TokenEof()]
