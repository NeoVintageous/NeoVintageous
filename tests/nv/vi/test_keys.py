from unittest import mock
import unittest

from NeoVintageous.nv.vi.keys import KeySequenceTokenizer
from NeoVintageous.nv.vi.keys import seqs
from NeoVintageous.nv.vi.keys import to_bare_command_name
from NeoVintageous.nv.vi.utils import translate_char


class TestKeySequenceTokenizer(unittest.TestCase):

    @mock.patch.dict('NeoVintageous.nv.vi.variables._variables', {}, clear=True)
    def test_tokenize_one(self):
        def tokenize_one(source):
            return KeySequenceTokenizer(source).tokenize_one()

        self.assertEqual(tokenize_one('p'), 'p', 'lower letter key')
        self.assertEqual(tokenize_one('P'), 'P', 'upper case letter key')
        self.assertEqual(tokenize_one('<C-p>'), '<C-p>', 'ctrl-modified lower case letter key')
        self.assertEqual(tokenize_one('<C-P>'), '<C-P>', 'ctrl-modified upper case letter key')
        self.assertEqual(tokenize_one('<C-S-.>'), '<C-S-.>', 'ctrl-shift modified period key')
        self.assertEqual(tokenize_one('<Esc>'), '<esc>', 'esc key title case')
        self.assertEqual(tokenize_one('<esc>'), '<esc>', 'esc key lowercase')
        self.assertEqual(tokenize_one('<eSc>'), '<esc>', 'esc key mixed case')
        self.assertEqual(tokenize_one('<lt>'), '<lt>', 'less than key')
        self.assertEqual(tokenize_one('<HOME>'), '<home>', 'less than key')
        self.assertEqual(tokenize_one('<enD>'), '<end>', 'less than key')
        self.assertEqual(tokenize_one('<uP>'), '<up>', 'less than key')
        self.assertEqual(tokenize_one('<DoWn>'), '<down>', 'less than key')
        self.assertEqual(tokenize_one('<left>'), '<left>', 'less than key')
        self.assertEqual(tokenize_one('<RigHt>'), '<right>', 'less than key')
        self.assertEqual(tokenize_one('<Space>'), '<space>', 'space key')
        self.assertEqual(tokenize_one('<c-Space>'), '<C-space>', 'ctrl-space key')
        self.assertEqual(tokenize_one('0'), '0', 'zero key')
        self.assertEqual(tokenize_one('<c-m-.>'), '<C-M-.>', 'ctrl-alt-period key')
        self.assertEqual(tokenize_one('<tab>'), '<tab>', 'tab key')
        self.assertEqual(tokenize_one('<Leader>'), '\\', 'leader key')
        self.assertEqual(tokenize_one('<D-a>'), '<D-a>', 'super key')
        self.assertEqual(tokenize_one('<d-a>'), '<D-a>', 'super key')
        self.assertEqual(tokenize_one('<D-A>'), '<D-A>', 'super key')
        self.assertEqual(tokenize_one('<d-A>'), '<D-A>', 'super key')

    @mock.patch.dict('NeoVintageous.nv.vi.variables._variables', {}, clear=True)
    def test_iter_tokenize(self):
        def iter_tokenize(source):
            return list(KeySequenceTokenizer(source).iter_tokenize())

        self.assertEqual(iter_tokenize('pp'), ['p', 'p'])
        self.assertEqual(iter_tokenize('<C-p>'), ['<C-p>'])
        self.assertEqual(iter_tokenize('<C-P>x'), ['<C-P>', 'x'])
        self.assertEqual(iter_tokenize('<C-S-.>'), ['<C-S-.>'])
        self.assertEqual(iter_tokenize('<Esc>ai'), ['<esc>', 'a', 'i'])
        self.assertEqual(iter_tokenize('<lt><lt>'), ['<lt>', '<lt>'])
        self.assertEqual(iter_tokenize('<DoWn>abc.'), ['<down>', 'a', 'b', 'c', '.'])
        self.assertEqual(iter_tokenize('0<down>'), ['0', '<down>'])
        self.assertEqual(iter_tokenize('<c-m-.>'), ['<C-M-.>'])
        self.assertEqual(iter_tokenize('<d-i>i.'), ['<D-i>', 'i', '.'])
        self.assertEqual(iter_tokenize('<d-i><c-i>'), ['<D-i>', '<C-i>'])
        self.assertEqual(iter_tokenize('<d-i><c-d>'), ['<D-i>', '<C-d>'])


