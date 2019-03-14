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

from NeoVintageous.nv.mappings import _find_full_match
from NeoVintageous.nv.mappings import _find_partial_matches
from NeoVintageous.nv.mappings import _seq_to_mapping
from NeoVintageous.nv.mappings import INSERT
from NeoVintageous.nv.mappings import Mapping
from NeoVintageous.nv.mappings import mappings_add
from NeoVintageous.nv.mappings import mappings_clear
from NeoVintageous.nv.mappings import mappings_is_incomplete
from NeoVintageous.nv.mappings import mappings_remove
from NeoVintageous.nv.mappings import mappings_resolve
from NeoVintageous.nv.mappings import NORMAL
from NeoVintageous.nv.mappings import OPERATOR_PENDING
from NeoVintageous.nv.mappings import SELECT
from NeoVintageous.nv.mappings import VISUAL
from NeoVintageous.nv.mappings import VISUAL_BLOCK
from NeoVintageous.nv.mappings import VISUAL_LINE
from NeoVintageous.nv.plugin_commentary import CommentLines
from NeoVintageous.nv.vi.cmd_base import ViMissingCommandDef
from NeoVintageous.nv.vi.cmd_defs import ViMoveByWords


# We need to patch the mappings storage dictionary so that out tests don't mess
# up our userland mappings, which would obviously be bad.
from NeoVintageous.nv.mappings import _mappings as _mappings_struct_


# Reusable mappings test patcher (also passes a clean mappings structure to tests).
_patch_mappings = unittest.mock.patch('NeoVintageous.nv.mappings._mappings',
                                      new_callable=lambda: {k: {} for k in _mappings_struct_})


class TestMapping(unittest.TestCase):

    def test_mapping(self):
        mapping = Mapping('lhs', 'rhs')
        self.assertEqual(mapping.sequence, 'lhs')
        self.assertEqual(mapping.mapping, 'rhs')

    def test_allows_empty_sequence(self):
        mapping = Mapping('', '')
        self.assertEqual(mapping.sequence, '')
        self.assertEqual(mapping.mapping, '')


