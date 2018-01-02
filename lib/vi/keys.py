import re

from NeoVintageous.lib import nvim
from NeoVintageous.lib import plugin
from NeoVintageous.lib.vi import cmd_base
from NeoVintageous.lib.vi import variables
from NeoVintageous.lib.vi.utils import modes


_logger = nvim.get_logger(__name__)


class mapping_scopes:
    """Scopes for mappings."""

    DEFAULT = 0
    USER = 1
    PLUGIN = 2
    NAME_SPACE = 3
    LEADER = 4
    LOCAL_LEADER = 5


class seqs:
    """
    Vim's built-in key sequences plus Sublime Text 3 staple commands.

    These are the sequences of key presses known to NeoVintageous. Any other
    sequence pressed will be treated as 'unmapped'.
    """

    A = 'a'
    ALT_CTRL_P = '<C-M-p>'
    AMPERSAND = '&'
    AT = '@'
    AW = 'aw'
    B = 'b'
    BACKSPACE = '<bs>'
    BACKTICK = '`'
    BIG_A = 'A'
    BIG_B = 'B'
    BIG_C = 'C'
    BIG_D = 'D'
    BIG_E = 'E'
    BIG_F = 'F'
    BIG_G = 'G'
    BIG_H = 'H'
    BIG_I = 'I'
    BIG_J = 'J'
    BIG_K = 'K'
    BIG_L = 'L'
    BIG_M = 'M'
    BIG_N = 'N'
    BIG_O = 'O'
    BIG_P = 'P'
    BIG_Q = 'Q'
    BIG_R = 'R'
    BIG_S = 'S'
    BIG_T = 'T'
    BIG_U = 'U'
    BIG_V = 'V'
    BIG_W = 'W'
    BIG_X = 'X'
    BIG_Y = 'Y'
    BIG_Z = 'Z'
    BIG_Z_BIG_Q = 'ZQ'
    BIG_Z_BIG_Z = 'ZZ'
    C = 'c'
    CC = 'cc'
    COLON = ':'
    COMMA = ','
    CTRL_0 = '<C-0>'
    CTRL_1 = '<C-1>'
    CTRL_2 = '<C-2>'
    CTRL_3 = '<C-3>'
    CTRL_4 = '<C-4>'
    CTRL_5 = '<C-5>'
    CTRL_6 = '<C-6>'
    CTRL_7 = '<C-7>'
    CTRL_8 = '<C-8>'
    CTRL_9 = '<C-9>'
    CTRL_A = '<C-a>'
    CTRL_B = '<C-b>'
    CTRL_BIG_F = '<C-F>'
    CTRL_BIG_P = '<C-P>'
    CTRL_C = '<C-c>'
    CTRL_D = '<C-d>'
    CTRL_DOT = '<C-.>'
    CTRL_E = '<C-e>'
    CTRL_ENTER = '<C-cr>'
    CTRL_F = '<C-f>'
    CTRL_F12 = '<C-f12>'
    CTRL_F2 = '<C-f2>'
    CTRL_G = '<C-g>'
    CTRL_I = '<C-i>'
    CTRL_J = '<C-j>'
    CTRL_K = '<C-k>'
    CTRL_K_CTRL_B = '<C-k><C-b>'
    CTRL_L = '<C-l>'
    CTRL_LEFT_SQUARE_BRACKET = '<C-[>'
    CTRL_N = '<C-n>'
    CTRL_O = '<C-o>'
    CTRL_P = '<C-p>'
    CTRL_R = '<C-r>'
    CTRL_R_EQUAL = '<C-r>='
    CTRL_RIGHT_SQUARE_BRACKET = '<C-]>'
    CTRL_SHIFT_B = '<C-S-b>'
    CTRL_SHIFT_DOT = '<C-S-.>'
    CTRL_SHIFT_ENTER = '<C-S-cr>'
    CTRL_SHIFT_F2 = '<C-S-f2>'
    CTRL_U = '<C-u>'
    CTRL_V = '<C-v>'
    CTRL_W = '<C-w>'
    CTRL_W_B = '<C-w>b'
    CTRL_W_BACKSPACE = '<C-w><bs>'
    CTRL_W_BIG_H = '<C-w>H'
    CTRL_W_BIG_J = '<C-w>J'
    CTRL_W_BIG_K = '<C-w>K'
    CTRL_W_BIG_L = '<C-w>L'
    CTRL_W_BIG_S = '<C-w>S'
    CTRL_W_C = '<C-w>c'
    CTRL_W_CTRL_B = '<C-w><C-b>'
    CTRL_W_CTRL_H = '<C-w><C-h>'
    CTRL_W_CTRL_J = '<C-w><C-j>'
    CTRL_W_CTRL_K = '<C-w><C-k>'
    CTRL_W_CTRL_L = '<C-w><C-l>'
    CTRL_W_CTRL_N = '<C-w><C-n>'
    CTRL_W_CTRL_O = '<C-w><C-o>'
    CTRL_W_CTRL_Q = '<C-w><C-q>'
    CTRL_W_CTRL_S = '<C-w><C-s>'
    CTRL_W_CTRL_T = '<C-w><C-t>'
    CTRL_W_CTRL_UNDERSCORE = '<C-w><C-_>'
    CTRL_W_CTRL_V = '<C-w><C-v>'
    CTRL_W_CTRL_X = '<C-w><C-x>'
    CTRL_W_DOWN = '<C-w><down>'
    CTRL_W_EQUAL = '<C-w>='
    CTRL_W_GREATER_THAN = '<C-w>>'
    CTRL_W_H = '<C-w>h'
    CTRL_W_J = '<C-w>j'
    CTRL_W_K = '<C-w>k'
    CTRL_W_L = '<C-w>l'
    CTRL_W_LEFT = '<C-w><left>'
    CTRL_W_LESS_THAN = '<C-w><lt>'
    CTRL_W_MINUS = '<C-w>-'
    CTRL_W_N = '<C-w>n'
    CTRL_W_O = '<C-w>o'
    CTRL_W_PIPE = '<C-w>|'
    CTRL_W_PLUS = '<C-w>+'
    CTRL_W_Q = '<C-w>q'
    CTRL_W_RIGHT = '<C-w><right>'
    CTRL_W_S = '<C-w>s'
    CTRL_W_T = '<C-w>t'
    CTRL_W_UNDERSCORE = '<C-w>_'
    CTRL_W_UP = '<C-w><up>'
    CTRL_W_V = '<C-w>v'
    CTRL_W_X = '<C-w>x'
    CTRL_X = '<C-x>'
    CTRL_X = '<C-x>'
    CTRL_X_CTRL_L = '<C-x><C-l>'
    CTRL_Y = '<C-y>'
    D = 'd'
    DD = 'dd'
    DOLLAR = '$'
    DOT = '.'
    DOUBLE_QUOTE = '"'
    DOWN = '<down>'
    E = 'e'
    END = '<end>'
    ENTER = '<cr>'  # Or rather <Enter>?
    EQUAL = '='
    EQUAL_EQUAL = '=='
    ESC = '<esc>'
    F = 'f'
    F1 = '<f1>'
    F10 = '<f10>'
    F11 = '<f11>'
    F12 = '<f12>'
    F13 = '<f13>'
    F14 = '<f14>'
    F15 = '<f15>'
    F2 = '<f2>'
    F3 = '<f3>'
    F4 = '<f4>'
    F5 = '<f5>'
    F6 = '<f6>'
    F7 = '<f7>'
    F8 = '<f8>'
    F9 = '<f9>'
    G = 'g'
    G_BIG_C = 'gC'
    G_BIG_D = 'gD'
    G_BIG_E = 'gE'
    G_BIG_H = 'gH'
    G_BIG_J = 'gJ'
    G_BIG_T = 'gT'
    G_BIG_U = 'gU'
    G_BIG_U_BIG_U = 'gUU'
    G_BIG_U_G_BIG_U = 'gUgU'
    G_TILDE = 'g~'
    G_TILDE_G_TILDE = 'g~g~'
    G_TILDE_TILDE = 'g~~'
    G_UNDERSCORE = 'g_'
    GA = 'ga'
    GC = 'gc'
    GCC = 'gcc'
    GD = 'gd'
    GE = 'ge'
    GG = 'gg'
    GH = 'gh'
    GJ = 'gj'
    GK = 'gk'
    GM = 'gm'
    GQ = 'gq'
    GREATER_THAN = '>'
    GREATER_THAN_GREATER_THAN = '>>'
    GT = 'gt'
    GU = 'gu'
    GUGU = 'gugu'
    GUU = 'guu'
    GV = 'gv'
    GX = 'gx'
    H = 'h'
    HAT = '^'
    HOME = '<home>'
    I = 'i'  # noqa: E741
    J = 'j'
    K = 'k'
    L = 'l'
    LEFT = '<left>'
    LEFT_BRACE = '{'
    LEFT_PAREN = '('
    LEFT_SQUARE_BRACKET = '['
    LEFT_SQUARE_BRACKET_C = '[c'
    LESS_THAN = '<lt>'
    LESS_THAN_LESS_THAN = '<lt><lt>'
    M = 'm'
    MINUS = '-'
    N = 'n'
    O = 'o'  # noqa: E741
    OCTOTHORP = '#'
    P = 'p'
    PAGE_DOWN = 'pagedown'
    PAGE_UP = 'pageup'
    PERCENT = '%'
    PIPE = '|'
    PLUS = '+'
    Q = 'q'
    QUESTION_MARK = '?'
    QUOTE = "'"
    QUOTE_QUOTE = "''"
    R = 'r'
    RIGHT = '<right>'
    RIGHT_BRACE = '}'
    RIGHT_PAREN = ')'
    RIGHT_SQUARE_BRACKET = ']'
    RIGHT_SQUARE_BRACKET_C = ']c'
    S = 's'
    SEMICOLON = ';'
    SHIFT_CTRL_F12 = '<C-S-f12>'
    SHIFT_ENTER = '<S-cr>'
    SHIFT_F11 = '<S-f11>'
    SHIFT_F2 = '<S-f2>'
    SHIFT_F3 = '<S-f3>'
    SHIFT_F4 = '<S-f4>'
    SLASH = '/'
    SPACE = '<space>'
    STAR = '*'
    T = 't'
    TAB = '<tab>'
    TILDE = '~'
    U = 'u'
    UNDERSCORE = '_'
    UP = '<up>'
    V = 'v'
    W = 'w'
    X = 'x'
    Y = 'y'
    YY = 'yy'
    Z = 'z'
    Z_ENTER = 'z<cr>'
    Z_MINUS = 'z-'
    ZB = 'zb'
    ZERO = '0'
    ZT = 'zt'
    ZZ = 'zz'


