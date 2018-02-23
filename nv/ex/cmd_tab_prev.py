from .tokens import TOKEN_COMMAND_TAB_PREV
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('tabprev', 'tabp')
class TokenCommandTabPrev(TokenOfCommand):
    def __init__(self, *args, **kwargs):
        super().__init__([], TOKEN_COMMAND_TAB_PREV, 'tabprev', *args, **kwargs)
        self.target_command = 'ex_tabprev'


def scan_cmd_tab_prev(state):
    c = state.consume()
    if c == state.EOF:
        return None, [TokenCommandTabPrev(), TokenEof()]

    bang = c == '!'

    return None, [TokenCommandTabPrev(forced=bang), TokenEof()]
