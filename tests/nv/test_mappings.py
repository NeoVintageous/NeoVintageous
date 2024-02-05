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

from NeoVintageous.tests import unittest

from NeoVintageous.nv.mappings import INSERT
from NeoVintageous.nv.mappings import IncompleteMapping
from NeoVintageous.nv.mappings import Mapping
from NeoVintageous.nv.mappings import NORMAL
from NeoVintageous.nv.mappings import OPERATOR_PENDING
from NeoVintageous.nv.mappings import SELECT
from NeoVintageous.nv.mappings import VISUAL
from NeoVintageous.nv.mappings import VISUAL_BLOCK
from NeoVintageous.nv.mappings import VISUAL_LINE
from NeoVintageous.nv.mappings import _find_full_match
from NeoVintageous.nv.mappings import _has_partial_matches
from NeoVintageous.nv.mappings import _seq_to_command
from NeoVintageous.nv.mappings import _seq_to_mapping
from NeoVintageous.nv.mappings import clear_mappings
from NeoVintageous.nv.mappings import mappings_add
from NeoVintageous.nv.mappings import mappings_remove
from NeoVintageous.nv.mappings import mappings_resolve
from NeoVintageous.nv.plugin_commentary import CommentaryLines
from NeoVintageous.nv.plugin_sneak import SneakS
from NeoVintageous.nv.plugin_surround import SurroundS
from NeoVintageous.nv.plugin_unimpaired import UnimpairedBlankDown
from NeoVintageous.nv.vi.cmd_base import CommandNotFound
from NeoVintageous.nv.vi.cmd_defs import ViMoveByWordEnds
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
                mappings_add(mode, 'x', 'y')  # type: ignore[arg-type]
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
        mappings_add(unittest.NORMAL, 'FileType', 'js G H')
        mappings_add(unittest.NORMAL, 'FileType', 'php G H')
        mappings_add(unittest.NORMAL, 'I', 'J')
        mappings_add(unittest.NORMAL, 'FileType', 'php I J')
        mappings_add(unittest.NORMAL, 'FileType', 'php K L')
        mappings_remove(unittest.INSERT, 'C')
        mappings_remove(unittest.NORMAL, 'E')
        mappings_remove(unittest.NORMAL, 'G')
        mappings_remove(unittest.NORMAL, 'I')
        self.assertMappings({
            INSERT: {
                'A': 'B',
                'E': 'F',
            },
            NORMAL: {
                'A': 'B',
                'C': 'D',
                'K': {'php': 'L'}
            },
            OPERATOR_PENDING: {},
            SELECT: {},
            VISUAL_BLOCK: {},
            VISUAL_LINE: {},
            VISUAL: {},
        })

    @unittest.mock_mappings()
    def test_removing_unknown_mapping_raises_exception(self):
        with self.assertRaisesRegex(KeyError, 'foobar'):
            mappings_remove('foobar', 'foobar')

        with self.assertRaisesRegex(KeyError, 'foobar'):
            mappings_remove(unittest.INSERT, 'foobar')

        mappings_add(unittest.INSERT, 'X', 'Y')

        with self.assertRaisesRegex(KeyError, 'foobar'):
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
        mappings_add(unittest.NORMAL, 'FileType', 'php X Y')
        mappings_add(unittest.NORMAL, 'FileType', 'php P Y')
        mappings_add(unittest.NORMAL, 'FileType', 'js P Y')
        clear_mappings()
        self.assertMappingsEmpty()

    @unittest.mock_mappings()
    def test_seq_to_mapping(self):
        self.normal('fizz')
        mappings_add(unittest.NORMAL, 'G', 'G_')
        mappings_add(unittest.NORMAL, 'FileType', 'js G G^')
        mappings_add(unittest.NORMAL, 'FileType', 'php G G$')
        mapping = _seq_to_mapping(self.view, 'G')

        self.assertIsInstance(mapping, Mapping)
        self.assertEqual(mapping.rhs, 'G_')
        self.assertEqual(mapping.lhs, 'G')

        mappings_add(unittest.NORMAL, '<C-m>', 'daw')
        mapping = _seq_to_mapping(self.view, '<C-m>')

        self.assertIsInstance(mapping, Mapping)
        self.assertEqual(mapping.rhs, 'daw')
        self.assertEqual(mapping.lhs, '<C-m>')

        self.assignFileName('test.js')
        mapping = _seq_to_mapping(self.view, 'G')
        self.assertIsInstance(mapping, Mapping)
        self.assertEqual(mapping.lhs, 'G')
        self.assertEqual(mapping.rhs, 'G^')

        self.assignFileName('test.php')
        mapping = _seq_to_mapping(self.view, 'G')
        self.assertIsInstance(mapping, Mapping)
        self.assertEqual(mapping.lhs, 'G')
        self.assertEqual(mapping.rhs, 'G$')

    @unittest.mock_mappings()
    def test_seq_to_mapping_returns_none_when_not_found(self):
        self.normal('fizz')
        mappings_add(unittest.NORMAL, 'FileType', 'js G G_')
        self.assertIsNone(_seq_to_mapping(self.view, ''))
        self.assertIsNone(_seq_to_mapping(self.view, 'G'))
        self.assertIsNone(_seq_to_mapping(self.view, 'foobar'))
        self.assignFileName('test.php')
        self.assertIsNone(_seq_to_mapping(self.view, ''))
        self.assertIsNone(_seq_to_mapping(self.view, 'G'))

    @unittest.mock_mappings()
    def test_find_partial_match(self):
        self.assertFalse(_has_partial_matches(self.view, unittest.NORMAL, ''))
        self.assertFalse(_has_partial_matches(self.view, unittest.NORMAL, 'foobar'))

        mappings_add(unittest.NORMAL, 'x', 'y')

        self.assertTrue(_has_partial_matches(self.view, unittest.NORMAL, ''))
        self.assertTrue(_has_partial_matches(self.view, unittest.NORMAL, 'x'))
        self.assertFalse(_has_partial_matches(self.view, unittest.NORMAL, ' '))
        self.assertFalse(_has_partial_matches(self.view, unittest.NORMAL, 'x '))
        self.assertFalse(_has_partial_matches(self.view, unittest.NORMAL, ' x'))
        self.assertFalse(_has_partial_matches(self.view, unittest.NORMAL, 'y'))
        self.assertFalse(_has_partial_matches(self.view, unittest.NORMAL, 'xy'))
        self.assertFalse(_has_partial_matches(self.view, unittest.NORMAL, 'foobar'))

        mappings_add(unittest.NORMAL, 'FileType', 'js x yjs')
        self.assertTrue(_has_partial_matches(self.view, unittest.NORMAL, 'x'))

        mappings_add(unittest.NORMAL, 'yc', 'g')
        mappings_add(unittest.NORMAL, 'yd', 'g')
        mappings_add(unittest.NORMAL, 'ya', 'g')
        mappings_add(unittest.NORMAL, 'yb', 'g')
        mappings_add(unittest.NORMAL, 'Y', 'g')  # For case-sensitive test.
        mappings_add(unittest.NORMAL, 'Ya', 'g')  # For case-sensitive test.

        # Should also be sorted.
        self.assertTrue(_has_partial_matches(self.view, unittest.NORMAL, 'y'))
        self.assertTrue(_has_partial_matches(self.view, unittest.NORMAL, ''))
        self.assertTrue(_has_partial_matches(self.view, unittest.NORMAL, 'yd'))
        self.assertTrue(_has_partial_matches(self.view, unittest.NORMAL, 'x'))

        mappings_add(unittest.NORMAL, 'FileType', 'js fj1 g')
        mappings_add(unittest.NORMAL, 'FileType', 'js fj2 g')
        mappings_add(unittest.NORMAL, 'FileType', 'js yj1 g')
        mappings_add(unittest.NORMAL, 'FileType', 'js yj2 g')
        mappings_add(unittest.NORMAL, 'FileType', 'php yp g')
        mappings_add(unittest.NORMAL, 'FileType', 'php fp g')
        mappings_add(unittest.NORMAL, 'ta', 'g')
        mappings_add(unittest.NORMAL, 'FileType', 'php ta g')
        mappings_add(unittest.NORMAL, 'FileType', 'php tp g')

        self.assignFileName('test.js')
        self.assertTrue(_has_partial_matches(self.view, unittest.NORMAL, 'x'))
        self.assertTrue(_has_partial_matches(self.view, unittest.NORMAL, 'f'))
        self.assertTrue(_has_partial_matches(self.view, unittest.NORMAL, 'y'))
        self.assertTrue(_has_partial_matches(self.view, unittest.NORMAL, 'fj1'))
        self.assertFalse(_has_partial_matches(self.view, unittest.NORMAL, 'yp'))
        self.assertTrue(_has_partial_matches(self.view, unittest.NORMAL, 't'))
        self.assignFileName('test.php')
        self.assertTrue(_has_partial_matches(self.view, unittest.NORMAL, 'y'))
        self.assertTrue(_has_partial_matches(self.view, unittest.NORMAL, 'f'))
        self.assertFalse(_has_partial_matches(self.view, unittest.NORMAL, 'fj1'))
        self.assertTrue(_has_partial_matches(self.view, unittest.NORMAL, 't'))

    @unittest.mock_mappings()
    def test_find_full_match(self):
        self.assertEqual(_find_full_match(self.view, unittest.NORMAL, ''), None)
        self.assertEqual(_find_full_match(self.view, unittest.NORMAL, 'foobar'), None)

        mappings_add(unittest.NORMAL, 'xc', 'y')
        mappings_add(unittest.NORMAL, 'xd', 'abc')
        mappings_add(unittest.NORMAL, 'xa', 'y')
        mappings_add(unittest.NORMAL, 'xb', 'y')
        mappings_add(unittest.NORMAL, 'FileType', 'php xd aphp')
        mappings_add(unittest.NORMAL, 'FileType', 'php xj bphp')
        mappings_add(unittest.NORMAL, 'FileType', 'js xd ajs')
        mappings_add(unittest.NORMAL, 'FileType', 'html,go xd ahtmlgo')

        self.assertEqual(_find_full_match(self.view, unittest.NORMAL, ''), None)
        self.assertEqual(_find_full_match(self.view, unittest.NORMAL, ' '), None)
        self.assertEqual(_find_full_match(self.view, unittest.NORMAL, 'foobar'), None)
        self.assertEqual(_find_full_match(self.view, unittest.NORMAL, 'x'), None)
        self.assertEqual(_find_full_match(self.view, unittest.NORMAL, 'xdd'), None)
        self.assertEqual(_find_full_match(self.view, unittest.NORMAL, 'xd '), None)
        self.assertEqual(_find_full_match(self.view, unittest.NORMAL, ' xd'), None)
        self.assertEqual(_find_full_match(self.view, unittest.NORMAL, 'xd'), 'abc')
        self.assertEqual(_find_full_match(self.view, unittest.NORMAL, 'xd'), 'abc')
        self.assertEqual(_find_full_match(self.view, unittest.NORMAL, 'xd'), 'abc')
        self.assertEqual(_find_full_match(self.view, unittest.NORMAL, 'xd'), 'abc')

        mappings_add(unittest.NORMAL, 'bbc', 'y')
        mappings_add(unittest.NORMAL, 'bbd', 'y')
        mappings_add(unittest.NORMAL, 'bbb', 'cde')
        mappings_add(unittest.NORMAL, 'bba', 'y')
        mappings_add(unittest.NORMAL, 'FileType', 'php bbp yphp')
        mappings_add(unittest.NORMAL, 'FileType', 'js bbp yjs')

        self.assertEqual(_find_full_match(self.view, unittest.NORMAL, ''), None)
        self.assertEqual(_find_full_match(self.view, unittest.NORMAL, 'b'), None)
        self.assertEqual(_find_full_match(self.view, unittest.NORMAL, 'bb'), None)
        self.assertEqual(_find_full_match(self.view, unittest.NORMAL, 'bbb'), 'cde')

        self.assignFileName('test.js')
        self.assertEqual(_find_full_match(self.view, unittest.NORMAL, 'xd'), 'ajs')
        self.assertEqual(_find_full_match(self.view, unittest.NORMAL, 'bbp'), 'yjs')
        self.assignFileName('test.php')
        self.assertEqual(_find_full_match(self.view, unittest.NORMAL, 'xd'), 'aphp')
        self.assertEqual(_find_full_match(self.view, unittest.NORMAL, 'xj'), 'bphp')
        self.assertEqual(_find_full_match(self.view, unittest.NORMAL, 'bbp'), 'yphp')
        self.assignFileName('test.html')
        self.assertEqual(_find_full_match(self.view, unittest.NORMAL, 'xd'), 'ahtmlgo')
        self.assignFileName('test.go')
        self.assertEqual(_find_full_match(self.view, unittest.NORMAL, 'xd'), 'ahtmlgo')

    @unittest.mock_mappings()
    @unittest.mock.patch('NeoVintageous.nv.mappings.get_partial_sequence')
    @unittest.mock.patch('NeoVintageous.nv.mappings.get_mode')
    def test_is_incomplete(self, get_mode, get_partial_sequence):
        get_mode.return_value = NORMAL
        get_partial_sequence.return_value = 'f'
        self.assertFalse(isinstance(mappings_resolve(self.view), IncompleteMapping))
        mappings_add(unittest.NORMAL, 'aa', 'y')
        get_partial_sequence.return_value = 'a'
        self.assertTrue(isinstance(mappings_resolve(self.view), IncompleteMapping))
        mappings_add(unittest.NORMAL, 'b', 'y')
        get_partial_sequence.return_value = 'b'
        self.assertFalse(isinstance(mappings_resolve(self.view), IncompleteMapping))
        mappings_add(unittest.NORMAL, 'c', 'y')
        mappings_add(unittest.NORMAL, 'cc', 'y')
        get_partial_sequence.return_value = 'c'
        self.assertFalse(isinstance(mappings_resolve(self.view), IncompleteMapping))
        mappings_add(unittest.NORMAL, 'd', 'y')
        mappings_add(unittest.NORMAL, 'ddd', 'y')
        get_partial_sequence.return_value = 'dd'
        self.assertTrue(isinstance(mappings_resolve(self.view), IncompleteMapping))
        get_partial_sequence.return_value = 'f'
        self.assertFalse(isinstance(mappings_resolve(self.view), IncompleteMapping))
        mappings_add(unittest.NORMAL, 'FileType', 'php a y')
        mappings_add(unittest.NORMAL, 'FileType', 'php eee y')
        mappings_add(unittest.NORMAL, 'FileType', 'js b y')
        mappings_add(unittest.NORMAL, 'FileType', 'js ee y')
        self.assignFileName('test.php')
        get_partial_sequence.return_value = 'a'
        self.assertFalse(isinstance(mappings_resolve(self.view), IncompleteMapping))
        get_partial_sequence.return_value = 'b'
        self.assertFalse(isinstance(mappings_resolve(self.view), IncompleteMapping))
        get_partial_sequence.return_value = 'e'
        self.assertTrue(isinstance(mappings_resolve(self.view), IncompleteMapping))
        get_partial_sequence.return_value = 'ee'
        self.assertTrue(isinstance(mappings_resolve(self.view), IncompleteMapping))
        get_partial_sequence.return_value = 'eee'
        self.assertFalse(isinstance(mappings_resolve(self.view), IncompleteMapping))
        self.assignFileName('test.js')
        get_partial_sequence.return_value = 'e'
        self.assertTrue(isinstance(mappings_resolve(self.view), IncompleteMapping))
        get_partial_sequence.return_value = 'ee'
        self.assertFalse(isinstance(mappings_resolve(self.view), IncompleteMapping))


