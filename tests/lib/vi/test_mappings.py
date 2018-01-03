from NeoVintageous.tests import unittest

from NeoVintageous.lib.vi.mappings import CMD_TYPE_USER
from NeoVintageous.lib.vi.mappings import INSERT_MODE
from NeoVintageous.lib.vi.mappings import Mapping
from NeoVintageous.lib.vi.mappings import _STATUS_COMPLETE
from NeoVintageous.lib.vi.mappings import _STATUS_INCOMPLETE
from NeoVintageous.lib.vi.mappings import Mappings
from NeoVintageous.lib.vi.mappings import NORMAL_MODE
from NeoVintageous.lib.vi.mappings import OPERATOR_PENDING_MODE
from NeoVintageous.lib.vi.mappings import SELECT_MODE
from NeoVintageous.lib.vi.mappings import VISUAL_BLOCK_MODE
from NeoVintageous.lib.vi.mappings import VISUAL_LINE_MODE
from NeoVintageous.lib.vi.mappings import VISUAL_MODE


# We need to patch the mappings storage dictionary so that out tests don't mess
# up our userland mappings, which would obviously be bad.
from NeoVintageous.lib.vi.mappings import _mappings as __mappings_struct__


# Reusable mappings test patcher (also passes a clean mappings structure to tests).
_patch_mappings = unittest.mock.patch('NeoVintageous.lib.vi.mappings._mappings',
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
            INSERT_MODE: {},
            NORMAL_MODE: {},
            OPERATOR_PENDING_MODE: {},
            SELECT_MODE: {},
            VISUAL_BLOCK_MODE: {},
            VISUAL_LINE_MODE: {},
            VISUAL_MODE: {},
        })

    @_patch_mappings
    def test_can_add(self, _mappings):
        mappings = Mappings(unittest.mock.Mock(mode=unittest.NORMAL_MODE))
        mappings.add(unittest.INSERT_MODE, 'A', 'B')
        mappings.add(unittest.NORMAL_MODE, 'C', 'D')
        mappings.add(unittest.NORMAL_MODE, 'C2', 'D2')
        mappings.add(unittest.NORMAL_MODE, 'C3', 'D3')
        mappings.add(unittest.NORMAL_MODE, 'A', 'B')
        mappings.add(unittest.OPERATOR_PENDING_MODE, 'E', 'F')
        mappings.add(unittest.SELECT_MODE, 'G', 'H')
        mappings.add(unittest.VISUAL_BLOCK_MODE, 'I', 'J')
        mappings.add(unittest.VISUAL_BLOCK_MODE, 'I2', 'J2')
        mappings.add(unittest.VISUAL_BLOCK_MODE, 'K', 'L')
        mappings.add(unittest.VISUAL_LINE_MODE, 'K', 'L')
        mappings.add(unittest.VISUAL_MODE, 'M', 'N')

        self.assertEquals(_mappings, {
            INSERT_MODE: {'A': {'name': 'B', 'type': CMD_TYPE_USER}},
            NORMAL_MODE: {
                'C': {'name': 'D', 'type': CMD_TYPE_USER},
                'C2': {'name': 'D2', 'type': CMD_TYPE_USER},
                'C3': {'name': 'D3', 'type': CMD_TYPE_USER},
                'A': {'name': 'B', 'type': CMD_TYPE_USER},
            },
            OPERATOR_PENDING_MODE: {'E': {'name': 'F', 'type': CMD_TYPE_USER}},
            SELECT_MODE: {'G': {'name': 'H', 'type': CMD_TYPE_USER}},
            VISUAL_BLOCK_MODE: {
                'I': {'name': 'J', 'type': CMD_TYPE_USER},
                'I2': {'name': 'J2', 'type': CMD_TYPE_USER},
                'K': {'name': 'L', 'type': CMD_TYPE_USER},
            },
            VISUAL_LINE_MODE: {'K': {'name': 'L', 'type': CMD_TYPE_USER}},
            VISUAL_MODE: {'M': {'name': 'N', 'type': CMD_TYPE_USER}},
        })

    @_patch_mappings
    def test_add_raises_exception(self, _mappings):
        expected = _mappings.copy()
        mappings = Mappings(unittest.mock.Mock(mode=unittest.NORMAL_MODE))

        with self.assertRaises(KeyError):
            mappings.add('foobar', 'X', 'Y')

        self.assertEqual(_mappings, expected)

        # Should not raise exception (protect against false positive).
        mappings.add(unittest.INSERT_MODE, 'A', 'B')

    @_patch_mappings
    def test_can_remove(self, _mappings):
        mappings = Mappings(unittest.mock.Mock(mode=unittest.NORMAL_MODE))
        mappings.add(unittest.INSERT_MODE, 'A', 'B')
        mappings.add(unittest.INSERT_MODE, 'C', 'D')
        mappings.add(unittest.INSERT_MODE, 'E', 'F')
        mappings.add(unittest.NORMAL_MODE, 'A', 'B')
        mappings.add(unittest.NORMAL_MODE, 'C', 'D')
        mappings.add(unittest.NORMAL_MODE, 'E', 'F')
        mappings.remove(unittest.INSERT_MODE, 'C')
        mappings.remove(unittest.NORMAL_MODE, 'E')

        self.assertEquals(_mappings, {
            INSERT_MODE: {
                'A': {'name': 'B', 'type': CMD_TYPE_USER},
                'E': {'name': 'F', 'type': CMD_TYPE_USER},
            },
            NORMAL_MODE: {
                'A': {'name': 'B', 'type': CMD_TYPE_USER},
                'C': {'name': 'D', 'type': CMD_TYPE_USER},
            },
            OPERATOR_PENDING_MODE: {},
            SELECT_MODE: {},
            VISUAL_BLOCK_MODE: {},
            VISUAL_LINE_MODE: {},
            VISUAL_MODE: {},
        })

    @_patch_mappings
    def test_remove_raises_exception(self, _mappings):
        expected = _mappings.copy()
        mappings = Mappings(unittest.mock.Mock(mode=unittest.NORMAL_MODE))

        with self.assertRaises(KeyError, msg='mapping not found'):
            mappings.remove('foobar', 'foobar')

        with self.assertRaises(KeyError, msg='mapping not found'):
            mappings.remove(unittest.INSERT_MODE, 'foobar')

        mappings.add(unittest.INSERT_MODE, 'X', 'Y')

        with self.assertRaises(KeyError, msg='mapping not found'):
            mappings.remove(unittest.INSERT_MODE, 'foobar')

        # Should not raise exception (protect against false positive).
        mappings.remove(unittest.INSERT_MODE, 'X')

        self.assertEqual(_mappings, expected)

    @_patch_mappings
    @unittest.mock.patch('NeoVintageous.lib.vi.variables._DEFAULTS', {'mapleader': '\\'})
    @unittest.mock.patch('NeoVintageous.lib.vi.variables._VARIABLES', {})
    def test_add_expands_keys(self, _mappings):
        mappings = Mappings(unittest.mock.Mock(mode=unittest.NORMAL_MODE))
        mappings.add(unittest.NORMAL_MODE, '<leader>d', ':NeovintageousToggleSideBar<CR>')

        self.assertEqual(_mappings[unittest.NORMAL_MODE], {
            '\\d': {'name': ':NeovintageousToggleSideBar<CR>', 'type': CMD_TYPE_USER}
        })

    @_patch_mappings
    @unittest.mock.patch('NeoVintageous.lib.vi.variables._DEFAULTS', {'mapleader': '\\'})
    @unittest.mock.patch('NeoVintageous.lib.vi.variables._VARIABLES', {})
    def test_can_remove_expanded_keys(self, _mappings):
        mappings = Mappings(unittest.mock.Mock(mode=unittest.NORMAL_MODE))

        mappings.add(unittest.NORMAL_MODE, '<leader>d', ':NeovintageousToggleSideBar<CR>')
        mappings.remove(unittest.NORMAL_MODE, '\\d')

        self.assertEqual(_mappings[unittest.NORMAL_MODE], {})

        mappings.add(unittest.NORMAL_MODE, '<leader>d', ':NeovintageousToggleSideBar<CR>')
        mappings.remove(unittest.NORMAL_MODE, '<leader>d')

        self.assertEqual(_mappings[unittest.NORMAL_MODE], {})

    @_patch_mappings
    def test_can_clear(self, _mappings):
        mappings = Mappings(unittest.mock.Mock(mode=unittest.NORMAL_MODE))
        mappings.add(unittest.NORMAL_MODE, 'X', 'Y')
        mappings.add(unittest.INSERT_MODE, 'X', 'Y')
        mappings.add(unittest.NORMAL_MODE, 'X', 'Y')
        mappings.add(unittest.OPERATOR_PENDING_MODE, 'X', 'Y')
        mappings.add(unittest.SELECT_MODE, 'X', 'Y')
        mappings.add(unittest.VISUAL_BLOCK_MODE, 'X', 'Y')
        mappings.add(unittest.VISUAL_LINE_MODE, 'X', 'Y')
        mappings.add(unittest.VISUAL_MODE, 'X', 'Y')
        mappings.clear()

        self.assertEquals(_mappings, {
            INSERT_MODE: {},
            NORMAL_MODE: {},
            OPERATOR_PENDING_MODE: {},
            SELECT_MODE: {},
            VISUAL_BLOCK_MODE: {},
            VISUAL_LINE_MODE: {},
            VISUAL_MODE: {},
        })

    @_patch_mappings
    def test_expand_first(self, _mappings):
        mappings = Mappings(unittest.mock.Mock(mode=unittest.NORMAL_MODE))

        mappings.add(unittest.NORMAL_MODE, 'G', 'G_')
        mapping = mappings.expand_first('G')
        self.assertIsInstance(mapping, Mapping)
        self.assertEqual(mapping.head, 'G')
        self.assertEqual(mapping.mapping, 'G_')
        self.assertEqual(mapping.tail, '')
        self.assertEqual(mapping.sequence, 'G')
        self.assertEqual(mapping.status, _STATUS_COMPLETE)

        mappings.add(unittest.NORMAL_MODE, '<C-m>', 'daw')
        mapping = mappings.expand_first('<C-m>')
        self.assertIsInstance(mapping, Mapping)
        self.assertEqual(mapping.head, '<C-m>')
        self.assertEqual(mapping.mapping, 'daw')
        self.assertEqual(mapping.tail, '')
        self.assertEqual(mapping.sequence, '<C-m>')
        self.assertEqual(mapping.status, _STATUS_COMPLETE)

        mappings.add(unittest.NORMAL_MODE, '<C-m>', 'daw')
        mapping = mappings.expand_first('<C-m>x')
        self.assertIsInstance(mapping, Mapping)
        self.assertEqual(mapping.head, '<C-m>')
        self.assertEqual(mapping.mapping, 'daw')
        self.assertEqual(mapping.tail, 'x')
        self.assertEqual(mapping.sequence, '<C-m>x')
        self.assertEqual(mapping.status, _STATUS_COMPLETE)

        mappings.add(unittest.NORMAL_MODE, 'xxA', 'daw')
        mapping = mappings.expand_first('xx')
        self.assertIsInstance(mapping, Mapping)
        self.assertEqual(mapping.head, 'xx')
        self.assertEqual(mapping.mapping, '')
        self.assertEqual(mapping.tail, '')
        self.assertEqual(mapping.sequence, 'xx')
        self.assertEqual(mapping.status, _STATUS_INCOMPLETE)

    @_patch_mappings
    def test_expand_first_returns_none_when_not_found(self, _mappings):
        mappings = Mappings(unittest.mock.Mock(mode=unittest.NORMAL_MODE))
        self.assertIsNone(mappings.expand_first(''))
        self.assertIsNone(mappings.expand_first('G'))
        self.assertIsNone(mappings.expand_first('foobar'))

    @_patch_mappings
    def test_get_mapped_seqs(self, _mappings):
        mappings = Mappings(unittest.mock.Mock(mode=unittest.NORMAL_MODE))

        self.assertEqual(mappings._get_mapped_seqs(unittest.NORMAL_MODE), [])

        mappings.add(unittest.NORMAL_MODE, 'B', 'Y')
        mappings.add(unittest.NORMAL_MODE, 'C', 'Z')
        mappings.add(unittest.NORMAL_MODE, 'A', 'X')
        mappings.add(unittest.INSERT_MODE, 'J', 'K')
        mappings.add(unittest.INSERT_MODE, 'I', 'L')
        mappings.add(unittest.VISUAL_MODE, 'M', 'N')

        # Should be sorted.
        self.assertEqual(mappings._get_mapped_seqs(unittest.NORMAL_MODE), ['A', 'B', 'C'])
        self.assertEqual(mappings._get_mapped_seqs(unittest.INSERT_MODE), ['I', 'J'])
        self.assertEqual(mappings._get_mapped_seqs(unittest.VISUAL_MODE), ['M'])
        self.assertEqual(mappings._get_mapped_seqs(unittest.SELECT_MODE), [])

    @_patch_mappings
    def test_find_partial_match(self, _mappings):
        mappings = Mappings(unittest.mock.Mock(mode=unittest.NORMAL_MODE))

        self.assertEqual(mappings._find_partial_match(unittest.NORMAL_MODE, ''), [])
        self.assertEqual(mappings._find_partial_match(unittest.NORMAL_MODE, 'foobar'), [])

        mappings.add(unittest.NORMAL_MODE, 'x', 'y')

        # XXX Should this really accept empty string?
        self.assertEqual(mappings._find_partial_match(unittest.NORMAL_MODE, ''), ['x'])
        self.assertEqual(mappings._find_partial_match(unittest.NORMAL_MODE, 'x'), ['x'])

        self.assertEqual(mappings._find_partial_match(unittest.NORMAL_MODE, ' '), [])
        self.assertEqual(mappings._find_partial_match(unittest.NORMAL_MODE, 'x '), [])
        self.assertEqual(mappings._find_partial_match(unittest.NORMAL_MODE, ' x'), [])
        self.assertEqual(mappings._find_partial_match(unittest.NORMAL_MODE, 'y'), [])
        self.assertEqual(mappings._find_partial_match(unittest.NORMAL_MODE, 'xy'), [])
        self.assertEqual(mappings._find_partial_match(unittest.NORMAL_MODE, 'foobar'), [])

        mappings.add(unittest.NORMAL_MODE, 'yc', 'g')
        mappings.add(unittest.NORMAL_MODE, 'yd', 'g')
        mappings.add(unittest.NORMAL_MODE, 'ya', 'g')
        mappings.add(unittest.NORMAL_MODE, 'yb', 'g')

        # Should be case-sensitive.
        mappings.add(unittest.NORMAL_MODE, 'Y', 'g')
        mappings.add(unittest.NORMAL_MODE, 'Ya', 'g')

        # Should also be sorted.
        self.assertEqual(mappings._find_partial_match(unittest.NORMAL_MODE, 'y'),
                         ['ya', 'yb', 'yc', 'yd'])

        # XXX Should this really accept empty string?
        self.assertEqual(mappings._find_partial_match(unittest.NORMAL_MODE, ''),
                         ['Y', 'Ya', 'x', 'ya', 'yb', 'yc', 'yd'])

        self.assertEqual(mappings._find_partial_match(unittest.NORMAL_MODE, 'yd'), ['yd'])
        self.assertEqual(mappings._find_partial_match(unittest.NORMAL_MODE, 'x'), ['x'])

    @_patch_mappings
    def test_find_full_match(self, _mappings):
        mappings = Mappings(unittest.mock.Mock(mode=unittest.NORMAL_MODE))

        self.assertEqual(mappings._find_full_match(unittest.NORMAL_MODE, ''), (None, None))
        self.assertEqual(mappings._find_full_match(unittest.NORMAL_MODE, 'foobar'), (None, None))

        mappings.add(unittest.NORMAL_MODE, 'xc', 'y')
        mappings.add(unittest.NORMAL_MODE, 'xd', 'abc')
        mappings.add(unittest.NORMAL_MODE, 'xa', 'y')
        mappings.add(unittest.NORMAL_MODE, 'xb', 'y')

        self.assertEqual(mappings._find_full_match(unittest.NORMAL_MODE, ''), (None, None))
        self.assertEqual(mappings._find_full_match(unittest.NORMAL_MODE, ' '), (None, None))
        self.assertEqual(mappings._find_full_match(unittest.NORMAL_MODE, 'foobar'), (None, None))
        self.assertEqual(mappings._find_full_match(unittest.NORMAL_MODE, 'x'), (None, None))
        self.assertEqual(mappings._find_full_match(unittest.NORMAL_MODE, 'xdd'), (None, None))
        self.assertEqual(mappings._find_full_match(unittest.NORMAL_MODE, 'xd '), (None, None))
        self.assertEqual(mappings._find_full_match(unittest.NORMAL_MODE, ' xd'), (None, None))

        self.assertEqual(mappings._find_full_match(unittest.NORMAL_MODE, 'xd'),
                         ('xd', {'name': 'abc', 'type': CMD_TYPE_USER}))

        self.assertEqual(mappings._find_full_match(unittest.NORMAL_MODE, 'xd'),
                         ('xd', {'name': 'abc', 'type': CMD_TYPE_USER}))

        self.assertEqual(mappings._find_full_match(unittest.NORMAL_MODE, 'xd'),
                         ('xd', {'name': 'abc', 'type': CMD_TYPE_USER}))

        self.assertEqual(mappings._find_full_match(unittest.NORMAL_MODE, 'xd'),
                         ('xd', {'name': 'abc', 'type': CMD_TYPE_USER}))

        mappings.add(unittest.NORMAL_MODE, 'bbc', 'y')
        mappings.add(unittest.NORMAL_MODE, 'bbd', 'y')
        mappings.add(unittest.NORMAL_MODE, 'bbb', 'cde')
        mappings.add(unittest.NORMAL_MODE, 'bba', 'y')

        self.assertEqual(mappings._find_full_match(unittest.NORMAL_MODE, ''), (None, None))
        self.assertEqual(mappings._find_full_match(unittest.NORMAL_MODE, 'b'), (None, None))
        self.assertEqual(mappings._find_full_match(unittest.NORMAL_MODE, 'bb'), (None, None))
        self.assertEqual(mappings._find_full_match(unittest.NORMAL_MODE, 'bbb'),
                         ('bbb', {'name': 'cde', 'type': CMD_TYPE_USER}))

    @_patch_mappings
    def test_incomplete_user_mapping(self, _mappings):

        mappings = Mappings(unittest.mock.Mock(mode=unittest.NORMAL_MODE, partial_sequence='a'))
        mappings.add(unittest.NORMAL_MODE, 'aa', 'y')
        self.assertEqual(mappings.incomplete_user_mapping(), True)

        mappings = Mappings(unittest.mock.Mock(mode=unittest.NORMAL_MODE, partial_sequence='b'))
        mappings.add(unittest.NORMAL_MODE, 'b', 'y')
        self.assertFalse(mappings.incomplete_user_mapping())

        mappings = Mappings(unittest.mock.Mock(mode=unittest.NORMAL_MODE, partial_sequence='c'))
        mappings.add(unittest.NORMAL_MODE, 'c', 'y')
        mappings.add(unittest.NORMAL_MODE, 'cc', 'y')
        self.assertFalse(mappings.incomplete_user_mapping())

        mappings = Mappings(unittest.mock.Mock(mode=unittest.NORMAL_MODE, partial_sequence='dd'))
        mappings.add(unittest.NORMAL_MODE, 'd', 'y')
        mappings.add(unittest.NORMAL_MODE, 'ddd', 'y')
        self.assertEquals(mappings.incomplete_user_mapping(), True)
