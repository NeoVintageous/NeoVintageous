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

from NeoVintageous.nv.vi.cmd_base import ViMissingCommandDef
from NeoVintageous.nv.vi.keys import KeySequenceTokenizer
from NeoVintageous.nv.vi.keys import seq_to_command
from NeoVintageous.nv.vi.keys import to_bare_command_name


class TestKeySequenceTokenizer(unittest.TestCase):

    @mock.patch.dict('NeoVintageous.nv.variables._variables', {}, clear=True)
    def test_tokenize_one(self):
        def tokenize_one(source):
            return KeySequenceTokenizer(source).tokenize_one()

        self.assertEqual(tokenize_one('p'), 'p', 'lower letter key')
        self.assertEqual(tokenize_one('P'), 'P', 'upper case letter key')
        self.assertEqual(tokenize_one('<C-p>'), '<C-p>', 'ctrl-modified lower case letter key')
        self.assertEqual(tokenize_one('<C-P>'), '<C-P>', 'ctrl-modified upper case letter key')
        self.assertEqual(tokenize_one('<C-S-.>'), '<C-S-.>', 'ctrl-shift modified period key')
        self.assertEqual(tokenize_one('<C-S-f3>'), '<C-S-f3>')
        self.assertEqual(tokenize_one('<C-S-F3>'), '<C-S-f3>')
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
        self.assertEqual(tokenize_one('<space>'), '<space>', 'space key')
        self.assertEqual(tokenize_one('<c-Space>'), '<C-space>', 'ctrl-space key')
        self.assertEqual(tokenize_one('0'), '0', 'zero key')
        self.assertEqual(tokenize_one('<c-m-.>'), '<C-M-.>', 'ctrl-alt-period key')
        self.assertEqual(tokenize_one('<c-m-s-a>'), '<C-M-S-a>')
        self.assertEqual(tokenize_one('<c-m-s>'), '<C-M-s>')
        self.assertEqual(tokenize_one('<c-s-b>'), '<C-S-b>')
        self.assertEqual(tokenize_one('<m-c-x>'), '<C-M-x>')
        self.assertEqual(tokenize_one('<m-s-c>'), '<M-S-c>')
        self.assertEqual(tokenize_one('<s-c-x>'), '<C-S-x>')
        self.assertEqual(tokenize_one('<s-m-x>'), '<M-S-x>')
        self.assertEqual(tokenize_one('<tab>'), '<tab>', 'tab key')
        self.assertEqual(tokenize_one('<Leader>'), '<bslash>', 'leader key')
        self.assertEqual(tokenize_one('<leader>'), '<bslash>', 'leader key')
        self.assertEqual(tokenize_one('<Bar>'), '<bar>')
        self.assertEqual(tokenize_one('<bs>'), '<bs>')
        self.assertEqual(tokenize_one('<Bslash>'), '<bslash>')
        self.assertEqual(tokenize_one('<C-s>'), '<C-s>')
        self.assertEqual(tokenize_one('<C-w>'), '<C-w>')
        self.assertEqual(tokenize_one('<D-a>'), '<D-a>')
        self.assertEqual(tokenize_one('<d-a>'), '<D-a>')
        self.assertEqual(tokenize_one('<D-A>'), '<D-A>')
        self.assertEqual(tokenize_one('<d-A>'), '<D-A>')
        self.assertEqual(tokenize_one('<D-i>'), '<D-i>')
        self.assertEqual(tokenize_one('>'), '>')

    def test_expected_closing_bracket(self):
        invalid_tokens = (
            '<c-',
            '<C-',
            '<D-',
            '<d-'
            '<s-',
            '<S-',
            '<C',
            '<S',
        )

        for token in invalid_tokens:
            with self.assertRaisesRegex(ValueError, "expected '>' at index"):
                KeySequenceTokenizer(token).tokenize_one()

    def test_invalid_modifier_sequence(self):
        invalid_tokens = (
            '<c-c->',
            '<C-C->',
            '<d-d->',
            '<c-s-c->',
        )

        for token in invalid_tokens:
            with self.assertRaisesRegex(ValueError, "invalid modifier sequence"):
                KeySequenceTokenizer(token).tokenize_one()

    def test_invalid_key_name(self):
        invalid_tokens = {
            '<>': '\'\' is not a known key',
            '<foobar>': '\'foobar\' is not a known key',
            '<a>': 'wrong sequence <a>',
        }

        for token, msg in invalid_tokens.items():
            with self.assertRaisesRegex(ValueError, msg):
                KeySequenceTokenizer(token).tokenize_one()

    @mock.patch.dict('NeoVintageous.nv.variables._variables', {}, clear=True)
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
        self.assertEqual(iter_tokenize('<Leader>d'), ['<bslash>', 'd'])
        self.assertEqual(iter_tokenize('<leader><leader>d'), ['<bslash>', '<bslash>', 'd'])
        self.assertEqual(iter_tokenize('<leader>d'), ['<bslash>', 'd'])
        self.assertEqual(iter_tokenize('<leader>ek'), ['<bslash>', 'e', 'k'])
        self.assertEqual(iter_tokenize('<C-w>b'), ['<C-w>', 'b'])
        self.assertEqual(iter_tokenize('<C-w><bs>'), ['<C-w>', '<bs>'])
        self.assertEqual(iter_tokenize('<C-w><C-b>'), ['<C-w>', '<C-b>'])
        self.assertEqual(iter_tokenize('<C-w><C-_>'), ['<C-w>', '<C-_>'])
        self.assertEqual(iter_tokenize('<C-w>='), ['<C-w>', '='])
        self.assertEqual(iter_tokenize('<C-w>>'), ['<C-w>', '>'])
        self.assertEqual(iter_tokenize('<C-w><Bar>'), ['<C-w>', '<bar>'])
        self.assertEqual(iter_tokenize('<C-w><Space>'), ['<C-w>', '<space>'])


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


