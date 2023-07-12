# Copyright (C) 2018-2023 The NeoVintageous Team (NeoVintageous).
#
# This file is part of NeoVintageous.
#
# NeoVintageous is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# NeoVintageous is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NeoVintageous.  If not, see <https://www.gnu.org/licenses/>.

import unittest

from NeoVintageous.nv.vi.keys import to_bare_command_name
from NeoVintageous.nv.vi.keys import tokenize_keys


def _tokenize(source) -> list:
    return list(tokenize_keys(source))


class TestKeySequenceTokenizer(unittest.TestCase):

    @unittest.mock.patch.dict('NeoVintageous.nv.variables._variables', {}, clear=True)
    def test_tokenize_one(self):

        self.assertEqual(_tokenize('0'), ['0'], 'zero key')
        self.assertEqual(_tokenize('<A-i>'), ['<M-i>'])
        self.assertEqual(_tokenize('<Bar>'), ['<bar>'])
        self.assertEqual(_tokenize('<Bslash>'), ['<bslash>'])
        self.assertEqual(_tokenize('<C-P>'), ['<C-P>'], 'ctrl-modified upper case letter key')
        self.assertEqual(_tokenize('<C-S-.>'), ['<C-S-.>'], 'ctrl-shift modified period key')
        self.assertEqual(_tokenize('<C-S-F3>'), ['<C-S-f3>'])
        self.assertEqual(_tokenize('<C-S-f3>'), ['<C-S-f3>'])
        self.assertEqual(_tokenize('<C-p>'), ['<C-p>'], 'ctrl-modified lower case letter key')
        self.assertEqual(_tokenize('<C-s>'), ['<C-s>'])
        self.assertEqual(_tokenize('<C-w>'), ['<C-w>'])
        self.assertEqual(_tokenize('<D-A>'), ['<D-A>'])
        self.assertEqual(_tokenize('<D-a>'), ['<D-a>'])
        self.assertEqual(_tokenize('<D-i>'), ['<D-i>'])
        self.assertEqual(_tokenize('<DoWn>'), ['<down>'], 'less than key')
        self.assertEqual(_tokenize('<Enter>'), ['<cr>'])
        self.assertEqual(_tokenize('<Esc>'), ['<esc>'], 'esc key title case')
        self.assertEqual(_tokenize('<HOME>'), ['<home>'], 'less than key')
        self.assertEqual(_tokenize('<Leader>'), ['<bslash>'], 'leader key')
        self.assertEqual(_tokenize('<M-i>'), ['<M-i>'])
        self.assertEqual(_tokenize('<RETURN>'), ['<cr>'])
        self.assertEqual(_tokenize('<Return>'), ['<cr>'])
        self.assertEqual(_tokenize('<RigHt>'), ['<right>'], 'less than key')
        self.assertEqual(_tokenize('<Space>'), ['<space>'], 'space key')
        self.assertEqual(_tokenize('<bs>'), ['<bs>'])
        self.assertEqual(_tokenize('<c-Space>'), ['<C-space>'], 'ctrl-space key')
        self.assertEqual(_tokenize('<c-m-.>'), ['<C-M-.>'], 'ctrl-alt-period key')
        self.assertEqual(_tokenize('<c-m-s-a>'), ['<C-M-S-a>'])
        self.assertEqual(_tokenize('<c-m-s>'), ['<C-M-s>'])
        self.assertEqual(_tokenize('<c-s-b>'), ['<C-S-b>'])
        self.assertEqual(_tokenize('<d-A>'), ['<D-A>'])
        self.assertEqual(_tokenize('<d-a>'), ['<D-a>'])
        self.assertEqual(_tokenize('<eSc>'), ['<esc>'], 'esc key mixed case')
        self.assertEqual(_tokenize('<enD>'), ['<end>'], 'less than key')
        self.assertEqual(_tokenize('<enter>'), ['<cr>'])
        self.assertEqual(_tokenize('<esc>'), ['<esc>'], 'esc key lowercase')
        self.assertEqual(_tokenize('<insert>'), ['<insert>'])
        self.assertEqual(_tokenize('<leader>'), ['<bslash>'], 'leader key')
        self.assertEqual(_tokenize('<left>'), ['<left>'], 'less than key')
        self.assertEqual(_tokenize('<lt>'), ['<lt>'], 'less than key')
        self.assertEqual(_tokenize('<m-c-x>'), ['<C-M-x>'])
        self.assertEqual(_tokenize('<m-s-c>'), ['<M-S-c>'])
        self.assertEqual(_tokenize('<s-c-x>'), ['<C-S-x>'])
        self.assertEqual(_tokenize('<s-m-x>'), ['<M-S-x>'])
        self.assertEqual(_tokenize('<space>'), ['<space>'], 'space key')
        self.assertEqual(_tokenize('<tab>'), ['<tab>'], 'tab key')
        self.assertEqual(_tokenize('<uP>'), ['<up>'], 'less than key')
        self.assertEqual(_tokenize('>'), ['>'])
        self.assertEqual(_tokenize('P'), ['P'], 'upper case letter key')
        self.assertEqual(_tokenize('p'), ['p'], 'lower letter key')

    @unittest.mock.patch.dict('NeoVintageous.nv.variables._variables', {}, clear=True)
    def test_tokenize_many(self):

        self.assertEqual(_tokenize('0<down>'), ['0', '<down>'])
        self.assertEqual(_tokenize('3<insert>'), ['3', '<insert>'])
        self.assertEqual(_tokenize('3<return>'), ['3', '<cr>'])
        self.assertEqual(_tokenize('3w<A-f>'), ['3', 'w', '<M-f>'])
        self.assertEqual(_tokenize('3w<M-f>'), ['3', 'w', '<M-f>'])
        self.assertEqual(_tokenize('<A-a><A-b>'), ['<M-a>', '<M-b>'])
        self.assertEqual(_tokenize('<C-P>x'), ['<C-P>', 'x'])
        self.assertEqual(_tokenize('<C-S-.>'), ['<C-S-.>'])
        self.assertEqual(_tokenize('<C-p>'), ['<C-p>'])
        self.assertEqual(_tokenize('<C-w><Bar>'), ['<C-w>', '<bar>'])
        self.assertEqual(_tokenize('<C-w><C-_>'), ['<C-w>', '<C-_>'])
        self.assertEqual(_tokenize('<C-w><C-b>'), ['<C-w>', '<C-b>'])
        self.assertEqual(_tokenize('<C-w><Space>'), ['<C-w>', '<space>'])
        self.assertEqual(_tokenize('<C-w><bs>'), ['<C-w>', '<bs>'])
        self.assertEqual(_tokenize('<C-w>='), ['<C-w>', '='])
        self.assertEqual(_tokenize('<C-w>>'), ['<C-w>', '>'])
        self.assertEqual(_tokenize('<C-w>b'), ['<C-w>', 'b'])
        self.assertEqual(_tokenize('<DoWn>abc.'), ['<down>', 'a', 'b', 'c', '.'])
        self.assertEqual(_tokenize('<Esc><ENTER>'), ['<esc>', '<cr>'])
        self.assertEqual(_tokenize('<Esc>ai'), ['<esc>', 'a', 'i'])
        self.assertEqual(_tokenize('<Leader>d'), ['<bslash>', 'd'])
        self.assertEqual(_tokenize('<M-a><A-b>'), ['<M-a>', '<M-b>'])
        self.assertEqual(_tokenize('<a-a><a-b>'), ['<M-a>', '<M-b>'])
        self.assertEqual(_tokenize('<c-m-.>'), ['<C-M-.>'])
        self.assertEqual(_tokenize('<d-i><c-d>'), ['<D-i>', '<C-d>'])
        self.assertEqual(_tokenize('<d-i><c-i>'), ['<D-i>', '<C-i>'])
        self.assertEqual(_tokenize('<d-i>i.'), ['<D-i>', 'i', '.'])
        self.assertEqual(_tokenize('<leader><leader>d'), ['<bslash>', '<bslash>', 'd'])
        self.assertEqual(_tokenize('<leader>d'), ['<bslash>', 'd'])
        self.assertEqual(_tokenize('<leader>ek'), ['<bslash>', 'e', 'k'])
        self.assertEqual(_tokenize('<lt><lt>'), ['<lt>', '<lt>'])
        self.assertEqual(_tokenize('<m-a><a-b>'), ['<M-a>', '<M-b>'])
        self.assertEqual(_tokenize('pp'), ['p', 'p'])

    def test_expected_closing_bracket(self):
        invalid_tokens = (
            '<A',
            '<C',
            '<C-',
            '<D-',
            '<M',
            '<S',
            '<S-',
            '<c-',
            '<d-'
            '<s-',
        )

        for invalid_token in invalid_tokens:
            with self.assertRaisesRegex(ValueError, "expected '>' at index"):
                _tokenize(invalid_token)

    def test_invalid_modifier_sequence(self):
        invalid_tokens = (
            '<A-A->',
            '<C-C->',
            '<a-a->',
            '<c-c->',
            '<c-s-c->',
            '<d-d->',
        )

        for invalid_token in invalid_tokens:
            with self.assertRaisesRegex(ValueError, "invalid modifier sequence"):
                _tokenize(invalid_token)

    def test_invalid_key_name(self):
        invalid_tokens = {
            '<>': '\'<>\' is not a known key',
            '<a>': 'wrong sequence <a>',
            '<foobar>': '\'<foobar>\' is not a known key',
            '<sp>': '\'<sp>\' is not a known key',
        }

        for invalid_token, invalid_token_msg in invalid_tokens.items():
            with self.assertRaisesRegex(ValueError, invalid_token_msg):
                _tokenize(invalid_token)


class TestToBareCommandName(unittest.TestCase):

    def test_basic(self):
        self.assertEquals('0', to_bare_command_name('0'))
        self.assertEquals('<f7>', to_bare_command_name('"210<f7>'))
        self.assertEquals('<f7>', to_bare_command_name('"a10<f7>'))
        self.assertEquals('<f7>', to_bare_command_name('10<f7>'))
        self.assertEquals('<f7>', to_bare_command_name('<f7>'))
        self.assertEquals('daw', to_bare_command_name('"12d2aw'))
        self.assertEquals('daw', to_bare_command_name('"a2d2aw'))
        self.assertEquals('daw', to_bare_command_name('2d2aw'))
        self.assertEquals('daw', to_bare_command_name('2daw'))
        self.assertEquals('daw', to_bare_command_name('d2aw'))
        self.assertEquals('daw', to_bare_command_name('daw'))
        self.assertEquals('dd', to_bare_command_name('d2d'))
