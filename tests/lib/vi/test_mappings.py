from NeoVintageous.tests.utils import ViewTestCase

from NeoVintageous.lib.vi.mappings import Mappings
from NeoVintageous.lib.vi.mappings import _mappings
from NeoVintageous.lib.vi.mappings import mapping_status
from NeoVintageous.lib.vi.cmd_base import cmd_types


_ADDING_TESTS = (
    (ViewTestCase.modes.NORMAL, 'G', 'G_', 'adding to normal mode'),
    (ViewTestCase.modes.VISUAL, 'G', 'G_', 'adding to visual mode'),
    (ViewTestCase.modes.OPERATOR_PENDING, 'G', 'G_', 'adding to operator pending mode'),
    (ViewTestCase.modes.VISUAL_LINE, 'G', 'G_', 'adding to visual line mode'),
    (ViewTestCase.modes.VISUAL_BLOCK, 'G', 'G_', 'adding to visual block mode'),
)


class Test_Mappings_AddingAndRemoving(ViewTestCase):

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

        self.assertFalse(_mappings[ViewTestCase.modes.NORMAL])
        self.assertFalse(_mappings[ViewTestCase.modes.VISUAL])
        self.assertFalse(_mappings[ViewTestCase.modes.VISUAL_LINE])
        self.assertFalse(_mappings[ViewTestCase.modes.VISUAL_BLOCK])


_EXPANDING_TESTS = (
    ((ViewTestCase.modes.NORMAL, 'G', 'G_'), ('G', 'G', 'G_', '', 'G', mapping_status.COMPLETE)),
    ((ViewTestCase.modes.NORMAL, '<C-m>', 'daw'), ('<C-m>', '<C-m>', 'daw', '', '<C-m>', mapping_status.COMPLETE)),
    ((ViewTestCase.modes.NORMAL, '<C-m>', 'daw'), ('<C-m>x', '<C-m>', 'daw', 'x', '<C-m>x', mapping_status.COMPLETE)),
    ((ViewTestCase.modes.NORMAL, 'xxA', 'daw'), ('xx', 'xx', '', '', 'xx', mapping_status.INCOMPLETE)),
)


class Test_Mapping_Expanding(ViewTestCase):

    def setUp(self):
        super().setUp()
        self.mappings = Mappings(self.state)
        self.mappings.clear()

    def test_can_expand(self):
        for (i, data) in enumerate(_EXPANDING_TESTS):
            setup_data, test_data = data

            mode, keys, new_mapping = setup_data
            self.mappings.add(mode, keys, new_mapping)

            self.state.mode = ViewTestCase.modes.NORMAL

            seq, expected_head, expected_mapping, expected_tail, expected_full, expected_status = test_data
            result = self.mappings.expand_first(seq)

            self.assertEqual(result.head, expected_head, '[{0}] head failed'.format(i))
            self.assertEqual(result.tail, expected_tail, '[{0}] tail failed'.format(i))
            self.assertEqual(result.mapping, expected_mapping, '[{0}] mapping failed'.format(i))
            self.assertEqual(result.sequence, expected_full, '[{0}] sequence failed'.format(i))
            self.assertEqual(result.status, expected_status, '[{0}] status failed'.format(i))

            self.mappings.clear()
