from .tokens import TOKEN_COMMAND_GOTO
from .tokens import TokenOfCommand


# TODO Make this default command separate to normal ex commands
# This command cannot be scanned.
# It's the default command when
# no command is named.
class TokenCommandGoto(TokenOfCommand):
    def __init__(self, *args, **kwargs):
        super().__init__([], TOKEN_COMMAND_GOTO, 'goto', *args, **kwargs)
        self.target_command = 'ex_goto'