def seq_to_command(state, seq, mode=None):
    # Return the command definition mapped to seq.
    #
    # Args:
    #   seq (str): The command sequence.
    #   mode (str): Forces the use of this mode instead of the global state's.
    #
    # Returns:
    #   Mapping:
    #   ViMissingCommandDef: If not found.
    mode = mode or state.mode

    _logger.info('mode = \'%s\', seq = \'%s\'', mode, seq)

    command = None

    if state.mode in plugin.mappings:
        command = plugin.mappings[mode].get(seq, None)

        # The plugin command might only be enabled under certain conditions
        if command and hasattr(command, 'is_enabled') and (not command.is_enabled(state)):
            command = None

    if not command and state.mode in mappings:
        command = mappings[mode].get(seq, cmd_base.ViMissingCommandDef())

    if command:
        return command

    return cmd_base.ViMissingCommandDef()


# Mappings 'key sequence' ==> 'command definition'
#
# 'key sequence' is a sequence of key presses.
#
mappings = {
    modes.INSERT: {},
    modes.NORMAL: {},
    modes.VISUAL: {},
    modes.OPERATOR_PENDING: {},
    modes.VISUAL_LINE: {},
    modes.VISUAL_BLOCK: {},
    modes.SELECT: {},
    '_missing': dict(name='_missing')
}


