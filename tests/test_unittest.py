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

from sublime import Region
from sublime import Settings

from NeoVintageous.nv.settings import set_mode
from NeoVintageous.nv.vim import DIRECTION_DOWN
from NeoVintageous.tests import unittest


class TestViewTestCase(unittest.ViewTestCase):

    def test_content(self):
        self.view.run_command('insert', {'characters': 'hello world'})
        self.assertEqual('hello world', self.content())

    def test_region(self):
        self.assertEqual(self.Region(3), Region(3))
        self.assertEqual(self.Region(3, 5), Region(3, 5))

    def test_select(self):
        self.view.run_command('insert', {'characters': 'another brick in the wall'})

        # Int.
        self.select(3)
        self.assertEqual([Region(3)], list(self.view.sel()))
        self.select(5)
        self.assertEqual([Region(5)], list(self.view.sel()))

        # Tuple.
        self.select((3, 5))
        self.assertEqual([Region(3, 5)], list(self.view.sel()))
        self.select((7, 11))
        self.assertEqual([Region(7, 11)], list(self.view.sel()))

        # Region.
        self.select(Region(3, 5))
        self.assertEqual([Region(3, 5)], list(self.view.sel()))
        self.select(Region(7, 11))
        self.assertEqual([Region(7, 11)], list(self.view.sel()))

        # Ints.
        self.select([3])
        self.assertEqual([Region(3)], list(self.view.sel()))
        self.select([5, 7])
        self.assertEqual([Region(5), Region(7)], list(self.view.sel()))

        # Tuples.
        self.select([(3, 5)])
        self.assertEqual([Region(3, 5)], list(self.view.sel()))
        self.select([(7, 11), (13, 17)])
        self.assertEqual([Region(7, 11), Region(13, 17)], list(self.view.sel()))

        # Regions.
        self.select([Region(3, 5)])
        self.assertEqual([Region(3, 5)], list(self.view.sel()))
        self.select([Region(7, 11), Region(13, 17)])
        self.assertEqual([Region(7, 11), Region(13, 17)], list(self.view.sel()))

        # Misc.
        self.select([3, (11, 13), Region(5, 7)])
        self.assertEqual([Region(3), Region(5, 7), Region(11, 13)], list(self.view.sel()))

    def test_settings(self):
        self.assertIsInstance(self.settings(), Settings)

    def test_write(self):
        self.write('Hello world!')
        self.assertEqual('Hello world!', self.view.substr(Region(0, self.view.size())))
        self.assertEqual([Region(12)], list(self.view.sel()))

    def test_normal_default_selection_is_eof(self):
        self.normal('Hello world!')
        self.assertEqual('Hello world!', self.view.substr(Region(0, self.view.size())))
        self.assertEqual([Region(12)], list(self.view.sel()))

    def test_normal_is_normal_mode(self):
        self.normal('Hello world!')
        self.assertNormalMode()

    def test_normal_erases_view_before_insert(self):
        self.normal('foobar')
        self.normal('a')
        self.assertEqual('a', self.view.substr(Region(0, self.view.size())))
        self.normal('b')
        self.assertEqual('b', self.view.substr(Region(0, self.view.size())))

    def test_normal_zero_pos_selection(self):
        self.normal('|hello world!')
        self.assertEqual([Region(0)], list(self.view.sel()))

    def test_normal_middle_pos_selection(self):
        self.normal('hello| world!')
        self.assertEqual([Region(5)], list(self.view.sel()))

    def test_normal_end_pos_selection(self):
        self.normal('hello world|!')
        self.assertEqual([Region(11)], list(self.view.sel()))

    def test_normal_multiple_selections(self):
        self.normal('h|el|lo world!')
        self.assertEqual([Region(1), Region(3)], list(self.view.sel()))
        self.normal('hell|o |wo|rld!')
        self.assertEqual([Region(4), Region(6), Region(8)], list(self.view.sel()))
        self.normal('hel|lo| w|orld|!')
        self.assertEqual([Region(3), Region(5), Region(7), Region(11)], list(self.view.sel()))

    def test_insert(self):
        self.insert('t|ext')
        self.assertEqual('text', self.view.substr(Region(0, self.view.size())))
        self.assertEqual([Region(1)], list(self.view.sel()))
        self.assertInsertMode()

    def test_internal_normal(self):
        self.internalNormal('hel|lo wo|rld!')
        self.assertEqual([Region(3, 8)], list(self.view.sel()))
        self.assertInternalNormalMode()

    def test_internal_normal_reversed(self):
        self.rinternalNormal('hel|lo wo|rld!')
        self.assertEqual([Region(8, 3)], list(self.view.sel()))
        self.assertInternalNormalMode()

    def test_internal_normal_zero_pos(self):
        self.internalNormal('|hello world!')
        self.assertEqual([Region(0, 1)], list(self.view.sel()))
        self.assertInternalNormalMode()

    def test_internal_normal_multiple_selections(self):
        self.internalNormal('h|el|lo w|orl|d!')
        self.assertEqual([Region(1, 3), Region(7, 10)], list(self.view.sel()))
        self.assertInternalNormalMode()

    def test_visual(self):
        self.visual('t|ex|t')
        self.assertEqual('text', self.view.substr(Region(0, self.view.size())))
        self.assertEqual([Region(1, 3)], list(self.view.sel()))
        self.assertVisualMode()

    def test_visual_single_selection_expands_one_character(self):
        self.visual('t|ext')
        self.assertEqual('text', self.view.substr(Region(0, self.view.size())))
        self.assertEqual([Region(1, 2)], list(self.view.sel()))
        self.assertVisualMode()

    def test_visual_multiple_selection(self):
        self.visual('h|ell|o |worl|d')
        self.assertEqual([Region(1, 4), Region(6, 10)], list(self.view.sel()))
        self.assertVisualMode()

    def test_visual_raises_exception_if_malformed_visual_selection(self):
        with self.assertRaisesRegex(Exception, 'invalid visual selection'):
            self.visual('hello world!')
        with self.assertRaisesRegex(Exception, 'invalid visual selection'):
            self.visual('h|e|l|lo world!')
        with self.assertRaisesRegex(Exception, 'invalid visual selection'):
            self.visual('h|e|l|lo |w|orld!')

    def test_vselect(self):
        self.vselect('t|ex|t')
        self.assertEqual('text', self.view.substr(Region(0, self.view.size())))
        self.assertEqual([Region(1, 3)], list(self.view.sel()))
        self.assertSelectMode()

    def test_rvselect(self):
        self.rvselect('t|ex|t')
        self.assertEqual('text', self.view.substr(Region(0, self.view.size())))
        self.assertEqual([Region(3, 1)], list(self.view.sel()))
        self.assertSelectMode()

    def test_vline_sets_vline_mode(self):
        self.vline('x|text\n|y')
        self.assertVlineMode()

    def test_vblock(self):
        self.vblock('xf|iz|zy\nxb|uz|zy\n')
        self.assertEqual([Region(2, 4), Region(9, 11)], list(self.view.sel()))
        self.assertVblockMode()

    def test_vblock_reversed(self):
        self.rvblock('xf|iz|zy\nxb|uz|zy\n')
        self.assertEqual([Region(4, 2), Region(11, 9)], list(self.view.sel()))
        self.assertVblockMode()

    def test_rvisual_selection_is_reversed(self):
        self.rvisual('t|ex|t fooo')
        self.assertEqual([Region(3, 1)], list(self.view.sel()))
        self.rvisual('t|ex|t f|oo|o')
        self.assertEqual([Region(3, 1), Region(8, 6)], list(self.view.sel()))

    def test_rvline_selection_is_reversed(self):
        self.rvline('x\n|ab\n|y')
        self.assertEqual([Region(5, 2)], list(self.view.sel()))
        self.rvline('x\n|a\n|y\n|b\n|z')
        self.assertEqual([Region(4, 2), Region(8, 6)], list(self.view.sel()))

    def test_assertNormal(self):
        self.view.run_command('insert', {'characters': 'hello world'})
        set_mode(self.view, unittest.NORMAL)

        self.view.sel().clear()
        self.assertNormal('hello world')

        self.view.sel().add(0)
        self.assertNormal('|hello world')

        with self.assertRaises(AssertionError):
            self.assertNormal('hello world')

        self.view.sel().add(4)
        self.assertNormal('|hell|o world')

        self.view.sel().clear()
        self.view.sel().add(6)
        self.assertNormal('hello |world')

        with self.assertRaises(AssertionError):
            self.assertNormal('hello world')

        with self.assertRaises(AssertionError):
            self.assertNormal('hello| world')

        with self.assertRaises(AssertionError):
            self.assertNormal('hello world|')

        self.view.sel().clear()
        self.view.sel().add(3)
        self.view.sel().add(5)
        self.view.sel().add(7)
        self.assertNormal('hel|lo| w|orld')

    def test_assertNormal_asserts_normal_mode(self):
        self.view.run_command('insert', {'characters': 'hello world'})
        set_mode(self.view, unittest.VISUAL)
        with self.assertRaises(AssertionError):
            self.assertNormal('hello world|')
        set_mode(self.view, unittest.NORMAL)
        self.assertNormal('hello world|')

    def test_assertInsert(self):
        self.view.run_command('insert', {'characters': 'hello world'})
        set_mode(self.view, unittest.INSERT)

        self.view.sel().clear()
        self.assertInsert('hello world')

        self.view.sel().clear()
        self.view.sel().add(3)
        self.view.sel().add(5)
        self.view.sel().add(7)
        self.assertInsert('hel|lo| w|orld')

    def test_assertInsert_asserts_insert_mode(self):
        self.view.run_command('insert', {'characters': 'hello world'})
        set_mode(self.view, unittest.NORMAL)
        with self.assertRaises(AssertionError):
            self.assertInsert('hello world|')
        set_mode(self.view, unittest.INSERT)
        self.assertInsert('hello world|')

    def test_assertVisual(self):
        self.view.run_command('insert', {'characters': 'hello world'})
        set_mode(self.view, unittest.VISUAL)

        self.view.sel().clear()
        self.assertVisual('hello world')

        self.view.sel().add(Region(3, 5))
        self.assertVisual('hel|lo| world')

        with self.assertRaises(AssertionError):
            self.assertVisual('|hello| world')

        self.view.sel().add(Region(3, 5))
        self.view.sel().add(Region(7, 11))
        self.assertVisual('hel|lo| w|orld|')

    def test_assertVisual_asserts_visual_mode(self):
        self.view.run_command('insert', {'characters': 'hello world'})
        self.view.sel().clear()
        self.view.sel().add(3)
        self.view.sel().add(5)
        set_mode(self.view, unittest.NORMAL)
        with self.assertRaises(AssertionError):
            self.assertVisual('hel|lo| world')
        set_mode(self.view, unittest.VISUAL)
        self.assertVisual('hel|lo| world')

    def test_assertVline_asserts_vline_mode(self):
        self.view.run_command('insert', {'characters': 'hello world'})
        self.view.sel().clear()
        self.view.sel().add(0)
        self.view.sel().add(11)
        set_mode(self.view, unittest.NORMAL)
        with self.assertRaises(AssertionError):
            self.assertVline('|hello world|')
        set_mode(self.view, unittest.VISUAL_LINE)
        self.assertVline('|hello world|')

    def test_assertVBlock_asserts_vblock_mode(self):
        self.view.run_command('insert', {'characters': 'hello world'})
        self.view.sel().clear()
        self.view.sel().add(0)
        self.view.sel().add(11)
        set_mode(self.view, unittest.NORMAL)
        with self.assertRaises(AssertionError):
            self.assertVblock('|hello world|')
        set_mode(self.view, unittest.VISUAL_BLOCK)
        self.assertVblock('|hello world|')

    def test_assert_content(self):
        self.view.run_command('insert', {'characters': 'hello world'})

        self.assertContent('hello world')

        with self.assertRaises(AssertionError):
            self.assertContent('foobar')

    def test_assert_content_regex(self):
        self.view.run_command('insert', {'characters': 'hello world'})

        self.assertContentRegex('hello world', 'foo msg')

        with self.assertRaises(AssertionError, msg='foo msg'):
            self.assertContentRegex('foobar', 'foo msg')

    def test_assert_region(self):
        self.view.run_command('insert', {'characters': 'hello world'})

        self.assertRegion(Region(1), 1)
        self.assertRegion(Region(1), (1, 1))
        self.assertRegion(Region(3, 5), (3, 5))
        self.assertRegion(Region(3, 5), Region(3, 5))
        self.assertRegion(Region(0, 5), 'hello')
        self.assertRegion(Region(4, 9), 'o wor')

        class NotARegion():
            pass

        with self.assertRaisesRegex(AssertionError, 'is not an instance of <class \'sublime.Region\'>'):
            self.assertRegion(NotARegion, Region(1))

    def test_assert_selection(self):
        self.view.run_command('insert', {'characters': 'hello world'})
        self.view.sel().clear()

        self.view.sel().add(3)
        self.assertSelection(3)
        self.assertSelection((3, 3))
        self.assertSelection(Region(3, 3))
        self.assertSelection([Region(3, 3)])
        with self.assertRaises(AssertionError):
            self.assertSelection(10)
        with self.assertRaises(AssertionError):
            self.assertSelection((10, 10))
        with self.assertRaises(AssertionError):
            self.assertSelection(Region(10, 10))
        with self.assertRaises(AssertionError):
            self.assertSelection([Region(10, 10)])
        with self.assertRaises(AssertionError):
            self.assertSelection(20)
        with self.assertRaises(AssertionError):
            self.assertSelection([])

        self.view.sel().add(11)
        self.assertSelection([Region(3, 3), Region(11, 11)])
        with self.assertRaises(AssertionError):
            self.assertSelection(3)
        with self.assertRaises(AssertionError):
            self.assertSelection(11)
        with self.assertRaises(AssertionError):
            self.assertSelection((3, 11))
        with self.assertRaises(AssertionError):
            self.assertSelection(Region(3, 11))
        with self.assertRaises(AssertionError):
            self.assertSelection([Region(4, 4), Region(11, 11)])

        self.view.sel().add(Region(5, 7))
        self.assertSelection([Region(3, 3), Region(5, 7), Region(11, 11)])
        with self.assertRaises(AssertionError):
            self.assertSelection([Region(3, 3), Region(11, 11)])

        self.view.sel().clear()
        self.assertSelection([])
        with self.assertRaises(AssertionError):
            self.assertSelection([Region(3, 3), Region(5, 7), Region(11, 11)])

        self.view.sel().add(Region(3, 7))
        self.assertSelection((3, 7))
        self.assertSelection(Region(3, 7))
        self.assertSelection([Region(3, 7)])
        self.assertSelection([Region(3, 7)])
        with self.assertRaises(AssertionError):
            self.assertSelection([])
        with self.assertRaises(AssertionError):
            self.assertSelection([Region(2, 7)])

    def test_assert_selection_count(self):
        self.view.run_command('insert', {'characters': 'hello world'})

        self.view.sel().clear()
        self.assertSelectionCount(0)

        self.view.sel().add(0)
        self.assertSelectionCount(1)

        self.view.sel().add(3)
        self.view.sel().add(5)
        self.assertSelectionCount(3)
        with self.assertRaises(AssertionError):
            self.assertSelectionCount(1)

        self.view.sel().clear()
        self.assertSelectionCount(0)
        with self.assertRaises(AssertionError):
            self.assertSelectionCount(1)

        self.view.sel().add(7)
        self.assertSelectionCount(1)
        with self.assertRaises(AssertionError):
            self.assertSelectionCount(0)

    def test_assert_size(self):
        self.view.run_command('insert', {'characters': 'hello world'})

        self.assertSize(11)

        with self.assertRaises(AssertionError):
            self.assertSize(5)

        with self.assertRaises(AssertionError):
            self.assertSize(12)

    def test_numbered_register(self):
        self.set_setting('use_sys_clipboard', False)
        self.register('"x')
        self.assertRegister('"x')
        self.register('0y')
        self.assertRegister('0y')
        self.register('1y')
        self.assertRegister('1y')

    @unittest.mock_mappings()
    def test_mock_mappings_default(self):
        self.assertMappingsEmpty()

    @unittest.mock_mappings(
        (unittest.INSERT, 'A', 'B'),
        (unittest.NORMAL, 'C', 'D'),
        (unittest.NORMAL, 'C2', 'D2'),
        (unittest.NORMAL, 'C3', 'D3'),
        (unittest.NORMAL, 'A', 'B'),
        (unittest.OPERATOR_PENDING, 'E', 'F'),
        (unittest.SELECT, 'G', 'H'),
        (unittest.VISUAL_BLOCK, 'I', 'J'),
        (unittest.VISUAL_BLOCK, 'I2', 'J2'),
        (unittest.VISUAL_BLOCK, 'K', 'L'),
        (unittest.VISUAL_LINE, 'K', 'L'),
        (unittest.VISUAL, 'M', 'N'),
    )
    def test_mock_mappings(self):
        self.assertMappings({
            unittest.INSERT: {'A': 'B'},
            unittest.NORMAL: {
                'C': 'D',
                'C2': 'D2',
                'C3': 'D3',
                'A': 'B',
            },
            unittest.OPERATOR_PENDING: {'E': 'F'},
            unittest.SELECT: {'G': 'H'},
            unittest.VISUAL_BLOCK: {
                'I': 'J',
                'I2': 'J2',
                'K': 'L',
            },
            unittest.VISUAL_LINE: {'K': 'L'},
            unittest.VISUAL: {'M': 'N'},
        })

        self.assertMapping(unittest.NORMAL, 'C2', 'D2')
        self.assertNotMapping('foo')
        self.assertNotMapping('foo', unittest.NORMAL)


