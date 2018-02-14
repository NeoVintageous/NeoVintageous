from .scanner_state import EOF
from .tokens import TOKEN_COMMAND_TAB_ONLY
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('tabonly', 'tabo')
class TokenTabOnly(TokenOfCommand):
    def __init__(self, *args, **kwargs):
        super().__init__([], TOKEN_COMMAND_TAB_ONLY, 'tabonly', *args, **kwargs)
        self.target_command = 'ex_tabonly'


def scan_cmd_tab_only(state):
    c = state.consume()
    if c == EOF:
        return None, [TokenTabOnly(), TokenEof()]

    bang = c == '!'

    return None, [TokenTabOnly(forced=bang), TokenEof()]