# TODO: Add a timeout for ambiguous cmd_base.
# Key sequence to command mapping. Mappings are set by the user.
#
# Returns a partial definition containing the user-pressed keys so that we
# can replay the command exactly as it was typed in.
user_mappings = {
    # 'jkl': dict(name='dd', type=cmd_types.USER),
}


EOF = -2


class key_names:
    """Names of special keys."""

    BACKSPACE = '<bs>'
    CR = '<cr>'
    DOWN = '<down>'
    END = '<end>'
    ENTER = '<enter>'
    ESC = '<esc>'
    HOME = '<home>'
    LEFT = '<left>'
    LESS_THAN = '<lt>'
    RIGHT = '<right>'
    SPACE = '<sp>'
    SPACE_LONG = '<space>'
    TAB = '<tab>'
    UP = '<up>'

    F1 = '<f1>'
    F2 = '<f2>'
    F3 = '<f3>'
    F4 = '<f4>'
    F5 = '<f5>'
    F6 = '<f6>'
    F7 = '<f7>'
    F8 = '<f8>'
    F9 = '<f9>'
    F10 = '<f10>'
    F11 = '<f11>'
    F12 = '<f12>'
    F13 = '<f13>'
    F14 = '<f14>'
    F15 = '<f15>'
    Leader = '<leader>'

    as_list = [
        BACKSPACE,
        CR,
        DOWN,
        END,
        ENTER,
        ESC,
        HOME,
        LEFT,
        LESS_THAN,
        RIGHT,
        SPACE,
        SPACE_LONG,
        TAB,
        UP,

        F1,
        F2,
        F3,
        F4,
        F5,
        F6,
        F7,
        F8,
        F9,
        F10,
        F11,
        F12,
        F13,
        F14,
        F15,

        Leader,
    ]

    max_len = len('<space>')