class TestFunctions(unittest.TestCase):

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

    def test_translate_char(self):
        self.assertEqual(translate_char('<enter>'), '\n')
        self.assertEqual(translate_char('<cr>'), '\n')
        self.assertEqual(translate_char('<sp>'), ' ')
        self.assertEqual(translate_char('<space>'), ' ')
        self.assertEqual(translate_char('<lt>'), '<')
        self.assertEqual(translate_char('a'), 'a')


_known_seqs_dataset = (
    (seqs.A, 'a'),
    (seqs.ALT_CTRL_P, '<C-M-p>'),
    (seqs.AMPERSAND, '&'),
    (seqs.AT, '@'),
    (seqs.AW, 'aw'),
    (seqs.B, 'b'),
    (seqs.BACKSPACE, '<bs>'),
    (seqs.BACKTICK, '`'),
    (seqs.BIG_A, 'A'),
    (seqs.BIG_B, 'B'),
    (seqs.BIG_C, 'C'),
    (seqs.BIG_D, 'D'),
    (seqs.BIG_E, 'E'),
    (seqs.BIG_F, 'F'),
    (seqs.BIG_G, 'G'),
    (seqs.BIG_H, 'H'),
    (seqs.BIG_I, 'I'),
    (seqs.BIG_J, 'J'),
    (seqs.BIG_K, 'K'),
    (seqs.BIG_L, 'L'),
    (seqs.BIG_M, 'M'),
    (seqs.BIG_N, 'N'),
    (seqs.BIG_O, 'O'),
    (seqs.BIG_P, 'P'),
    (seqs.BIG_Q, 'Q'),
    (seqs.BIG_R, 'R'),
    (seqs.BIG_S, 'S'),
    (seqs.BIG_T, 'T'),
    (seqs.BIG_U, 'U'),
    (seqs.BIG_V, 'V'),
    (seqs.BIG_W, 'W'),
    (seqs.BIG_X, 'X'),
    (seqs.BIG_Y, 'Y'),
    (seqs.BIG_Z, 'Z'),
    (seqs.BIG_Z_BIG_Q, 'ZQ'),
    (seqs.BIG_Z_BIG_Z, 'ZZ'),
    (seqs.C, 'c'),
    (seqs.CC, 'cc'),
    (seqs.COLON, ':'),
    (seqs.COMMA, ','),
    (seqs.COMMAND_BIG_B, '<D-B>'),
    (seqs.COMMAND_BIG_F, '<D-F>'),
    (seqs.COMMAND_BIG_P, '<D-P>'),
    (seqs.COMMAND_P, '<D-p>'),
    (seqs.CTRL_0, '<C-0>'),
    (seqs.CTRL_1, '<C-1>'),
    (seqs.CTRL_2, '<C-2>'),
    (seqs.CTRL_3, '<C-3>'),
    (seqs.CTRL_4, '<C-4>'),
    (seqs.CTRL_5, '<C-5>'),
    (seqs.CTRL_6, '<C-6>'),
    (seqs.CTRL_7, '<C-7>'),
    (seqs.CTRL_8, '<C-8>'),
    (seqs.CTRL_9, '<C-9>'),
    (seqs.CTRL_A, '<C-a>'),
    (seqs.CTRL_B, '<C-b>'),
    (seqs.CTRL_BIG_F, '<C-F>'),
    (seqs.CTRL_BIG_P, '<C-P>'),
    (seqs.CTRL_C, '<C-c>'),
    (seqs.CTRL_D, '<C-d>'),
    (seqs.CTRL_DOT, '<C-.>'),
    (seqs.CTRL_E, '<C-e>'),
    (seqs.CTRL_ENTER, '<C-cr>'),
    (seqs.CTRL_F, '<C-f>'),
    (seqs.CTRL_F12, '<C-f12>'),
    (seqs.CTRL_F2, '<C-f2>'),
    (seqs.CTRL_G, '<C-g>'),
    (seqs.CTRL_I, '<C-i>'),
    (seqs.CTRL_J, '<C-j>'),
    (seqs.CTRL_K, '<C-k>'),
    (seqs.CTRL_K_CTRL_B, '<C-k><C-b>'),
    (seqs.CTRL_L, '<C-l>'),
    (seqs.CTRL_LEFT_SQUARE_BRACKET, '<C-[>'),
    (seqs.CTRL_N, '<C-n>'),
    (seqs.CTRL_O, '<C-o>'),
    (seqs.CTRL_P, '<C-p>'),
    (seqs.CTRL_R, '<C-r>'),
    (seqs.CTRL_R_EQUAL, '<C-r>='),
    (seqs.CTRL_RIGHT_SQUARE_BRACKET, '<C-]>'),
    (seqs.CTRL_SHIFT_B, '<C-S-b>'),
    (seqs.CTRL_SHIFT_DOT, '<C-S-.>'),
    (seqs.CTRL_SHIFT_ENTER, '<C-S-cr>'),
    (seqs.CTRL_SHIFT_F2, '<C-S-f2>'),
    (seqs.CTRL_U, '<C-u>'),
    (seqs.CTRL_V, '<C-v>'),
    (seqs.CTRL_W, '<C-w>'),
    (seqs.CTRL_W_B, '<C-w>b'),
    (seqs.CTRL_W_BACKSPACE, '<C-w><bs>'),
    (seqs.CTRL_W_BIG_H, '<C-w>H'),
    (seqs.CTRL_W_BIG_J, '<C-w>J'),
    (seqs.CTRL_W_BIG_K, '<C-w>K'),
    (seqs.CTRL_W_BIG_L, '<C-w>L'),
    (seqs.CTRL_W_BIG_S, '<C-w>S'),
    (seqs.CTRL_W_C, '<C-w>c'),
    (seqs.CTRL_W_CTRL_B, '<C-w><C-b>'),
    (seqs.CTRL_W_CTRL_H, '<C-w><C-h>'),
    (seqs.CTRL_W_CTRL_J, '<C-w><C-j>'),
    (seqs.CTRL_W_CTRL_K, '<C-w><C-k>'),
    (seqs.CTRL_W_CTRL_L, '<C-w><C-l>'),
    (seqs.CTRL_W_CTRL_N, '<C-w><C-n>'),
    (seqs.CTRL_W_CTRL_O, '<C-w><C-o>'),
    (seqs.CTRL_W_CTRL_Q, '<C-w><C-q>'),
    (seqs.CTRL_W_CTRL_S, '<C-w><C-s>'),
    (seqs.CTRL_W_CTRL_T, '<C-w><C-t>'),
    (seqs.CTRL_W_CTRL_UNDERSCORE, '<C-w><C-_>'),
    (seqs.CTRL_W_CTRL_V, '<C-w><C-v>'),
    (seqs.CTRL_W_CTRL_X, '<C-w><C-x>'),
    (seqs.CTRL_W_DOWN, '<C-w><down>'),
    (seqs.CTRL_W_EQUAL, '<C-w>='),
    (seqs.CTRL_W_GREATER_THAN, '<C-w>>'),
    (seqs.CTRL_W_H, '<C-w>h'),
    (seqs.CTRL_W_J, '<C-w>j'),
    (seqs.CTRL_W_K, '<C-w>k'),
    (seqs.CTRL_W_L, '<C-w>l'),
    (seqs.CTRL_W_LEFT, '<C-w><left>'),
    (seqs.CTRL_W_LESS_THAN, '<C-w><lt>'),
    (seqs.CTRL_W_MINUS, '<C-w>-'),
    (seqs.CTRL_W_N, '<C-w>n'),
    (seqs.CTRL_W_O, '<C-w>o'),
    (seqs.CTRL_W_PIPE, '<C-w>|'),
    (seqs.CTRL_W_PLUS, '<C-w>+'),
    (seqs.CTRL_W_Q, '<C-w>q'),
    (seqs.CTRL_W_RIGHT, '<C-w><right>'),
    (seqs.CTRL_W_S, '<C-w>s'),
    (seqs.CTRL_W_T, '<C-w>t'),
    (seqs.CTRL_W_UNDERSCORE, '<C-w>_'),
    (seqs.CTRL_W_UP, '<C-w><up>'),
    (seqs.CTRL_W_V, '<C-w>v'),
    (seqs.CTRL_W_X, '<C-w>x'),
    (seqs.CTRL_X, '<C-x>'),
    (seqs.CTRL_X_CTRL_L, '<C-x><C-l>'),
    (seqs.CTRL_Y, '<C-y>'),
    (seqs.D, 'd'),
    (seqs.DD, 'dd'),
    (seqs.DOLLAR, '$'),
    (seqs.DOT, '.'),
    (seqs.DOUBLE_QUOTE, '"'),
    (seqs.DOWN, '<down>'),
    (seqs.E, 'e'),
    (seqs.END, '<end>'),
    (seqs.ENTER, '<cr>'),
    (seqs.EQUAL, '='),
    (seqs.EQUAL_EQUAL, '=='),
    (seqs.ESC, '<esc>'),
    (seqs.F, 'f'),
    (seqs.F1, '<f1>'),
    (seqs.F10, '<f10>'),
    (seqs.F11, '<f11>'),
    (seqs.F12, '<f12>'),
    (seqs.F13, '<f13>'),
    (seqs.F14, '<f14>'),
    (seqs.F15, '<f15>'),
    (seqs.F2, '<f2>'),
    (seqs.F3, '<f3>'),
    (seqs.F4, '<f4>'),
    (seqs.F5, '<f5>'),
    (seqs.F6, '<f6>'),
    (seqs.F7, '<f7>'),
    (seqs.F8, '<f8>'),
    (seqs.F9, '<f9>'),
    (seqs.G, 'g'),
    (seqs.G_BIG_C, 'gC'),
    (seqs.G_BIG_D, 'gD'),
    (seqs.G_BIG_E, 'gE'),
    (seqs.G_BIG_H, 'gH'),
    (seqs.G_BIG_J, 'gJ'),
    (seqs.G_BIG_T, 'gT'),
    (seqs.G_BIG_U, 'gU'),
    (seqs.G_BIG_U_BIG_U, 'gUU'),
    (seqs.G_BIG_U_G_BIG_U, 'gUgU'),
    (seqs.G_TILDE, 'g~'),
    (seqs.G_TILDE_G_TILDE, 'g~g~'),
    (seqs.G_TILDE_TILDE, 'g~~'),
    (seqs.G_UNDERSCORE, 'g_'),
    (seqs.GA, 'ga'),
    (seqs.GC, 'gc'),
    (seqs.GCC, 'gcc'),
    (seqs.GD, 'gd'),
    (seqs.GE, 'ge'),
    (seqs.GG, 'gg'),
    (seqs.GH, 'gh'),
    (seqs.GJ, 'gj'),
    (seqs.GK, 'gk'),
    (seqs.GM, 'gm'),
    (seqs.GQ, 'gq'),
    (seqs.GREATER_THAN, '>'),
    (seqs.GREATER_THAN_GREATER_THAN, '>>'),
    (seqs.GT, 'gt'),
    (seqs.GU, 'gu'),
    (seqs.GUGU, 'gugu'),
    (seqs.GUU, 'guu'),
    (seqs.GV, 'gv'),
    (seqs.GX, 'gx'),
    (seqs.H, 'h'),
    (seqs.HAT, '^'),
    (seqs.HOME, '<home>'),
    (seqs.I, 'i'),
    (seqs.J, 'j'),
    (seqs.K, 'k'),
    (seqs.L, 'l'),
    (seqs.LEFT, '<left>'),
    (seqs.LEFT_BRACE, '{'),
    (seqs.LEFT_PAREN, '('),
    (seqs.LEFT_SQUARE_BRACKET, '['),
    (seqs.LEFT_SQUARE_BRACKET_C, '[c'),
    (seqs.LESS_THAN, '<lt>'),
    (seqs.LESS_THAN_LESS_THAN, '<lt><lt>'),
    (seqs.M, 'm'),
    (seqs.MINUS, '-'),
    (seqs.N, 'n'),
    (seqs.O, 'o'),
    (seqs.OCTOTHORP, '#'),
    (seqs.P, 'p'),
    (seqs.PAGE_DOWN, 'pagedown'),
    (seqs.PAGE_UP, 'pageup'),
    (seqs.PERCENT, '%'),
    (seqs.PIPE, '|'),
    (seqs.PLUS, '+'),
    (seqs.Q, 'q'),
    (seqs.QUESTION_MARK, '?'),
    (seqs.QUOTE, "'"),
    (seqs.QUOTE_QUOTE, "''"),
    (seqs.R, 'r'),
    (seqs.RIGHT, '<right>'),
    (seqs.RIGHT_BRACE, '}'),
    (seqs.RIGHT_PAREN, ')'),
    (seqs.RIGHT_SQUARE_BRACKET, ']'),
    (seqs.RIGHT_SQUARE_BRACKET_C, ']c'),
    (seqs.S, 's'),
    (seqs.SEMICOLON, ';'),
    (seqs.SHIFT_CTRL_F12, '<C-S-f12>'),
    (seqs.SHIFT_ENTER, '<S-cr>'),
    (seqs.SHIFT_F11, '<S-f11>'),
    (seqs.SHIFT_F2, '<S-f2>'),
    (seqs.SHIFT_F3, '<S-f3>'),
    (seqs.SHIFT_F4, '<S-f4>'),
    (seqs.SLASH, '/'),
    (seqs.SPACE, '<space>'),
    (seqs.STAR, '*'),
    (seqs.T, 't'),
    (seqs.TAB, '<tab>'),
    (seqs.TILDE, '~'),
    (seqs.U, 'u'),
    (seqs.UNDERSCORE, '_'),
    (seqs.UP, '<up>'),
    (seqs.V, 'v'),
    (seqs.W, 'w'),
    (seqs.X, 'x'),
    (seqs.Y, 'y'),
    (seqs.YY, 'yy'),
    (seqs.Z, 'z'),
    (seqs.Z_ENTER, 'z<cr>'),
    (seqs.Z_MINUS, 'z-'),
    (seqs.ZB, 'zb'),
    (seqs.ZERO, '0'),
    (seqs.ZT, 'zt'),
    (seqs.ZZ, 'zz'),
)


class TestKeySequenceNames(unittest.TestCase):

    def test_seqs(self):
        for i, (actual, expected) in enumerate(_known_seqs_dataset):
            self.assertEqual(actual, expected, 'failed at index {}'.format(i))

    def test_all_key_sequence_names_are_tested(self):
        self.assertEqual(
            sorted([k[1] for k in _known_seqs_dataset]),
            sorted([v for (k, v) in seqs.__dict__.items() if k.isupper()])
        )
