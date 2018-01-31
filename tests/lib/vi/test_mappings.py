from NeoVintageous.tests import unittest

from NeoVintageous.lib.vi.mappings import CMD_TYPE_USER
from NeoVintageous.lib.vi.mappings import INSERT
from NeoVintageous.lib.vi.mappings import Mapping
from NeoVintageous.lib.vi.mappings import _STATUS_COMPLETE
from NeoVintageous.lib.vi.mappings import _STATUS_INCOMPLETE
from NeoVintageous.lib.vi.mappings import Mappings
from NeoVintageous.lib.vi.mappings import NORMAL
from NeoVintageous.lib.vi.mappings import OPERATOR_PENDING
from NeoVintageous.lib.vi.mappings import SELECT
from NeoVintageous.lib.vi.mappings import VISUAL_BLOCK
from NeoVintageous.lib.vi.mappings import VISUAL_LINE
from NeoVintageous.lib.vi.mappings import VISUAL


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
        mappings = Mappings(unittest.mock.Mock(mode=unittest.NORMAL))
        mappings.add(unittest.INSERT, 'A', 'B')
        mappings.add(unittest.NORMAL, 'C', 'D')
        mappings.add(unittest.NORMAL, 'C2', 'D2')
        mappings.add(unittest.NORMAL, 'C3', 'D3')
        mappings.add(unittest.NORMAL, 'A', 'B')
        mappings.add(unittest.OPERATOR_PENDING, 'E', 'F')
        mappings.add(unittest.SELECT, 'G', 'H')
        mappings.add(unittest.VISUAL_BLOCK, 'I', 'J')
        mappings.add(unittest.VISUAL_BLOCK, 'I2', 'J2')
        mappings.add(unittest.VISUAL_BLOCK, 'K', 'L')
        mappings.add(unittest.VISUAL_LINE, 'K', 'L')
        mappings.add(unittest.VISUAL, 'M', 'N')

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
        mappings = Mappings(unittest.mock.Mock(mode=unittest.NORMAL))

        with self.assertRaises(KeyError):
            mappings.add('foobar', 'X', 'Y')

        self.assertEqual(_mappings, expected)

        # Should not raise exception (protect against false positive).
        mappings.add(unittest.INSERT, 'A', 'B')

    @_patch_mappings
    def test_can_remove(self, _mappings):
        mappings = Mappings(unittest.mock.Mock(mode=unittest.NORMAL))
        mappings.add(unittest.INSERT, 'A', 'B')
        mappings.add(unittest.INSERT, 'C', 'D')
        mappings.add(unittest.INSERT, 'E', 'F')
        mappings.add(unittest.NORMAL, 'A', 'B')
        mappings.add(unittest.NORMAL, 'C', 'D')
        mappings.add(unittest.NORMAL, 'E', 'F')
        mappings.remove(unittest.INSERT, 'C')
        mappings.remove(unittest.NORMAL, 'E')

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
        mappings = Mappings(unittest.mock.Mock(mode=unittest.NORMAL))

        with self.assertRaises(KeyError, msg='mapping not found'):
            mappings.remove('foobar', 'foobar')

        with self.assertRaises(KeyError, msg='mapping not found'):
            mappings.remove(unittest.INSERT, 'foobar')

        mappings.add(unittest.INSERT, 'X', 'Y')

        with self.assertRaises(KeyError, msg='mapping not found'):
            mappings.remove(unittest.INSERT, 'foobar')

        # Should not raise exception (protect against false positive).
        mappings.remove(unittest.INSERT, 'X')

        self.assertEqual(_mappings, expected)

    @_patch_mappings
    @unittest.mock.patch('NeoVintageous.lib.vi.variables._DEFAULTS', {'mapleader': '\\'})
    @unittest.mock.patch('NeoVintageous.lib.vi.variables._VARIABLES', {})
    def test_add_expands_keys(self, _mappings):
        mappings = Mappings(unittest.mock.Mock(mode=unittest.NORMAL))
        mappings.add(unittest.NORMAL, '<leader>d', ':NeovintageousToggleSideBar<CR>')

        self.assertEqual(_mappings[unittest.NORMAL], {
            '\\d': {'name': ':NeovintageousToggleSideBar<CR>', 'type': CMD_TYPE_USER}
        })

    @_patch_mappings
    @unittest.mock.patch('NeoVintageous.lib.vi.variables._DEFAULTS', {'mapleader': '\\'})
    @unittest.mock.patch('NeoVintageous.lib.vi.variables._VARIABLES', {})
    def test_can_remove_expanded_keys(self, _mappings):
        mappings = Mappings(unittest.mock.Mock(mode=unittest.NORMAL))

        mappings.add(unittest.NORMAL, '<leader>d', ':NeovintageousToggleSideBar<CR>')
        mappings.remove(unittest.NORMAL, '\\d')

        self.assertEqual(_mappings[unittest.NORMAL], {})

        mappings.add(unittest.NORMAL, '<leader>d', ':NeovintageousToggleSideBar<CR>')
        mappings.remove(unittest.NORMAL, '<leader>d')

        self.assertEqual(_mappings[unittest.NORMAL], {})

    @_patch_mappings
    def test_can_clear(self, _mappings):
        mappings = Mappings(unittest.mock.Mock(mode=unittest.NORMAL))
        mappings.add(unittest.NORMAL, 'X', 'Y')
        mappings.add(unittest.INSERT, 'X', 'Y')
        mappings.add(unittest.NORMAL, 'X', 'Y')
        mappings.add(unittest.OPERATOR_PENDING, 'X', 'Y')
        mappings.add(unittest.SELECT, 'X', 'Y')
        mappings.add(unittest.VISUAL_BLOCK, 'X', 'Y')
        mappings.add(unittest.VISUAL_LINE, 'X', 'Y')
        mappings.add(unittest.VISUAL, 'X', 'Y')
        mappings.clear()

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
        mappings = Mappings(unittest.mock.Mock(mode=unittest.NORMAL))

        mappings.add(unittest.NORMAL, 'G', 'G_')
        mapping = mappings.expand_first('G')
        self.assertIsInstance(mapping, Mapping)
        self.assertEqual(mapping.head, 'G')
        self.assertEqual(mapping.mapping, 'G_')
        self.assertEqual(mapping.tail, '')
        self.assertEqual(mapping.sequence, 'G')
        self.assertEqual(mapping.status, _STATUS_COMPLETE)

        mappings.add(unittest.NORMAL, '<C-m>', 'daw')
        mapping = mappings.expand_first('<C-m>')
        self.assertIsInstance(mapping, Mapping)
        self.assertEqual(mapping.head, '<C-m>')
        self.assertEqual(mapping.mapping, 'daw')
        self.assertEqual(mapping.tail, '')
        self.assertEqual(mapping.sequence, '<C-m>')
        self.assertEqual(mapping.status, _STATUS_COMPLETE)

        mappings.add(unittest.NORMAL, '<C-m>', 'daw')
        mapping = mappings.expand_first('<C-m>x')
        self.assertIsInstance(mapping, Mapping)
        self.assertEqual(mapping.head, '<C-m>')
        self.assertEqual(mapping.mapping, 'daw')
        self.assertEqual(mapping.tail, 'x')
        self.assertEqual(mapping.sequence, '<C-m>x')
        self.assertEqual(mapping.status, _STATUS_COMPLETE)

        mappings.add(unittest.NORMAL, 'xxA', 'daw')
        mapping = mappings.expand_first('xx')
        self.assertIsInstance(mapping, Mapping)
        self.assertEqual(mapping.head, 'xx')
        self.assertEqual(mapping.mapping, '')
        self.assertEqual(mapping.tail, '')
        self.assertEqual(mapping.sequence, 'xx')
        self.assertEqual(mapping.status, _STATUS_INCOMPLETE)

    @_patch_mappings
    def test_expand_first_returns_none_when_not_found(self, _mappings):
        mappings = Mappings(unittest.mock.Mock(mode=unittest.NORMAL))
        self.assertIsNone(mappings.expand_first(''))
        self.assertIsNone(mappings.expand_first('G'))
        self.assertIsNone(mappings.expand_first('foobar'))

    @_patch_mappings
    def test_get_mapped_seqs(self, _mappings):
        mappings = Mappings(unittest.mock.Mock(mode=unittest.NORMAL))

        self.assertEqual(mappings._get_mapped_seqs(unittest.NORMAL), [])

        mappings.add(unittest.NORMAL, 'B', 'Y')
        mappings.add(unittest.NORMAL, 'C', 'Z')
        mappings.add(unittest.NORMAL, 'A', 'X')
        mappings.add(unittest.INSERT, 'J', 'K')
        mappings.add(unittest.INSERT, 'I', 'L')
        mappings.add(unittest.VISUAL, 'M', 'N')

        # Should be sorted.
        self.assertEqual(mappings._get_mapped_seqs(unittest.NORMAL), ['A', 'B', 'C'])
        self.assertEqual(mappings._get_mapped_seqs(unittest.INSERT), ['I', 'J'])
        self.assertEqual(mappings._get_mapped_seqs(unittest.VISUAL), ['M'])
        self.assertEqual(mappings._get_mapped_seqs(unittest.SELECT), [])

    @_patch_mappings
    def test_find_partial_match(self, _mappings):
        mappings = Mappings(unittest.mock.Mock(mode=unittest.NORMAL))

        self.assertEqual(mappings._find_partial_match(unittest.NORMAL, ''), [])
        self.assertEqual(mappings._find_partial_match(unittest.NORMAL, 'foobar'), [])

        mappings.add(unittest.NORMAL, 'x', 'y')

        # XXX Should this really accept empty string?
        self.assertEqual(mappings._find_partial_match(unittest.NORMAL, ''), ['x'])
        self.assertEqual(mappings._find_partial_match(unittest.NORMAL, 'x'), ['x'])

        self.assertEqual(mappings._find_partial_match(unittest.NORMAL, ' '), [])
        self.assertEqual(mappings._find_partial_match(unittest.NORMAL, 'x '), [])
        self.assertEqual(mappings._find_partial_match(unittest.NORMAL, ' x'), [])
        self.assertEqual(mappings._find_partial_match(unittest.NORMAL, 'y'), [])
        self.assertEqual(mappings._find_partial_match(unittest.NORMAL, 'xy'), [])
        self.assertEqual(mappings._find_partial_match(unittest.NORMAL, 'foobar'), [])

        mappings.add(unittest.NORMAL, 'yc', 'g')
        mappings.add(unittest.NORMAL, 'yd', 'g')
        mappings.add(unittest.NORMAL, 'ya', 'g')
        mappings.add(unittest.NORMAL, 'yb', 'g')

        # Should be case-sensitive.
        mappings.add(unittest.NORMAL, 'Y', 'g')
        mappings.add(unittest.NORMAL, 'Ya', 'g')

        # Should also be sorted.
        self.assertEqual(mappings._find_partial_match(unittest.NORMAL, 'y'),
                         ['ya', 'yb', 'yc', 'yd'])

        # XXX Should this really accept empty string?
        self.assertEqual(mappings._find_partial_match(unittest.NORMAL, ''),
                         ['Y', 'Ya', 'x', 'ya', 'yb', 'yc', 'yd'])

        self.assertEqual(mappings._find_partial_match(unittest.NORMAL, 'yd'), ['yd'])
        self.assertEqual(mappings._find_partial_match(unittest.NORMAL, 'x'), ['x'])

    @_patch_mappings
    def test_find_full_match(self, _mappings):
        mappings = Mappings(unittest.mock.Mock(mode=unittest.NORMAL))

        self.assertEqual(mappings._find_full_match(unittest.NORMAL, ''), (None, None))
        self.assertEqual(mappings._find_full_match(unittest.NORMAL, 'foobar'), (None, None))

        mappings.add(unittest.NORMAL, 'xc', 'y')
        mappings.add(unittest.NORMAL, 'xd', 'abc')
        mappings.add(unittest.NORMAL, 'xa', 'y')
        mappings.add(unittest.NORMAL, 'xb', 'y')

        self.assertEqual(mappings._find_full_match(unittest.NORMAL, ''), (None, None))
        self.assertEqual(mappings._find_full_match(unittest.NORMAL, ' '), (None, None))
        self.assertEqual(mappings._find_full_match(unittest.NORMAL, 'foobar'), (None, None))
        self.assertEqual(mappings._find_full_match(unittest.NORMAL, 'x'), (None, None))
        self.assertEqual(mappings._find_full_match(unittest.NORMAL, 'xdd'), (None, None))
        self.assertEqual(mappings._find_full_match(unittest.NORMAL, 'xd '), (None, None))
        self.assertEqual(mappings._find_full_match(unittest.NORMAL, ' xd'), (None, None))

        self.assertEqual(mappings._find_full_match(unittest.NORMAL, 'xd'),
                         ('xd', {'name': 'abc', 'type': CMD_TYPE_USER}))

        self.assertEqual(mappings._find_full_match(unittest.NORMAL, 'xd'),
                         ('xd', {'name': 'abc', 'type': CMD_TYPE_USER}))

        self.assertEqual(mappings._find_full_match(unittest.NORMAL, 'xd'),
                         ('xd', {'name': 'abc', 'type': CMD_TYPE_USER}))

        self.assertEqual(mappings._find_full_match(unittest.NORMAL, 'xd'),
                         ('xd', {'name': 'abc', 'type': CMD_TYPE_USER}))

        mappings.add(unittest.NORMAL, 'bbc', 'y')
        mappings.add(unittest.NORMAL, 'bbd', 'y')
        mappings.add(unittest.NORMAL, 'bbb', 'cde')
        mappings.add(unittest.NORMAL, 'bba', 'y')

        self.assertEqual(mappings._find_full_match(unittest.NORMAL, ''), (None, None))
        self.assertEqual(mappings._find_full_match(unittest.NORMAL, 'b'), (None, None))
        self.assertEqual(mappings._find_full_match(unittest.NORMAL, 'bb'), (None, None))
        self.assertEqual(mappings._find_full_match(unittest.NORMAL, 'bbb'),
                         ('bbb', {'name': 'cde', 'type': CMD_TYPE_USER}))

    @_patch_mappings
    def test_incomplete_user_mapping(self, _mappings):

        mappings = Mappings(unittest.mock.Mock(mode=unittest.NORMAL, partial_sequence='a'))
        mappings.add(unittest.NORMAL, 'aa', 'y')
        self.assertEqual(mappings.incomplete_user_mapping(), True)

        mappings = Mappings(unittest.mock.Mock(mode=unittest.NORMAL, partial_sequence='b'))
        mappings.add(unittest.NORMAL, 'b', 'y')
        self.assertFalse(mappings.incomplete_user_mapping())

        mappings = Mappings(unittest.mock.Mock(mode=unittest.NORMAL, partial_sequence='c'))
        mappings.add(unittest.NORMAL, 'c', 'y')
        mappings.add(unittest.NORMAL, 'cc', 'y')
        self.assertFalse(mappings.incomplete_user_mapping())

        mappings = Mappings(unittest.mock.Mock(mode=unittest.NORMAL, partial_sequence='dd'))
        mappings.add(unittest.NORMAL, 'd', 'y')
        mappings.add(unittest.NORMAL, 'ddd', 'y')
        self.assertEquals(mappings.incomplete_user_mapping(), True)
