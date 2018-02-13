from .tokens import TOKEN_COMMAND_HELP
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('help', 'h')
class TokenHelp(TokenOfCommand):
    def __init__(self, params, *args, **kwargs):
        super().__init__(params, TOKEN_COMMAND_HELP, 'help', *args, **kwargs)
        self.target_command = 'ex_help'

    @property
    def subject(self):
        return self.params['subject']


def scan_command_help(state):
    match = state.expect_match(r'(?P<bang>!)?\s*(?P<subject>.+)?$').groupdict()

    params = {'subject': match['subject']}
    bang = bool(match['bang'])

    return None, [TokenHelp(params, forced=bang), TokenEof()]
