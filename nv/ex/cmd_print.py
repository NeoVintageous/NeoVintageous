from .tokens import TOKEN_COMMAND_PRINT
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('print', 'p')
class TokenCommandPrint(TokenOfCommand):
    def __init__(self, params, *args, **kwargs):
        super().__init__(params, TOKEN_COMMAND_PRINT, 'print', *args, **kwargs)
        self.addressable = True
        self.cooperates_with_global = True
        self.target_command = 'ex_print'

    def __str__(self):
        return "{0} {1} {2}".format(self.content, ''.join(self.flags), self.count).strip()

    @property
    def count(self):
        return self.params['count']

    @property
    def flags(self):
        return self.params['flags']


def scan_cmd_print(state):
    params = {
        'count': '',
        'flags': [],
    }

    while True:
        c = state.consume()

        state.skip(' ')
        state.ignore()

        if c == state.EOF:
            return None, [TokenCommandPrint(params), TokenEof()]

        if c.isdigit():
            state.match(r'\d*')
            params['count'] = state.emit()
            continue

        m = state.expect_match(r'[l#p]+')
        params['flags'] = list(m.group(0))
        state.ignore()
        state.expect_eof()
        break

    return None, [TokenCommandPrint(params), TokenEof()]
