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

from NeoVintageous.nv.commands import nv_feed_key
from NeoVintageous.nv.settings import append_sequence
from NeoVintageous.nv.settings import get_action_count
from NeoVintageous.nv.settings import get_count
from NeoVintageous.nv.settings import get_glue_until_normal_mode
from NeoVintageous.nv.settings import get_last_buffer_search
from NeoVintageous.nv.settings import get_last_char_search
from NeoVintageous.nv.settings import get_last_char_search_command
from NeoVintageous.nv.settings import get_mode
from NeoVintageous.nv.settings import get_motion_count
from NeoVintageous.nv.settings import get_partial_sequence
from NeoVintageous.nv.settings import get_register
from NeoVintageous.nv.settings import get_reset_during_init
from NeoVintageous.nv.settings import get_sequence
from NeoVintageous.nv.settings import is_interactive
from NeoVintageous.nv.settings import is_must_capture_register_name
from NeoVintageous.nv.settings import is_processing_notation
from NeoVintageous.nv.settings import set_action_count
from NeoVintageous.nv.settings import set_mode
from NeoVintageous.nv.settings import set_motion_count
from NeoVintageous.nv.settings import set_must_capture_register_name
from NeoVintageous.nv.settings import set_partial_sequence
from NeoVintageous.nv.settings import set_register
from NeoVintageous.nv.state import _must_scroll_into_view
from NeoVintageous.nv.state import get_action
from NeoVintageous.nv.state import get_motion
from NeoVintageous.nv.state import is_runnable
from NeoVintageous.nv.state import reset_command_data
from NeoVintageous.nv.state import set_action
from NeoVintageous.nv.state import set_motion
from NeoVintageous.nv.vi import cmd_defs
from NeoVintageous.nv.vi.cmd_base import ViCommandDefBase


class TestState(unittest.ViewTestCase):

    def test_can_initialize(self):
        # Make sure the actual usage of NeoVintageous doesn't change the
        # pristine state. This isn't great, though.
        self.view.window().settings().erase('_vintageous_last_char_search_command')
        self.view.window().settings().erase('_vintageous_last_char_search')
        self.view.window().settings().erase('_vintageous_last_buffer_search')

        self.assertEqual(get_sequence(self.view), '')
        self.assertEqual(get_partial_sequence(self.view), '')

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
            self.assertEqual(get_mode(self.view), unittest.NORMAL)
        except AssertionError:
            self.assertEqual(get_mode(self.view), unittest.UNKNOWN)

        self.assertEqual(get_action(self.view), None)
        self.assertEqual(get_motion(self.view), None)
        self.assertEqual(get_action_count(self.view), '')
        self.assertEqual(get_glue_until_normal_mode(self.view), False)
        self.assertEqual(is_processing_notation(self.view), False)
        self.assertEqual(get_last_char_search(self.view), '')
        self.assertEqual(get_last_char_search_command(self.view), 'vi_f')
        self.assertEqual(is_interactive(self.view), True)
        self.assertEqual(is_must_capture_register_name(self.view), False)
        self.assertEqual(get_last_buffer_search(self.view), '')
        self.assertEqual(get_reset_during_init(self.view), True)

    def test_must_scroll_into_view(self):
        self.assertFalse(_must_scroll_into_view(get_motion(self.view), get_action(self.view)))

        motion = cmd_defs.ViGotoSymbolInFile()
        set_motion(self.view, motion)
        self.assertTrue(_must_scroll_into_view(get_motion(self.view), get_action(self.view)))


class TestStateResettingState(unittest.ViewTestCase):

    def test_reset_command_data(self):
        append_sequence(self.view, 'abc')
        set_partial_sequence(self.view, 'x')
        set_action(self.view, cmd_defs.ViReplaceCharacters())
        set_motion(self.view, cmd_defs.ViGotoSymbolInFile())
        set_action_count(self.view, '10')
        set_motion_count(self.view, '100')
        set_register(self.view, 'a')
        set_must_capture_register_name(self.view, True)

        reset_command_data(self.view)

        self.assertEqual(get_action(self.view), None)
        self.assertEqual(get_motion(self.view), None)
        self.assertEqual(get_action_count(self.view), '')
        self.assertEqual(get_motion_count(self.view), '')

        self.assertEqual(get_sequence(self.view), '')
        self.assertEqual(get_partial_sequence(self.view), '')
        self.assertEqual(get_register(self.view), '"')
        self.assertEqual(is_must_capture_register_name(self.view), False)


class TestStateCounts(unittest.ViewTestCase):

    def test_can_retrieve_good_action_count(self):
        set_action_count(self.view, '10')
        self.assertEqual(get_count(self.view), 10)

    def test_fails_if_bad_action_count(self):
        def set_count():
            set_action_count(self.view, 'x')
        self.assertRaises(ValueError, set_count)

    def test_fails_if_bad_motion_count(self):
        def set_count():
            set_motion_count(self.view, 'x')
        self.assertRaises(ValueError, set_count)

    def test_count_is_never_less_than1(self):
        set_motion_count(self.view, '0')
        self.assertEqual(get_count(self.view), 1)

        def set_count():
            set_motion_count(self.view, '-1')

        self.assertRaises(ValueError, set_count)

    def test_can_retrieve_good_motion_count(self):
        set_motion_count(self.view, '10')
        self.assertEqual(get_count(self.view), 10)

    def test_can_retrieve_good_combined_count(self):
        set_motion_count(self.view, '10')
        set_action_count(self.view, '10')
        self.assertEqual(get_count(self.view), 100)


