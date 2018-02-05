from .state import EOF
from .tokens import TokenEof
from .tokens_base import TOKEN_COMMAND_TAB_PREV
from .tokens_base import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('tabprev', 'tabp')
class TokenTabPrev(TokenOfCommand):
    def __init__(self, *args, **kwargs):
        super().__init__([], TOKEN_COMMAND_TAB_PREV, 'tabprev', *args, **kwargs)
        self.target_command = 'ex_tabprev'


def scan_command_tab_prev(state):
    c = state.consume()

    if c == EOF:
        return None, [TokenTabPrev(), TokenEof()]

    bang = c == '!'

    return None, [TokenTabPrev(forced=bang), TokenEof()]
