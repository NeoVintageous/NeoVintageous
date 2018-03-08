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

from NeoVintageous.nv.mappings import _expand_first
from NeoVintageous.nv.mappings import _find_full_match
from NeoVintageous.nv.mappings import _find_partial_match
from NeoVintageous.nv.mappings import _get_seqs
from NeoVintageous.nv.mappings import _STATUS_COMPLETE
from NeoVintageous.nv.mappings import _STATUS_INCOMPLETE
from NeoVintageous.nv.mappings import CMD_TYPE_USER
from NeoVintageous.nv.mappings import INSERT
from NeoVintageous.nv.mappings import Mapping
from NeoVintageous.nv.mappings import mappings_add
from NeoVintageous.nv.mappings import mappings_clear
from NeoVintageous.nv.mappings import mappings_is_incomplete
from NeoVintageous.nv.mappings import mappings_remove
from NeoVintageous.nv.mappings import NORMAL
from NeoVintageous.nv.mappings import OPERATOR_PENDING
from NeoVintageous.nv.mappings import SELECT
from NeoVintageous.nv.mappings import VISUAL
from NeoVintageous.nv.mappings import VISUAL_BLOCK
from NeoVintageous.nv.mappings import VISUAL_LINE


# We need to patch the mappings storage dictionary so that out tests don't mess
# up our userland mappings, which would obviously be bad.
from NeoVintageous.nv.mappings import _mappings as __mappings_struct__


# Reusable mappings test patcher (also passes a clean mappings structure to tests).
_patch_mappings = unittest.mock.patch('NeoVintageous.nv.mappings._mappings',
                                      new_callable=lambda: {k: {} for k in __mappings_struct__})


