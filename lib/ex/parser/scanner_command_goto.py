from .tokens_base import TOKEN_COMMAND_GOTO
from .tokens_base import TokenOfCommand


# This command cannot be scanned.
# It's the default command when
# no command is named.
class TokenCommandGoto(TokenOfCommand):
    def __init__(self, *args, **kwargs):
        super().__init__([], TOKEN_COMMAND_GOTO, 'goto', *args, **kwargs)
        self.target_command = 'ex_goto'
