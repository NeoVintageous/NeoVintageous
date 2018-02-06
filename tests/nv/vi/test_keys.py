from collections import namedtuple
import unittest

from NeoVintageous.nv.vi import variables
from NeoVintageous.nv.vi.keys import KeySequenceTokenizer
from NeoVintageous.nv.vi.keys import seqs
from NeoVintageous.nv.vi.keys import to_bare_command_name
from NeoVintageous.nv.vi.utils import translate_char


_TESTS_TOKENIZER = (
    ('p', 'p', 'lower letter key'),
    ('P', 'P', 'upper case letter key'),
    ('<C-p>', '<C-p>', 'ctrl-modified lower case letter key'),
    ('<C-P>', '<C-P>', 'ctrl-modified upper case letter key'),
    ('<C-S-.>', '<C-S-.>', 'ctrl-shift modified period key'),
    ('<Esc>', '<esc>', 'esc key title case'),
    ('<esc>', '<esc>', 'esc key lowercase'),
    ('<eSc>', '<esc>', 'esc key mixed case'),
    ('<lt>', '<lt>', 'less than key'),
    ('<HOME>', '<home>', 'less than key'),
    ('<enD>', '<end>', 'less than key'),
    ('<uP>', '<up>', 'less than key'),
    ('<DoWn>', '<down>', 'less than key'),
    ('<left>', '<left>', 'less than key'),
    ('<RigHt>', '<right>', 'less than key'),
    ('<Space>', '<space>', 'space key'),
    ('<c-Space>', '<C-space>', 'ctrl-space key'),
    ('0', '0', 'zero key'),
    ('<c-m-.>', '<C-M-.>', 'ctrl-alt-period key'),
    ('<tab>', '<tab>', 'tab key'),
    ('<Leader>', '\\', 'leader key'),
)