class TestSeqToCommand(unittest.TestCase):

    @mock.patch.dict('NeoVintageous.nv.vi.keys.mappings', {
        'a': {'s': 'asv'},
        'b': {'s': 'bsv', 't': 'tsv', 'ep': 'ep', 'dp2': 'dp2'}
    })
    @mock.patch('NeoVintageous.nv.vi.keys.plugin')
    def test_seq_to_command(self, plugin):
        class EnabledPlugin():
            def is_enabled(self, settings):
                return True

        class DisabledPlugin():
            def is_enabled(self, settings):
                return False

        ep = EnabledPlugin()
        dp = DisabledPlugin()

        plugin.mappings = {
            'b': {'s': 'plugin_bsv', 'ep': ep, 'dp': dp, 'dp2': dp},
            'c': {'s': 'plugin_csv'}
        }

        class View():
            def settings(self):
                pass

        self.assertEqual(seq_to_command(seq='s', view=View(), mode='a'), 'asv')
        self.assertIsInstance(seq_to_command(seq='s', view=View(), mode=None), ViMissingCommandDef)
        # Plugin mode exists, but not sequence.
        self.assertEqual(seq_to_command(seq='t', view=View(), mode='b'), 'tsv')
        # Plugin mapping override.
        self.assertEqual(seq_to_command(seq='s', view=View(), mode='b'), 'plugin_bsv')
        self.assertEqual(seq_to_command(seq='ep', view=View(), mode='b'), ep)
        self.assertIsInstance(seq_to_command(seq='dp', view=View(), mode='b'), ViMissingCommandDef)
        self.assertEqual(seq_to_command(seq='dp2', view=View(), mode='b'), 'dp2')
        # Plugin.
        self.assertEqual(seq_to_command(seq='s', view=View(), mode='c'), 'plugin_csv')

    def test_unkown_mode(self):
        class View():
            def settings(self):
                pass
        self.assertIsInstance(seq_to_command(seq='s', view=View(), mode='unknown'), ViMissingCommandDef)
        self.assertIsInstance(seq_to_command(seq='s', view=View(), mode='u'), ViMissingCommandDef)

    def test_unknown_sequence(self):
        class View():
            def settings(self):
                pass
        self.assertIsInstance(seq_to_command(seq='foobar', view=View(), mode='a'), ViMissingCommandDef)
