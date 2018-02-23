from .tokens import TOKEN_COMMAND_TAB_FIRST
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('tabfirst', 'tabfir')
@ex.command('tabrewind', 'tabr')
class TokenCommandTabFirst(TokenOfCommand):
    def __init__(self, *args, **kwargs):
        super().__init__([], TOKEN_COMMAND_TAB_FIRST, 'tabfirst', *args, **kwargs)
        self.target_command = 'ex_tabfirst'


def scan_cmd_tab_first(state):
    c = state.consume()
    if c == state.EOF:
        return None, [TokenCommandTabFirst(), TokenEof()]

    # TODO [bug] ":command" followed by character that is not "!"  shouldn't be
    # valid e.g. the ":close" command should run when !:closex". There are a
    # bunch of commands that have this bug.

    bang = c == '!'

    return None, [TokenCommandTabFirst(forced=bang), TokenEof()]