class TestKeySequenceTokenizerTokenizeOne(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.old_vars = variables._VARIABLES
        variables._VARIABLES = {}

    def parse(self, input_):
        tokenizer = KeySequenceTokenizer(input_)
        return tokenizer.tokenize_one()

    def test_all(self):
        for (i, t) in enumerate(_TESTS_TOKENIZER):
            input_, expected, msg = t
            self.assertEqual(self.parse(input_), expected, "{0} - {1}".format(i, msg))

    def tearDown(self):
        super().tearDown()
        variables._VARIABLES = self.old_vars


_TESTS_ITER_TOKENIZE = (
    ('pp', ['p', 'p'], 'sequence'),
    ('<C-p>', ['<C-p>'], 'sequence'),
    ('<C-P>x', ['<C-P>', 'x'], 'sequence'),
    ('<C-S-.>', ['<C-S-.>'], 'sequence'),
    ('<Esc>ai', ['<esc>', 'a', 'i'], 'sequence'),
    ('<lt><lt>', ['<lt>', '<lt>'], 'sequence'),
    ('<DoWn>abc.', ['<down>', 'a', 'b', 'c', '.'], 'sequence'),
    ('0<down>', ['0', '<down>'], 'sequence'),
    ('<c-m-.>', ['<C-M-.>'], 'sequence'),
)


class TestKeySequenceTokenizerIterTokenize(unittest.TestCase):

    def parse(self, input_):
        tokenizer = KeySequenceTokenizer(input_)
        return list(tokenizer.iter_tokenize())

    def test_all(self):
        for (i, t) in enumerate(_TESTS_ITER_TOKENIZE):
            input_, expected, msg = t
            self.assertEqual(self.parse(input_), expected, "{0} - {1}".format(i, msg))


class TestToBareCommandName(unittest.TestCase):

    def test_to_bare_command_name(self):
        self.assertEquals('daw', to_bare_command_name('daw'))
        self.assertEquals('daw', to_bare_command_name('2daw'))
        self.assertEquals('daw', to_bare_command_name('d2aw'))
        self.assertEquals('daw', to_bare_command_name('2d2aw'))
        self.assertEquals('daw', to_bare_command_name('"a2d2aw'))
        self.assertEquals('daw', to_bare_command_name('"12d2aw'))
        self.assertEquals('<f7>', to_bare_command_name('<f7>'))
        self.assertEquals('<f7>', to_bare_command_name('10<f7>'))
        self.assertEquals('<f7>', to_bare_command_name('"a10<f7>'))
        self.assertEquals('<f7>', to_bare_command_name('"a10<f7>'))
        self.assertEquals('<f7>', to_bare_command_name('"210<f7>'))
        self.assertEquals('0', to_bare_command_name('0'))
        self.assertEquals('dd', to_bare_command_name('d2d'))


_TRANLATION_TESTS = (
    ('<enter>', '\n', ''),
    ('<cr>', '\n', ''),
    ('<sp>', ' ', ''),
    ('<space>', ' ', ''),
    ('<lt>', '<', ''),
    ('a', 'a', ''),
)


class TestTranslateChar(unittest.TestCase):

    def test_all(self):
        for (i, t) in enumerate(_TRANLATION_TESTS):
            input_, expected, msg = t
            self.assertEqual(translate_char(input_), expected, "{0} - {1}".format(i, msg))


_seq_test = namedtuple('_seq_test', 'actual expected')


_TESTS_KNOWN_SEQUENCES = (
    _seq_test(actual=seqs.A, expected='a'),
    _seq_test(actual=seqs.ALT_CTRL_P, expected='<C-M-p>'),
    _seq_test(actual=seqs.AMPERSAND, expected='&'),
    _seq_test(actual=seqs.AT, expected='@'),
    _seq_test(actual=seqs.AW, expected='aw'),
    _seq_test(actual=seqs.B, expected='b'),
    _seq_test(actual=seqs.BACKSPACE, expected='<bs>'),
    _seq_test(actual=seqs.BACKTICK, expected='`'),
    _seq_test(actual=seqs.BIG_A, expected='A'),
    _seq_test(actual=seqs.BIG_B, expected='B'),
    _seq_test(actual=seqs.BIG_C, expected='C'),
    _seq_test(actual=seqs.BIG_D, expected='D'),
    _seq_test(actual=seqs.BIG_E, expected='E'),
    _seq_test(actual=seqs.BIG_F, expected='F'),
    _seq_test(actual=seqs.BIG_G, expected='G'),
    _seq_test(actual=seqs.BIG_H, expected='H'),
    _seq_test(actual=seqs.BIG_I, expected='I'),
    _seq_test(actual=seqs.BIG_J, expected='J'),
    _seq_test(actual=seqs.BIG_K, expected='K'),
    _seq_test(actual=seqs.BIG_L, expected='L'),
    _seq_test(actual=seqs.BIG_M, expected='M'),
    _seq_test(actual=seqs.BIG_N, expected='N'),
    _seq_test(actual=seqs.BIG_O, expected='O'),
    _seq_test(actual=seqs.BIG_P, expected='P'),
    _seq_test(actual=seqs.BIG_Q, expected='Q'),
    _seq_test(actual=seqs.BIG_R, expected='R'),
    _seq_test(actual=seqs.BIG_S, expected='S'),
    _seq_test(actual=seqs.BIG_T, expected='T'),
    _seq_test(actual=seqs.BIG_U, expected='U'),
    _seq_test(actual=seqs.BIG_V, expected='V'),
    _seq_test(actual=seqs.BIG_W, expected='W'),
    _seq_test(actual=seqs.BIG_X, expected='X'),
    _seq_test(actual=seqs.BIG_Y, expected='Y'),
    _seq_test(actual=seqs.BIG_Z, expected='Z'),
    _seq_test(actual=seqs.BIG_Z_BIG_Q, expected='ZQ'),
    _seq_test(actual=seqs.BIG_Z_BIG_Z, expected='ZZ'),
    _seq_test(actual=seqs.C, expected='c'),
    _seq_test(actual=seqs.CC, expected='cc'),
    _seq_test(actual=seqs.COLON, expected=':'),
    _seq_test(actual=seqs.COMMA, expected=','),
    _seq_test(actual=seqs.COMMAND_BIG_B, expected='<D-B>'),
    _seq_test(actual=seqs.COMMAND_BIG_F, expected='<D-F>'),
    _seq_test(actual=seqs.COMMAND_BIG_P, expected='<D-P>'),
    _seq_test(actual=seqs.COMMAND_P, expected='<D-p>'),
    _seq_test(actual=seqs.CTRL_0, expected='<C-0>'),
    _seq_test(actual=seqs.CTRL_1, expected='<C-1>'),
    _seq_test(actual=seqs.CTRL_2, expected='<C-2>'),
    _seq_test(actual=seqs.CTRL_3, expected='<C-3>'),
    _seq_test(actual=seqs.CTRL_4, expected='<C-4>'),
    _seq_test(actual=seqs.CTRL_5, expected='<C-5>'),
    _seq_test(actual=seqs.CTRL_6, expected='<C-6>'),
    _seq_test(actual=seqs.CTRL_7, expected='<C-7>'),
    _seq_test(actual=seqs.CTRL_8, expected='<C-8>'),
    _seq_test(actual=seqs.CTRL_9, expected='<C-9>'),
    _seq_test(actual=seqs.CTRL_A, expected='<C-a>'),
    _seq_test(actual=seqs.CTRL_B, expected='<C-b>'),
    _seq_test(actual=seqs.CTRL_BIG_F, expected='<C-F>'),
    _seq_test(actual=seqs.CTRL_BIG_P, expected='<C-P>'),
    _seq_test(actual=seqs.CTRL_C, expected='<C-c>'),
    _seq_test(actual=seqs.CTRL_D, expected='<C-d>'),
    _seq_test(actual=seqs.CTRL_DOT, expected='<C-.>'),
    _seq_test(actual=seqs.CTRL_E, expected='<C-e>'),
    _seq_test(actual=seqs.CTRL_ENTER, expected='<C-cr>'),
    _seq_test(actual=seqs.CTRL_F, expected='<C-f>'),
    _seq_test(actual=seqs.CTRL_F12, expected='<C-f12>'),
    _seq_test(actual=seqs.CTRL_F2, expected='<C-f2>'),
    _seq_test(actual=seqs.CTRL_G, expected='<C-g>'),
    _seq_test(actual=seqs.CTRL_I, expected='<C-i>'),
    _seq_test(actual=seqs.CTRL_J, expected='<C-j>'),
    _seq_test(actual=seqs.CTRL_K, expected='<C-k>'),
    _seq_test(actual=seqs.CTRL_K_CTRL_B, expected='<C-k><C-b>'),
    _seq_test(actual=seqs.CTRL_L, expected='<C-l>'),
    _seq_test(actual=seqs.CTRL_LEFT_SQUARE_BRACKET, expected='<C-[>'),
    _seq_test(actual=seqs.CTRL_N, expected='<C-n>'),
    _seq_test(actual=seqs.CTRL_O, expected='<C-o>'),
    _seq_test(actual=seqs.CTRL_P, expected='<C-p>'),
    _seq_test(actual=seqs.CTRL_R, expected='<C-r>'),
    _seq_test(actual=seqs.CTRL_R_EQUAL, expected='<C-r>='),
    _seq_test(actual=seqs.CTRL_RIGHT_SQUARE_BRACKET, expected='<C-]>'),
    _seq_test(actual=seqs.CTRL_SHIFT_B, expected='<C-S-b>'),
    _seq_test(actual=seqs.CTRL_SHIFT_DOT, expected='<C-S-.>'),
    _seq_test(actual=seqs.CTRL_SHIFT_ENTER, expected='<C-S-cr>'),
    _seq_test(actual=seqs.CTRL_SHIFT_F2, expected='<C-S-f2>'),
    _seq_test(actual=seqs.CTRL_U, expected='<C-u>'),
    _seq_test(actual=seqs.CTRL_V, expected='<C-v>'),
    _seq_test(actual=seqs.CTRL_W, expected='<C-w>'),
    _seq_test(actual=seqs.CTRL_W_B, expected='<C-w>b'),
    _seq_test(actual=seqs.CTRL_W_BACKSPACE, expected='<C-w><bs>'),
    _seq_test(actual=seqs.CTRL_W_BIG_H, expected='<C-w>H'),
    _seq_test(actual=seqs.CTRL_W_BIG_J, expected='<C-w>J'),
    _seq_test(actual=seqs.CTRL_W_BIG_K, expected='<C-w>K'),
    _seq_test(actual=seqs.CTRL_W_BIG_L, expected='<C-w>L'),
    _seq_test(actual=seqs.CTRL_W_BIG_S, expected='<C-w>S'),
    _seq_test(actual=seqs.CTRL_W_C, expected='<C-w>c'),
    _seq_test(actual=seqs.CTRL_W_CTRL_B, expected='<C-w><C-b>'),
    _seq_test(actual=seqs.CTRL_W_CTRL_H, expected='<C-w><C-h>'),
    _seq_test(actual=seqs.CTRL_W_CTRL_J, expected='<C-w><C-j>'),
    _seq_test(actual=seqs.CTRL_W_CTRL_K, expected='<C-w><C-k>'),
    _seq_test(actual=seqs.CTRL_W_CTRL_L, expected='<C-w><C-l>'),
    _seq_test(actual=seqs.CTRL_W_CTRL_N, expected='<C-w><C-n>'),
    _seq_test(actual=seqs.CTRL_W_CTRL_O, expected='<C-w><C-o>'),
    _seq_test(actual=seqs.CTRL_W_CTRL_Q, expected='<C-w><C-q>'),
    _seq_test(actual=seqs.CTRL_W_CTRL_S, expected='<C-w><C-s>'),
    _seq_test(actual=seqs.CTRL_W_CTRL_T, expected='<C-w><C-t>'),
    _seq_test(actual=seqs.CTRL_W_CTRL_UNDERSCORE, expected='<C-w><C-_>'),
    _seq_test(actual=seqs.CTRL_W_CTRL_V, expected='<C-w><C-v>'),
    _seq_test(actual=seqs.CTRL_W_CTRL_X, expected='<C-w><C-x>'),
    _seq_test(actual=seqs.CTRL_W_DOWN, expected='<C-w><down>'),
    _seq_test(actual=seqs.CTRL_W_EQUAL, expected='<C-w>='),
    _seq_test(actual=seqs.CTRL_W_GREATER_THAN, expected='<C-w>>'),
    _seq_test(actual=seqs.CTRL_W_H, expected='<C-w>h'),
    _seq_test(actual=seqs.CTRL_W_J, expected='<C-w>j'),
    _seq_test(actual=seqs.CTRL_W_K, expected='<C-w>k'),
    _seq_test(actual=seqs.CTRL_W_L, expected='<C-w>l'),
    _seq_test(actual=seqs.CTRL_W_LEFT, expected='<C-w><left>'),
    _seq_test(actual=seqs.CTRL_W_LESS_THAN, expected='<C-w><lt>'),
    _seq_test(actual=seqs.CTRL_W_MINUS, expected='<C-w>-'),
    _seq_test(actual=seqs.CTRL_W_N, expected='<C-w>n'),
    _seq_test(actual=seqs.CTRL_W_O, expected='<C-w>o'),
    _seq_test(actual=seqs.CTRL_W_PIPE, expected='<C-w>|'),
    _seq_test(actual=seqs.CTRL_W_PLUS, expected='<C-w>+'),
    _seq_test(actual=seqs.CTRL_W_Q, expected='<C-w>q'),
    _seq_test(actual=seqs.CTRL_W_RIGHT, expected='<C-w><right>'),
    _seq_test(actual=seqs.CTRL_W_S, expected='<C-w>s'),
    _seq_test(actual=seqs.CTRL_W_T, expected='<C-w>t'),
    _seq_test(actual=seqs.CTRL_W_UNDERSCORE, expected='<C-w>_'),
    _seq_test(actual=seqs.CTRL_W_UP, expected='<C-w><up>'),
    _seq_test(actual=seqs.CTRL_W_V, expected='<C-w>v'),
    _seq_test(actual=seqs.CTRL_W_X, expected='<C-w>x'),
    _seq_test(actual=seqs.CTRL_X, expected='<C-x>'),
    _seq_test(actual=seqs.CTRL_X_CTRL_L, expected='<C-x><C-l>'),
    _seq_test(actual=seqs.CTRL_Y, expected='<C-y>'),
    _seq_test(actual=seqs.D, expected='d'),
    _seq_test(actual=seqs.DD, expected='dd'),
    _seq_test(actual=seqs.DOLLAR, expected='$'),
    _seq_test(actual=seqs.DOT, expected='.'),
    _seq_test(actual=seqs.DOUBLE_QUOTE, expected='"'),
    _seq_test(actual=seqs.DOWN, expected='<down>'),
    _seq_test(actual=seqs.E, expected='e'),
    _seq_test(actual=seqs.END, expected='<end>'),
    _seq_test(actual=seqs.ENTER, expected='<cr>'),
    _seq_test(actual=seqs.EQUAL, expected='='),
    _seq_test(actual=seqs.EQUAL_EQUAL, expected='=='),
    _seq_test(actual=seqs.ESC, expected='<esc>'),
    _seq_test(actual=seqs.F, expected='f'),
    _seq_test(actual=seqs.F1, expected='<f1>'),
    _seq_test(actual=seqs.F10, expected='<f10>'),
    _seq_test(actual=seqs.F11, expected='<f11>'),
    _seq_test(actual=seqs.F12, expected='<f12>'),
    _seq_test(actual=seqs.F13, expected='<f13>'),
    _seq_test(actual=seqs.F14, expected='<f14>'),
    _seq_test(actual=seqs.F15, expected='<f15>'),
    _seq_test(actual=seqs.F2, expected='<f2>'),
    _seq_test(actual=seqs.F3, expected='<f3>'),
    _seq_test(actual=seqs.F4, expected='<f4>'),
    _seq_test(actual=seqs.F5, expected='<f5>'),
    _seq_test(actual=seqs.F6, expected='<f6>'),
    _seq_test(actual=seqs.F7, expected='<f7>'),
    _seq_test(actual=seqs.F8, expected='<f8>'),
    _seq_test(actual=seqs.F9, expected='<f9>'),
    _seq_test(actual=seqs.G, expected='g'),
    _seq_test(actual=seqs.G_BIG_C, expected='gC'),
    _seq_test(actual=seqs.G_BIG_D, expected='gD'),
    _seq_test(actual=seqs.G_BIG_E, expected='gE'),
    _seq_test(actual=seqs.G_BIG_H, expected='gH'),
    _seq_test(actual=seqs.G_BIG_J, expected='gJ'),
    _seq_test(actual=seqs.G_BIG_T, expected='gT'),
    _seq_test(actual=seqs.G_BIG_U, expected='gU'),
    _seq_test(actual=seqs.G_BIG_U_BIG_U, expected='gUU'),
    _seq_test(actual=seqs.G_BIG_U_G_BIG_U, expected='gUgU'),
    _seq_test(actual=seqs.G_TILDE, expected='g~'),
    _seq_test(actual=seqs.G_TILDE_G_TILDE, expected='g~g~'),
    _seq_test(actual=seqs.G_TILDE_TILDE, expected='g~~'),
    _seq_test(actual=seqs.G_UNDERSCORE, expected='g_'),
    _seq_test(actual=seqs.GA, expected='ga'),
    _seq_test(actual=seqs.GC, expected='gc'),
    _seq_test(actual=seqs.GCC, expected='gcc'),
    _seq_test(actual=seqs.GD, expected='gd'),
    _seq_test(actual=seqs.GE, expected='ge'),
    _seq_test(actual=seqs.GG, expected='gg'),
    _seq_test(actual=seqs.GH, expected='gh'),
    _seq_test(actual=seqs.GJ, expected='gj'),
    _seq_test(actual=seqs.GK, expected='gk'),
    _seq_test(actual=seqs.GM, expected='gm'),
    _seq_test(actual=seqs.GQ, expected='gq'),
    _seq_test(actual=seqs.GREATER_THAN, expected='>'),
    _seq_test(actual=seqs.GREATER_THAN_GREATER_THAN, expected='>>'),
    _seq_test(actual=seqs.GT, expected='gt'),
    _seq_test(actual=seqs.GU, expected='gu'),
    _seq_test(actual=seqs.GUGU, expected='gugu'),
    _seq_test(actual=seqs.GUU, expected='guu'),
    _seq_test(actual=seqs.GV, expected='gv'),
    _seq_test(actual=seqs.GX, expected='gx'),
    _seq_test(actual=seqs.H, expected='h'),
    _seq_test(actual=seqs.HAT, expected='^'),
    _seq_test(actual=seqs.HOME, expected='<home>'),
    _seq_test(actual=seqs.I, expected='i'),
    _seq_test(actual=seqs.J, expected='j'),
    _seq_test(actual=seqs.K, expected='k'),
    _seq_test(actual=seqs.L, expected='l'),
    _seq_test(actual=seqs.LEFT, expected='<left>'),
    _seq_test(actual=seqs.LEFT_BRACE, expected='{'),
    _seq_test(actual=seqs.LEFT_PAREN, expected='('),
    _seq_test(actual=seqs.LEFT_SQUARE_BRACKET, expected='['),
    _seq_test(actual=seqs.LEFT_SQUARE_BRACKET_C, expected='[c'),
    _seq_test(actual=seqs.LESS_THAN, expected='<lt>'),
    _seq_test(actual=seqs.LESS_THAN_LESS_THAN, expected='<lt><lt>'),
    _seq_test(actual=seqs.M, expected='m'),
    _seq_test(actual=seqs.MINUS, expected='-'),
    _seq_test(actual=seqs.N, expected='n'),
    _seq_test(actual=seqs.O, expected='o'),
    _seq_test(actual=seqs.OCTOTHORP, expected='#'),
    _seq_test(actual=seqs.P, expected='p'),
    _seq_test(actual=seqs.PAGE_DOWN, expected='pagedown'),
    _seq_test(actual=seqs.PAGE_UP, expected='pageup'),
    _seq_test(actual=seqs.PERCENT, expected='%'),
    _seq_test(actual=seqs.PIPE, expected='|'),
    _seq_test(actual=seqs.PLUS, expected='+'),
    _seq_test(actual=seqs.Q, expected='q'),
    _seq_test(actual=seqs.QUESTION_MARK, expected='?'),
    _seq_test(actual=seqs.QUOTE, expected="'"),
    _seq_test(actual=seqs.QUOTE_QUOTE, expected="''"),
    _seq_test(actual=seqs.R, expected='r'),
    _seq_test(actual=seqs.RIGHT, expected='<right>'),
    _seq_test(actual=seqs.RIGHT_BRACE, expected='}'),
    _seq_test(actual=seqs.RIGHT_PAREN, expected=')'),
    _seq_test(actual=seqs.RIGHT_SQUARE_BRACKET, expected=']'),
    _seq_test(actual=seqs.RIGHT_SQUARE_BRACKET_C, expected=']c'),
    _seq_test(actual=seqs.S, expected='s'),
    _seq_test(actual=seqs.SEMICOLON, expected=';'),
    _seq_test(actual=seqs.SHIFT_CTRL_F12, expected='<C-S-f12>'),
    _seq_test(actual=seqs.SHIFT_ENTER, expected='<S-cr>'),
    _seq_test(actual=seqs.SHIFT_F11, expected='<S-f11>'),
    _seq_test(actual=seqs.SHIFT_F2, expected='<S-f2>'),
    _seq_test(actual=seqs.SHIFT_F3, expected='<S-f3>'),
    _seq_test(actual=seqs.SHIFT_F4, expected='<S-f4>'),
    _seq_test(actual=seqs.SLASH, expected='/'),
    _seq_test(actual=seqs.SPACE, expected='<space>'),
    _seq_test(actual=seqs.STAR, expected='*'),
    _seq_test(actual=seqs.T, expected='t'),
    _seq_test(actual=seqs.TAB, expected='<tab>'),
    _seq_test(actual=seqs.TILDE, expected='~'),
    _seq_test(actual=seqs.U, expected='u'),
    _seq_test(actual=seqs.UNDERSCORE, expected='_'),
    _seq_test(actual=seqs.UP, expected='<up>'),
    _seq_test(actual=seqs.V, expected='v'),
    _seq_test(actual=seqs.W, expected='w'),
    _seq_test(actual=seqs.X, expected='x'),
    _seq_test(actual=seqs.Y, expected='y'),
    _seq_test(actual=seqs.YY, expected='yy'),
    _seq_test(actual=seqs.Z, expected='z'),
    _seq_test(actual=seqs.Z_ENTER, expected='z<cr>'),
    _seq_test(actual=seqs.Z_MINUS, expected='z-'),
    _seq_test(actual=seqs.ZB, expected='zb'),
    _seq_test(actual=seqs.ZERO, expected='0'),
    _seq_test(actual=seqs.ZT, expected='zt'),
    _seq_test(actual=seqs.ZZ, expected='zz'),
)


class TestKeySequenceNames(unittest.TestCase):

    def test_all(self):
        for (i, data) in enumerate(_TESTS_KNOWN_SEQUENCES):
            self.assertEqual(data.actual, data.expected, "failed at index {0}".format(i))

    def test_all_key_sequence_names_are_tested(self):
        tested_seqs = [k.actual for k in _TESTS_KNOWN_SEQUENCES]

        self.assertEqual(
            sorted(tested_seqs),
            sorted([v for (k, v) in seqs.__dict__.items() if k.isupper()])
        )
