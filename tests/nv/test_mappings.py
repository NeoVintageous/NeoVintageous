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

from NeoVintageous.tests import unittest

from NeoVintageous.nv.mappings import INSERT
from NeoVintageous.nv.mappings import Mapping
from NeoVintageous.nv.mappings import NORMAL
from NeoVintageous.nv.mappings import OPERATOR_PENDING
from NeoVintageous.nv.mappings import SELECT
from NeoVintageous.nv.mappings import VISUAL
from NeoVintageous.nv.mappings import VISUAL_BLOCK
from NeoVintageous.nv.mappings import VISUAL_LINE
from NeoVintageous.nv.mappings import _find_full_match
from NeoVintageous.nv.mappings import _find_partial_matches
from NeoVintageous.nv.mappings import _seq_to_command
from NeoVintageous.nv.mappings import _seq_to_mapping
from NeoVintageous.nv.mappings import mappings_add
from NeoVintageous.nv.mappings import mappings_clear
from NeoVintageous.nv.mappings import mappings_is_incomplete
from NeoVintageous.nv.mappings import mappings_remove
from NeoVintageous.nv.mappings import mappings_resolve
from NeoVintageous.nv.plugin_commentary import CommentaryLines
from NeoVintageous.nv.plugin_sneak import SneakS
from NeoVintageous.nv.plugin_surround import SurroundS
from NeoVintageous.nv.plugin_unimpaired import UnimpairedBlankDown
from NeoVintageous.nv.vi.cmd_base import ViMissingCommandDef
from NeoVintageous.nv.vi.cmd_defs import ViMoveByWords
from NeoVintageous.nv.vi.cmd_defs import ViSubstituteByLines


class TestMapping(unittest.TestCase):

    def test_mapping(self):
        mapping = Mapping('lhs', 'rhs')
        self.assertEqual(mapping.lhs, 'lhs')
        self.assertEqual(mapping.rhs, 'rhs')

    def test_allows_empty_sequence(self):
        mapping = Mapping('', '')
        self.assertEqual(mapping.lhs, '')
        self.assertEqual(mapping.rhs, '')