class TestResolve(unittest.ViewTestCase):

    def assertMappingEqual(self, expected: Mapping, actual) -> None:
        self.assertIsInstance(actual, Mapping)
        self.assertEqual(actual.rhs, expected.rhs)
        self.assertEqual(actual.lhs, expected.lhs)

    @unittest.mock_mappings()
    @unittest.mock.patch('NeoVintageous.nv.mappings.get_partial_sequence')
    @unittest.mock.patch('NeoVintageous.nv.mappings.get_mode')
    def test_resolve(self, get_mode, get_partial_sequence):
        get_mode.return_value = NORMAL
        get_partial_sequence.return_value = None
        mappings_add(NORMAL, 'lhs', 'rhs')
        mappings_add(NORMAL, 'FileType', 'php e y')
        mappings_add(NORMAL, 'FileType', 'js w y')
        self.assertIsInstance(mappings_resolve(self.view, 'foobar', NORMAL), CommandNotFound)
        self.assertIsInstance(mappings_resolve(self.view, 'w', NORMAL), ViMoveByWords, 'expected core command')
        self.assertIsInstance(mappings_resolve(self.view, 'gcc', NORMAL), CommentaryLines, 'expected plugin comman')
        self.assertIsInstance(mappings_resolve(self.view, 'e', NORMAL), ViMoveByWordEnds, 'expected core command')
        self.assertMappingEqual(Mapping('lhs', 'rhs'), mappings_resolve(self.view, 'lhs', NORMAL))
        self.assignFileName('test.php')
        self.assertMappingEqual(Mapping('e', 'y'), mappings_resolve(self.view, 'e', NORMAL))
        self.assertIsInstance(mappings_resolve(self.view, 'w', NORMAL), ViMoveByWords, 'expected core command')
        self.assignFileName('test.js')
        self.assertIsInstance(mappings_resolve(self.view, 'e', NORMAL), ViMoveByWordEnds, 'expected core command')
        self.assertMappingEqual(Mapping('w', 'y'), mappings_resolve(self.view, 'w', NORMAL))

    @unittest.mock_mappings()
    def test_can_resolve_core_mapping(self):
        self.setNormalMode()
        self.assertIsInstance(mappings_resolve(self.view, 'w', unittest.NORMAL, True), ViMoveByWords)
        self.assertIsInstance(mappings_resolve(self.view, 'w', unittest.NORMAL, False), ViMoveByWords)

    @unittest.mock_mappings()
    def test_can_resolve_user_mapping(self):
        self.setNormalMode()
        mappings_add(NORMAL, 'w', 'b')
        mappings_add(NORMAL, 'FileType', 'php e y')
        self.assertMappingEqual(Mapping('w', 'b'), mappings_resolve(self.view, 'w', NORMAL))
        self.assertIsInstance(mappings_resolve(self.view, 'w', unittest.NORMAL, False), ViMoveByWords)
        self.assertIsInstance(mappings_resolve(self.view, 'e', unittest.NORMAL), ViMoveByWordEnds)
        self.assignFileName('test.php')
        self.assertMappingEqual(Mapping('e', 'y'), mappings_resolve(self.view, 'e', NORMAL))
        self.assertIsInstance(mappings_resolve(self.view, 'e', unittest.NORMAL, False), ViMoveByWordEnds)

    @unittest.mock_mappings()
    def test_resolve_missing_command(self):
        self.setNormalMode()
        for mode in (NORMAL, VISUAL, OPERATOR_PENDING, 'unknownmode'):
            self.assertIsInstance(mappings_resolve(self.view, 'foobar', mode), CommandNotFound)

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
        self.assertIsInstance(mappings_resolve(self.view, 'gcc', NORMAL), CommandNotFound)
        self.assertIsInstance(mappings_resolve(self.view, ']<Space>', NORMAL), CommandNotFound)
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
        self.assertIsInstance(_seq_to_command(seq='s', view=View(), mode=''), CommandNotFound)
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
        self.assertIsInstance(_seq_to_command(seq='s', view=View(), mode='unknown'), CommandNotFound)
        self.assertIsInstance(_seq_to_command(seq='s', view=View(), mode='u'), CommandNotFound)

    def test_unknown_sequence(self):
        class View():
            def settings(self):
                pass
        self.assertIsInstance(_seq_to_command(seq='foobar', view=View(), mode='a'), CommandNotFound)