class TestMapping(unittest.TestCase):

    def test_mapping(self):
        mapping = Mapping('h', 'm', 't', 's')
        self.assertEqual(mapping.head, 'h')
        self.assertEqual(mapping.tail, 't')
        self.assertEqual(mapping.status, 's')
        self.assertEqual(mapping.mapping, 'm')
        self.assertEqual(mapping.sequence, 'ht')

    def test_allows_empty_sequence(self):
        mapping = Mapping('', '', '', '')
        self.assertEqual(mapping.head, '')
        self.assertEqual(mapping.tail, '')
        self.assertEqual(mapping.status, '')
        self.assertEqual(mapping.mapping, '')
        self.assertEqual(mapping.sequence, '')

    def test_raises_exception(self):
        mapping = Mapping(None, None, None, None)
        with self.assertRaises(ValueError, msg='no mapping found'):
            mapping.sequence

        mapping = Mapping(None, 'm', 't', 's')
        with self.assertRaises(ValueError, msg='no mapping found'):
            mapping.sequence

        mapping = Mapping('h', 'm', None, 's')
        with self.assertRaises(ValueError, msg='no mapping found'):
            mapping.sequence


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
            INSERT: {'A': {'name': 'B', 'type': CMD_TYPE_USER}},
            NORMAL: {
                'C': {'name': 'D', 'type': CMD_TYPE_USER},
                'C2': {'name': 'D2', 'type': CMD_TYPE_USER},
                'C3': {'name': 'D3', 'type': CMD_TYPE_USER},
                'A': {'name': 'B', 'type': CMD_TYPE_USER},
            },
            OPERATOR_PENDING: {'E': {'name': 'F', 'type': CMD_TYPE_USER}},
            SELECT: {'G': {'name': 'H', 'type': CMD_TYPE_USER}},
            VISUAL_BLOCK: {
                'I': {'name': 'J', 'type': CMD_TYPE_USER},
                'I2': {'name': 'J2', 'type': CMD_TYPE_USER},
                'K': {'name': 'L', 'type': CMD_TYPE_USER},
            },
            VISUAL_LINE: {'K': {'name': 'L', 'type': CMD_TYPE_USER}},
            VISUAL: {'M': {'name': 'N', 'type': CMD_TYPE_USER}},
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
                'A': {'name': 'B', 'type': CMD_TYPE_USER},
                'E': {'name': 'F', 'type': CMD_TYPE_USER},
            },
            NORMAL: {
                'A': {'name': 'B', 'type': CMD_TYPE_USER},
                'C': {'name': 'D', 'type': CMD_TYPE_USER},
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
    @unittest.mock.patch('NeoVintageous.nv.vi.variables._DEFAULTS', {'mapleader': '\\'})
    @unittest.mock.patch('NeoVintageous.nv.vi.variables._VARIABLES', {})
    def test_add_expands_keys(self, _mappings):
        mappings_add(unittest.NORMAL, '<leader>d', ':NeovintageousToggleSideBar<CR>')

        self.assertEqual(_mappings[unittest.NORMAL], {
            '\\d': {'name': ':NeovintageousToggleSideBar<CR>', 'type': CMD_TYPE_USER}
        })

    @_patch_mappings
    @unittest.mock.patch('NeoVintageous.nv.vi.variables._DEFAULTS', {'mapleader': '\\'})
    @unittest.mock.patch('NeoVintageous.nv.vi.variables._VARIABLES', {})
    def test_can_remove_expanded_keys(self, _mappings):
        mappings_add(unittest.NORMAL, '<leader>d', ':NeovintageousToggleSideBar<CR>')
        mappings_remove(unittest.NORMAL, '\\d')

        self.assertEqual(_mappings[unittest.NORMAL], {})

        mappings_add(unittest.NORMAL, '<leader>d', ':NeovintageousToggleSideBar<CR>')
        mappings_remove(unittest.NORMAL, '<leader>d')

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
    def test_expand_first(self, _mappings):
        mappings_add(unittest.NORMAL, 'G', 'G_')
        mapping = _expand_first(unittest.NORMAL, 'G')

        self.assertIsInstance(mapping, Mapping)
        self.assertEqual(mapping.head, 'G')
        self.assertEqual(mapping.mapping, 'G_')
        self.assertEqual(mapping.tail, '')
        self.assertEqual(mapping.sequence, 'G')
        self.assertEqual(mapping.status, _STATUS_COMPLETE)

        mappings_add(unittest.NORMAL, '<C-m>', 'daw')
        mapping = _expand_first(unittest.NORMAL, '<C-m>')

        self.assertIsInstance(mapping, Mapping)
        self.assertEqual(mapping.head, '<C-m>')
        self.assertEqual(mapping.mapping, 'daw')
        self.assertEqual(mapping.tail, '')
        self.assertEqual(mapping.sequence, '<C-m>')
        self.assertEqual(mapping.status, _STATUS_COMPLETE)

        mappings_add(unittest.NORMAL, '<C-m>', 'daw')
        mapping = _expand_first(unittest.NORMAL, '<C-m>x')

        self.assertIsInstance(mapping, Mapping)
        self.assertEqual(mapping.head, '<C-m>')
        self.assertEqual(mapping.mapping, 'daw')
        self.assertEqual(mapping.tail, 'x')
        self.assertEqual(mapping.sequence, '<C-m>x')
        self.assertEqual(mapping.status, _STATUS_COMPLETE)

        mappings_add(unittest.NORMAL, 'xxA', 'daw')
        mapping = _expand_first(unittest.NORMAL, 'xx')

        self.assertIsInstance(mapping, Mapping)
        self.assertEqual(mapping.head, 'xx')
        self.assertEqual(mapping.mapping, '')
        self.assertEqual(mapping.tail, '')
        self.assertEqual(mapping.sequence, 'xx')
        self.assertEqual(mapping.status, _STATUS_INCOMPLETE)

    @_patch_mappings
    def test_expand_first_returns_none_when_not_found(self, _mappings):
        self.assertIsNone(_expand_first(unittest.NORMAL, ''))
        self.assertIsNone(_expand_first(unittest.NORMAL, 'G'))
        self.assertIsNone(_expand_first(unittest.NORMAL, 'foobar'))

    @_patch_mappings
    def test_get_mapped_seqs(self, _mappings):
        self.assertEqual(_get_seqs(unittest.NORMAL), [])

        mappings_add(unittest.NORMAL, 'B', 'Y')
        mappings_add(unittest.NORMAL, 'C', 'Z')
        mappings_add(unittest.NORMAL, 'A', 'X')
        mappings_add(unittest.INSERT, 'J', 'K')
        mappings_add(unittest.INSERT, 'I', 'L')
        mappings_add(unittest.VISUAL, 'M', 'N')

        # Should be sorted.
        self.assertEqual(_get_seqs(unittest.NORMAL), ['A', 'B', 'C'])
        self.assertEqual(_get_seqs(unittest.INSERT), ['I', 'J'])
        self.assertEqual(_get_seqs(unittest.VISUAL), ['M'])
        self.assertEqual(_get_seqs(unittest.SELECT), [])

    @_patch_mappings
    def test_find_partial_match(self, _mappings):
        self.assertEqual(_find_partial_match(unittest.NORMAL, ''), [])
        self.assertEqual(_find_partial_match(unittest.NORMAL, 'foobar'), [])

        mappings_add(unittest.NORMAL, 'x', 'y')

        # XXX Should _find_partial_match() accept an empty string?
        self.assertEqual(_find_partial_match(unittest.NORMAL, ''), ['x'])
        self.assertEqual(_find_partial_match(unittest.NORMAL, 'x'), ['x'])
        self.assertEqual(_find_partial_match(unittest.NORMAL, ' '), [])
        self.assertEqual(_find_partial_match(unittest.NORMAL, 'x '), [])
        self.assertEqual(_find_partial_match(unittest.NORMAL, ' x'), [])
        self.assertEqual(_find_partial_match(unittest.NORMAL, 'y'), [])
        self.assertEqual(_find_partial_match(unittest.NORMAL, 'xy'), [])
        self.assertEqual(_find_partial_match(unittest.NORMAL, 'foobar'), [])

        mappings_add(unittest.NORMAL, 'yc', 'g')
        mappings_add(unittest.NORMAL, 'yd', 'g')
        mappings_add(unittest.NORMAL, 'ya', 'g')
        mappings_add(unittest.NORMAL, 'yb', 'g')
        mappings_add(unittest.NORMAL, 'Y', 'g')  # For case-sensitive test.
        mappings_add(unittest.NORMAL, 'Ya', 'g')  # For case-sensitive test.

        # Should also be sorted.
        self.assertEqual(_find_partial_match(unittest.NORMAL, 'y'), ['ya', 'yb', 'yc', 'yd'])
        self.assertEqual(_find_partial_match(unittest.NORMAL, ''), ['Y', 'Ya', 'x', 'ya', 'yb', 'yc', 'yd'])
        # XXX Should _find_partial_match() accept empty string?
        self.assertEqual(_find_partial_match(unittest.NORMAL, 'yd'), ['yd'])
        self.assertEqual(_find_partial_match(unittest.NORMAL, 'x'), ['x'])

    @_patch_mappings
    def test_find_full_match(self, _mappings):
        self.assertEqual(_find_full_match(unittest.NORMAL, ''), (None, None))
        self.assertEqual(_find_full_match(unittest.NORMAL, 'foobar'), (None, None))

        mappings_add(unittest.NORMAL, 'xc', 'y')
        mappings_add(unittest.NORMAL, 'xd', 'abc')
        mappings_add(unittest.NORMAL, 'xa', 'y')
        mappings_add(unittest.NORMAL, 'xb', 'y')

        self.assertEqual(_find_full_match(unittest.NORMAL, ''), (None, None))
        self.assertEqual(_find_full_match(unittest.NORMAL, ' '), (None, None))
        self.assertEqual(_find_full_match(unittest.NORMAL, 'foobar'), (None, None))
        self.assertEqual(_find_full_match(unittest.NORMAL, 'x'), (None, None))
        self.assertEqual(_find_full_match(unittest.NORMAL, 'xdd'), (None, None))
        self.assertEqual(_find_full_match(unittest.NORMAL, 'xd '), (None, None))
        self.assertEqual(_find_full_match(unittest.NORMAL, ' xd'), (None, None))

        self.assertEqual(_find_full_match(unittest.NORMAL, 'xd'), ('xd', {'name': 'abc', 'type': CMD_TYPE_USER}))
        self.assertEqual(_find_full_match(unittest.NORMAL, 'xd'), ('xd', {'name': 'abc', 'type': CMD_TYPE_USER}))
        self.assertEqual(_find_full_match(unittest.NORMAL, 'xd'), ('xd', {'name': 'abc', 'type': CMD_TYPE_USER}))
        self.assertEqual(_find_full_match(unittest.NORMAL, 'xd'), ('xd', {'name': 'abc', 'type': CMD_TYPE_USER}))

        mappings_add(unittest.NORMAL, 'bbc', 'y')
        mappings_add(unittest.NORMAL, 'bbd', 'y')
        mappings_add(unittest.NORMAL, 'bbb', 'cde')
        mappings_add(unittest.NORMAL, 'bba', 'y')

        self.assertEqual(_find_full_match(unittest.NORMAL, ''), (None, None))
        self.assertEqual(_find_full_match(unittest.NORMAL, 'b'), (None, None))
        self.assertEqual(_find_full_match(unittest.NORMAL, 'bb'), (None, None))
        self.assertEqual(_find_full_match(unittest.NORMAL, 'bbb'), ('bbb', {'name': 'cde', 'type': CMD_TYPE_USER}))

    @_patch_mappings
    def test_is_incomplete(self, _mappings):
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