class TestMappings(unittest.ViewTestCase):

    @unittest.mock_mappings()
    def test_add_raises_exception(self):
        for mode in ('unknownmode', 0, '', True, False):
            with self.assertRaises(KeyError):
                mappings_add(mode, 'x', 'y')
        self.assertMappingsEmpty()

    @unittest.mock_mappings()
    def test_add(self):
        mappings_add(unittest.INSERT, 'a', 'b')
        self.assertMapping(unittest.INSERT, 'a', 'b')

    @unittest.mock_mappings()
    def test_remove(self):
        mappings_add(unittest.INSERT, 'A', 'B')
        mappings_add(unittest.INSERT, 'C', 'D')
        mappings_add(unittest.INSERT, 'E', 'F')
        mappings_add(unittest.NORMAL, 'A', 'B')
        mappings_add(unittest.NORMAL, 'C', 'D')
        mappings_add(unittest.NORMAL, 'E', 'F')
        mappings_remove(unittest.INSERT, 'C')
        mappings_remove(unittest.NORMAL, 'E')
        self.assertMappings({
            INSERT: {
                'A': 'B',
                'E': 'F',
            },
            NORMAL: {
                'A': 'B',
                'C': 'D',
            },
            OPERATOR_PENDING: {},
            SELECT: {},
            VISUAL_BLOCK: {},
            VISUAL_LINE: {},
            VISUAL: {},
        })

    @unittest.mock_mappings()
    def test_remove_raises_exception(self):
        with self.assertRaises(KeyError, msg='mapping not found'):
            mappings_remove('foobar', 'foobar')

        with self.assertRaises(KeyError, msg='mapping not found'):
            mappings_remove(unittest.INSERT, 'foobar')

        mappings_add(unittest.INSERT, 'X', 'Y')

        with self.assertRaises(KeyError, msg='mapping not found'):
            mappings_remove(unittest.INSERT, 'foobar')

        # Should not raise exception (protect against false positive).
        mappings_remove(unittest.INSERT, 'X')
        self.assertMappingsEmpty()

    @unittest.mock_mappings()
    @unittest.mock.patch('NeoVintageous.nv.variables._defaults', {'mapleader': '\\'})
    @unittest.mock.patch('NeoVintageous.nv.variables._variables', {})
    def test_add_expands_keys(self):
        mappings_add(unittest.NORMAL, '<leader>d', ':NeovintageousTestX<CR>')
        self.assertMapping(unittest.NORMAL, '\\d', ':NeovintageousTestX<CR>')

    @unittest.mock_mappings()
    @unittest.mock.patch('NeoVintageous.nv.variables._defaults', {'mapleader': ','})
    @unittest.mock.patch('NeoVintageous.nv.variables._variables', {})
    def test_add_normalises_mapping(self):
        mappings_add(NORMAL, '<Space>', 'a')
        mappings_add(VISUAL, '<SPACE>', 'v')
        mappings_add(VISUAL_LINE, '<Leader><Space>', 'b')
        mappings_add(VISUAL_BLOCK, '<LeaDeR><SpAcE><c-w><C-w><c-s-b><c-s-B>', 'c')
        self.assertMapping(unittest.NORMAL, '<space>', 'a')
        self.assertMapping(unittest.VISUAL, '<space>', 'v')
        self.assertMapping(unittest.VISUAL_LINE, ',<space>', 'b')
        self.assertMapping(unittest.VISUAL_BLOCK, ',<space><C-w><C-w><C-S-b><C-S-B>', 'c')

    @unittest.mock_mappings()
    @unittest.mock.patch('NeoVintageous.nv.variables._defaults', {'mapleader': '\\'})
    @unittest.mock.patch('NeoVintageous.nv.variables._variables', {})
    def test_can_remove_expanded_keys(self):
        mappings_add(unittest.NORMAL, '<leader>d', ':NeovintageousTestX<CR>')
        mappings_remove(unittest.NORMAL, '\\d')
        self.assertMappingsEmpty()
        mappings_add(unittest.NORMAL, '<leader>d', ':NeovintageousTestX<CR>')
        mappings_remove(unittest.NORMAL, '<leader>d')
        self.assertMappingsEmpty()

    @unittest.mock_mappings()
    @unittest.mock.patch('NeoVintageous.nv.variables._defaults', {'mapleader': ','})
    def test_can_remove_normalised_mapping(self):
        for seq in ('<Space>', '<SPACE>', '<Space>', '<SpAcE>'):
            mappings_add(NORMAL, '<Space>', 'a')
            self.assertMapping(NORMAL, '<space>', 'a')
            mappings_remove(NORMAL, seq)
            self.assertMappingsEmpty()

        mappings_add(NORMAL, '<Space><C-w><C-M-b><C-M-B>', 'a')
        mappings_remove(NORMAL, '<SpAcE><c-w><c-m-b><c-m-B>')
        self.assertMappingsEmpty()

    @unittest.mock_mappings()
    def test_can_clear(self):
        mappings_add(unittest.NORMAL, 'X', 'Y')
        mappings_add(unittest.INSERT, 'X', 'Y')
        mappings_add(unittest.NORMAL, 'X', 'Y')
        mappings_add(unittest.OPERATOR_PENDING, 'X', 'Y')
        mappings_add(unittest.SELECT, 'X', 'Y')
        mappings_add(unittest.VISUAL_BLOCK, 'X', 'Y')
        mappings_add(unittest.VISUAL_LINE, 'X', 'Y')
        mappings_add(unittest.VISUAL, 'X', 'Y')
        mappings_clear()
        self.assertMappingsEmpty()

    @unittest.mock_mappings()
    def test_seq_to_mapping(self):
        mappings_add(unittest.NORMAL, 'G', 'G_')
        mapping = _seq_to_mapping(unittest.NORMAL, 'G')

        self.assertIsInstance(mapping, Mapping)
        self.assertEqual(mapping.rhs, 'G_')
        self.assertEqual(mapping.lhs, 'G')

        mappings_add(unittest.NORMAL, '<C-m>', 'daw')
        mapping = _seq_to_mapping(unittest.NORMAL, '<C-m>')

        self.assertIsInstance(mapping, Mapping)
        self.assertEqual(mapping.rhs, 'daw')
        self.assertEqual(mapping.lhs, '<C-m>')

    @unittest.mock_mappings()
    def test_seq_to_mapping_returns_none_when_not_found(self):
        self.assertIsNone(_seq_to_mapping(unittest.NORMAL, ''))
        self.assertIsNone(_seq_to_mapping(unittest.NORMAL, 'G'))
        self.assertIsNone(_seq_to_mapping(unittest.NORMAL, 'foobar'))

    @unittest.mock_mappings()
    def test_find_partial_match(self):
        self.assertEqual(_find_partial_matches(unittest.NORMAL, ''), [])
        self.assertEqual(_find_partial_matches(unittest.NORMAL, 'foobar'), [])

        mappings_add(unittest.NORMAL, 'x', 'y')

        self.assertEqual(_find_partial_matches(unittest.NORMAL, ''), ['x'])
        self.assertEqual(_find_partial_matches(unittest.NORMAL, 'x'), ['x'])
        self.assertEqual(_find_partial_matches(unittest.NORMAL, ' '), [])
        self.assertEqual(_find_partial_matches(unittest.NORMAL, 'x '), [])
        self.assertEqual(_find_partial_matches(unittest.NORMAL, ' x'), [])
        self.assertEqual(_find_partial_matches(unittest.NORMAL, 'y'), [])
        self.assertEqual(_find_partial_matches(unittest.NORMAL, 'xy'), [])
        self.assertEqual(_find_partial_matches(unittest.NORMAL, 'foobar'), [])

        mappings_add(unittest.NORMAL, 'yc', 'g')
        mappings_add(unittest.NORMAL, 'yd', 'g')
        mappings_add(unittest.NORMAL, 'ya', 'g')
        mappings_add(unittest.NORMAL, 'yb', 'g')
        mappings_add(unittest.NORMAL, 'Y', 'g')  # For case-sensitive test.
        mappings_add(unittest.NORMAL, 'Ya', 'g')  # For case-sensitive test.

        # Should also be sorted.
        self.assertEqual(sorted(_find_partial_matches(unittest.NORMAL, 'y')), ['ya', 'yb', 'yc', 'yd'])
        self.assertEqual(sorted(_find_partial_matches(unittest.NORMAL, '')), ['Y', 'Ya', 'x', 'ya', 'yb', 'yc', 'yd'])
        self.assertEqual(sorted(_find_partial_matches(unittest.NORMAL, 'yd')), ['yd'])
        self.assertEqual(sorted(_find_partial_matches(unittest.NORMAL, 'x')), ['x'])

    @unittest.mock_mappings()
    def test_find_full_match(self):
        self.assertEqual(_find_full_match(unittest.NORMAL, ''), None)
        self.assertEqual(_find_full_match(unittest.NORMAL, 'foobar'), None)

        mappings_add(unittest.NORMAL, 'xc', 'y')
        mappings_add(unittest.NORMAL, 'xd', 'abc')
        mappings_add(unittest.NORMAL, 'xa', 'y')
        mappings_add(unittest.NORMAL, 'xb', 'y')

        self.assertEqual(_find_full_match(unittest.NORMAL, ''), None)
        self.assertEqual(_find_full_match(unittest.NORMAL, ' '), None)
        self.assertEqual(_find_full_match(unittest.NORMAL, 'foobar'), None)
        self.assertEqual(_find_full_match(unittest.NORMAL, 'x'), None)
        self.assertEqual(_find_full_match(unittest.NORMAL, 'xdd'), None)
        self.assertEqual(_find_full_match(unittest.NORMAL, 'xd '), None)
        self.assertEqual(_find_full_match(unittest.NORMAL, ' xd'), None)

        self.assertEqual(_find_full_match(unittest.NORMAL, 'xd'), 'abc')
        self.assertEqual(_find_full_match(unittest.NORMAL, 'xd'), 'abc')
        self.assertEqual(_find_full_match(unittest.NORMAL, 'xd'), 'abc')
        self.assertEqual(_find_full_match(unittest.NORMAL, 'xd'), 'abc')

        mappings_add(unittest.NORMAL, 'bbc', 'y')
        mappings_add(unittest.NORMAL, 'bbd', 'y')
        mappings_add(unittest.NORMAL, 'bbb', 'cde')
        mappings_add(unittest.NORMAL, 'bba', 'y')

        self.assertEqual(_find_full_match(unittest.NORMAL, ''), None)
        self.assertEqual(_find_full_match(unittest.NORMAL, 'b'), None)
        self.assertEqual(_find_full_match(unittest.NORMAL, 'bb'), None)
        self.assertEqual(_find_full_match(unittest.NORMAL, 'bbb'), 'cde')

    @unittest.mock_mappings()
    def test_is_incomplete(self):
        self.assertFalse(mappings_is_incomplete(NORMAL, 'f'))
        mappings_add(unittest.NORMAL, 'aa', 'y')
        self.assertEqual(mappings_is_incomplete(unittest.NORMAL, 'a'), True)
        mappings_add(unittest.NORMAL, 'b', 'y')
        self.assertFalse(mappings_is_incomplete(unittest.NORMAL, 'b'))
        mappings_add(unittest.NORMAL, 'c', 'y')
        mappings_add(unittest.NORMAL, 'cc', 'y')
        self.assertFalse(mappings_is_incomplete(unittest.NORMAL, 'c'))
        mappings_add(unittest.NORMAL, 'd', 'y')
        mappings_add(unittest.NORMAL, 'ddd', 'y')
        self.assertEquals(mappings_is_incomplete(unittest.NORMAL, 'dd'), True)
        self.assertFalse(mappings_is_incomplete(NORMAL, 'f'))


