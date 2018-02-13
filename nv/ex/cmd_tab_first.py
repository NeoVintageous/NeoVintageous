from .state import EOF
from .tokens import TOKEN_COMMAND_TAB_FIRST
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('tabfirst', 'tabfir')
@ex.command('tabrewind', 'tabr')
class TokenTabFirst(TokenOfCommand):
    def __init__(self, *args, **kwargs):
        super().__init__([], TOKEN_COMMAND_TAB_FIRST, 'tabfirst', *args, **kwargs)
        self.target_command = 'ex_tabfirst'


def scan_cmd_tab_first(state):
    c = state.consume()
    if c == EOF:
        return None, [TokenTabFirst(), TokenEof()]

    bang = c == '!'

    return None, [TokenTabFirst(forced=bang), TokenEof()]
