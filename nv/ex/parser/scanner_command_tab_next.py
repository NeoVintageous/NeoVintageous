from .state import EOF
from .tokens import TokenEof
from .tokens_base import TOKEN_COMMAND_TAB_NEXT
from .tokens_base import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('tabnext', 'tabn')
class TokenTabNext(TokenOfCommand):
    def __init__(self, *args, **kwargs):
        super().__init__([], TOKEN_COMMAND_TAB_NEXT, 'tabnext', *args, **kwargs)
        self.target_command = 'ex_tabnext'


def scan_command_tab_next(state):
    c = state.consume()

    if c == EOF:
        return None, [TokenTabNext(), TokenEof()]

    bang = c == '!'

    return None, [TokenTabNext(forced=bang), TokenEof()]