class TestResolve(unittest.ViewTestCase):

    @unittest.mock_mappings()
    @unittest.mock.patch('NeoVintageous.nv.mappings.get_partial_sequence')
    @unittest.mock.patch('NeoVintageous.nv.mappings.get_mode')
    def test_resolve(self, get_mode, get_partial_sequence):
        get_mode.return_value = NORMAL
        get_partial_sequence.return_value = None

        mappings_add(NORMAL, 'lhs', 'rhs')

        self.assertIsInstance(mappings_resolve(self.view, 'foobar', NORMAL), ViMissingCommandDef)
        self.assertIsInstance(mappings_resolve(self.view, 'w', NORMAL), ViMoveByWords, 'expected core command')
        self.assertIsInstance(mappings_resolve(self.view, 'gcc', NORMAL), CommentaryLines, 'expected plugin comman')

        actual = mappings_resolve(self.view, 'lhs', NORMAL)
        self.assertIsInstance(actual, Mapping)
        expected = Mapping('lhs', 'rhs')
        self.assertEqual(actual.rhs, expected.rhs)
        self.assertEqual(actual.lhs, expected.lhs)

    @unittest.mock_mappings()
    def test_can_resolve_core_mapping(self):
        self.setNormalMode()
        self.assertIsInstance(mappings_resolve(self.view, 'w', unittest.NORMAL, True), ViMoveByWords)
        self.assertIsInstance(mappings_resolve(self.view, 'w', unittest.NORMAL, False), ViMoveByWords)

    @unittest.mock_mappings()
    def test_can_resolve_user_mapping(self):
        self.setNormalMode()
        mappings_add(NORMAL, 'w', 'b')
        mapping = mappings_resolve(self.view, 'w', unittest.NORMAL, True)
        self.assertIsInstance(mapping, Mapping)
        self.assertEqual((mapping.lhs, mapping.rhs), ('w', 'b'))
        self.assertIsInstance(mappings_resolve(self.view, 'w', unittest.NORMAL, False), ViMoveByWords)

    @unittest.mock_mappings()
    def test_resolve_missing_command(self):
        self.setNormalMode()
        for mode in (NORMAL, VISUAL, OPERATOR_PENDING, 'unknownmode'):
            self.assertIsInstance(mappings_resolve(self.view, 'foobar', mode), ViMissingCommandDef)

    @unittest.mock_mappings()
    def test_resolve_plugin(self):
        self.setNormalMode()
        self.assertIsInstance(mappings_resolve(self.view, 'gcc', NORMAL), CommentaryLines)
        self.assertIsInstance(mappings_resolve(self.view, ']<Space>', NORMAL), UnimpairedBlankDown)
        self.set_setting('enable_sneak', False)
        self.assertIsInstance(mappings_resolve(self.view, 'S', NORMAL), ViSubstituteByLines)
        self.set_setting('enable_sneak', True)
        self.assertIsInstance(mappings_resolve(self.view, 'S', NORMAL), SneakS)
        self.setVisualMode()
        self.assertIsInstance(mappings_resolve(self.view, 'S', VISUAL), SurroundS)

    @unittest.mock_mappings()
    def test_resolve_plugin_disabled(self):
        self.setNormalMode()
        self.set_setting('enable_commentary', False)
        self.set_setting('enable_unimpaired', False)
        self.set_setting('enable_surround', False)
        self.assertIsInstance(mappings_resolve(self.view, 'gcc', NORMAL), ViMissingCommandDef)
        self.assertIsInstance(mappings_resolve(self.view, ']<Space>', NORMAL), ViMissingCommandDef)
        self.set_setting('enable_sneak', False)
        self.assertIsInstance(mappings_resolve(self.view, 'S', NORMAL), ViSubstituteByLines)
        self.set_setting('enable_sneak', True)
        self.assertIsInstance(mappings_resolve(self.view, 'S', NORMAL), SneakS)
        self.setVisualMode()
        self.assertIsInstance(mappings_resolve(self.view, 'S', VISUAL), ViSubstituteByLines)
        self.set_setting('enable_commentary', True)
        self.set_setting('enable_unimpaired', True)
        self.set_setting('enable_surround', True)
        self.assertIsInstance(mappings_resolve(self.view, 'gcc', NORMAL), CommentaryLines)
        self.assertIsInstance(mappings_resolve(self.view, ']<Space>', NORMAL), UnimpairedBlankDown)
        self.set_setting('enable_sneak', False)
        self.assertIsInstance(mappings_resolve(self.view, 'S', NORMAL), ViSubstituteByLines)
        self.set_setting('enable_sneak', True)
        self.assertIsInstance(mappings_resolve(self.view, 'S', NORMAL), SneakS)
        self.setVisualMode()
        self.assertIsInstance(mappings_resolve(self.view, 'S', VISUAL), SurroundS)