# TODO: detect counts, registers, marks...
class KeySequenceTokenizer(object):
    """Takes in a sequence of key names and tokenizes it."""

    def __init__(self, source):
        """Sequence of key names in Vim notation."""
        self.idx = -1
        self.source = source
        self.in_named_key = False

    def consume(self):
        self.idx += 1
        if self.idx >= len(self.source):
            self.idx -= -1
            return EOF
        return self.source[self.idx]

    def peek_one(self):
        if (self.idx + 1) >= len(self.source):
            return EOF
        return self.source[self.idx + 1]

    def is_named_key(self, key):
        return key.lower() in key_names.as_list

    def sort_modifiers(self, modifiers):
        """Ensure consistency in the order of modifier letters according to c > m > s."""
        if len(modifiers) == 6:
            modifiers = 'c-m-s-'
        elif len(modifiers) > 2:
            if modifiers.startswith('s-') and modifiers.endswith('c-'):
                modifiers = 'c-s-'
            elif modifiers.startswith('s-') and modifiers.endswith('m-'):
                modifiers = 'm-s-'
            elif modifiers.startswith('m-') and modifiers.endswith('c-'):
                modifiers = 'c-m-'
        return modifiers

    def long_key_name(self):
        self.in_named_key = True
        key_name = ''
        modifiers = ''

        while True:
            c = self.consume()

            if c == EOF:
                raise ValueError("expected '>' at index {0}".format(self.idx))

            elif (c.lower() in ('c', 's', 'm')) and (self.peek_one() == '-'):
                if c.lower() in modifiers.lower():
                    raise ValueError('invalid modifier sequence: {0}'.format(self.source))

                modifiers += c + self.consume()

            elif c == '>' and self.peek_one() == '>':
                modifiers = self.sort_modifiers(modifiers.lower())

                if len(key_name) == 0:
                    return '<' + modifiers.upper() + self.consume() + '>'

                else:
                    raise ValueError('wrong key {0}'.format(key_name))

            elif c == '>':
                modifiers = self.sort_modifiers(modifiers.lower())

                if len(key_name) == 1:
                    if not modifiers:
                        raise ValueError('wrong sequence {0}'.format(self.source))
                    return '<' + modifiers.upper() + key_name + '>'

                elif self.is_named_key('<' + key_name + '>'):
                    self.in_named_key = False
                    return '<' + modifiers.upper() + key_name.lower() + '>'

                else:
                    raise ValueError("'{0}' is not a known key".format(key_name))

            else:
                key_name += c

    def tokenize_one(self):
        c = self.consume()

        if c == '<':
            return self._expand_vars(self.long_key_name())
        else:
            return c

    def iter_tokenize(self):
        while True:
            token = self.tokenize_one()
            if token == EOF:
                break
            yield token

    def _expand_vars(self, c):
        return variables.get(c) if variables.is_key_name(c) else c


def to_bare_command_name(seq):
    # Args:
    #   seq (str): The command sequence.
    #
    # Return:
    #   str: The command sequence with register and counts strips e.g. 2daw ->
    #       daw, "a2d2aw -> daw, etc. The special case '0' is returned
    #       unmodified.
    if seq == '0':
        return seq

    new_seq = re.sub(r'^(?:".)?(?:[1-9]+)?', '', seq)
    # Account for d2d and similar sequences.
    new_seq = list(KeySequenceTokenizer(new_seq).iter_tokenize())

    return ''.join(k for k in new_seq if not k.isdigit())


def assign(seq, modes, *args, **kwargs):
    """
    Register a 'key sequence' to 'command' mapping with NeoVintageous.

    The registered key sequence must be known to NeoVintageous. The
    registered command must be a ViMotionDef or ViOperatorDef.

    The decorated class is instantiated with `*args` and `**kwargs`.

    @keys
      A list of (`mode:tuple`, `sequence:string`) pairs to map the decorated
      class to.
    """
    def inner(cls):
        for mode in modes:
            mappings[mode][seq] = cls(*args, **kwargs)
        return cls
    return inner
