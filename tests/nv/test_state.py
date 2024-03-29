# Copyright (C) 2018-2023 The NeoVintageous Team (NeoVintageous).
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

from NeoVintageous.nv.feed_key import FeedKeyHandler
from NeoVintageous.nv.settings import append_sequence
from NeoVintageous.nv.settings import get_action_count
from NeoVintageous.nv.settings import get_capture_register
from NeoVintageous.nv.settings import get_count
from NeoVintageous.nv.settings import get_glue_until_normal_mode
from NeoVintageous.nv.settings import get_last_char_search_character
from NeoVintageous.nv.settings import get_last_char_search_command
from NeoVintageous.nv.settings import get_last_search_pattern
from NeoVintageous.nv.settings import get_mode
from NeoVintageous.nv.settings import get_motion_count
from NeoVintageous.nv.settings import get_partial_sequence
from NeoVintageous.nv.settings import get_register
from NeoVintageous.nv.settings import get_reset_during_init
from NeoVintageous.nv.settings import get_sequence
from NeoVintageous.nv.settings import is_interactive
from NeoVintageous.nv.settings import is_processing_notation
from NeoVintageous.nv.settings import set_action_count
from NeoVintageous.nv.settings import set_capture_register
from NeoVintageous.nv.settings import set_mode
from NeoVintageous.nv.settings import set_motion_count
from NeoVintageous.nv.settings import set_partial_sequence
from NeoVintageous.nv.settings import set_register
from NeoVintageous.nv.state import _should_scroll_into_view
from NeoVintageous.nv.state import get_action
from NeoVintageous.nv.state import get_motion
from NeoVintageous.nv.state import init_view
from NeoVintageous.nv.state import is_runnable
from NeoVintageous.nv.state import reset_command_data
from NeoVintageous.nv.state import set_action
from NeoVintageous.nv.state import set_motion
from NeoVintageous.nv.vi import cmd_defs
from NeoVintageous.nv.vi.cmd_base import ViCommandDefBase


class TestState(unittest.ViewTestCase):

    def test_init_view_on_invalid_view(self):
        panel = self.view.window().create_output_panel('test_invalid_state', unlisted=True)  # type: ignore[union-attr]
        panel.settings().set('is_widget', True)
        panel.settings().set('command_mode', True)
        panel.settings().set('inverse_caret_state', True)
        panel.settings().set('vintage', True)
        init_view(panel)
        self.assertIsNone(panel.settings().get('command_mode'))
        self.assertIsNone(panel.settings().get('inverse_caret_state'))
        self.assertIsNone(panel.settings().get('vintage'))

    @unittest.mock_session()
    def test_can_initialize(self):
        # Make sure the actual usage of NeoVintageous doesn't change the
        # pristine state. This isn't great, though.

        # DEPRECATED
        self.view.window().settings().erase('_vintageous_last_char_search_command')  # type: ignore[union-attr]
        self.view.window().settings().erase('_vintageous_last_char_search_character')  # type: ignore[union-attr]
        self.view.window().settings().erase('_vintageous_last_buff_search_command')  # type: ignore[union-attr]
        self.view.window().settings().erase('_vintageous_last_buff_search_pattern')  # type: ignore[union-attr]
        self.view.window().settings().erase('_vintageous_last_search_pattern')  # type: ignore[union-attr]
        self.view.window().settings().erase('_vintageous_last_search_pattern_command')  # type: ignore[union-attr]

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
        self.assertEqual(get_last_char_search_character(self.view), '')
        self.assertEqual(get_last_char_search_command(self.view), 'vi_f')
        self.assertEqual(is_interactive(self.view), True)
        self.assertEqual(get_capture_register(self.view), False)
        self.assertEqual(get_last_search_pattern(self.view), '')
        self.assertEqual(get_reset_during_init(self.view), True)

    def test_must_scroll_into_view(self):
        self.assertFalse(_should_scroll_into_view(get_motion(self.view), get_action(self.view)))

        motion = cmd_defs.ViGotoSymbolInFile()
        set_motion(self.view, motion)
        self.assertTrue(_should_scroll_into_view(get_motion(self.view), get_action(self.view)))


