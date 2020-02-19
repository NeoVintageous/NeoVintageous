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

from NeoVintageous.nv.settings import get_last_buffer_search
from NeoVintageous.nv.settings import get_last_char_search_command
from NeoVintageous.nv.settings import get_last_char_search
from NeoVintageous.nv.settings import get_reset_during_init
from NeoVintageous.nv.settings import set_reset_during_init
from NeoVintageous.nv.state import State
from NeoVintageous.nv.vi import cmd_defs


class TestState(unittest.ViewTestCase):

    def _assertDefaultMode(self, mode):
        # The default mode assertion can sometimes fail.
        #
        # Apparently it can fail on the CI servers aswell as local development
        # machines, though at the time of writing I wasn't able to reproduce the
        # issue on the CI servers.
        #
        # The issue:
        #
        # The default mode is UNKNOWN. The event listener on_activated event
        # initialises views and part of that initialisation is to set the
        # default mode to NORMAL.
        #
        # An issue arises when the Sublime Text window doesn't have focus e.g.
        # start a test run, then quickly move the focus to another application
        # while the tests are run.
        #
        # When ST doesn't have focus it doesn't fire the on_activated event. I
        # assume it's expected ST behaviour e.g. maybe because the when you move
        # focus away from ST is fires the on_deactivate event on the active
        # view.
        #
        # When the on_activated event is NOT fired for the test view then the
        # mode will stay in an UNKNOWN state, but when it is fired it is set to
        # a NORMAL state.

        try:
            self.assertEqual(mode, unittest.NORMAL)
        except AssertionError:
            self.assertEqual(mode, unittest.UNKNOWN)

    def test_can_initialize(self):
        s = State(self.view)
        # Make sure the actual usage of NeoVintageous doesn't change the
        # pristine state. This isn't great, though.
        self.view.window().settings().erase('_vintageous_last_char_search_command')
        self.view.window().settings().erase('_vintageous_last_char_search')
        self.view.window().settings().erase('_vintageous_last_buffer_search')

        self.assertEqual(s.sequence, '')
        self.assertEqual(s.partial_sequence, '')
        self._assertDefaultMode(s.mode)
        self.assertEqual(s.action, None)
        self.assertEqual(s.motion, None)
        self.assertEqual(s.action_count, '')
        self.assertEqual(s.glue_until_normal_mode, False)
        self.assertEqual(s.processing_notation, False)
        self.assertEqual(get_last_char_search(self.view), '')
        self.assertEqual(get_last_char_search_command(self.view), 'vi_f')
        self.assertEqual(s.non_interactive, False)
        self.assertEqual(s.must_capture_register_name, False)
        self.assertEqual(get_last_buffer_search(self.view), '')
        self.assertEqual(get_reset_during_init(self.view), True)

    def test_must_scroll_into_view(self):
        self.assertFalse(self.state.must_scroll_into_view())

        motion = cmd_defs.ViGotoSymbolInFile()
        self.state.motion = motion
        self.assertTrue(self.state.must_scroll_into_view())

    def test_enter_normal_mode(self):
        self._assertDefaultMode(self.state.mode)
        self.state.mode = unittest.UNKNOWN
        self.assertNotEqual(self.state.mode, unittest.NORMAL)
        self.state.enter_normal_mode()
        self.assertEqual(self.state.mode, unittest.NORMAL)

    def test_enter_visual_mode(self):
        self._assertDefaultMode(self.state.mode)
        self.state.enter_visual_mode()
        self.assertEqual(self.state.mode, unittest.VISUAL)

    def test_enter_insert_mode(self):
        self._assertDefaultMode(self.state.mode)
        self.state.enter_insert_mode()
        self.assertEqual(self.state.mode, unittest.INSERT)


class TestStateResettingState(unittest.ViewTestCase):

    def test_reset_sequence(self):
        self.state.sequence = 'x'
        self.state.reset_sequence()
        self.assertEqual(self.state.sequence, '')

    def test_reset_command_data(self):
        self.state.sequence = 'abc'
        self.state.partial_sequence = 'x'
        self.state.user_input = 'f'
        self.state.action = cmd_defs.ViReplaceCharacters()
        self.state.motion = cmd_defs.ViGotoSymbolInFile()
        self.state.action_count = '10'
        self.state.motion_count = '100'
        self.state.register = 'a'
        self.state.must_capture_register_name = True

        self.state.reset_command_data()

        self.assertEqual(self.state.action, None)
        self.assertEqual(self.state.motion, None)
        self.assertEqual(self.state.action_count, '')
        self.assertEqual(self.state.motion_count, '')

        self.assertEqual(self.state.sequence, '')
        self.assertEqual(self.state.partial_sequence, '')
        self.assertEqual(self.state.register, '"')
        self.assertEqual(self.state.must_capture_register_name, False)


class TestStateResettingVolatileData(unittest.ViewTestCase):

    def test_reset_volatile_data(self):
        self.state.glue_until_normal_mode = True
        self.state.processing_notation = True
        self.state.non_interactive = True
        set_reset_during_init(self.view, False)

        self.state.reset_volatile_data()

        self.assertFalse(self.state.glue_until_normal_mode)
        self.assertFalse(self.state.processing_notation)
        self.assertFalse(self.state.non_interactive)
        self.assertTrue(get_reset_during_init(self.view))


