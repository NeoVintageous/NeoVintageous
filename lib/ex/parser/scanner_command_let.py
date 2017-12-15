from .tokens import TokenEof
from .tokens_base import TOKEN_COMMAND_LET
from .tokens_base import TokenOfCommand
from NeoVintageous.lib import ex


@ex.command('let', 'let')
class TokenCommandLet(TokenOfCommand):
    def __init__(self, params, *args, **kwargs):
        super().__init__(params, TOKEN_COMMAND_LET, 'let', *args, **kwargs)
        self.target_command = 'ex_let'

    @property
    def variable_name(self):
        return self.params['name']

    @property
    def variable_value(self):
        return self.params['value']


# TODO [enhancement] Implement other options.
def scan_command_let(state):
    params = {
        'name': None,
        'value': None,
    }

    m = state.expect_match(
        r'(?P<name>.+?)\s*=\s*(?P<value>.+?)\s*$',
        on_error=lambda: Exception("E121: Undefined variable"))

    params.update(m.groupdict())

    return None, [TokenCommandLet(params), TokenEof()]