class TestStateRunnability(unittest.ViewTestCase):

    def test_runnable_if_action_and_motion_available(self):
        set_mode(self.view, unittest.NORMAL)
        set_action(self.view, cmd_defs.ViDeleteLine())
        set_motion(self.view, cmd_defs.ViMoveRightByChars())
        self.assertEqual(is_runnable(self.view), True)

    def test_runnable_raises_exception_if_action_and_motion_available_but_has_invalid_mode(self):
        set_mode(self.view, 'foobar')
        set_action(self.view, cmd_defs.ViDeleteByChars())
        set_motion(self.view, cmd_defs.ViMoveRightByChars())
        with self.assertRaisesRegex(ValueError, 'invalid mode'):
            is_runnable(self.view)

    def test_runnable_if_action_available(self):
        set_mode(self.view, unittest.NORMAL)
        set_action(self.view, cmd_defs.ViDeleteLine())
        self.assertEqual(is_runnable(self.view), True)
        set_action(self.view, cmd_defs.ViDeleteByChars())
        self.assertEqual(is_runnable(self.view), False)

    def test_runnable_raises_exception_if_action_available_but_has_invalid_mode(self):
        set_mode(self.view, unittest.OPERATOR_PENDING)
        set_action(self.view, cmd_defs.ViDeleteLine())
        with self.assertRaisesRegex(ValueError, 'action has invalid mode'):
            is_runnable(self.view)

    def test_runnable_if_action_motion_not_required_in_visual_returns_true(self):
        set_mode(self.view, unittest.VISUAL)
        set_action(self.view, cmd_defs.ViDeleteLine())
        self.assertEqual(is_runnable(self.view), True)

    def test_runnable_if_action_motion_not_required_not_visual_returns_true(self):
        set_mode(self.view, unittest.NORMAL)
        set_action(self.view, cmd_defs.ViDeleteLine())
        self.assertEqual(is_runnable(self.view), True)

    def test_runnable_if_action_motion_is_required_in_visual_returns_true(self):
        set_mode(self.view, unittest.VISUAL)
        set_action(self.view, cmd_defs.ViDeleteByChars())
        self.assertEqual(is_runnable(self.view), True)

    def test_runnable_if_action_motion_is_required_not_in_visual_returns_false(self):
        set_mode(self.view, unittest.NORMAL)
        set_action(self.view, cmd_defs.ViDeleteByChars())
        self.assertEqual(is_runnable(self.view), False)

    def test_runnable_if_motion_available(self):
        set_mode(self.view, unittest.NORMAL)
        set_motion(self.view, cmd_defs.ViMoveRightByChars())
        self.assertEqual(is_runnable(self.view), True)

    def test_runnable_raises_exception_if_motion_available_but_has_invalid_mode(self):
        set_mode(self.view, unittest.OPERATOR_PENDING)
        set_motion(self.view, cmd_defs.ViMoveRightByChars())
        with self.assertRaisesRegex(ValueError, 'motion has invalid mode'):
            is_runnable(self.view)


class TestStateSetCommand(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        self.command = nv_feed_key(self.view.window())
        self.command.view = self.view

    def test_raise_error_if_unknown_command_type(self):
        with self.assertRaisesRegex(ValueError, 'unexpected command type'):
            self.command._handle_command('foobar', True)

    def test_unexpected_type(self):
        class Foobar(ViCommandDefBase):
            pass

        with self.assertRaisesRegex(ValueError, 'unexpected command type'):
            self.command._handle_command(Foobar(), True)

    def test_raises_error_if_too_many_motions(self):
        set_motion(self.view, cmd_defs.ViMoveRightByChars())
        with self.assertRaisesRegex(ValueError, 'too many motions'):
            self.command._handle_command(cmd_defs.ViMoveRightByChars(), True)

    def test_changes_mode_for_lone_motion(self):
        set_mode(self.view, unittest.OPERATOR_PENDING)
        motion = cmd_defs.ViMoveRightByChars()
        self.command._handle_command(motion, True)
        self.assertEqual(get_mode(self.view), unittest.NORMAL)

    def test_raises_error_if_too_many_actions(self):
        set_motion(self.view, cmd_defs.ViDeleteLine())
        with self.assertRaisesRegex(ValueError, 'too many actions'):
            self.command._handle_command(cmd_defs.ViDeleteLine(), True)

    def test_changes_mode_for_lone_action(self):
        operator = cmd_defs.ViDeleteByChars()
        self.command._handle_command(operator, True)
        self.assertEqual(get_mode(self.view), unittest.OPERATOR_PENDING)
