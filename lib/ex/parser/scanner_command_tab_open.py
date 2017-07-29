from .tokens_base import TOKEN_COMMAND_TAB_OPEN
from .tokens_base import TokenOfCommand


class TokenTabOpen(TokenOfCommand):
    def __init__(self, params, *args, **kwargs):
        super().__init__([], TOKEN_COMMAND_TAB_OPEN, 'tab_open', *args, **kwargs)
        self.target_command = 'ex_tabopen'


def scan_command_tab_open(state):
    raise NotImplementedError()