class FunctionalTestCaseStub(unittest.FunctionalTestCase):

    def __init__(self, view):
        self.view = view


_PATCH_FEEDSEQ2CMD = {
    'b': {'command': 'cmd_b', 'args': {}},
    'w': {'command': 'cmd_w', 'args': {'mode': unittest.NORMAL}},
    'e': {'command': 'cmd_e', 'args': {'count': 2}},
    '$': {'command': 'cmd_dollar'},
    'cs"(': {'command': 'cmd_cs', 'args': {'action': 'cs', 'target': '"', 'replacement': '('}}
}


class TestFunctionalTestCase_feed(unittest.TestCase):

    def setUp(self):
        self.view = unittest.mock.Mock()
        self.window = unittest.mock.Mock()
        self.view.window.return_value = self.window
        self.instance = FunctionalTestCaseStub(self.view)

    def test_unknown_feed_raises_exception(self):
        with self.assertRaisesRegex(KeyError, 'test command definition not found for feed \'foobar\''):
            self.instance.feed('foobar')

    def test_feed_esc(self):
        self.instance.feed('<Esc>')
        self.window.run_command.assert_called_once_with('nv_feed_key', {'key': '<esc>', 'check_user_mappings': False})

    @unittest.mock.patch('NeoVintageous.tests.unittest._do_ex_cmdline')
    def test_feed_cmdline(self, do_ex_cmdline):
        self.instance.feed(':')
        do_ex_cmdline.assert_called_once_with(self.window, ':')

    @unittest.mock.patch('NeoVintageous.tests.unittest._do_ex_cmdline')
    def test_feed_cmdline_cmd(self, do_ex_cmdline):
        self.instance.feed(':pwd')
        do_ex_cmdline.assert_called_once_with(self.window, ':pwd')

    @unittest.mock.patch('NeoVintageous.tests.unittest._SEQ2CMD', _PATCH_FEEDSEQ2CMD)
    def test_feed_cmd(self):
        self.instance.feed('b')
        self.window.run_command.assert_called_once_with('cmd_b', {'mode': unittest.INTERNAL_NORMAL})

    @unittest.mock.patch('NeoVintageous.tests.unittest._SEQ2CMD', _PATCH_FEEDSEQ2CMD)
    def test_feed_cmd_with_no_args(self):
        self.instance.feed('$')
        self.window.run_command.assert_called_once_with('cmd_dollar', {'mode': unittest.INTERNAL_NORMAL})

    @unittest.mock.patch('NeoVintageous.tests.unittest._SEQ2CMD', _PATCH_FEEDSEQ2CMD)
    def test_feed_cs(self):
        self.instance.feed('cs"(')
        self.window.run_command.assert_called_once_with('cmd_cs', {
            'mode': unittest.INTERNAL_NORMAL, 'action': 'cs', 'target': '"', 'replacement': '('
        })

    @unittest.mock.patch('NeoVintageous.tests.unittest._SEQ2CMD', _PATCH_FEEDSEQ2CMD)
    def test_feed_can_specify_mode(self):
        self.instance.feed('b')
        self.window.run_command.assert_called_with('cmd_b', {'mode': unittest.INTERNAL_NORMAL})
        self.instance.feed('v_b')
        self.window.run_command.assert_called_with('cmd_b', {'mode': unittest.VISUAL})
        self.instance.feed('i_b')
        self.window.run_command.assert_called_with('cmd_b', {'mode': unittest.INSERT})
        self.instance.feed('n_b')
        self.window.run_command.assert_called_with('cmd_b', {'mode': unittest.NORMAL})
        self.instance.feed('V_b')
        self.window.run_command.assert_called_with('cmd_b', {'mode': unittest.VISUAL_LINE})
        self.instance.feed('b_b')
        self.window.run_command.assert_called_with('cmd_b', {'mode': unittest.VISUAL_BLOCK})

    @unittest.mock.patch('NeoVintageous.tests.unittest._SEQ2CMD', _PATCH_FEEDSEQ2CMD)
    def test_feed_can_override_cmd_default_mode(self):
        self.instance.feed('w')
        self.window.run_command.assert_called_with('cmd_w', {'mode': unittest.NORMAL})
        self.instance.feed('v_w')
        self.window.run_command.assert_called_with('cmd_w', {'mode': unittest.VISUAL})
        self.instance.feed('i_w')
        self.window.run_command.assert_called_with('cmd_w', {'mode': unittest.INSERT})
        self.instance.feed('n_w')
        self.window.run_command.assert_called_with('cmd_w', {'mode': unittest.NORMAL})
        self.instance.feed('V_w')
        self.window.run_command.assert_called_with('cmd_w', {'mode': unittest.VISUAL_LINE})
        self.instance.feed('b_w')
        self.window.run_command.assert_called_with('cmd_w', {'mode': unittest.VISUAL_BLOCK})

    @unittest.mock.patch('NeoVintageous.tests.unittest._SEQ2CMD', _PATCH_FEEDSEQ2CMD)
    def test_feed_can_specify_mode_with_count(self):
        self.instance.feed('2w')
        self.window.run_command.assert_called_with('cmd_w', {'mode': unittest.NORMAL, 'count': 2})
        self.instance.feed('v_2w')
        self.window.run_command.assert_called_with('cmd_w', {'mode': unittest.VISUAL, 'count': 2})
        self.instance.feed('i_2w')
        self.window.run_command.assert_called_with('cmd_w', {'mode': unittest.INSERT, 'count': 2})
        self.instance.feed('n_2w')
        self.window.run_command.assert_called_with('cmd_w', {'mode': unittest.NORMAL, 'count': 2})
        self.instance.feed('V_2w')
        self.window.run_command.assert_called_with('cmd_w', {'mode': unittest.VISUAL_LINE, 'count': 2})
        self.instance.feed('b_2w')
        self.window.run_command.assert_called_with('cmd_w', {'mode': unittest.VISUAL_BLOCK, 'count': 2})

    @unittest.mock.patch('NeoVintageous.tests.unittest._SEQ2CMD', _PATCH_FEEDSEQ2CMD)
    def test_feed_can_specify_counts(self):
        self.instance.feed('3b')
        self.window.run_command.assert_called_with('cmd_b', {'mode': unittest.INTERNAL_NORMAL, 'count': 3})

    @unittest.mock.patch('NeoVintageous.tests.unittest._SEQ2CMD', _PATCH_FEEDSEQ2CMD)
    def test_feed_can_override_default_counts(self):
        self.instance.feed('3e')
        self.window.run_command.assert_called_once_with('cmd_e', {'mode': unittest.INTERNAL_NORMAL, 'count': 3})

    @unittest.mock.patch('NeoVintageous.tests.unittest._SEQ2CMD', _PATCH_FEEDSEQ2CMD)
    def test_feed_count_resets_to_default_if_no_count_given(self):
        self.instance.feed('e')
        self.window.run_command.assert_called_with('cmd_e', {'mode': unittest.INTERNAL_NORMAL, 'count': 2})

        self.instance.feed('3e')
        self.window.run_command.assert_called_with('cmd_e', {'mode': unittest.INTERNAL_NORMAL, 'count': 3})

        self.instance.feed('e')
        self.window.run_command.assert_called_with('cmd_e', {'mode': unittest.INTERNAL_NORMAL, 'count': 2})