class TestStateResettingState(unittest.ViewTestCase):

    def test_reset_command_data(self):
        append_sequence(self.view, 'abc')
        set_partial_sequence(self.view, 'x')
        set_action(self.view, cmd_defs.ViReplaceCharacters())
        set_motion(self.view, cmd_defs.ViGotoSymbolInFile())
        set_action_count(self.view, '10')
        set_motion_count(self.view, '100')
        set_register(self.view, 'a')
        set_capture_register(self.view, True)

        reset_command_data(self.view)

        self.assertEqual(get_action(self.view), None)
        self.assertEqual(get_motion(self.view), None)
        self.assertEqual(get_action_count(self.view), '')
        self.assertEqual(get_motion_count(self.view), '')

        self.assertEqual(get_sequence(self.view), '')
        self.assertEqual(get_partial_sequence(self.view), '')
        self.assertEqual(get_register(self.view), '"')
        self.assertEqual(get_capture_register(self.view), False)


class TestStateCounts(unittest.ViewTestCase):

    def test_can_retrieve_good_action_count(self):
        set_action_count(self.view, '10')
        self.assertEqual(get_count(self.view), 10)

    def test_count_is_never_less_than1(self):
        set_motion_count(self.view, '0')
        self.assertEqual(get_count(self.view), 1)

    def test_can_retrieve_good_motion_count(self):
        set_motion_count(self.view, '10')
        self.assertEqual(get_count(self.view), 10)

    def test_can_retrieve_good_combined_count(self):
        set_motion_count(self.view, '10')
        set_action_count(self.view, '10')
        self.assertEqual(get_count(self.view), 100)

    def test_adding_action_count_concatinates_str_not_int_addition(self):
        # NOTE motion/action counts need to be cast to strings because they need
        # to be "joined" to the previous key press, not added. For example when
        # you press the digit 1 followed by 2, it's a count of 12, not 3.
        set_action_count(self.view, '1')
        set_action_count(self.view, get_action_count(self.view) + '2')
        self.assertEqual('12', get_action_count(self.view))
        set_action_count(self.view, get_action_count(self.view) + '3')
        self.assertEqual('123', get_action_count(self.view))
        with self.assertRaisesRegex(TypeError, self._get_type_error()):
            set_action_count(self.view, get_action_count(self.view) + 4)  # type: ignore[operator]

    def test_adding_motion_count_concatinates_str_not_int_addition(self):
        # NOTE motion/action counts need to be cast to strings because they need
        # to be "joined" to the previous key press, not added. For example when
        # you press the digit 1 followed by 2, it's a count of 12, not 3.
        set_motion_count(self.view, '1')
        set_motion_count(self.view, get_motion_count(self.view) + '2')
        self.assertEqual('12', get_motion_count(self.view))
        set_motion_count(self.view, get_motion_count(self.view) + '3')
        self.assertEqual('123', get_motion_count(self.view))
        with self.assertRaisesRegex(TypeError, self._get_type_error()):
            set_motion_count(self.view, get_motion_count(self.view) + 4)  # type: ignore[operator]

    def _get_type_error(self) -> str:
        if unittest.ST_VERSION < 4000:
            return 'Can\'t convert \'int\' object to str'

        return 'can only concatenate str'


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
        self.handler = FeedKeyHandler(self.view, 'w', 0, True, False)

    def test_raise_error_if_unknown_command_type(self):
        with self.assertRaisesRegex(ValueError, 'unexpected command type'):
            self.handler._handle_command('foobar', True)  # type: ignore[arg-type]

    def test_unexpected_type(self):
        class Foobar(ViCommandDefBase):
            pass

        with self.assertRaisesRegex(ValueError, 'unexpected command type'):
            self.handler._handle_command(Foobar(), True)

    def test_raises_error_if_too_many_motions(self):
        set_motion(self.view, cmd_defs.ViMoveRightByChars())
        with self.assertRaisesRegex(ValueError, 'too many motions'):
            self.handler._handle_command(cmd_defs.ViMoveRightByChars(), True)

    def test_changes_mode_for_lone_motion(self):
        set_mode(self.view, unittest.OPERATOR_PENDING)
        motion = cmd_defs.ViMoveRightByChars()
        self.handler._handle_command(motion, True)
        self.assertEqual(get_mode(self.view), unittest.NORMAL)

    def test_raises_error_if_too_many_actions(self):
        set_motion(self.view, cmd_defs.ViDeleteLine())
        with self.assertRaisesRegex(ValueError, 'too many actions'):
            self.handler._handle_command(cmd_defs.ViDeleteLine(), True)

    def test_changes_mode_for_lone_action(self):
        operator = cmd_defs.ViDeleteByChars()
        self.handler._handle_command(operator, True)
        self.assertEqual(get_mode(self.view), unittest.OPERATOR_PENDING)
