from NeoVintageous.tests import unittest

from NeoVintageous.lib.vi.mappings import Mappings
from NeoVintageous.lib.vi.mappings import _mappings
from NeoVintageous.lib.vi.mappings import mapping_status
from NeoVintageous.lib.vi.cmd_base import cmd_types


_ADDING_TESTS = (
    (unittest.NORMAL_MODE, 'G', 'G_', 'adding to normal mode'),
    (unittest.VISUAL_MODE, 'G', 'G_', 'adding to visual mode'),
    (unittest.OPERATOR_PENDING_MODE, 'G', 'G_', 'adding to operator pending mode'),
    (unittest.VISUAL_LINE_MODE, 'G', 'G_', 'adding to visual line mode'),
    (unittest.VISUAL_BLOCK_MODE, 'G', 'G_', 'adding to visual block mode'),
)


class Test_Mappings_AddingAndRemoving(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        self.mappings = Mappings(self.state)
        self.mappings.clear()

    def test_can_add(self):
        for (i, data) in enumerate(_ADDING_TESTS):
            mode, keys, target, msg = data
            self.mappings.add(mode, keys, target)
            self.assertEqual(
                _mappings[mode][keys],
                {'name': target, 'type': cmd_types.USER},
                '{0} [{1}] failed'.format(msg, i)
            )
            self.mappings.clear()

    def test_can_remove(self):
        for (i, data) in enumerate(_ADDING_TESTS):
            mode, keys, target, msg = data
            self.mappings.add(mode, keys, target)
            self.mappings.remove(mode, keys)

        self.assertFalse(_mappings[unittest.NORMAL_MODE])
        self.assertFalse(_mappings[unittest.VISUAL_MODE])
        self.assertFalse(_mappings[unittest.VISUAL_LINE_MODE])
        self.assertFalse(_mappings[unittest.VISUAL_BLOCK_MODE])


_EXPANDING_TESTS = (
    ((unittest.NORMAL_MODE, 'G', 'G_'), ('G', 'G', 'G_', '', 'G', mapping_status.COMPLETE)),
    ((unittest.NORMAL_MODE, '<C-m>', 'daw'), ('<C-m>', '<C-m>', 'daw', '', '<C-m>', mapping_status.COMPLETE)),
    ((unittest.NORMAL_MODE, '<C-m>', 'daw'), ('<C-m>x', '<C-m>', 'daw', 'x', '<C-m>x', mapping_status.COMPLETE)),  # noqa: E501
    ((unittest.NORMAL_MODE, 'xxA', 'daw'), ('xx', 'xx', '', '', 'xx', mapping_status.INCOMPLETE)),
)


class Test_Mapping_Expanding(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        self.mappings = Mappings(self.state)
        self.mappings.clear()

    def test_can_expand(self):
        for (i, data) in enumerate(_EXPANDING_TESTS):
            setup_data, test_data = data

            mode, keys, new_mapping = setup_data
            self.mappings.add(mode, keys, new_mapping)

            self.state.mode = unittest.NORMAL_MODE

            seq, expected_head, expected_mapping, expected_tail, expected_full, expected_status = test_data
            result = self.mappings.expand_first(seq)

            self.assertEqual(result.head, expected_head, '[{0}] head failed'.format(i))
            self.assertEqual(result.tail, expected_tail, '[{0}] tail failed'.format(i))
            self.assertEqual(result.mapping, expected_mapping, '[{0}] mapping failed'.format(i))
            self.assertEqual(result.sequence, expected_full, '[{0}] sequence failed'.format(i))
            self.assertEqual(result.status, expected_status, '[{0}] status failed'.format(i))

            self.mappings.clear()