class TestSeqToCommand(unittest.TestCase):

    @unittest.mock.patch.dict('NeoVintageous.nv.vi.keys.mappings', {
        'a': {'s': 'asv'},
        'b': {'s': 'bsv', 't': 'tsv', 'ep': 'ep', 'dp2': 'dp2'}
    })
    @unittest.mock.patch('NeoVintageous.nv.mappings.plugin')
    def test_seq_to_command(self, plugin):
        class Plugin():
            pass

        ep = Plugin()
        dp = Plugin()

        plugin.mappings = {
            'b': {'s': 'plugin_bsv', 'ep': ep, 'dp': dp, 'dp2': dp},
            'c': {'s': 'plugin_csv'}
        }

        class Settings():
            def get(self, name, default=None):
                return True

        class View():
            def settings(self):
                return Settings()

        self.assertEqual(_seq_to_command(seq='s', view=View(), mode='a'), 'asv')
        self.assertIsInstance(_seq_to_command(seq='s', view=View(), mode=''), ViMissingCommandDef)
        # Plugin mode exists, but not sequence.
        self.assertEqual(_seq_to_command(seq='t', view=View(), mode='b'), 'tsv')
        # Plugin mapping override.
        self.assertEqual(_seq_to_command(seq='s', view=View(), mode='b'), 'plugin_bsv')
        self.assertEqual(_seq_to_command(seq='ep', view=View(), mode='b'), ep)
        self.assertEqual(_seq_to_command(seq='s', view=View(), mode='c'), 'plugin_csv')

    def test_unknown_mode(self):
        class View():
            def settings(self):
                pass
        self.assertIsInstance(_seq_to_command(seq='s', view=View(), mode='unknown'), ViMissingCommandDef)
        self.assertIsInstance(_seq_to_command(seq='s', view=View(), mode='u'), ViMissingCommandDef)

    def test_unknown_sequence(self):
        class View():
            def settings(self):
                pass
        self.assertIsInstance(_seq_to_command(seq='foobar', view=View(), mode='a'), ViMissingCommandDef)