class TestFunctionalTestCase_eq(unittest.TestCase):

    def setUp(self):
        self.view = unittest.mock.Mock()
        self.view.sel.return_value = []
        self.window = unittest.mock.Mock()
        self.view.window.return_value = self.window
        self.instance = FunctionalTestCaseStub(self.view)
        self.instance.feed = unittest.mock.Mock()
        self.instance.normal = unittest.mock.Mock()
        self.instance.insert = unittest.mock.Mock()
        self.instance.internalNormal = unittest.mock.Mock()
        self.instance.rinternalNormal = unittest.mock.Mock()
        self.instance.vselect = unittest.mock.Mock()
        self.instance.rvselect = unittest.mock.Mock()
        self.instance.visual = unittest.mock.Mock()
        self.instance.vline = unittest.mock.Mock()
        self.instance.vblock = unittest.mock.Mock()
        self.instance.assertNormal = unittest.mock.Mock()
        self.instance.assertInsert = unittest.mock.Mock()
        self.instance.assertInternalNormal = unittest.mock.Mock()
        self.instance.assertRInternalNormal = unittest.mock.Mock()
        self.instance.assertVselect = unittest.mock.Mock()
        self.instance.assertRVselect = unittest.mock.Mock()
        self.instance.assertVisual = unittest.mock.Mock()
        self.instance.assertVline = unittest.mock.Mock()
        self.instance.assertVblock = unittest.mock.Mock()

    def assert_insert(self, *args):
        self.instance.insert.assert_called_once_with(*args)

    def assert_internal_normal(self, *args):
        self.instance.internalNormal.assert_called_once_with(*args)

    def assert_r_internal_normal(self, *args):
        self.instance.rinternalNormal.assert_called_once_with(*args)

    def assert_normal(self, *args):
        self.instance.normal.assert_called_once_with(*args)

    def assert_visual(self, *args):
        self.instance.visual.assert_called_once_with(*args)

    def assert_vline(self, *args):
        self.instance.vline.assert_called_once_with(*args)

    def assert_vblock(self, *args):
        self.instance.vblock.assert_called_once_with(*args)

    def assert_vselect(self, *args):
        self.instance.vselect.assert_called_once_with(*args)

    def assert_rvselect(self, *args):
        self.instance.rvselect.assert_called_once_with(*args)

    def assert_feed(self, *args):
        self.instance.feed.assert_called_once_with(*args)

    def assert_assertInsert(self, *args):
        self.instance.assertInsert.assert_called_once_with(*args)

    def assert_assertInternalNormal(self, *args):
        self.instance.assertInternalNormal.assert_called_once_with(*args)

    def assert_assertRInternalNormal(self, *args):
        self.instance.assertRInternalNormal.assert_called_once_with(*args)

    def assert_assertVSelect(self, *args):
        self.instance.assertVselect.assert_called_once_with(*args)

    def assert_assertRVSelect(self, *args):
        self.instance.assertRVselect.assert_called_once_with(*args)

    def assert_assertNormal(self, *args):
        self.instance.assertNormal.assert_called_once_with(*args)

    def assert_assertVisual(self, *args):
        self.instance.assertVisual.assert_called_once_with(*args)

    def assert_assertVline(self, *args):
        self.instance.assertVline.assert_called_once_with(*args)

    def assert_assertVblock(self, *args):
        self.instance.assertVblock.assert_called_once_with(*args)

    def test_eq(self):
        self.instance.eq('a', 'b', 'c')
        self.assert_normal('a')
        self.assert_feed('b')
        self.assert_assertNormal('c', None)

    def test_eq_expected_should_be_optional(self):
        self.instance.eq('a', 'b')
        self.assert_normal('a')
        self.assert_feed('b')
        self.assert_assertNormal('a', None)

    def test_eq_assertNormal_insert(self):
        self.instance.eq('a', 'b', 'i_c')
        self.assert_normal('a')
        self.assert_feed('b')
        self.assert_assertInsert('c', None)

    def test_eq_assertNormal_visual(self):
        self.instance.eq('a', 'b', 'v_c')
        self.assert_normal('a')
        self.assert_feed('b')
        self.assert_assertVisual('c', None)

    def test_eq_assertNormal_visual_block(self):
        self.instance.eq('a', 'b', 'b_c')
        self.assert_normal('a')
        self.assert_feed('b')
        self.assert_assertVblock('c', DIRECTION_DOWN, None)

    def test_eq_assertNormal_visual_line(self):
        self.instance.eq('a', 'b', 'V_c')
        self.assert_normal('a')
        self.assert_feed('b')
        self.assert_assertVline('c', None)

    def test_eq_normal(self):
        self.instance.eq('a', 'n_b', 'c')
        self.assert_normal('a')
        self.assert_feed('n_b')
        self.assert_assertNormal('c', None)

    def test_eq_insert(self):
        self.instance.eq('text', 'i_x', 'expected')
        self.assert_insert('text')
        self.assert_feed('i_x')
        self.assert_assertInsert('expected', None)

    def test_eq_internal_normal(self):
        self.instance.eq('text', 'N_x', 'expected')
        self.assert_internal_normal('text')
        self.assert_feed('N_x')
        self.assert_assertInternalNormal('expected', None)

    def test_eq_r_internal_normal(self):
        self.instance.eq('r_text', 'N_x', 'expected')
        self.assert_r_internal_normal('text')
        self.assert_feed('N_x')
        self.assert_assertInternalNormal('expected', None)

    def test_eq_internal_normal_r(self):
        self.instance.eq('text', 'N_x', 'r_expected')
        self.assert_internal_normal('text')
        self.assert_feed('N_x')
        self.assert_assertRInternalNormal('expected', None)

    def test_eq_normal_assertNormal_insert(self):
        self.instance.eq('a', 'n_b', 'i_c')
        self.assert_normal('a')
        self.assert_feed('n_b')
        self.assert_assertInsert('c', None)

    def test_eq_normal_assertNormal_visual_block(self):
        self.instance.eq('a', 'n_b', 'b_c')
        self.assert_normal('a')
        self.assert_feed('n_b')
        self.assert_assertVblock('c', DIRECTION_DOWN, None)

    def test_eq_normal_assertNormal_visual_line(self):
        self.instance.eq('a', 'n_b', 'V_c')
        self.assert_normal('a')
        self.assert_feed('n_b')
        self.assert_assertVline('c', None)

    def test_eq_visual(self):
        self.instance.eq('a', 'v_b', 'c')
        self.assert_visual('a')
        self.assert_feed('v_b')
        self.assert_assertVisual('c', None)

    def test_eq_visual_assertNormal_insert(self):
        self.instance.eq('a', 'v_b', 'i_c')
        self.assert_visual('a')
        self.assert_feed('v_b')
        self.assert_assertInsert('c', None)

    def test_eq_visual_assertNormal_normal(self):
        self.instance.eq('a', 'v_b', 'n_c')
        self.assert_visual('a')
        self.assert_feed('v_b')
        self.assert_assertNormal('c', None)

    def test_eq_visual_assertNormal_visual_block(self):
        self.instance.eq('a', 'v_b', 'b_c')
        self.assert_visual('a')
        self.assert_feed('v_b')
        self.assert_assertVblock('c', DIRECTION_DOWN, None)

    def test_eq_visual_assertNormal_visual_line(self):
        self.instance.eq('a', 'v_b', 'V_c')
        self.assert_visual('a')
        self.assert_feed('v_b')
        self.assert_assertVline('c', None)

    def test_eq_visual_line(self):
        self.instance.eq('a', 'V_b', 'c')
        self.assert_vline('a')
        self.assert_feed('V_b')
        self.assert_assertVline('c', None)

    def test_eq_vselect(self):
        self.instance.eq('a', 's_b', 'c')
        self.assert_vselect('a')
        self.assert_feed('s_b')
        self.assert_assertVSelect('c', None)

    def test_eq_rvselect(self):
        self.instance.eq('r_a', 's_b', 'r_c')
        self.assert_rvselect('a')
        self.assert_feed('s_b')
        self.assert_assertRVSelect('c', None)

    def test_eq_visual_line_assertNormal_insert(self):
        self.instance.eq('a', 'V_b', 'i_c')
        self.assert_vline('a')
        self.assert_feed('V_b')
        self.assert_assertInsert('c', None)

    def test_eq_visual_line_assertNormal_normal(self):
        self.instance.eq('a', 'V_b', 'n_c')
        self.assert_vline('a')
        self.assert_feed('V_b')
        self.assert_assertNormal('c', None)

    def test_eq_visual_line_assertNormal_visual(self):
        self.instance.eq('a', 'V_b', 'v_c')
        self.assert_vline('a')
        self.assert_feed('V_b')
        self.assert_assertVisual('c', None)

    def test_eq_visual_line_assertNormal_visual_block(self):
        self.instance.eq('a', 'V_b', 'b_c')
        self.assert_vline('a')
        self.assert_feed('V_b')
        self.assert_assertVblock('c', DIRECTION_DOWN, None)

    def test_eq_visual_block(self):
        self.instance.eq('a', 'b_b', 'c')
        self.assert_vblock('a', DIRECTION_DOWN)
        self.assert_feed('b_b')
        self.assert_assertVblock('c', DIRECTION_DOWN, None)

    def test_eq_visual_block_assertNormal_insert(self):
        self.instance.eq('a', 'b_b', 'i_c')
        self.assert_vblock('a', DIRECTION_DOWN)
        self.assert_feed('b_b')
        self.assert_assertInsert('c', None)

    def test_eq_visual_block_assertNormal_normal(self):
        self.instance.eq('a', 'b_b', 'n_c')
        self.assert_vblock('a', DIRECTION_DOWN)
        self.assert_feed('b_b')
        self.assert_assertNormal('c', None)

    def test_eq_visual_block_assertNormal_visual(self):
        self.instance.eq('a', 'b_b', 'v_c')
        self.assert_vblock('a', DIRECTION_DOWN)
        self.assert_feed('b_b')
        self.assert_assertVisual('c', None)

    def test_eq_visual_block_assertNormal_visual_block(self):
        self.instance.eq('a', 'b_b', 'b_c')
        self.assert_vblock('a', DIRECTION_DOWN)
        self.assert_feed('b_b')
        self.assert_assertVblock('c', DIRECTION_DOWN, None)

    def test_eq_visual_block_assertNormal_visual_line(self):
        self.instance.eq('a', 'b_b', 'V_c')
        self.assert_vblock('a', DIRECTION_DOWN)
        self.assert_feed('b_b')
        self.assert_assertVline('c', None)

    def test_eq_cmdline(self):
        self.instance.eq('a', ':b', 'c')
        self.assert_normal('a')
        self.assert_feed(':b')
        self.assert_assertNormal('c', None)

    def test_eq_visual_cmdline(self):
        self.instance.eq('a', ':\'<,\'>b', 'c')
        self.assert_visual('a')
        self.assert_feed(':\'<,\'>b')
        self.assert_assertVisual('c', None)
