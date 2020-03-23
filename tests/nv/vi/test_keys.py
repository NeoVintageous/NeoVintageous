# Copyright (C) 2018 The NeoVintageous Team (NeoVintageous).
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

from unittest import mock
import unittest

from NeoVintageous.nv.vi.keys import KeySequenceTokenizer
from NeoVintageous.nv.vi.keys import to_bare_command_name
from NeoVintageous.nv.vi.keys import tokenize_keys


class TestKeySequenceTokenizer(unittest.TestCase):

    @mock.patch.dict('NeoVintageous.nv.variables._variables', {}, clear=True)
    def test_tokenize_one(self):
        def _tokenize_one(source):
            return KeySequenceTokenizer(source)._tokenize_one()

        self.assertEqual(_tokenize_one('0'), '0', 'zero key')
        self.assertEqual(_tokenize_one('<A-i>'), '<M-i>')
        self.assertEqual(_tokenize_one('<Bar>'), '<bar>')
        self.assertEqual(_tokenize_one('<Bslash>'), '<bslash>')
        self.assertEqual(_tokenize_one('<C-P>'), '<C-P>', 'ctrl-modified upper case letter key')
        self.assertEqual(_tokenize_one('<C-S-.>'), '<C-S-.>', 'ctrl-shift modified period key')
        self.assertEqual(_tokenize_one('<C-S-F3>'), '<C-S-f3>')
        self.assertEqual(_tokenize_one('<C-S-f3>'), '<C-S-f3>')
        self.assertEqual(_tokenize_one('<C-p>'), '<C-p>', 'ctrl-modified lower case letter key')
        self.assertEqual(_tokenize_one('<C-s>'), '<C-s>')
        self.assertEqual(_tokenize_one('<C-w>'), '<C-w>')
        self.assertEqual(_tokenize_one('<D-A>'), '<D-A>')
        self.assertEqual(_tokenize_one('<D-a>'), '<D-a>')
        self.assertEqual(_tokenize_one('<D-i>'), '<D-i>')
        self.assertEqual(_tokenize_one('<DoWn>'), '<down>', 'less than key')
        self.assertEqual(_tokenize_one('<Enter>'), '<cr>')
        self.assertEqual(_tokenize_one('<Esc>'), '<esc>', 'esc key title case')
        self.assertEqual(_tokenize_one('<HOME>'), '<home>', 'less than key')
        self.assertEqual(_tokenize_one('<Leader>'), '<bslash>', 'leader key')
        self.assertEqual(_tokenize_one('<M-i>'), '<M-i>')
        self.assertEqual(_tokenize_one('<RETURN>'), '<cr>')
        self.assertEqual(_tokenize_one('<Return>'), '<cr>')
        self.assertEqual(_tokenize_one('<RigHt>'), '<right>', 'less than key')
        self.assertEqual(_tokenize_one('<Space>'), '<space>', 'space key')
        self.assertEqual(_tokenize_one('<bs>'), '<bs>')
        self.assertEqual(_tokenize_one('<c-Space>'), '<C-space>', 'ctrl-space key')
        self.assertEqual(_tokenize_one('<c-m-.>'), '<C-M-.>', 'ctrl-alt-period key')
        self.assertEqual(_tokenize_one('<c-m-s-a>'), '<C-M-S-a>')
        self.assertEqual(_tokenize_one('<c-m-s>'), '<C-M-s>')
        self.assertEqual(_tokenize_one('<c-s-b>'), '<C-S-b>')
        self.assertEqual(_tokenize_one('<d-A>'), '<D-A>')
        self.assertEqual(_tokenize_one('<d-a>'), '<D-a>')
        self.assertEqual(_tokenize_one('<eSc>'), '<esc>', 'esc key mixed case')
        self.assertEqual(_tokenize_one('<enD>'), '<end>', 'less than key')
        self.assertEqual(_tokenize_one('<enter>'), '<cr>')
        self.assertEqual(_tokenize_one('<esc>'), '<esc>', 'esc key lowercase')
        self.assertEqual(_tokenize_one('<insert>'), '<insert>')
        self.assertEqual(_tokenize_one('<leader>'), '<bslash>', 'leader key')
        self.assertEqual(_tokenize_one('<left>'), '<left>', 'less than key')
        self.assertEqual(_tokenize_one('<lt>'), '<lt>', 'less than key')
        self.assertEqual(_tokenize_one('<m-c-x>'), '<C-M-x>')
        self.assertEqual(_tokenize_one('<m-s-c>'), '<M-S-c>')
        self.assertEqual(_tokenize_one('<s-c-x>'), '<C-S-x>')
        self.assertEqual(_tokenize_one('<s-m-x>'), '<M-S-x>')
        self.assertEqual(_tokenize_one('<space>'), '<space>', 'space key')
        self.assertEqual(_tokenize_one('<tab>'), '<tab>', 'tab key')
        self.assertEqual(_tokenize_one('<uP>'), '<up>', 'less than key')
        self.assertEqual(_tokenize_one('>'), '>')
        self.assertEqual(_tokenize_one('P'), 'P', 'upper case letter key')
        self.assertEqual(_tokenize_one('p'), 'p', 'lower letter key')

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

        for token in invalid_tokens:
            with self.assertRaisesRegex(ValueError, "expected '>' at index"):
                KeySequenceTokenizer(token)._tokenize_one()

    def test_invalid_modifier_sequence(self):
        invalid_tokens = (
            '<A-A->',
            '<C-C->',
            '<a-a->',
            '<c-c->',
            '<c-s-c->',
            '<d-d->',
        )

        for token in invalid_tokens:
            with self.assertRaisesRegex(ValueError, "invalid modifier sequence"):
                KeySequenceTokenizer(token)._tokenize_one()

    def test_invalid_key_name(self):
        invalid_tokens = {
            '<>': '\'<>\' is not a known key',
            '<a>': 'wrong sequence <a>',
            '<foobar>': '\'<foobar>\' is not a known key',
            '<sp>': '\'<sp>\' is not a known key',
        }

        for token, msg in invalid_tokens.items():
            with self.assertRaisesRegex(ValueError, msg):
                KeySequenceTokenizer(token)._tokenize_one()

    @mock.patch.dict('NeoVintageous.nv.variables._variables', {}, clear=True)
    def test_tokenize_keys(self):
        def tokenize(source):
            return list(tokenize_keys(source))

        self.assertEqual(tokenize('0<down>'), ['0', '<down>'])
        self.assertEqual(tokenize('3<insert>'), ['3', '<insert>'])
        self.assertEqual(tokenize('3<return>'), ['3', '<cr>'])
        self.assertEqual(tokenize('3w<A-f>'), ['3', 'w', '<M-f>'])
        self.assertEqual(tokenize('3w<M-f>'), ['3', 'w', '<M-f>'])
        self.assertEqual(tokenize('<A-a><A-b>'), ['<M-a>', '<M-b>'])
        self.assertEqual(tokenize('<C-P>x'), ['<C-P>', 'x'])
        self.assertEqual(tokenize('<C-S-.>'), ['<C-S-.>'])
        self.assertEqual(tokenize('<C-p>'), ['<C-p>'])
        self.assertEqual(tokenize('<C-w><Bar>'), ['<C-w>', '<bar>'])
        self.assertEqual(tokenize('<C-w><C-_>'), ['<C-w>', '<C-_>'])
        self.assertEqual(tokenize('<C-w><C-b>'), ['<C-w>', '<C-b>'])
        self.assertEqual(tokenize('<C-w><Space>'), ['<C-w>', '<space>'])
        self.assertEqual(tokenize('<C-w><bs>'), ['<C-w>', '<bs>'])
        self.assertEqual(tokenize('<C-w>='), ['<C-w>', '='])
        self.assertEqual(tokenize('<C-w>>'), ['<C-w>', '>'])
        self.assertEqual(tokenize('<C-w>b'), ['<C-w>', 'b'])
        self.assertEqual(tokenize('<DoWn>abc.'), ['<down>', 'a', 'b', 'c', '.'])
        self.assertEqual(tokenize('<Esc><ENTER>'), ['<esc>', '<cr>'])
        self.assertEqual(tokenize('<Esc>ai'), ['<esc>', 'a', 'i'])
        self.assertEqual(tokenize('<Leader>d'), ['<bslash>', 'd'])
        self.assertEqual(tokenize('<M-a><A-b>'), ['<M-a>', '<M-b>'])
        self.assertEqual(tokenize('<a-a><a-b>'), ['<M-a>', '<M-b>'])
        self.assertEqual(tokenize('<c-m-.>'), ['<C-M-.>'])
        self.assertEqual(tokenize('<d-i><c-d>'), ['<D-i>', '<C-d>'])
        self.assertEqual(tokenize('<d-i><c-i>'), ['<D-i>', '<C-i>'])
        self.assertEqual(tokenize('<d-i>i.'), ['<D-i>', 'i', '.'])
        self.assertEqual(tokenize('<leader><leader>d'), ['<bslash>', '<bslash>', 'd'])
        self.assertEqual(tokenize('<leader>d'), ['<bslash>', 'd'])
        self.assertEqual(tokenize('<leader>ek'), ['<bslash>', 'e', 'k'])
        self.assertEqual(tokenize('<lt><lt>'), ['<lt>', '<lt>'])
        self.assertEqual(tokenize('<m-a><a-b>'), ['<M-a>', '<M-b>'])
        self.assertEqual(tokenize('pp'), ['p', 'p'])


class TestFunctions(unittest.TestCase):

    def test_to_bare_command_name(self):
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
