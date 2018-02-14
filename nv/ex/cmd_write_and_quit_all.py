from .scanner_state import EOF
from .tokens import TOKEN_COMMAND_WRITE_AND_QUIT_ALL
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


plus_plus_translations = {
    'ff': 'fileformat',
    'bin': 'binary',
    'enc': 'fileencoding',
    'nobin': 'nobinary',
}


@ex.command('wqall', 'wqa')
@ex.command('xall', 'xa')
class TokenCommandWriteAndQuitAll(TokenOfCommand):
    def __init__(self, params, *args, **kwargs):
        super().__init__(params, TOKEN_COMMAND_WRITE_AND_QUIT_ALL, 'wqall', *args, **kwargs)
        self.addressable = True
        self.target_command = 'ex_write_and_quit_all'

    @property
    def options(self):
        return self.params['++']


def scan_cmd_write_and_quit_all(state):
    params = {
        '++': '',
    }

    state.skip(' ')
    state.ignore()

    c = state.consume()
    if c == '+':
        state.expect('+')
        state.ignore()
        # TODO: expect_match should work with emit()
        # https://vimhelp.appspot.com/editing.txt.html#[++opt]
        m = state.expect_match(
            r'(?:f(?:ile)?f(?:ormat)?|(?:file)?enc(?:oding)?|(?:no)?bin(?:ary)?|bad|edit)(?=\s|$)',
            lambda: Exception("E474: Invalid argument"))

        name = m.group(0)
        params['++'] = plus_plus_translations.get(name, name)
        state.ignore()

    state.expect(EOF)

    return None, [TokenCommandWriteAndQuitAll(params), TokenEof()]
