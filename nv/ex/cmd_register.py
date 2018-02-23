from .tokens import TOKEN_COMMAND_REGISTERS
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('registers', 'reg')
class TokenCommandRegisters(TokenOfCommand):
    def __init__(self, params, *args, **kwargs):
        super().__init__(params, TOKEN_COMMAND_REGISTERS, 'registers', *args, **kwargs)
        self.target_command = 'ex_registers'


def scan_cmd_register(state):
    params = {'names': []}

    state.skip(' ')
    state.ignore()

    while True:
        c = state.consume()
        if c == state.EOF:
            return None, [TokenCommandRegisters(params), TokenEof()]
        elif c.isalpha() or c.isdigit():
            params['names'].append(c)
        else:
            raise ValueError('wrong arguments')
