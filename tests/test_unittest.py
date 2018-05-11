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

    def test_fixture_default_selection_is_eof(self):
        self.fixture('Hello world!')
        self.assertEqual('Hello world!', self.view.substr(Region(0, self.view.size())))
        self.assertEqual([Region(12)], list(self.view.sel()))

    def test_fixture_is_normal_mode(self):
        self.fixture('Hello world!')
        self.assertNormalMode()

    def test_fixture_erases_view_before_insert(self):
        self.fixture('foobar')
        self.fixture('a')
        self.assertEqual('a', self.view.substr(Region(0, self.view.size())))
        self.fixture('b')
        self.assertEqual('b', self.view.substr(Region(0, self.view.size())))

    def test_fixture_zero_pos_selection(self):
        self.fixture('|hello world!')
        self.assertEqual([Region(0)], list(self.view.sel()))

    def test_fixture_middle_pos_selection(self):
        self.fixture('hello| world!')
        self.assertEqual([Region(5)], list(self.view.sel()))

    def test_fixture_end_pos_selection(self):
        self.fixture('hello world|!')
        self.assertEqual([Region(11)], list(self.view.sel()))

    def test_fixture_multiple_selections(self):
        self.fixture('h|el|lo world!')
        self.assertEqual([Region(1), Region(3)], list(self.view.sel()))
        self.fixture('hell|o |wo|rld!')
        self.assertEqual([Region(4), Region(6), Region(8)], list(self.view.sel()))
        self.fixture('hel|lo| w|orld|!')
        self.assertEqual([Region(3), Region(5), Region(7), Region(11)], list(self.view.sel()))

    def test_ifixture(self):
        self.iFixture('t|ext')
        self.assertEqual('text', self.view.substr(Region(0, self.view.size())))
        self.assertEqual([Region(1)], list(self.view.sel()))
        self.assertInsertMode()

    def test_vfixture(self):
        self.vFixture('t|ex|t')
        self.assertEqual('text', self.view.substr(Region(0, self.view.size())))
        self.assertEqual([Region(1, 3)], list(self.view.sel()))
        self.assertVisualMode()

    def test_vfixture_single_selection_expands_one_character(self):
        self.vFixture('t|ext')
        self.assertEqual('text', self.view.substr(Region(0, self.view.size())))
        self.assertEqual([Region(1, 2)], list(self.view.sel()))
        self.assertVisualMode()

    def test_vfixture_multiple_selection(self):
        self.vFixture('h|ell|o |worl|d')
        self.assertEqual([Region(1, 4), Region(6, 10)], list(self.view.sel()))
        self.assertVisualMode()

    def test_vfixture_raises_exception_if_malformed_visual_selection(self):
        with self.assertRaisesRegex(Exception, 'invalid fixture visual selection'):
            self.vFixture('hello world!')
        with self.assertRaisesRegex(Exception, 'invalid fixture visual selection'):
            self.vFixture('h|e|l|lo world!')
        with self.assertRaisesRegex(Exception, 'invalid fixture visual selection'):
            self.vFixture('h|e|l|lo |w|orld!')

    def test_vline_fixture_sets_visual_line_mode(self):
        self.vLineFixture('|text|')
        self.assertVisualLineMode()

    def test_vblock_fixture_sets_visual_block_mode(self):
        self.vBlockFixture('|text|')
        self.assertVisualBlockMode()

    def test_expects(self):
        self.view.run_command('insert', {'characters': 'hello world'})
        self.state.mode = unittest.NORMAL

        self.view.sel().clear()
        self.expects('hello world')

        self.view.sel().add(0)
        self.expects('|hello world')

        with self.assertRaises(AssertionError):
            self.expects('hello world')

        self.view.sel().add(4)
        self.expects('|hell|o world')

        self.view.sel().clear()
        self.view.sel().add(6)
        self.expects('hello |world')

        with self.assertRaises(AssertionError):
            self.expects('hello world')

        with self.assertRaises(AssertionError):
            self.expects('hello| world')

        with self.assertRaises(AssertionError):
            self.expects('hello world|')

        self.view.sel().clear()
        self.view.sel().add(3)
        self.view.sel().add(5)
        self.view.sel().add(7)
        self.expects('hel|lo| w|orld')

    def test_expects_asserts_normal_mode(self):
        self.view.run_command('insert', {'characters': 'hello world'})
        self.state.mode = unittest.VISUAL
        with self.assertRaises(AssertionError):
            self.expects('hello world|')
        self.state.mode = unittest.NORMAL
        self.expects('hello world|')

    def test_expects_i(self):
        self.view.run_command('insert', {'characters': 'hello world'})
        self.state.mode = unittest.INSERT

        self.view.sel().clear()
        self.expectsI('hello world')

        self.view.sel().clear()
        self.view.sel().add(3)
        self.view.sel().add(5)
        self.view.sel().add(7)
        self.expectsI('hel|lo| w|orld')

    def test_expects_i_asserts_insert_mode(self):
        self.view.run_command('insert', {'characters': 'hello world'})
        self.state.mode = unittest.NORMAL
        with self.assertRaises(AssertionError):
            self.expectsI('hello world|')
        self.state.mode = unittest.INSERT
        self.expectsI('hello world|')

    def test_expects_v(self):
        self.view.run_command('insert', {'characters': 'hello world'})
        self.state.mode = unittest.VISUAL

        self.view.sel().clear()
        self.expectsV('hello world')

        self.view.sel().add(Region(3, 5))
        self.expectsV('hel|lo| world')

        with self.assertRaises(AssertionError):
            self.expectsV('|hello| world')

        self.view.sel().add(Region(3, 5))
        self.view.sel().add(Region(7, 11))
        self.expectsV('hel|lo| w|orld|')

    def test_expects_v_asserts_visual_mode(self):
        self.view.run_command('insert', {'characters': 'hello world'})
        self.view.sel().clear()
        self.view.sel().add(3)
        self.view.sel().add(5)
        self.state.mode = unittest.NORMAL
        with self.assertRaises(AssertionError):
            self.expectsV('hel|lo| world')
        self.state.mode = unittest.VISUAL
        self.expectsV('hel|lo| world')

    def test_expects_vline_asserts_visual_line_mode(self):
        self.view.run_command('insert', {'characters': 'hello world'})
        self.view.sel().clear()
        self.view.sel().add(0)
        self.view.sel().add(11)
        self.state.mode = unittest.NORMAL
        with self.assertRaises(AssertionError):
            self.expectsVLine('|hello world|')
        self.state.mode = unittest.VISUAL_LINE
        self.expectsVLine('|hello world|')

    def test_expects_vblock_asserts_visual_block_mode(self):
        self.view.run_command('insert', {'characters': 'hello world'})
        self.view.sel().clear()
        self.view.sel().add(0)
        self.view.sel().add(11)
        self.state.mode = unittest.NORMAL
        with self.assertRaises(AssertionError):
            self.expectsVBlock('|hello world|')
        self.state.mode = unittest.VISUAL_BLOCK
        self.expectsVBlock('|hello world|')

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

        self.assertRegion(1, Region(1))
        self.assertRegion((1, 1), Region(1))
        self.assertRegion((3, 5), Region(3, 5))
        self.assertRegion(Region(3, 5), Region(3, 5))
        self.assertRegion('hello', Region(0, 5))
        self.assertRegion('o wor', Region(4, 9))

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