class TestStateCounts(unittest.ViewTestCase):

    def test_can_retrieve_good_action_count(self):
        self.state.action_count = '10'
        self.assertEqual(self.state.count, 10)

    def test_fails_if_bad_action_count(self):
        def set_count():
            self.state.action_count = 'x'
        self.assertRaises(AssertionError, set_count)

    def test_fails_if_bad_motion_count(self):
        def set_count():
            self.state.motion_count = 'x'
        self.assertRaises(AssertionError, set_count)

    def test_count_is_never_less_than1(self):
        self.state.motion_count = '0'
        self.assertEqual(self.state.count, 1)

        def set_count():
            self.state.motion_count = '-1'

        self.assertRaises(AssertionError, set_count)

    def test_can_retrieve_good_motion_count(self):
        self.state.motion_count = '10'
        self.assertEqual(self.state.count, 10)

    def test_can_retrieve_good_combined_count(self):
        self.state.motion_count = '10'
        self.state.action_count = '10'
        self.assertEqual(self.state.count, 100)


class TestStateRunnability(unittest.ViewTestCase):

    def test_runnable_if_action_and_motion_available(self):
        self.state.mode = unittest.NORMAL
        self.state.action = cmd_defs.ViDeleteLine()
        self.state.motion = cmd_defs.ViMoveRightByChars()
        self.assertEqual(self.state.runnable(), True)

    def test_runnable_raises_exception_if_action_and_motion_available_but_has_invalid_mode(self):
        self.state.mode = 'foobar'
        self.state.action = cmd_defs.ViDeleteByChars()
        self.state.motion = cmd_defs.ViMoveRightByChars()
        self.assertRaisesRegex(ValueError, 'invalid mode', self.state.runnable)

    def test_runnable_if_action_available(self):
        self.state.mode = unittest.NORMAL
        self.state.action = cmd_defs.ViDeleteLine()
        self.assertEqual(self.state.runnable(), True)
        self.state.action = cmd_defs.ViDeleteByChars()
        self.assertEqual(self.state.runnable(), False)

    def test_runnable_raises_exception_if_action_available_but_has_invalid_mode(self):
        self.state.mode = unittest.OPERATOR_PENDING
        self.state.action = cmd_defs.ViDeleteLine()
        self.assertRaisesRegex(ValueError, 'action has invalid mode', self.state.runnable)

    def test_runnable_if_action_motion_not_required_in_visual_returns_true(self):
        self.state.mode = unittest.VISUAL
        self.state.action = cmd_defs.ViDeleteLine()
        self.assertEqual(self.state.runnable(), True)

    def test_runnable_if_action_motion_not_required_not_visual_returns_true(self):
        self.state.mode = unittest.NORMAL
        self.state.action = cmd_defs.ViDeleteLine()
        self.assertEqual(self.state.runnable(), True)

    def test_runnable_if_action_motion_is_required_in_visual_returns_true(self):
        self.state.mode = unittest.VISUAL
        self.state.action = cmd_defs.ViDeleteByChars()
        self.assertEqual(self.state.runnable(), True)

    def test_runnable_if_action_motion_is_required_not_in_visual_returns_false(self):
        self.state.mode = unittest.NORMAL
        self.state.action = cmd_defs.ViDeleteByChars()
        self.assertEqual(self.state.runnable(), False)

    def test_runnable_if_motion_available(self):
        self.state.mode = unittest.NORMAL
        self.state.motion = cmd_defs.ViMoveRightByChars()
        self.assertEqual(self.state.runnable(), True)

    def test_runnable_raises_exception_if_motion_available_but_has_invalid_mode(self):
        self.state.mode = unittest.OPERATOR_PENDING
        self.state.motion = cmd_defs.ViMoveRightByChars()
        self.assertRaisesRegex(ValueError, 'motion has invalid mode', self.state.runnable)


class TestStateSetCommand(unittest.ViewTestCase):

    def test_raise_error_if_unknown_command_type(self):
        fake_command = {'type': 'foo'}
        self.assertRaises(AssertionError, self.state.set_command, fake_command)

    def test_raises_error_if_too_many_motions(self):
        self.state.motion = cmd_defs.ViMoveRightByChars()

        self.assertRaises(ValueError, self.state.set_command, cmd_defs.ViMoveRightByChars())

    def test_changes_mode_for_lone_motion(self):
        self.state.mode = unittest.OPERATOR_PENDING

        motion = cmd_defs.ViMoveRightByChars()
        self.state.set_command(motion)

        self.assertEqual(self.state.mode, unittest.NORMAL)

    def test_raises_error_if_too_many_actions(self):
        self.state.motion = cmd_defs.ViDeleteLine()

        self.assertRaises(ValueError, self.state.set_command, cmd_defs.ViDeleteLine())

    def test_changes_mode_for_lone_action(self):
        operator = cmd_defs.ViDeleteByChars()

        self.state.set_command(operator)

        self.assertEqual(self.state.mode, unittest.OPERATOR_PENDING)
