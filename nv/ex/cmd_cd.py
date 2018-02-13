from .state import EOF
from .tokens import TOKEN_COMMAND_CD
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('cd', 'cd')
class TokenCd(TokenOfCommand):
    def __init__(self, params, *args, **kwargs):
        super().__init__(params, TOKEN_COMMAND_CD, 'cd', *args, **kwargs)
        self.target_command = 'ex_cd'

    @property
    def path(self):
        return self.params['path']

    @property
    def must_go_back(self):
        return self.params['-']


def scan_cmd_cd(state):
    params = {
        'path': None,
        '-': None,
    }

    bang = state.consume() == '!'
    if not bang:
        state.backup()

    state.skip(' ')
    state.ignore()

    c = state.consume()
    if c == '-':
        params['-'] = '-'
        state.expect(EOF)
        raise NotImplementedError('parameter not implemented')
    elif c != EOF:
        state.backup()
        m = state.match(r'(?P<path>.+?)\s*$')
        params.update(m.groupdict())

    return None, [TokenCd(params, forced=bang), TokenEof()]