class TestMappings(unittest.TestCase):

    @_patch_mappings
    def test_defaults(self, _mappings):
        self.assertEquals(_mappings, {
            INSERT: {},
            NORMAL: {},
            OPERATOR_PENDING: {},
            SELECT: {},
            VISUAL_BLOCK: {},
            VISUAL_LINE: {},
            VISUAL: {},
        })

    @_patch_mappings
    def test_can_add(self, _mappings):
        mappings_add(unittest.INSERT, 'A', 'B')
        mappings_add(unittest.NORMAL, 'C', 'D')
        mappings_add(unittest.NORMAL, 'C2', 'D2')
        mappings_add(unittest.NORMAL, 'C3', 'D3')
        mappings_add(unittest.NORMAL, 'A', 'B')
        mappings_add(unittest.OPERATOR_PENDING, 'E', 'F')
        mappings_add(unittest.SELECT, 'G', 'H')
        mappings_add(unittest.VISUAL_BLOCK, 'I', 'J')
        mappings_add(unittest.VISUAL_BLOCK, 'I2', 'J2')
        mappings_add(unittest.VISUAL_BLOCK, 'K', 'L')
        mappings_add(unittest.VISUAL_LINE, 'K', 'L')
        mappings_add(unittest.VISUAL, 'M', 'N')

        self.assertEquals(_mappings, {
            INSERT: {'A': 'B'},
            NORMAL: {
                'C': 'D',
                'C2': 'D2',
                'C3': 'D3',
                'A': 'B',
            },
            OPERATOR_PENDING: {'E': 'F'},
            SELECT: {'G': 'H'},
            VISUAL_BLOCK: {
                'I': 'J',
                'I2': 'J2',
                'K': 'L',
            },
            VISUAL_LINE: {'K': 'L'},
            VISUAL: {'M': 'N'},
        })

    @_patch_mappings
    def test_add_raises_exception(self, _mappings):
        expected = _mappings.copy()

        with self.assertRaises(KeyError):
            mappings_add('foobar', 'X', 'Y')

        self.assertEqual(_mappings, expected)

        # Should not raise exception (protect against false positive).
        mappings_add(unittest.INSERT, 'A', 'B')

    @_patch_mappings
    def test_can_remove(self, _mappings):
        mappings_add(unittest.INSERT, 'A', 'B')
        mappings_add(unittest.INSERT, 'C', 'D')
        mappings_add(unittest.INSERT, 'E', 'F')
        mappings_add(unittest.NORMAL, 'A', 'B')
        mappings_add(unittest.NORMAL, 'C', 'D')
        mappings_add(unittest.NORMAL, 'E', 'F')
        mappings_remove(unittest.INSERT, 'C')
        mappings_remove(unittest.NORMAL, 'E')

        self.assertEquals(_mappings, {
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

    @_patch_mappings
    def test_remove_raises_exception(self, _mappings):
        expected = _mappings.copy()

        with self.assertRaises(KeyError, msg='mapping not found'):
            mappings_remove('foobar', 'foobar')

        with self.assertRaises(KeyError, msg='mapping not found'):
            mappings_remove(unittest.INSERT, 'foobar')

        mappings_add(unittest.INSERT, 'X', 'Y')

        with self.assertRaises(KeyError, msg='mapping not found'):
            mappings_remove(unittest.INSERT, 'foobar')

        # Should not raise exception (protect against false positive).
        mappings_remove(unittest.INSERT, 'X')

        self.assertEqual(_mappings, expected)

    @_patch_mappings
    @unittest.mock.patch('NeoVintageous.nv.variables._defaults', {'mapleader': '\\'})
    @unittest.mock.patch('NeoVintageous.nv.variables._variables', {})
    def test_add_expands_keys(self, _mappings):
        mappings_add(unittest.NORMAL, '<leader>d', ':NeovintageousTestX<CR>')

        self.assertEqual(_mappings[unittest.NORMAL], {
            '\\d': ':NeovintageousTestX<CR>'
        })

    @_patch_mappings
    @unittest.mock.patch('NeoVintageous.nv.variables._defaults', {'mapleader': ','})
    def test_add_normalises_mapping(self, _mappings):
        mappings_add(NORMAL, '<Space>', 'a')
        mappings_add(VISUAL, '<SPACE>', 'v')
        mappings_add(VISUAL_LINE, '<Leader><Space>', 'b')
        mappings_add(VISUAL_BLOCK, '<LeaDeR><SpAcE><c-w><C-w><c-s-b><c-s-B>', 'c')
        self.assertEqual(_mappings[unittest.NORMAL], {'<space>': 'a'})
        self.assertEqual(_mappings[unittest.VISUAL], {'<space>': 'v'})
        self.assertEqual(_mappings[unittest.VISUAL_LINE], {',<space>': 'b'})
        self.assertEqual(_mappings[unittest.VISUAL_BLOCK], {',<space><C-w><C-w><C-S-b><C-S-B>': 'c'})

    @_patch_mappings
    @unittest.mock.patch('NeoVintageous.nv.variables._defaults', {'mapleader': '\\'})
    @unittest.mock.patch('NeoVintageous.nv.variables._variables', {})
    def test_can_remove_expanded_keys(self, _mappings):
        mappings_add(unittest.NORMAL, '<leader>d', ':NeovintageousTestX<CR>')
        mappings_remove(unittest.NORMAL, '\\d')

        self.assertEqual(_mappings[unittest.NORMAL], {})

        mappings_add(unittest.NORMAL, '<leader>d', ':NeovintageousTestX<CR>')
        mappings_remove(unittest.NORMAL, '<leader>d')

        self.assertEqual(_mappings[unittest.NORMAL], {})

    @_patch_mappings
    @unittest.mock.patch('NeoVintageous.nv.variables._defaults', {'mapleader': ','})
    def test_can_remove_normalised_mapping(self, _mappings):

        for seq in ('<Space>', '<SPACE>', '<Space>', '<SpAcE>'):
            mappings_add(NORMAL, '<Space>', 'a')
            self.assertNotEqual(_mappings[unittest.NORMAL], {})
            mappings_remove(NORMAL, seq)
            self.assertEqual(_mappings[unittest.NORMAL], {})

        mappings_add(NORMAL, '<Space><C-w><C-M-b><C-M-B>', 'a')
        self.assertNotEqual(_mappings[unittest.NORMAL], {})
        mappings_remove(NORMAL, '<SpAcE><c-w><c-m-b><c-m-B>')
        self.assertEqual(_mappings[unittest.NORMAL], {})

    @_patch_mappings
    def test_can_clear(self, _mappings):
        mappings_add(unittest.NORMAL, 'X', 'Y')
        mappings_add(unittest.INSERT, 'X', 'Y')
        mappings_add(unittest.NORMAL, 'X', 'Y')
        mappings_add(unittest.OPERATOR_PENDING, 'X', 'Y')
        mappings_add(unittest.SELECT, 'X', 'Y')
        mappings_add(unittest.VISUAL_BLOCK, 'X', 'Y')
        mappings_add(unittest.VISUAL_LINE, 'X', 'Y')
        mappings_add(unittest.VISUAL, 'X', 'Y')
        mappings_clear()

        self.assertEquals(_mappings, {
            INSERT: {},
            NORMAL: {},
            OPERATOR_PENDING: {},
            SELECT: {},
            VISUAL_BLOCK: {},
            VISUAL_LINE: {},
            VISUAL: {},
        })

    @_patch_mappings
    def test_seq_to_mapping(self, _mappings):
        mappings_add(unittest.NORMAL, 'G', 'G_')
        mapping = _seq_to_mapping(unittest.NORMAL, 'G')

        self.assertIsInstance(mapping, Mapping)
        self.assertEqual(mapping.mapping, 'G_')
        self.assertEqual(mapping.sequence, 'G')

        mappings_add(unittest.NORMAL, '<C-m>', 'daw')
        mapping = _seq_to_mapping(unittest.NORMAL, '<C-m>')

        self.assertIsInstance(mapping, Mapping)
        self.assertEqual(mapping.mapping, 'daw')
        self.assertEqual(mapping.sequence, '<C-m>')

    @_patch_mappings
    def test_seq_to_mapping_returns_none_when_not_found(self, _mappings):
        self.assertIsNone(_seq_to_mapping(unittest.NORMAL, ''))
        self.assertIsNone(_seq_to_mapping(unittest.NORMAL, 'G'))
        self.assertIsNone(_seq_to_mapping(unittest.NORMAL, 'foobar'))

    @_patch_mappings
    def test_find_partial_match(self, _mappings):
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

    @_patch_mappings
    def test_find_full_match(self, _mappings):
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

    @_patch_mappings
    def test_is_incomplete(self, _mappings):
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

    @_patch_mappings
    def test_resolve(self, _mappings):
        state = unittest.mock.Mock(partial_sequence=None, mode=NORMAL, view=self.view)
        mappings_add(NORMAL, 'lhs', 'rhs')

        self.assertIsInstance(mappings_resolve(state, 'foobar', NORMAL), ViMissingCommandDef)
        self.assertIsInstance(mappings_resolve(state, 'w', NORMAL), ViMoveByWords, 'expected core command')
        self.assertIsInstance(mappings_resolve(state, 'gcc', NORMAL), CommentLines, 'expected plugin comman')

        actual = mappings_resolve(state, 'lhs', NORMAL)
        self.assertIsInstance(actual, Mapping)
        expected = Mapping('lhs', 'rhs')
        self.assertEqual(actual.mapping, expected.mapping)
        self.assertEqual(actual.sequence, expected.sequence)
