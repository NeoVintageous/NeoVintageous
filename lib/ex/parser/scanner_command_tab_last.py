from .state import EOF
from .tokens import TokenEof
from .tokens_base import TOKEN_COMMAND_TAB_LAST
from .tokens_base import TokenOfCommand
from NeoVintageous.lib import ex


@ex.command('tablast', 'tabl')
class TokenTabLast(TokenOfCommand):
    def __init__(self, *args, **kwargs):
        super().__init__([], TOKEN_COMMAND_TAB_LAST, 'tablast', *args, **kwargs)
        self.target_command = 'ex_tablast'


def scan_command_tab_last(state):
    c = state.consume()

    if c == EOF:
        return None, [TokenTabLast(), TokenEof()]

    bang = c == '!'

    return None, [TokenTabLast(forced=bang), TokenEof()]
