from . import scanner_commands
from .scanner_state import ScannerState
from .tokens import TokenComma
from .tokens import TokenDigits
from .tokens import TokenDollar
from .tokens import TokenDot
from .tokens import TokenEof
from .tokens import TokenMark
from .tokens import TokenOffset
from .tokens import TokenPercent
from .tokens import TokenSearchBackward
from .tokens import TokenSearchForward
from .tokens import TokenSemicolon


class Scanner:

    # Produce ex command-line tokens from a string.
    #
    # Attributes:
    #   :state (ScannerState):
    #
    # TODO Make this class a function. We don't need a state object reference.

    def __init__(self, source):
        # type: (str) -> None
        self.state = ScannerState(source)

    def scan(self):
        # Generate ex command-line tokens for source. The scanner works its way
        # through the source string by passing the current state to the next
        # scanning function.
        next_func = _scan_range
        while True:
            # We return multiple tokens so that we can work around cyclic
            # imports: functions that need to, return TokenEof without having to
            # call a function in this module from a separate module. Keep
            # scanning while we get a scanning function.
            (next_func, items) = next_func(self.state)
            yield from items
            if not next_func:
                break


def _scan_range(state):
    # Produce tokens found in a command line range.
    # https://vimhelp.appspot.com/cmdline.txt.html#cmdline-ranges
    #
    # Args:
    #   :state (ScannerState):
    #
    # Returns:
    #   tuple

    c = state.consume()

    if c == state.EOF:
        return None, [TokenEof()]

    if c == '.':
        state.emit()

        return _scan_range, [TokenDot()]

    if c == '$':
        state.emit()

        return _scan_range, [TokenDollar()]

    if c in ',;':
        token = TokenComma if c == ',' else TokenSemicolon
        state.emit()

        return _scan_range, [token()]

    if c == "'":
        return _scan_mark(state)

    if c in '/?':
        return _scan_search(state)

    if c in '+-':
        return _scan_offset(state)

    if c == '%':
        state.emit()

        return _scan_range, [TokenPercent()]

    if c in '\t ':
        state.skip_run(' \t')
        state.ignore()

    if c.isdigit():
        return _scan_digits(state)

    state.backup()

    return _scan_command, []


def _scan_mark(state):
    c = state.expect_match(r'[a-zA-Z\[\]()<>]')

    return _scan_range, [TokenMark(c.group(0))]


def _scan_digits(state):
    while True:
        c = state.consume()
        if not c.isdigit():
            if c == state.EOF:
                return None, [TokenDigits(state.emit()), TokenEof()]

            state.backup()
            break

    return _scan_range, [TokenDigits(state.emit())]


def _scan_search(state):
    delim = state.source[state.position - 1]
    while True:
        c = state.consume()

        if c == delim:
            state.start += 1
            state.backup()
            content = state.emit()
            state.consume()
            token = TokenSearchForward if c == '/' else TokenSearchBackward

            return _scan_range, [token(content)]

        elif c == state.EOF:
            raise ValueError('unclosed search pattern: {0}'.format(state.source))


def _scan_offset(state):
    offsets = []

    def to_int(x):
        return int(x, 10)

    sign = '-' if state.source[state.position - 1] == '-' else ''

    digits = state.expect_match(r'\s*(\d+)')
    offsets.append(sign + digits.group(1))

    while True:
        c = state.consume()

        if c == state.EOF:
            state.ignore()

            return None, [TokenOffset(list(map(to_int, offsets))), TokenEof()]

        if c == '+' or c == '-':
            digits = state.expect_match(r'\s*(\d+)')
            sign = '-' if state.source[state.position - 1] == '-' else ''
            offsets.append(sign + digits.group(1))
            continue

        if not c.isdigit():
            state.backup()
            state.ignore()

            return _scan_range, [TokenOffset(list(map(to_int, offsets)))]


def _scan_command(state):
    # Args:
    #   :state (ScannerState):
    #
    # Returns:
    #   Tuple[None, list(TokenEof)]
    for route, command in scanner_commands.routes.items():
        if state.match(route):
            state.ignore()

            return command(state)

    state.expect_eof(lambda: Exception("E492: Not an editor command"))

    return None, [TokenEof()]
