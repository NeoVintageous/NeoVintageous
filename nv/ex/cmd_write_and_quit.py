from .tokens import TOKEN_COMMAND_WRITE_AND_QUIT
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


plus_plus_translations = {
    'ff': 'fileformat',
    'bin': 'binary',
    'enc': 'fileencoding',
    'nobin': 'nobinary',
}


@ex.command('wq', 'wq')
class TokenCommandWriteAndQuit(TokenOfCommand):
    def __init__(self, params, *args, **kwargs):
        super().__init__(params, TOKEN_COMMAND_WRITE_AND_QUIT, 'wq', *args, **kwargs)
        self.target_command = 'ex_write_and_quit'


def scan_cmd_write_and_quit(state):
    params = {
        '++': None,
        'file': None,
    }

    c = state.consume()
    if c == state.EOF:
        return None, [TokenCommandWriteAndQuit(params), TokenEof()]

    bang = True if c == '!' else False
    if not bang:
        state.backup()

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
        raise NotImplementedError('param not implemented')

    if c == state.EOF:
        return None, [TokenCommandWriteAndQuit(params), TokenEof()]

    m = state.expect_match(r'.+$')
    params['file'] = m.group(0).strip()

    return None, [TokenCommandWriteAndQuit(params), TokenEof()]
