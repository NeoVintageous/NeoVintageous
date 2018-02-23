from .tokens import TOKEN_COMMAND_COPY
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('copy', 'co')
class TokenCommandCopy(TokenOfCommand):
    def __init__(self, params, *args, **kwargs):
        super().__init__(params, TOKEN_COMMAND_COPY, 'copy', *args, **kwargs)
        self.addressable = True
        self.target_command = 'ex_copy'

    @property
    def address(self):
        return self.params['address']


def scan_cmd_copy(state):
    params = {'address': None}
    m = state.expect_match(r'\s*(?P<address>.+?)\s*$')
    params.update(m.groupdict())

    return None, [TokenCommandCopy(params), TokenEof()]
