from .tokens import TOKEN_COMMAND_TAB_LAST
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('tablast', 'tabl')
class TokenCommandTabLast(TokenOfCommand):
    def __init__(self, *args, **kwargs):
        super().__init__([], TOKEN_COMMAND_TAB_LAST, 'tablast', *args, **kwargs)
        self.target_command = 'ex_tablast'


def scan_cmd_tab_last(state):
    c = state.consume()
    if c == state.EOF:
        return None, [TokenCommandTabLast(), TokenEof()]

    bang = c == '!'

    return None, [TokenCommandTabLast(forced=bang), TokenEof()]