class FunctionalTestCaseStub(unittest.FunctionalTestCase):

    def __init__(self, view):
        self.view = view


_patch_feedseq2cmd = {
    'b': {'command': 'cmd_b', 'args': {}},
    'w': {'command': 'cmd_w', 'args': {'mode': 'mode_normal'}},
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
        self.window.run_command.assert_called_once_with('_nv_feed_key', {'key': '<esc>'})

    @unittest.mock.patch('NeoVintageous.tests.unittest._do_ex_cmdline')
    def test_feed_cmdline(self, do_ex_cmdline):
        self.instance.feed(':')
        do_ex_cmdline.assert_called_once_with(self.window, ':')

    @unittest.mock.patch('NeoVintageous.tests.unittest._do_ex_cmdline')
    def test_feed_cmdline_cmd(self, do_ex_cmdline):
        self.instance.feed(':pwd')
        do_ex_cmdline.assert_called_once_with(self.window, ':pwd')

    @unittest.mock.patch('NeoVintageous.tests.unittest._feedseq2cmd', _patch_feedseq2cmd)
    def test_feed_cmd(self):
        self.instance.feed('b')
        self.view.run_command.assert_called_once_with('cmd_b', {'mode': 'mode_internal_normal'})

    @unittest.mock.patch('NeoVintageous.tests.unittest._feedseq2cmd', _patch_feedseq2cmd)
    def test_feed_cmd_with_no_args(self):
        self.instance.feed('$')
        self.view.run_command.assert_called_once_with('cmd_dollar', {'mode': 'mode_internal_normal'})

    @unittest.mock.patch('NeoVintageous.tests.unittest._feedseq2cmd', _patch_feedseq2cmd)
    def test_feed_cs(self):
        self.instance.feed('cs"(')
        self.view.run_command.assert_called_once_with('cmd_cs', {
            'mode': 'mode_internal_normal', 'action': 'cs', 'target': '"', 'replacement': '('
        })

    @unittest.mock.patch('NeoVintageous.tests.unittest._feedseq2cmd', _patch_feedseq2cmd)
    def test_feed_can_specify_mode(self):
        self.instance.feed('b')
        self.view.run_command.assert_called_with('cmd_b', {'mode': 'mode_internal_normal'})
        self.instance.feed('v_b')
        self.view.run_command.assert_called_with('cmd_b', {'mode': 'mode_visual'})
        self.instance.feed('i_b')
        self.view.run_command.assert_called_with('cmd_b', {'mode': 'mode_insert'})
        self.instance.feed('n_b')
        self.view.run_command.assert_called_with('cmd_b', {'mode': 'mode_normal'})
        self.instance.feed('l_b')
        self.view.run_command.assert_called_with('cmd_b', {'mode': 'mode_visual_line'})
        self.instance.feed('b_b')
        self.view.run_command.assert_called_with('cmd_b', {'mode': 'mode_visual_block'})

    @unittest.mock.patch('NeoVintageous.tests.unittest._feedseq2cmd', _patch_feedseq2cmd)
    def test_feed_can_override_cmd_default_mode(self):
        self.instance.feed('w')
        self.view.run_command.assert_called_with('cmd_w', {'mode': 'mode_normal'})
        self.instance.feed('v_w')
        self.view.run_command.assert_called_with('cmd_w', {'mode': 'mode_visual'})
        self.instance.feed('i_w')
        self.view.run_command.assert_called_with('cmd_w', {'mode': 'mode_insert'})
        self.instance.feed('n_w')
        self.view.run_command.assert_called_with('cmd_w', {'mode': 'mode_normal'})
        self.instance.feed('l_w')
        self.view.run_command.assert_called_with('cmd_w', {'mode': 'mode_visual_line'})
        self.instance.feed('b_w')
        self.view.run_command.assert_called_with('cmd_w', {'mode': 'mode_visual_block'})

    @unittest.mock.patch('NeoVintageous.tests.unittest._feedseq2cmd', _patch_feedseq2cmd)
    def test_feed_can_specify_mode_with_count(self):
        self.instance.feed('2w')
        self.view.run_command.assert_called_with('cmd_w', {'mode': 'mode_normal', 'count': 2})
        self.instance.feed('v_2w')
        self.view.run_command.assert_called_with('cmd_w', {'mode': 'mode_visual', 'count': 2})
        self.instance.feed('i_2w')
        self.view.run_command.assert_called_with('cmd_w', {'mode': 'mode_insert', 'count': 2})
        self.instance.feed('n_2w')
        self.view.run_command.assert_called_with('cmd_w', {'mode': 'mode_normal', 'count': 2})
        self.instance.feed('l_2w')
        self.view.run_command.assert_called_with('cmd_w', {'mode': 'mode_visual_line', 'count': 2})
        self.instance.feed('b_2w')
        self.view.run_command.assert_called_with('cmd_w', {'mode': 'mode_visual_block', 'count': 2})

    @unittest.mock.patch('NeoVintageous.tests.unittest._feedseq2cmd', _patch_feedseq2cmd)
    def test_feed_can_specify_counts(self):
        self.instance.feed('3b')
        self.view.run_command.assert_called_with('cmd_b', {'mode': 'mode_internal_normal', 'count': 3})

    @unittest.mock.patch('NeoVintageous.tests.unittest._feedseq2cmd', _patch_feedseq2cmd)
    def test_feed_can_override_default_counts(self):
        self.instance.feed('3e')
        self.view.run_command.assert_called_once_with('cmd_e', {'mode': 'mode_internal_normal', 'count': 3})

    @unittest.mock.patch('NeoVintageous.tests.unittest._feedseq2cmd', _patch_feedseq2cmd)
    def test_feed_count_resets_to_default_if_no_count_given(self):
        self.instance.feed('e')
        self.view.run_command.assert_called_with('cmd_e', {'mode': 'mode_internal_normal', 'count': 2})

        self.instance.feed('3e')
        self.view.run_command.assert_called_with('cmd_e', {'mode': 'mode_internal_normal', 'count': 3})

        self.instance.feed('e')
        self.view.run_command.assert_called_with('cmd_e', {'mode': 'mode_internal_normal', 'count': 2})


class TestFunctionalTestCase_eq(unittest.TestCase):

    def setUp(self):
        self.view = unittest.mock.Mock()
        self.window = unittest.mock.Mock()
        self.view.window.return_value = self.window
        self.instance = FunctionalTestCaseStub(self.view)
        self.instance.feed = unittest.mock.Mock()

    def test_eq(self):
        self.instance.fixture = unittest.mock.Mock()
        self.instance.expects = unittest.mock.Mock()
        self.instance.eq('a', 'b', 'c')
        self.instance.fixture.assert_called_once_with('a')
        self.instance.feed.assert_called_once_with('b')
        self.instance.expects.assert_called_once_with('c', None)

    def test_eq_expected_should_be_optional(self):
        self.instance.fixture = unittest.mock.Mock()
        self.instance.expects = unittest.mock.Mock()
        self.instance.eq('a', 'b')
        self.instance.fixture.assert_called_once_with('a')
        self.instance.feed.assert_called_once_with('b')
        self.instance.expects.assert_called_once_with('a', None)

    def test_eq_expects_visual(self):
        self.instance.fixture = unittest.mock.Mock()
        self.instance.expectsV = unittest.mock.Mock()
        self.instance.eq('a', 'b', 'v_c')
        self.instance.fixture.assert_called_once_with('a')
        self.instance.feed.assert_called_once_with('b')
        self.instance.expectsV.assert_called_once_with('c', None)

    def test_eq_expects_visual_line(self):
        self.instance.fixture = unittest.mock.Mock()
        self.instance.expectsVLine = unittest.mock.Mock()
        self.instance.eq('a', 'b', 'l_c')
        self.instance.fixture.assert_called_once_with('a')
        self.instance.feed.assert_called_once_with('b')
        self.instance.expectsVLine.assert_called_once_with('c', None)

    def test_eq_expects_visual_block(self):
        self.instance.fixture = unittest.mock.Mock()
        self.instance.expectsVBlock = unittest.mock.Mock()
        self.instance.eq('a', 'b', 'b_c')
        self.instance.fixture.assert_called_once_with('a')
        self.instance.feed.assert_called_once_with('b')
        self.instance.expectsVBlock.assert_called_once_with('c', None)

    def test_eq_expects_insert(self):
        self.instance.fixture = unittest.mock.Mock()
        self.instance.expectsI = unittest.mock.Mock()
        self.instance.eq('a', 'b', 'i_c')
        self.instance.fixture.assert_called_once_with('a')
        self.instance.feed.assert_called_once_with('b')
        self.instance.expectsI.assert_called_once_with('c', None)

    def test_eq_visual(self):
        self.instance.vFixture = unittest.mock.Mock()
        self.instance.expectsV = unittest.mock.Mock()
        self.instance.eq('a', 'v_b', 'c')
        self.instance.vFixture.assert_called_once_with('a')
        self.instance.feed.assert_called_once_with('v_b')
        self.instance.expectsV.assert_called_once_with('c', None)

    def test_eq_visual_expects_normal(self):
        self.instance.vFixture = unittest.mock.Mock()
        self.instance.expects = unittest.mock.Mock()
        self.instance.eq('a', 'v_b', 'n_c')
        self.instance.vFixture.assert_called_once_with('a')
        self.instance.feed.assert_called_once_with('v_b')
        self.instance.expects.assert_called_once_with('c', None)

    def test_eq_visual_expects_visual_line(self):
        self.instance.vFixture = unittest.mock.Mock()
        self.instance.expectsVLine = unittest.mock.Mock()
        self.instance.eq('a', 'v_b', 'l_c')
        self.instance.vFixture.assert_called_once_with('a')
        self.instance.feed.assert_called_once_with('v_b')
        self.instance.expectsVLine.assert_called_once_with('c', None)

    def test_eq_visual_expects_visual_block(self):
        self.instance.vFixture = unittest.mock.Mock()
        self.instance.expectsVBlock = unittest.mock.Mock()
        self.instance.eq('a', 'v_b', 'b_c')
        self.instance.vFixture.assert_called_once_with('a')
        self.instance.feed.assert_called_once_with('v_b')
        self.instance.expectsVBlock.assert_called_once_with('c', None)

    def test_eq_visual_expects_insert(self):
        self.instance.vFixture = unittest.mock.Mock()
        self.instance.expectsI = unittest.mock.Mock()
        self.instance.eq('a', 'v_b', 'i_c')
        self.instance.vFixture.assert_called_once_with('a')
        self.instance.feed.assert_called_once_with('v_b')
        self.instance.expectsI.assert_called_once_with('c', None)

    def test_eq_visual_line(self):
        self.instance.vLineFixture = unittest.mock.Mock()
        self.instance.expectsVLine = unittest.mock.Mock()
        self.instance.eq('a', 'l_b', 'c')
        self.instance.vLineFixture.assert_called_once_with('a')
        self.instance.feed.assert_called_once_with('l_b')
        self.instance.expectsVLine.assert_called_once_with('c', None)

    def test_eq_visual_line_expects_normal(self):
        self.instance.vLineFixture = unittest.mock.Mock()
        self.instance.expects = unittest.mock.Mock()
        self.instance.eq('a', 'l_b', 'n_c')
        self.instance.vLineFixture.assert_called_once_with('a')
        self.instance.feed.assert_called_once_with('l_b')
        self.instance.expects.assert_called_once_with('c', None)

    def test_eq_visual_line_expects_insert(self):
        self.instance.vLineFixture = unittest.mock.Mock()
        self.instance.expectsI = unittest.mock.Mock()
        self.instance.eq('a', 'l_b', 'i_c')
        self.instance.vLineFixture.assert_called_once_with('a')
        self.instance.feed.assert_called_once_with('l_b')
        self.instance.expectsI.assert_called_once_with('c', None)

    def test_eq_visual_line_expects_visual(self):
        self.instance.vLineFixture = unittest.mock.Mock()
        self.instance.expectsV = unittest.mock.Mock()
        self.instance.eq('a', 'l_b', 'v_c')
        self.instance.vLineFixture.assert_called_once_with('a')
        self.instance.feed.assert_called_once_with('l_b')
        self.instance.expectsV.assert_called_once_with('c', None)

    def test_eq_visual_line_expects_visual_block(self):
        self.instance.vLineFixture = unittest.mock.Mock()
        self.instance.expectsVBlock = unittest.mock.Mock()
        self.instance.eq('a', 'l_b', 'b_c')
        self.instance.vLineFixture.assert_called_once_with('a')
        self.instance.feed.assert_called_once_with('l_b')
        self.instance.expectsVBlock.assert_called_once_with('c', None)

    def test_eq_visual_block(self):
        self.instance.vBlockFixture = unittest.mock.Mock()
        self.instance.expectsVBlock = unittest.mock.Mock()
        self.instance.eq('a', 'b_b', 'c')
        self.instance.vBlockFixture.assert_called_once_with('a')
        self.instance.feed.assert_called_once_with('b_b')
        self.instance.expectsVBlock.assert_called_once_with('c', None)

    def test_eq_visual_block_expects_normal(self):
        self.instance.vBlockFixture = unittest.mock.Mock()
        self.instance.expects = unittest.mock.Mock()
        self.instance.eq('a', 'b_b', 'n_c')
        self.instance.vBlockFixture.assert_called_once_with('a')
        self.instance.feed.assert_called_once_with('b_b')
        self.instance.expects.assert_called_once_with('c', None)

    def test_eq_visual_block_expects_insert(self):
        self.instance.vBlockFixture = unittest.mock.Mock()
        self.instance.expectsI = unittest.mock.Mock()
        self.instance.eq('a', 'b_b', 'i_c')
        self.instance.vBlockFixture.assert_called_once_with('a')
        self.instance.feed.assert_called_once_with('b_b')
        self.instance.expectsI.assert_called_once_with('c', None)

    def test_eq_visual_block_expects_visual(self):
        self.instance.vBlockFixture = unittest.mock.Mock()
        self.instance.expectsV = unittest.mock.Mock()
        self.instance.eq('a', 'b_b', 'v_c')
        self.instance.vBlockFixture.assert_called_once_with('a')
        self.instance.feed.assert_called_once_with('b_b')
        self.instance.expectsV.assert_called_once_with('c', None)

    def test_eq_visual_block_expects_visual_block(self):
        self.instance.vBlockFixture = unittest.mock.Mock()
        self.instance.expectsVBlock = unittest.mock.Mock()
        self.instance.eq('a', 'b_b', 'b_c')
        self.instance.vBlockFixture.assert_called_once_with('a')
        self.instance.feed.assert_called_once_with('b_b')
        self.instance.expectsVBlock.assert_called_once_with('c', None)

    def test_eq_cmdline(self):
        self.instance.fixture = unittest.mock.Mock()
        self.instance.expects = unittest.mock.Mock()
        self.instance.eq('a', ':b', 'c')
        self.instance.fixture.assert_called_once_with('a')
        self.instance.feed.assert_called_once_with(':b')
        self.instance.expects.assert_called_once_with('c', None)

    def test_eq_visual_cmdline(self):
        self.instance.vFixture = unittest.mock.Mock()
        self.instance.expectsV = unittest.mock.Mock()
        self.instance.eq('a', ':\'<,\'>b', 'c')
        self.instance.vFixture.assert_called_once_with('a')
        self.instance.feed.assert_called_once_with(':\'<,\'>b')
        self.instance.expectsV.assert_called_once_with('c', None)
