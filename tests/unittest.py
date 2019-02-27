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

from unittest import mock  # noqa: F401
from unittest import skipIf  # noqa: F401
from unittest import TestCase  # noqa: F401
import os
import unittest

# Use aliases to indicate that they are not public testing APIs.
from sublime import active_window as _active_window
from sublime import Region

# Use aliases to indicate that they are not public testing APIs.
from NeoVintageous.nv.ex_cmds import do_ex_cmdline as _do_ex_cmdline
from NeoVintageous.nv.state import State as _State

from NeoVintageous.nv.vi import registers
from NeoVintageous.nv.vim import INSERT  # noqa: F401
from NeoVintageous.nv.vim import INTERNAL_NORMAL  # noqa: F401
from NeoVintageous.nv.vim import NORMAL  # noqa: F401
from NeoVintageous.nv.vim import OPERATOR_PENDING  # noqa: F401
from NeoVintageous.nv.vim import REPLACE  # noqa: F401
from NeoVintageous.nv.vim import SELECT  # noqa: F401
from NeoVintageous.nv.vim import UNKNOWN  # noqa: F401
from NeoVintageous.nv.vim import VISUAL  # noqa: F401
from NeoVintageous.nv.vim import VISUAL_BLOCK  # noqa: F401
from NeoVintageous.nv.vim import VISUAL_LINE  # noqa: F401


class ViewTestCase(unittest.TestCase):

    def setUp(self):
        self.view = _active_window().new_file()

    def tearDown(self):
        if self.view:
            self.view.set_scratch(True)
            self.view.close()

    def content(self):
        # type: () -> str
        return self.view.substr(Region(0, self.view.size()))

    def Region(self, a, b=None):
        # Return a Region with initial values a and b.
        #
        # This method can save having to import `sublime.Region` into test
        # modules.
        #
        # Args:
        #   a (int):
        #       The first end of the region.
        #   b (int):
        #       The second end of the region. Defaults to the same as the a end
        #       of the region. May be less that a, in which case the region is a
        #       reversed one.
        return Region(a, b)

    def select(self, selections):
        # Create selection in the view.
        #
        # Args:
        #   selections (int|tuple|Region|list<int|tuple|Region>)
        #
        # Existing selections are cleared.
        #
        # Integers and tuples are converted to Regions:
        # >>> select(3) is the short for: select(sublime.Region(3))
        # >>> select((3, 5)) is short for: select(sublime.Region(3, 5))
        #
        # Select a single point:
        # >>> select(3)
        #
        # Select a region of text e.g. from point 3 to 5:
        # >>> select((3, 5))
        #
        # Select multiple point selections:
        # >>> select([3, 5, 7])
        #
        # Select multiple text selections:
        # >>> select([(3, 5), (7, 11)])
        #
        # Select multiple points, and text selections:
        # >>> select([3, 5, (7, 11), 17, (19, 23)])

        self.view.sel().clear()

        if not isinstance(selections, list):
            selections = [selections]

        for selection in selections:
            if isinstance(selection, tuple):
                self.view.sel().add(Region(selection[0], selection[1]))
            else:
                self.view.sel().add(selection)

    def settings(self):
        return self.view.settings()

    def fixturePath(self, *args):
        return os.path.join(os.path.dirname(__file__), 'fixtures', *args)

    def write(self, text):
        # type: (str) -> None
        self.view.run_command('_nv_test_write', {'text': text})

    def _setupView(self, text, mode, reverse=False):
        if mode in (VISUAL, VISUAL_BLOCK, VISUAL_LINE, INTERNAL_NORMAL):
            self.view.run_command('_nv_test_write', {'text': text.replace('|', '')})
            sels = [i for i, c in enumerate(text) if c == '|']
            sel_len = len(sels)

            if sel_len == 1:
                sels.append(sels[0] + 2)
            elif sel_len % 2 != 0 or sel_len == 0:
                raise Exception('invalid visual selection')

            if sels:
                v_sels = []  # type: list
                a = None
                for i, x in enumerate(sels):
                    if a is None:
                        a = x - i
                    else:
                        v_sels.append(Region(a, x - i))
                        a = None

                self.view.sel().clear()

                if reverse:
                    v_sels.sort(reverse=True)
                    for s in v_sels:
                        self.view.sel().add(Region(s.b, s.a))
                else:
                    self.view.sel().add_all(v_sels)

            # This is required, because the cursor in VISUAL mode is a block
            # cursor. Without this setting some tests will pass when the window
            # running the tests has focus, and fail when it doesn't have focus.
            # This happens because ST doesn't fire events for views (test views)
            # when the window loses focus: the on_activated() event fixes VISUAL
            # mode selections that don't have a correct caret state.
            self.view.settings().set('inverse_caret_state', True)
        else:
            self.view.run_command('_nv_test_write', {'text': text.replace('|', '')})
            sels = [i for i, c in enumerate(text) if c == '|']
            if sels:
                self.view.sel().clear()
                for i, x in enumerate(sels):
                    self.view.sel().add(x - i)

        self.state.mode = mode

    def normal(self, text):
        self._setupView(text, NORMAL)

    def insert(self, text):
        self._setupView(text, INSERT)

    def internalNormal(self, text):
        self._setupView(text, INTERNAL_NORMAL)

    def rInternalNormal(self, text):
        self._setupView(text, INTERNAL_NORMAL, reverse=True)

    def visual(self, text):
        self._setupView(text, VISUAL)

    def rvisual(self, text):
        self._setupView(text, VISUAL, reverse=True)

    def vline(self, text):
        self._setupView(text, VISUAL_LINE)

    def rvline(self, text):
        self._setupView(text, VISUAL_LINE, reverse=True)

    def vblock(self, text):
        self._setupView(text, VISUAL_BLOCK)

    def rvblock(self, text):
        self._setupView(text, VISUAL_BLOCK, reverse=True)

    def vselect(self, text):
        self._setupView(text, SELECT)

    def rvselect(self, text):
        self._setupView(text, SELECT, reverse=True)

    def register(self, name, value=None, linewise=False):
        # Args:
        #   name (str)
        #   value (str)
        if value is None:
            value = name[1:]
            name = name[0]
        elif not isinstance(value, str):
            raise ValueError('argument #2 is not a valid str')

        if name.isdigit() and name != '0':
            registers._set_numbered_register(name, value)
        else:
            registers._data[name] = [value]
            registers._linewise[name] = linewise

    def resetRegisters(self):
        registers._reset_data()

    def _assertViewContent(self, sels, expected, msg=None):
        content = list(self.view.substr(Region(0, self.view.size())))
        counter = 0
        for sel in sels:
            content.insert(sel.begin() + counter, '|')
            counter += 1
            if sel.end() != sel.begin():
                content.insert(sel.end() + counter, '|')
                counter += 1

        self.assertEquals(''.join(content), expected, msg)

    def _assertViewRegionsContent(self, key, expected, msg=None):
        self._assertViewContent(self.view.get_regions(key), expected, msg)

    def _assertViewSelectionContent(self, expected, msg):
        self._assertViewContent(self.view.sel(), expected, msg)

    def _assertView(self, expected, mode, msg):
        self._assertViewSelectionContent(expected, msg)
        self._assertMode(mode)

    def assertSearch(self, expected: str, msg=None):
        self._assertViewRegionsContent('vi_search', expected, msg)
        self._assertMode(NORMAL)

    def assertSearchCurrent(self, expected: str, msg=None):
        self._assertViewRegionsContent('vi_search_current', expected, msg)
        self._assertMode(NORMAL)

    def assertNormal(self, expected, msg=None):
        self._assertView(expected, NORMAL, msg)
        for sel in self.view.sel():
            self.assertTrue(sel.b == sel.a, 'failed asserting selection is a valid NORMAL mode selection')

    def assertInsert(self, expected, msg=None):
        self._assertView(expected, INSERT, msg)
        for sel in self.view.sel():
            self.assertTrue(sel.b == sel.a, 'failed asserting selection is a valid INSERT mode selection')

    def assertReplace(self, expected, msg=None):
        self._assertView(expected, REPLACE, msg)
        for sel in self.view.sel():
            self.assertTrue(sel.b == sel.a, 'failed asserting selection is a valid REPLACE mode selection')

    def assertInternalNormal(self, expected, strict=False, msg=None):
        self._assertViewSelectionContent(expected, msg)
        self._assertMode(INTERNAL_NORMAL if strict else NORMAL)
        self.assertSelectionIsNotReversed()

    def assertRInternalNormal(self, expected, strict=False, msg=None):
        self._assertViewSelectionContent(expected, msg)
        self._assertMode(INTERNAL_NORMAL if strict else NORMAL)
        self.assertSelectionIsReversed()

    def assertVisual(self, expected, msg=None):
        self._assertView(expected, VISUAL, msg)
        self.assertSelectionIsNotReversed()

    def assertRVisual(self, expected, msg=None):
        self._assertView(expected, VISUAL, msg)
        self.assertSelectionIsReversed()

    def assertVline(self, expected, msg=None):
        self._assertView(expected, VISUAL_LINE, msg)
        self.assertSelectionIsNotReversed()

    def assertRVline(self, expected, msg=None):
        self._assertView(expected, VISUAL_LINE, msg)
        self.assertSelectionIsReversed()

    def assertVblock(self, expected, msg=None):
        self._assertView(expected, VISUAL_BLOCK, msg)
        self.assertSelectionIsNotReversed()

    def assertRVblock(self, expected, msg=None):
        self._assertView(expected, VISUAL_BLOCK, msg)
        self.assertSelectionIsReversed()

    def assertVSelect(self, expected, msg=None):
        self._assertView(expected, SELECT, msg)
        self.assertSelectionIsNotReversed()

    def assertRVSelect(self, expected, msg=None):
        self._assertView(expected, SELECT, msg)
        self.assertSelectionIsReversed()

    def assertContent(self, expected, msg=None):
        # Test that view contents and *expected* are equal.
        #
        # Args:
        #   expected (str):
        #       The expected contents of the view.
        #   msg (str, optional):
        #       If specified, is used as the error message on failure.
        self.assertEqual(self.content(), expected, msg)

    def assertContentRegex(self, expected, msg=None):
        # Test that view contents matches (or does not match) *expected*.
        #
        # Args:
        #   expected (str):
        #       Regular expression that should match view contents.
        #   msg (str):
        #       If specified, is used as the error message on failure.
        self.assertRegex(self.content(), expected, msg=msg)

    def _assertMode(self, mode):
        self.assertEquals(self.state.mode, mode)

    def assertInsertMode(self):
        self._assertMode(INSERT)

    def assertInternalNormalMode(self):
        self._assertMode(INTERNAL_NORMAL)

    def assertNormalMode(self):
        self._assertMode(NORMAL)

    def assertVisualMode(self):
        self._assertMode(VISUAL)

    def assertVblockMode(self):
        self._assertMode(VISUAL_BLOCK)

    def assertVlineMode(self):
        self._assertMode(VISUAL_LINE)

    def assertRegion(self, actual, expected):
        # Test that *actual* and *expected* are equal.
        #
        # Args:
        #   actual (Region):
        #       The actual region.
        #   expected (str|int|tuple|Region):
        #       If the expected value is a str, int, or a tuple, it will be
        #       converted to a Region before evaluating against the actual
        #       value.
        if isinstance(expected, int):
            self.assertEqual(actual, Region(expected))
        elif isinstance(expected, tuple):
            self.assertEqual(actual, Region(expected[0], expected[1]))
        elif isinstance(expected, str):
            self.assertEqual(self.view.substr(actual), expected)
        else:
            self.assertIsInstance(actual, Region)
            self.assertEqual(actual, expected)

    def _assertRegister(self, name, expected, linewise, msg):
        if expected is not None and not isinstance(expected, list):
            expected = [expected]

        self.assertEqual(self.state.registers[name], expected, msg or 'register = "' + name)
        if expected is not None:
            # FIXME digit registers linewise state is not implemented properly yet
            if not name.isdigit():
                self.assertEqual(registers._linewise[name], linewise, msg or 'linewise register = "' + name)

    def assertRegister(self, name, expected=None, linewise=False, msg=None):
        # Test that the value of the named register and *expected* are equal.
        #
        # Args:
        #   name (str):
        #       The name of the register.
        #   expected (str)
        if expected is None:
            expected = name[1:]
            name = name[0]

        self._assertRegister(name, expected, linewise, msg)

    def assertRegisterIsNone(self, name, linewise=False, msg=None):
        self._assertRegister(name, None, linewise, msg)

    def assertSelection(self, expected, msg=None):
        # Test that view selection and *expected* are equal.
        #
        # Args:
        #   expected (int|tuple|Region|list<Region>)
        #   msg (str)
        #
        # Integers and tuples are converted to Regions:
        # >>> assertSelection(3) is the short for: assertSelection(sublime.Region(3))
        # >>> assertSelection((3, 5)) is short for: assertSelection(sublime.Region(3, 5))
        #
        # Assert that the view has one point selection:
        # >>> self.assertSelection(3)
        #
        # Assert that the view has multiple point selections:
        # >>> self.assertSelection([3, 5, 7])
        #
        # Assert that the view has a text area selection:
        # >>> self.assertSelection((3, 5))
        #
        # Assert that the view has multiple text selections:
        # >>> self.assertSelection([(3, 5), (7, 9))
        #
        # Assert that the view has multiple points, and text selections:
        # >>> self.assertSelection([3, 5, (7, 11)])
        if isinstance(expected, int):
            self.assertEqual([Region(expected)], list(self.view.sel()), msg)
        elif isinstance(expected, tuple):
            self.assertEqual([Region(expected[0], expected[1])], list(self.view.sel()), msg)
        elif isinstance(expected, Region):
            self.assertEqual([expected], list(self.view.sel()), msg)
        else:
            # Defaults to expect a list of Regions.
            self.assertEqual(expected, list(self.view.sel()), msg)

    def assertSelectionCount(self, expected):
        # Test that view selection count and *expected* are equal.
        #
        # Args:
        #   expected (int):
        #       The expected number of selections in view.
        self.assertEqual(expected, len(self.view.sel()))

    def assertSelectionIsNotReversed(self):
        for sel in self.view.sel():
            self.assertTrue(sel.b >= sel.a, 'failed asserting selection is not reversed')

    def assertSelectionIsReversed(self):
        for sel in self.view.sel():
            self.assertGreater(sel.a, sel.b, 'failed asserting selection is reversed')

    # def assertSelectionIsNotReversed(self):

    def assertSize(self, expected):
        # Test that number of view characters and *expected* are equal.
        #
        # Args:
        #   expected (int):
        #       The expected number of characters in view.
        self.assertEqual(expected, self.view.size())

    def assertStatusLineRegex(self, expected, msg=None):
        # Test that view contents matches (or does not match) *expected*.
        #
        # Args:
        #   expected (str):
        #       Regular expression that should match view contents.
        #   msg (str):
        #       If specified, is used as the error message on failure.
        self.assertRegex(self.view.get_status('vim-mode') + ' ' + self.view.get_status('vim-seq'), expected, msg=msg)

    def assertStatusLineIsBlank(self, msg=None):
        self.assertStatusLineRegex('', msg)

    def assertStatusLineIsInsert(self, msg=None):
        self.assertStatusLineRegex('-- INSERT --', msg)

    def assertStatusLineIsReplace(self, msg=None):
        self.assertStatusLineRegex('-- REPLACE --', msg)

    def assertStatusLineIsSelect(self, msg=None):
        self.assertStatusLineRegex('-- SELECT --', msg)

    def assertStatusLineIsVisual(self, msg=None):
        self.assertStatusLineRegex('-- VISUAL --', msg)

    def assertStatusLineIsVisualLine(self, msg=None):
        self.assertStatusLineRegex('-- VISUAL LINE --', msg)

    def assertStatusLineIsVisualBlock(self, msg=None):
        self.assertStatusLineRegex('-- VISUAL BLOCK --', msg)

    def assertXpos(self, expected, msg=None):
        self.assertEqual(self.state.xpos, expected, msg)

    # DEPRECATED Try to avoid using this, it will eventually be removed in favour of something better.
    @property
    def state(self):
        return _State(self.view)

    # DEPRECATED Use newer APIs e.g. self.Region(), unittest.Region.
    def _R(self, a, b=None):
        return _make_region(self.view, a, b)

    # DEPRECATED Use newer APIs e.g. assertRegion(), assertSelection(), and assertContent().
    def _assertRegionsEqual(self, expected_region, actual_region, msg=None):
        # Test that regions covers the exact same region. Does not take region
        # orientation into account.
        if (expected_region.size() == 1) and (actual_region.size() == 1):
            expected_region = _make_region(
                self.view,
                expected_region.begin(),
                expected_region.end()
            )

            actual_region = _make_region(
                self.view,
                actual_region.begin(),
                actual_region.end()
            )

        self.assertEqual(expected_region, actual_region, msg)


_CHAR2MODE = {
    'i': INSERT,
    'n': NORMAL,
    's': SELECT,
    'v': VISUAL,
    'l': VISUAL_LINE,
    'b': VISUAL_BLOCK
}


class FunctionalTestCase(ViewTestCase):

    def feed(self, seq):
        # Args:
        #   seq (str):
        #       A command sequence e.g. 3w, <C-a>, cs'", :pwd
        #
        # The seq can be prefixed to specify a mode:
        #
        #   * n_ - Normal
        #   * i_ - Insert
        #   * v_ - Visual
        #   * l_ - Visual line
        #   * b_ - Visual block
        #
        # The default mode is Internal Normal.
        #
        # NOTE: This method currently uses a **hardcoded** map of sequences to
        # commands (except <Esc> and cmdline sequences). You may need to add the
        # a sequence to command map value. See the _SEQ2CMD variable.
        #
        # Examples:
        #
        # >>> feed('w')
        # >>> feed('3w')
        # >>> feed('v_w')
        # >>> feed('v_3w')
        # >>> feed('<Esc>')
        # >>> feed(':pwd')
        # >>> feed(':help neovintageous')

        if seq == '<Esc>':
            return self.view.window().run_command('_nv_feed_key', {'key': '<esc>'})

        if seq[0] == ':':
            return _do_ex_cmdline(self.view.window(), seq)

        orig_seq = seq
        seq_args = {}

        if seq[0] in 'vinlbs' and (len(seq) > 1 and seq[1] == '_'):
            seq_args['mode'] = _CHAR2MODE[seq[0]]
            seq = seq[2:]

        if seq[0].isdigit():
            if seq != '0':  # Special case motion.
                seq_args['count'] = int(seq[0])
                seq = seq[1:]

        try:
            # The reason for this try catch is because  some sequences map to
            # different commands by mode. For example n_u -> _vi_visual_u, and
            # all other modes u -> _vi_u (in other words all other modes).
            if orig_seq in _SEQ2CMD:
                seq = orig_seq

            command = _SEQ2CMD[seq]['command']

            if 'args' in _SEQ2CMD[seq]:
                args = _SEQ2CMD[seq]['args'].copy()
            else:
                args = {}

            if 'mode' not in args:
                args['mode'] = INTERNAL_NORMAL

            args.update(seq_args)
        except KeyError as e:
            raise KeyError('test command definition not found for feed %s' % str(e)) from None

        self.view.window().run_command(command, args)

    def eq(self, text, feed, expected=None, msg=None):
        # Args:
        #   text (str)
        #   feed (str)
        #   expected (str)
        #   msg (str)
        #
        # The feed and expected can be prefixed to specify a mode:
        #
        #   * n_ - NORMAL
        #   * i_ - INSERT
        #   * v_ - VISUAL
        #   * l_ - VISUAL LINE
        #   * b_ - VISUAL BLOCK
        #   * :<','> - VISUAL CMDLINE (feed parameter only)
        #   * N_ - INTERNAL NORMAL (special mode; translates as NORMAL with
        #          VISUAL selection)
        #   * r_ - Specifies a reversed selection (must come first when joined
        #          with mode prefix e.g. r_n_)
        #
        # The default mode is INTERNAL NORMAL.
        #
        # The mode specified by feed is used for the text, and the expected
        # arguments, unless a mode is otherwise specified.
        #
        # Examples:
        #
        # >>> eq('|Hello world!', 'n_w', 'Hello |world!')
        # >>> eq('|H|ello world!', 'v_w', '|Hello w|orld!')
        # >>> eq('xxx\nbu|zz\nxxx', 'n_cc', 'i_xxx\n|\nxxx')

        if expected is None:
            expected = text

        if text[:2] == 'r_':
            text = text[2:]
            reverse_text = True
        else:
            reverse_text = False

        if expected[:2] == 'r_':
            expected = expected[2:]
            reverse_expected = True
        else:
            reverse_expected = False

        is_feed_visual = feed[0] in 'vlb:' and (len(feed) > 1 and (feed[1] == '_') or feed.startswith(':\'<,\'>'))

        if feed[:2] in ('l_', 'b_', 'i_', 'N_', 's_'):
            text_mode = feed[0]
        elif is_feed_visual:
            text_mode = 'v'
        else:
            text_mode = 'n'

        if expected[:2] in ('n_', 'v_', 'l_', 'b_', 'i_', 'N_', 's_', 'R_'):
            expected_mode = expected[0]
            expected = expected[2:]
        elif feed[:2] in ('l_', 'b_', 'i_', 'N_', 's_'):
            expected_mode = feed[0]
        elif is_feed_visual:
            expected_mode = 'v'
        else:
            expected_mode = 'n'

        if text_mode == 'n':
            self.normal(text)
        elif text_mode == 'v':
            if reverse_text:
                self.rvisual(text)
            else:
                self.visual(text)
        elif text_mode == 'l':
            if reverse_text:
                self.rvline(text)
            else:
                self.vline(text)
        elif text_mode == 'b':
            if reverse_text:
                self.rvblock(text)
            else:
                self.vblock(text)
        elif text_mode == 'N':
            if reverse_text:
                self.rInternalNormal(text)
            else:
                self.internalNormal(text)
        elif text_mode == 'i':
            self.insert(text)
        elif text_mode == 's':
            self.vselect(text)
        else:
            self.assertTrue(False, 'invalid text mode')

        self.feed(feed)

        if expected_mode == 'n':
            self.assertNormal(expected, msg)
        elif expected_mode == 'v':
            if reverse_expected:
                self.assertRVisual(expected, msg)
            else:
                self.assertVisual(expected, msg)
        elif expected_mode == 'l':
            if reverse_expected:
                self.assertRVline(expected, msg)
            else:
                self.assertVline(expected, msg)
        elif expected_mode == 'b':
            if reverse_expected:
                self.assertRVblock(expected, msg)
            else:
                self.assertVblock(expected, msg)
        elif expected_mode == 'N':
            if reverse_expected:
                self.assertRInternalNormal(expected, msg)
            else:
                self.assertInternalNormal(expected, msg)
        elif expected_mode == 'i':
            self.assertInsert(expected, msg)
        elif expected_mode == 's':
            if reverse_expected:
                self.assertRVSelect(expected, msg)
            else:
                self.assertVSelect(expected, msg)
        elif expected_mode == 'R':
            self.assertReplace(expected, msg)
        else:
            self.assertTrue(False, 'invalid expected mode')


# DEPRECATED Use newer APIs.
def _make_region(view, a, b=None):
    # type: (...) -> Region
    try:
        pt_a = view.text_point(*a)
        pt_b = view.text_point(*b)

        return Region(pt_a, pt_b)
    except (TypeError, ValueError):
        pass

    if isinstance(a, int) and b is None:
        pass
    elif not (isinstance(a, int) and isinstance(b, int)):
        raise ValueError('a and b arguments must be integers or a tuple (row, col)')

    if b is not None:
        return Region(a, b)
    else:
        return Region(a)


# Usage:
#
#   @unitest.mock_bell()
#   def test_bell(self):
#       self.assertBell()
#       self.assertNoBell()
#
def mock_bell():
    def wrapper(f):
        @mock.patch('NeoVintageous.nv.cmds_vi_actions.ui_blink')
        @mock.patch('NeoVintageous.nv.cmds_vi_motions.ui_blink')
        def wrapped(self, *args, **kwargs):
            self.bells = [
                args[-1],
                args[-2]
            ]

            def _bell_call_count():
                bell_count = 0
                for bell in self.bells:
                    bell_count += bell.call_count

                return bell_count

            def _assertBell():
                self.assertEquals(1, _bell_call_count(), 'expects bell')

            def _assertNoBell():
                self.assertEquals(0, _bell_call_count(), 'expects no bell')

            self.assertBell = _assertBell
            self.assertNoBell = _assertNoBell

            return f(self, *args[:-2], **kwargs)
        return wrapped
    return wrapper


# Usage:
#
#   @unitest.mock_status_message()
#   def test_status_message(self):
#       self.assertStatusMessage('msg')
#
def mock_status_message():
    def wrapper(f):
        @mock.patch('NeoVintageous.nv.vim._status_message')
        def wrapped(self, *args, **kwargs):
            self.status_message = args[-1]

            def _assertStatusMessage(msg):
                self.status_message.assert_called_once_with(msg)

            self.assertStatusMessage = _assertStatusMessage

            return f(self, *args[:-1], **kwargs)
        return wrapped
    return wrapper


# Usage:
#
#   @unitest.mock_ui()
#   def test_ui(self):
#
#   @unitest.mock_ui(screen_rows=10)
#   def test_ui(self):
#
#   @unitest.mock_ui(visible_region=(2, 7))
#   def test_ui(self):
#
#  Screen rows and visible region defaults to the current size of the view.
#
def mock_ui(screen_rows=None, visible_region=None, em_width=10.0, line_height=22.0):
    def wrapper(f):
        @mock_bell()
        @mock.patch('sublime.View.em_width')
        @mock.patch('sublime.View.line_height')
        @mock.patch('sublime.View.viewport_extent')
        @mock.patch('sublime.View.visible_region')
        def wrapped(self, *args, **kwargs):
            self.em_width = args[-1]
            self.line_height = args[-2]
            self.viewport_extent = args[-3]
            self.visible_region = args[-4]

            def _viewport_extent():
                if screen_rows is not None:
                    rows = screen_rows
                else:
                    rows = self.view.rowcol(self.view.size())[0] + 1

                # Find the max cols of the view by cycling though all the lines.
                lines = self.view.lines(self.Region(0, self.view.size()))
                cols = max(lines, key=lambda item: item.size()).size()

                # The extent y position needs an additional "1.0". It's not
                # clear why Sublime needs to add it, but it always adds it.
                extent_x = em_width * (cols + 2)
                extent_y = (line_height * rows) + 1.0
                extent = (extent_x, extent_y)

                return extent

            # The default visible region uses the size of the current view. For
            # example when a test fixture is setup, the visible region will be
            # the same size as content. This makes most tests easier to setup.
            def _visible_region():
                if visible_region:
                    return self.Region(visible_region[0], visible_region[1])

                region = self.Region(0, self.view.size())

                return region

            self.em_width.return_value = em_width
            self.line_height.return_value = line_height
            self.viewport_extent.side_effect = _viewport_extent
            self.visible_region.side_effect = _visible_region

            return f(self, *args[:-4], **kwargs)
        return wrapped
    return wrapper


# Usage:
#
#   @unitest.mock_run_commands('redo', 'hide_panel')
#   def test_run_command(self):
#       self.assertRunCommand('redo')
#       self.assertRunCommand('redo', count=3)
#       self.assertRunCommand('hide_panel', {'cancel': True})
#
def mock_run_commands(*methods):
    def wrapper(f):
        import sublime_api

        def run_view_command(self, cmd, args=None):
            if cmd not in methods:
                sublime_api.view_run_command(self.id(), cmd, args)
            else:
                f._run_command_calls.append((cmd, args))

        def run_window_command(self, cmd, args=None):
            if cmd not in methods:
                sublime_api.window_run_command(self.id(), cmd, args)
            else:
                f._run_command_calls.append((cmd, args))

        @mock.patch('sublime.View.run_command', new=run_view_command)
        @mock.patch('sublime.Window.run_command', new=run_window_command)
        def wrapped(self, *args, **kwargs):
            f._run_command_calls = []

            def assertRunCommand(cmd, args=None, count=1):
                found = 0
                for actual_cmd, actual_args in f._run_command_calls:
                    if (cmd == actual_cmd) and (args == actual_args):
                        found += 1

                self.assertEqual(found, count, 'failed assert run command called once: "{}" {}'.format(cmd, args))

            self.assertRunCommand = assertRunCommand

            return f(self, *args, **kwargs)
        return wrapped
    return wrapper


# A hardcoded map of sequences to commands. Ideally we wouldn't need this
# hardcoded map, some internal refactoring and redesign is required to make that
# happen. For now make-do with the hardcoded map. Refactoring later should not
# impact the existing tests.
_SEQ2CMD = {

    '#':            {'command': '_vi_octothorp'},  # noqa: E241
    '$':            {'command': '_vi_dollar'},  # noqa: E241
    '%':            {'command': '_vi_percent', 'args': {'percent': None}},  # noqa: E241
    '(':            {'command': '_vi_left_paren'},  # noqa: E241
    ')':            {'command': '_vi_right_paren'},  # noqa: E241
    '*':            {'command': '_vi_star'},  # noqa: E241
    '/abc':         {'command': '_vi_slash_impl', 'args': {'search_string': 'abc'}},  # noqa: E241
    '0':            {'command': '_vi_zero'},  # noqa: E241
    '<':            {'command': '_vi_less_than'},  # noqa: E241
    '<C-a>':        {'command': '_vi_modify_numbers'},  # noqa: E241
    '<C-d>':        {'command': '_vi_ctrl_d'},  # noqa: E241
    '<C-r>':        {'command': '_vi_ctrl_r'},  # noqa: E241
    '<C-u>':        {'command': '_vi_ctrl_u'},  # noqa: E241
    '<C-v>':        {'command': '_enter_visual_block_mode'},  # noqa: E241
    '<C-x>':        {'command': '_vi_modify_numbers', 'args': {'subtract': True}},  # noqa: E241
    '<esc>':        {'command': '_enter_normal_mode'},  # noqa: E241
    '<{':           {'command': '_vi_less_than', 'args': {'motion': {'motion': '_vi_left_brace', 'motion_args': {'mode': INTERNAL_NORMAL, 'count': 1}, 'is_jump': True}}},  # noqa: E241,E501
    '=':            {'command': '_vi_equal'},  # noqa: E241
    '==':           {'command': '_vi_equal_equal'},  # noqa: E241
    '=}':           {'command': '_vi_equal', 'args': {'motion': {'motion': '_vi_right_brace', 'motion_args': {'mode': INTERNAL_NORMAL, 'count': 1}, 'is_jump': True}}},  # noqa: E241,E501
    '>':            {'command': '_vi_greater_than'},  # noqa: E241
    '>>':           {'command': '_vi_greater_than_greater_than'},  # noqa: E241
    '>G':           {'command': '_vi_greater_than', 'args': {'motion': {'motion_args': {'mode': INTERNAL_NORMAL}, 'motion': '_vi_big_g'}}},  # noqa: E241,E501
    '>ip':          {'command': '_vi_greater_than', 'args': {'motion': {'motion_args': {'inclusive': False, 'mode': INTERNAL_NORMAL, 'count': 1, 'text_object': 'p'}, 'motion': '_vi_select_text_object'}}},  # noqa: E241,E501
    '?abc':         {'command': '_vi_question_mark_impl', 'args': {'search_string': 'abc'}},  # noqa: E241
    '[ ':           {'command': '_nv_unimpaired', 'args': {'action': 'blank_up'}},  # noqa: E241
    '[(':           {'command': '_vi_left_square_bracket_target', 'args': {'target': '('}},  # noqa: E241,E501
    '[e':           {'command': '_nv_unimpaired', 'args': {'action': 'move_up'}},  # noqa: E241
    '[{':           {'command': '_vi_left_square_bracket_target', 'args': {'target': '{'}},  # noqa: E241,E501
    '] ':           {'command': '_nv_unimpaired', 'args': {'action': 'blank_down'}},  # noqa: E241
    '])':           {'command': '_vi_right_square_bracket_target', 'args': {'target': ')'}},  # noqa: E241,E501
    ']e':           {'command': '_nv_unimpaired', 'args': {'action': 'move_down'}},  # noqa: E241
    ']}':           {'command': '_vi_right_square_bracket_target', 'args': {'target': '}'}},  # noqa: E241,E501
    '^':            {'command': '_vi_hat'},  # noqa: E241
    'a"':           {'command': '_vi_select_text_object', 'args': {'text_object': '"', 'inclusive': True}},  # noqa: E241,E501
    'a':            {'command': '_vi_a'},  # noqa: E241
    'A':            {'command': '_vi_big_a'},  # noqa: E241
    'a(':           {'command': '_vi_select_text_object', 'args': {'text_object': '(', 'inclusive': True}},  # noqa: E241,E501
    'a)':           {'command': '_vi_select_text_object', 'args': {'text_object': ')', 'inclusive': True}},  # noqa: E241,E501
    'a<':           {'command': '_vi_select_text_object', 'args': {'text_object': '<', 'inclusive': True}},  # noqa: E241,E501
    'a>':           {'command': '_vi_select_text_object', 'args': {'text_object': '>', 'inclusive': True}},  # noqa: E241,E501
    'a[':           {'command': '_vi_select_text_object', 'args': {'text_object': '[', 'inclusive': True}},  # noqa: E241,E501
    'a\'':          {'command': '_vi_select_text_object', 'args': {'text_object': '\'', 'inclusive': True}},  # noqa: E241,E501
    'a]':           {'command': '_vi_select_text_object', 'args': {'text_object': ']', 'inclusive': True}},  # noqa: E241,E501
    'a`':           {'command': '_vi_select_text_object', 'args': {'text_object': '`', 'inclusive': True}},  # noqa: E241,E501
    'ab':           {'command': '_vi_select_text_object', 'args': {'text_object': 'b', 'inclusive': True}},  # noqa: E241,E501
    'aB':           {'command': '_vi_select_text_object', 'args': {'text_object': 'b', 'inclusive': True}},  # noqa: E241,E501
    'ap':           {'command': '_vi_select_text_object', 'args': {'text_object': 'p', 'inclusive': True}},  # noqa: E241,E501
    'as':           {'command': '_vi_select_text_object', 'args': {'text_object': 's', 'inclusive': True}},  # noqa: E241,E501
    'at':           {'command': '_vi_select_text_object', 'args': {'text_object': 't', 'inclusive': True}},  # noqa: E241,E501
    'aW':           {'command': '_vi_select_text_object', 'args': {'text_object': 'W', 'inclusive': True}},  # noqa: E241,E501
    'aw':           {'command': '_vi_select_text_object', 'args': {'text_object': 'w', 'inclusive': True}},  # noqa: E241,E501
    'a{':           {'command': '_vi_select_text_object', 'args': {'text_object': '{', 'inclusive': True}},  # noqa: E241,E501
    'a}':           {'command': '_vi_select_text_object', 'args': {'text_object': '}', 'inclusive': True}},  # noqa: E241,E501
    'b':            {'command': '_vi_b'},  # noqa: E241
    'c$':           {'command': '_vi_c', 'args': {'motion': {'motion_args': {'count': 1, 'mode': INTERNAL_NORMAL}, 'motion': '_vi_dollar', 'is_jump': True}}},  # noqa: E241,E501
    'C':            {'command': '_vi_big_c', 'args': {'register': '"'}},  # noqa: E241
    'c':            {'command': '_vi_c'},  # noqa: E241
    'cb':           {'command': '_vi_c', 'args': {'motion': {'motion_args': {'count': 1, 'mode': INTERNAL_NORMAL}, 'motion': '_vi_b'}}},  # noqa: E241,E501
    'cc':           {'command': '_vi_cc'},  # noqa: E241
    'ce':           {'command': '_vi_c', 'args': {'motion': {'motion_args': {'count': 1, 'mode': INTERNAL_NORMAL}, 'motion': '_vi_e'}}},  # noqa: E241,E501
    'ci"':          {'command': '_vi_c', 'args': {'motion': {'motion_args': {'text_object': "\"", 'inclusive': False, 'mode': INTERNAL_NORMAL, 'count': 1}, 'motion': '_vi_select_text_object'}}},  # noqa: E241,E501
    'cr ':          {'command': '_nv_abolish', 'args': {'to': '<space>'}},  # noqa: E241
    'cr-':          {'command': '_nv_abolish', 'args': {'to': '-'}},  # noqa: E241
    'cr.':          {'command': '_nv_abolish', 'args': {'to': '.'}},  # noqa: E241
    'cr_':          {'command': '_nv_abolish', 'args': {'to': '_'}},  # noqa: E241
    'crc':          {'command': '_nv_abolish', 'args': {'to': 'c'}},  # noqa: E241
    'crk':          {'command': '_nv_abolish', 'args': {'to': 'k'}},  # noqa: E241
    'crm':          {'command': '_nv_abolish', 'args': {'to': 'm'}},  # noqa: E241
    'crs':          {'command': '_nv_abolish', 'args': {'to': 's'}},  # noqa: E241
    'crt':          {'command': '_nv_abolish', 'args': {'to': 't'}},  # noqa: E241
    'cru':          {'command': '_nv_abolish', 'args': {'to': 'u'}},  # noqa: E241
    'crU':          {'command': '_nv_abolish', 'args': {'to': 'U'}},  # noqa: E241
    'cs""':         {'command': '_nv_surround', 'args': {'action': 'cs', 'target': '"', 'replacement': '"'}},  # noqa: E241,E501
    'cs"(':         {'command': '_nv_surround', 'args': {'action': 'cs', 'target': '"', 'replacement': '('}},  # noqa: E241,E501
    'cs")':         {'command': '_nv_surround', 'args': {'action': 'cs', 'target': '"', 'replacement': ')'}},  # noqa: E241,E501
    'cs"2':         {'command': '_nv_surround', 'args': {'action': 'cs', 'target': '"', 'replacement': '2'}},  # noqa: E241,E501
    'cs"<':         {'command': '_nv_surround', 'args': {'action': 'cs', 'target': '"', 'replacement': '<'}},  # noqa: E241,E501
    'cs"<x>':       {'command': '_nv_surround', 'args': {'action': 'cs', 'target': '"', 'replacement': '<x>'}},  # noqa: E241,E501
    'cs">':         {'command': '_nv_surround', 'args': {'action': 'cs', 'target': '"', 'replacement': '>'}},  # noqa: E241,E501
    'cs"[':         {'command': '_nv_surround', 'args': {'action': 'cs', 'target': '"', 'replacement': '['}},  # noqa: E241,E501
    'cs"\'':        {'command': '_nv_surround', 'args': {'action': 'cs', 'target': '"', 'replacement': "'"}},  # noqa: E241,E501
    'cs"]':         {'command': '_nv_surround', 'args': {'action': 'cs', 'target': '"', 'replacement': ']'}},  # noqa: E241,E501
    'cs"`':         {'command': '_nv_surround', 'args': {'action': 'cs', 'target': '"', 'replacement': '`'}},  # noqa: E241,E501
    'cs"{':         {'command': '_nv_surround', 'args': {'action': 'cs', 'target': '"', 'replacement': '{'}},  # noqa: E241,E501
    'cs"}':         {'command': '_nv_surround', 'args': {'action': 'cs', 'target': '"', 'replacement': '}'}},  # noqa: E241,E501
    'cs("':         {'command': '_nv_surround', 'args': {'action': 'cs', 'target': '(', 'replacement': '"'}},  # noqa: E241,E501
    'cs((':         {'command': '_nv_surround', 'args': {'action': 'cs', 'target': '(', 'replacement': '('}},  # noqa: E241,E501
    'cs()':         {'command': '_nv_surround', 'args': {'action': 'cs', 'target': '(', 'replacement': ')'}},  # noqa: E241,E501
    'cs(2':         {'command': '_nv_surround', 'args': {'action': 'cs', 'target': '(', 'replacement': '2'}},  # noqa: E241,E501
    'cs([':         {'command': '_nv_surround', 'args': {'action': 'cs', 'target': '(', 'replacement': '['}},  # noqa: E241,E501
    'cs(\'':        {'command': '_nv_surround', 'args': {'action': 'cs', 'target': '(', 'replacement': '\''}},  # noqa: E241,E501
    'cs(]':         {'command': '_nv_surround', 'args': {'action': 'cs', 'target': '(', 'replacement': ']'}},  # noqa: E241,E501
    'cs({':         {'command': '_nv_surround', 'args': {'action': 'cs', 'target': '(', 'replacement': '{'}},  # noqa: E241,E501
    'cs(}':         {'command': '_nv_surround', 'args': {'action': 'cs', 'target': '(', 'replacement': '}'}},  # noqa: E241,E501
    'cs)"':         {'command': '_nv_surround', 'args': {'action': 'cs', 'target': ')', 'replacement': '"'}},  # noqa: E241,E501
    'cs)(':         {'command': '_nv_surround', 'args': {'action': 'cs', 'target': ')', 'replacement': '('}},  # noqa: E241,E501
    'cs))':         {'command': '_nv_surround', 'args': {'action': 'cs', 'target': ')', 'replacement': ')'}},  # noqa: E241,E501
    'cs)2':         {'command': '_nv_surround', 'args': {'action': 'cs', 'target': ')', 'replacement': '2'}},  # noqa: E241,E501
    'cs)[':         {'command': '_nv_surround', 'args': {'action': 'cs', 'target': ')', 'replacement': '['}},  # noqa: E241,E501
    'cs)\'':        {'command': '_nv_surround', 'args': {'action': 'cs', 'target': ')', 'replacement': '\''}},  # noqa: E241,E501
    'cs)]':         {'command': '_nv_surround', 'args': {'action': 'cs', 'target': ')', 'replacement': ']'}},  # noqa: E241,E501
    'cs){':         {'command': '_nv_surround', 'args': {'action': 'cs', 'target': ')', 'replacement': '{'}},  # noqa: E241,E501
    'cs)}':         {'command': '_nv_surround', 'args': {'action': 'cs', 'target': ')', 'replacement': '}'}},  # noqa: E241,E501
    'cs,`':         {'command': '_nv_surround', 'args': {'action': 'cs', 'target': ',', 'replacement': '`'}},  # noqa: E241,E501
    'cs-_':         {'command': '_nv_surround', 'args': {'action': 'cs', 'target': '-', 'replacement': '_'}},  # noqa: E241,E501
    'cs."':         {'command': '_nv_surround', 'args': {'action': 'cs', 'target': '.', 'replacement': '"'}},  # noqa: E241,E501
    'cs>"':         {'command': '_nv_surround', 'args': {'action': 'cs', 'target': '>', 'replacement': '"'}},  # noqa: E241,E501
    'cs>{':         {'command': '_nv_surround', 'args': {'action': 'cs', 'target': '>', 'replacement': '{'}},  # noqa: E241,E501
    'cs>}':         {'command': '_nv_surround', 'args': {'action': 'cs', 'target': '>', 'replacement': '}'}},  # noqa: E241,E501
    'cs["':         {'command': '_nv_surround', 'args': {'action': 'cs', 'target': '[', 'replacement': '"'}},  # noqa: E241,E501
    'cs\'"':        {'command': '_nv_surround', 'args': {'action': 'cs', 'target': "'", 'replacement': '"'}},  # noqa: E241,E501
    'cs\'(':        {'command': '_nv_surround', 'args': {'action': 'cs', 'target': "'", 'replacement': '('}},  # noqa: E241,E501
    'cs\'<div>':    {'command': '_nv_surround', 'args': {'action': 'cs', 'target': "'", 'replacement': '<div>'}},  # noqa: E241,E501
    'cs\'<q>':      {'command': '_nv_surround', 'args': {'action': 'cs', 'target': "'", 'replacement': '<q>'}},  # noqa: E241,E501
    'cs\'`':        {'command': '_nv_surround', 'args': {'action': 'cs', 'target': "'", 'replacement': '`'}},  # noqa: E241,E501
    'cs\'tdiv>':    {'command': '_nv_surround', 'args': {'action': 'cs', 'target': "'", 'replacement': 'tdiv>'}},  # noqa: E241,E501
    'cs\'tq>':      {'command': '_nv_surround', 'args': {'action': 'cs', 'target': "'", 'replacement': 'tq>'}},  # noqa: E241,E501
    'cs]"':         {'command': '_nv_surround', 'args': {'action': 'cs', 'target': ']', 'replacement': '"'}},  # noqa: E241,E501
    'cs]>':         {'command': '_nv_surround', 'args': {'action': 'cs', 'target': ']', 'replacement': '>'}},  # noqa: E241,E501
    'cs]{':         {'command': '_nv_surround', 'args': {'action': 'cs', 'target': ']', 'replacement': '{'}},  # noqa: E241,E501
    'cs_-':         {'command': '_nv_surround', 'args': {'action': 'cs', 'target': '_', 'replacement': '-'}},  # noqa: E241,E501
    'cs`"':         {'command': '_nv_surround', 'args': {'action': 'cs', 'target': '`', 'replacement': '"'}},  # noqa: E241,E501
    'cs`\'':        {'command': '_nv_surround', 'args': {'action': 'cs', 'target': '`', 'replacement': "'"}},  # noqa: E241,E501
    'csa"':         {'command': '_nv_surround', 'args': {'action': 'cs', 'target': 'a', 'replacement': '"'}},  # noqa: E241,E501
    'csb"':         {'command': '_nv_surround', 'args': {'action': 'cs', 'target': 'b', 'replacement': '"'}},  # noqa: E241,E501
    'csB"':         {'command': '_nv_surround', 'args': {'action': 'cs', 'target': 'B', 'replacement': '"'}},  # noqa: E241,E501
    'csr"':         {'command': '_nv_surround', 'args': {'action': 'cs', 'target': 'r', 'replacement': '"'}},  # noqa: E241,E501
    'cst"':         {'command': '_nv_surround', 'args': {'action': 'cs', 'target': 't', 'replacement': '"'}},  # noqa: E241,E501
    'cst<a>':       {'command': '_nv_surround', 'args': {'action': 'cs', 'target': 't', 'replacement': '<a>'}},  # noqa: E241,E501
    'cstta>':       {'command': '_nv_surround', 'args': {'action': 'cs', 'target': 't', 'replacement': 'ta>'}},  # noqa: E241,E501
    'cs{(':         {'command': '_nv_surround', 'args': {'action': 'cs', 'target': '{', 'replacement': '('}},  # noqa: E241,E501
    'cs{)':         {'command': '_nv_surround', 'args': {'action': 'cs', 'target': '{', 'replacement': ')'}},  # noqa: E241,E501
    'cs}(':         {'command': '_nv_surround', 'args': {'action': 'cs', 'target': '}', 'replacement': '('}},  # noqa: E241,E501
    'cs})':         {'command': '_nv_surround', 'args': {'action': 'cs', 'target': '}', 'replacement': ')'}},  # noqa: E241,E501
    'cw':           {'command': '_vi_c', 'args': {'motion': {'motion_args': {'count': 1, 'mode': INTERNAL_NORMAL}, 'motion': '_vi_w'}}},  # noqa: E241,E501
    'd$':           {'command': '_vi_d', 'args': {'motion': {'motion_args': {'count': 1, 'mode': INTERNAL_NORMAL}, 'motion': '_vi_dollar', 'is_jump': True}}},  # noqa: E241,E501
    'D':            {'command': '_vi_big_d'},  # noqa: E241
    'd':            {'command': '_vi_d'},  # noqa: E241
    'd2ft':         {'command': '_vi_d', 'args': {'motion': {'motion_args': {'count': 2, 'mode': INTERNAL_NORMAL, 'inclusive': True, 'char': 't'}, 'motion': '_vi_find_in_line'}}},  # noqa: E241,E501
    'dd':           {'command': '_vi_dd'},  # noqa: E241,E501
    'de':           {'command': '_vi_d', 'args': {'motion': {'motion_args': {'count': 1, 'mode': INTERNAL_NORMAL}, 'motion': '_vi_e'}}},  # noqa: E241,E501
    'df=':          {'command': '_vi_d', 'args': {'motion': {'motion_args': {'count': 1, 'mode': INTERNAL_NORMAL, 'inclusive': True, 'char': '='}, 'motion': '_vi_find_in_line'}}},  # noqa: E241,E501
    'dft':          {'command': '_vi_d', 'args': {'motion': {'motion_args': {'count': 1, 'mode': INTERNAL_NORMAL, 'inclusive': True, 'char': 't'}, 'motion': '_vi_find_in_line'}}},  # noqa: E241,E501
    'ds ':          {'command': '_nv_surround', 'args': {'action': 'ds', 'target': ' '}},  # noqa: E241
    'ds"':          {'command': '_nv_surround', 'args': {'action': 'ds', 'target': '"'}},  # noqa: E241
    'ds(':          {'command': '_nv_surround', 'args': {'action': 'ds', 'target': '('}},  # noqa: E241
    'ds)':          {'command': '_nv_surround', 'args': {'action': 'ds', 'target': ')'}},  # noqa: E241
    'ds,':          {'command': '_nv_surround', 'args': {'action': 'ds', 'target': ','}},  # noqa: E241
    'ds-':          {'command': '_nv_surround', 'args': {'action': 'ds', 'target': '-'}},  # noqa: E241
    'ds.':          {'command': '_nv_surround', 'args': {'action': 'ds', 'target': '.'}},  # noqa: E241
    'ds0':          {'command': '_nv_surround', 'args': {'action': 'ds', 'target': '0'}},  # noqa: E241
    'ds2':          {'command': '_nv_surround', 'args': {'action': 'ds', 'target': '2'}},  # noqa: E241
    'ds<':          {'command': '_nv_surround', 'args': {'action': 'ds', 'target': '<'}},  # noqa: E241
    'ds>':          {'command': '_nv_surround', 'args': {'action': 'ds', 'target': '>'}},  # noqa: E241
    'ds[':          {'command': '_nv_surround', 'args': {'action': 'ds', 'target': '['}},  # noqa: E241
    'ds\'':         {'command': '_nv_surround', 'args': {'action': 'ds', 'target': '\''}},  # noqa: E241
    'ds]':          {'command': '_nv_surround', 'args': {'action': 'ds', 'target': ']'}},  # noqa: E241
    'ds_':          {'command': '_nv_surround', 'args': {'action': 'ds', 'target': '_'}},  # noqa: E241
    'ds`':          {'command': '_nv_surround', 'args': {'action': 'ds', 'target': '`'}},  # noqa: E241
    'dsa':          {'command': '_nv_surround', 'args': {'action': 'ds', 'target': 'a'}},  # noqa: E241
    'dsb':          {'command': '_nv_surround', 'args': {'action': 'ds', 'target': 'b'}},  # noqa: E241
    'dsB':          {'command': '_nv_surround', 'args': {'action': 'ds', 'target': 'B'}},  # noqa: E241
    'dse':          {'command': '_nv_surround', 'args': {'action': 'ds', 'target': 'e'}},  # noqa: E241
    'dsp':          {'command': '_nv_surround', 'args': {'action': 'ds', 'target': 'p'}},  # noqa: E241
    'dsq':          {'command': '_nv_surround', 'args': {'action': 'ds', 'target': 'q'}},  # noqa: E241
    'dsr':          {'command': '_nv_surround', 'args': {'action': 'ds', 'target': 'r'}},  # noqa: E241
    'dss':          {'command': '_nv_surround', 'args': {'action': 'ds', 'target': 's'}},  # noqa: E241
    'dst':          {'command': '_nv_surround', 'args': {'action': 'ds', 'target': 't'}},  # noqa: E241
    'dsw':          {'command': '_nv_surround', 'args': {'action': 'ds', 'target': 'w'}},  # noqa: E241
    'dsW':          {'command': '_nv_surround', 'args': {'action': 'ds', 'target': 'W'}},  # noqa: E241
    'ds{':          {'command': '_nv_surround', 'args': {'action': 'ds', 'target': '{'}},  # noqa: E241
    'ds}':          {'command': '_nv_surround', 'args': {'action': 'ds', 'target': '}'}},  # noqa: E241
    'dw':           {'command': '_vi_d', 'args': {'motion': {'motion_args': {'count': 1, 'mode': INTERNAL_NORMAL}, 'motion': '_vi_w'}}},  # noqa: E241,E501
    'e':            {'command': '_vi_e'},  # noqa: E241
    'f\\':          {'command': '_vi_find_in_line', 'args': {'char': '<bslash>', 'inclusive': True}},  # noqa: E241
    'fx':           {'command': '_vi_find_in_line', 'args': {'char': 'x', 'inclusive': True}},  # noqa: E241
    'f|':           {'command': '_vi_find_in_line', 'args': {'char': '<bar>', 'inclusive': True}},  # noqa: E241
    'G':            {'command': '_vi_big_g'},  # noqa: E241
    'g_':           {'command': '_vi_g__'},  # noqa: E241
    'ga':           {'command': '_vi_ga'},  # noqa: E241
    'gc':           {'command': '_nv_commentary', 'args': {'action': 'c'}},  # noqa: E241
    'gC':           {'command': '_nv_commentary', 'args': {'action': 'C'}},  # noqa: E241A
    'gcc':          {'command': '_nv_commentary', 'args': {'action': 'cc'}},  # noqa: E241
    'gcG':          {'command': '_nv_commentary', 'args': {'action': 'c', 'motion': {'motion_args': {'mode': INTERNAL_NORMAL}, 'motion': '_vi_big_g'}}},  # noqa: E241,E501
    'gC}':          {'command': '_nv_commentary', 'args': {'action': 'C', 'motion': {'motion_args': {'mode': INTERNAL_NORMAL}, 'motion': '_vi_right_brace', 'is_jump': True}}},  # noqa: E241,E501
    'gE':           {'command': '_vi_g_big_e'},  # noqa: E241
    'ge':           {'command': '_vi_ge'},  # noqa: E241
    'gf':           {'command': '_vi_g', 'args': {'action': 'f'}},  # noqa: E241
    'gg':           {'command': '_vi_gg'},  # noqa: E241
    'gh':           {'command': '_enter_select_mode'},  # noqa: E241
    'gJ':           {'command': '_vi_big_j', 'args': {'dont_insert_or_remove_spaces': True}},  # noqa: E241
    'gj':           {'command': '_vi_gj'},  # noqa: E241
    'gk':           {'command': '_vi_gk'},  # noqa: E241
    'gq':           {'command': '_vi_gq'},  # noqa: E241
    'gqip':         {'command': '_vi_gq', 'args': {'motion': {'motion_args': {'inclusive': False, 'mode': INTERNAL_NORMAL, 'count': 1, 'text_object': 'p'}, 'motion': '_vi_select_text_object'}}},  # noqa: E241,E501
    'gq}':          {'command': '_vi_gq', 'args': {'motion': {'motion_args': {'mode': INTERNAL_NORMAL, 'count': 1}, 'is_jump': True, 'motion': '_vi_right_brace'}}},  # noqa: E241,E501
    'gU':           {'command': '_vi_g_big_u'},  # noqa: E241
    'gu':           {'command': '_vi_gu'},  # noqa: E241
    'gUip':         {'command': '_vi_g_big_u', 'args': {'motion': {'motion_args': {'inclusive': False, 'mode': INTERNAL_NORMAL, 'count': 1, 'text_object': 'p'}, 'motion': '_vi_select_text_object'}}},  # noqa: E241,E501
    'guis':         {'command': '_vi_gu', 'args': {'motion': {'motion_args': {'inclusive': False, 'mode': INTERNAL_NORMAL, 'count': 1, 'text_object': 's'}, 'motion': '_vi_select_text_object'}}},  # noqa: E241,E501
    'gUU':          {'command': '_vi_g_big_u_big_u'},  # noqa: E241
    'guu':          {'command': '_vi_guu'},  # noqa: E241
    'gv':           {'command': '_vi_gv'},  # noqa: E241
    'gx':           {'command': '_vi_gx'},  # noqa: E241
    'g~$':          {'command': '_vi_g_tilde', 'args': {'motion': {'is_jump': True, 'motion_args': {'mode': INTERNAL_NORMAL, 'count': 1}, 'motion': '_vi_dollar'}}},  # noqa: E241,E501
    'g~':           {'command': '_vi_g_tilde'},  # noqa: E241
    'g~~':          {'command': '_vi_g_tilde_g_tilde'},  # noqa: E241
    'H':            {'command': '_vi_big_h'},  # noqa: E241
    'h':            {'command': '_vi_h'},  # noqa: E241
    'i"':           {'command': '_vi_select_text_object', 'args': {'text_object': '"', 'inclusive': False}},  # noqa: E241,E501
    'i':            {'command': '_enter_insert_mode'},  # noqa: E241
    'I':            {'command': '_vi_big_i'},  # noqa: E241
    'i(':           {'command': '_vi_select_text_object', 'args': {'text_object': '(', 'inclusive': False}},  # noqa: E241,E501
    'i)':           {'command': '_vi_select_text_object', 'args': {'text_object': ')', 'inclusive': False}},  # noqa: E241,E501
    'i<':           {'command': '_vi_select_text_object', 'args': {'text_object': '<', 'inclusive': False}},  # noqa: E241,E501
    'i>':           {'command': '_vi_select_text_object', 'args': {'text_object': '>', 'inclusive': False}},  # noqa: E241,E501
    'i[':           {'command': '_vi_select_text_object', 'args': {'text_object': '[', 'inclusive': False}},  # noqa: E241,E501
    'i\'':          {'command': '_vi_select_text_object', 'args': {'text_object': '\'', 'inclusive': False}},  # noqa: E241,E501
    'i]':           {'command': '_vi_select_text_object', 'args': {'text_object': ']', 'inclusive': False}},  # noqa: E241,E501
    'i`':           {'command': '_vi_select_text_object', 'args': {'text_object': '`', 'inclusive': False}},  # noqa: E241,E501
    'iB':           {'command': '_vi_select_text_object', 'args': {'text_object': 'B', 'inclusive': False}},  # noqa: E241,E501
    'ib':           {'command': '_vi_select_text_object', 'args': {'text_object': 'b', 'inclusive': False}},  # noqa: E241,E501
    'ip':           {'command': '_vi_select_text_object', 'args': {'text_object': 'p', 'inclusive': False}},  # noqa: E241,E501
    'is':           {'command': '_vi_select_text_object', 'args': {'text_object': 's', 'inclusive': False}},  # noqa: E241,E501
    'it':           {'command': '_vi_select_text_object', 'args': {'text_object': 't', 'inclusive': False}},  # noqa: E241,E501
    'iw':           {'command': '_vi_select_text_object', 'args': {'text_object': 'w', 'inclusive': False}},  # noqa: E241,E501
    'iW':           {'command': '_vi_select_text_object', 'args': {'text_object': 'W', 'inclusive': False}},  # noqa: E241,E501
    'i{':           {'command': '_vi_select_text_object', 'args': {'text_object': '{', 'inclusive': False}},  # noqa: E241,E501
    'i}':           {'command': '_vi_select_text_object', 'args': {'text_object': '}', 'inclusive': False}},  # noqa: E241,E501
    'J':            {'command': '_vi_big_j'},  # noqa: E241
    'j':            {'command': '_vi_select_j'},  # noqa: E241
    'k':            {'command': '_vi_select_k'},  # noqa: E241
    'L':            {'command': '_vi_big_l'},  # noqa: E241
    'l':            {'command': '_vi_l'},  # noqa: E241
    'l_o':          {'command': '_vi_visual_o'},  # noqa: E241,E501
    'M':            {'command': '_vi_big_m'},  # noqa: E241
    'N':            {'command': '_vi_repeat_buffer_search', 'args': {'reverse': True}},  # noqa: E241
    'n':            {'command': '_vi_repeat_buffer_search'},  # noqa: E241
    'O':            {'command': '_vi_big_o'},  # noqa: E241
    'o':            {'command': '_vi_o'},  # noqa: E241
    'P':            {'command': '_vi_big_p', 'args': {'register': '"'}},  # noqa: E241
    'p':            {'command': '_vi_p', 'args': {'register': '"'}},  # noqa: E241
    'R':            {'command': '_enter_replace_mode'},  # noqa: E241
    'rx':           {'command': '_vi_r', 'args': {'char': 'x'}},  # noqa: E241
    'S"':           {'command': '_nv_surround', 'args': {'action': 'ys', 'replacement': '"'}},  # noqa: E241
    'S':            {'command': '_vi_big_s'},  # noqa: E241
    's':            {'command': '_vi_s', 'args': {'register': '"'}},  # noqa: E241
    's_J':          {'command': '_vi_select_big_j'},  # noqa: E241
    't\\':          {'command': '_vi_find_in_line', 'args': {'char': '<bslash>', 'inclusive': False}},  # noqa: E241
    'tx':           {'command': '_vi_find_in_line', 'args': {'char': 'x', 'inclusive': False}},  # noqa: E241
    't|':           {'command': '_vi_find_in_line', 'args': {'char': '<bar>', 'inclusive': False}},  # noqa: E241
    'u':            {'command': '_vi_u'},  # noqa: E241,E501
    'U':            {'command': '_vi_visual_big_u'},  # noqa: E241,E501
    'V':            {'command': '_enter_visual_line_mode'},  # noqa: E241
    'v':            {'command': '_enter_visual_mode'},  # noqa: E241
    'v_o':          {'command': '_vi_visual_o'},  # noqa: E241,E501
    'v_u':          {'command': '_vi_visual_u'},  # noqa: E241,E501
    'W':            {'command': '_vi_big_w'},  # noqa: E241
    'w':            {'command': '_vi_w'},  # noqa: E241
    'X':            {'command': '_vi_big_x'},  # noqa: E241
    'x':            {'command': '_vi_x'},  # noqa: E241
    'y$':           {'command': '_vi_y', 'args': {'register': '"', 'motion': {'is_jump': True, 'motion_args': {'mode': INTERNAL_NORMAL, 'count': 1}, 'motion': '_vi_dollar'}}},  # noqa: E241,E501
    'y':            {'command': '_vi_y', 'args': {'register': '"'}},  # noqa: E241
    'Y':            {'command': '_vi_yy', 'args': {'register': '"'}},  # noqa: E241
    'yi(':          {'command': '_vi_y', 'args': {'motion': {'motion_args': {'inclusive': False, 'text_object': '(', 'mode': INTERNAL_NORMAL, 'count': 1}, 'motion': '_vi_select_text_object'}}},  # noqa: E241,E501
    'yi)':          {'command': '_vi_y', 'args': {'motion': {'motion_args': {'inclusive': False, 'text_object': ')', 'mode': INTERNAL_NORMAL, 'count': 1}, 'motion': '_vi_select_text_object'}}},  # noqa: E241,E501
    'yib':          {'command': '_vi_y', 'args': {'motion': {'motion_args': {'inclusive': False, 'text_object': 'b', 'mode': INTERNAL_NORMAL, 'count': 1}, 'motion': '_vi_select_text_object'}}},  # noqa: E241,E501
    'yiw':          {'command': '_vi_y', 'args': {'motion': {'motion_args': {'inclusive': False, 'text_object': 'w', 'mode': INTERNAL_NORMAL, 'count': 1}, 'motion': '_vi_select_text_object'}}},  # noqa: E241,E501
    'yse"':         {'command': '_nv_surround', 'args': {'action': 'ys', 'replacement': '"',     'motion': {'motion': '_vi_e', 'motion_args': {'mode': INTERNAL_NORMAL, 'count': 1}}}},  # noqa: E241,E501
    'yse(':         {'command': '_nv_surround', 'args': {'action': 'ys', 'replacement': '(',     'motion': {'motion': '_vi_e', 'motion_args': {'mode': INTERNAL_NORMAL, 'count': 1}}}},  # noqa: E241,E501
    'yse)':         {'command': '_nv_surround', 'args': {'action': 'ys', 'replacement': ')',     'motion': {'motion': '_vi_e', 'motion_args': {'mode': INTERNAL_NORMAL, 'count': 1}}}},  # noqa: E241,E501
    'yse2':         {'command': '_nv_surround', 'args': {'action': 'ys', 'replacement': '2',     'motion': {'motion': '_vi_e', 'motion_args': {'mode': INTERNAL_NORMAL, 'count': 1}}}},  # noqa: E241,E501
    'yse<foo>':     {'command': '_nv_surround', 'args': {'action': 'ys', 'replacement': '<foo>', 'motion': {'motion': '_vi_e', 'motion_args': {'mode': INTERNAL_NORMAL, 'count': 1}}}},  # noqa: E241,E501
    'yse[':         {'command': '_nv_surround', 'args': {'action': 'ys', 'replacement': '[',     'motion': {'motion': '_vi_e', 'motion_args': {'mode': INTERNAL_NORMAL, 'count': 1}}}},  # noqa: E241,E501
    'yse\'':        {'command': '_nv_surround', 'args': {'action': 'ys', 'replacement': '\'',    'motion': {'motion': '_vi_e', 'motion_args': {'mode': INTERNAL_NORMAL, 'count': 1}}}},  # noqa: E241,E501
    'yse]':         {'command': '_nv_surround', 'args': {'action': 'ys', 'replacement': ']',     'motion': {'motion': '_vi_e', 'motion_args': {'mode': INTERNAL_NORMAL, 'count': 1}}}},  # noqa: E241,E501
    'yse{':         {'command': '_nv_surround', 'args': {'action': 'ys', 'replacement': '{',     'motion': {'motion': '_vi_e', 'motion_args': {'mode': INTERNAL_NORMAL, 'count': 1}}}},  # noqa: E241,E501
    'yse}':         {'command': '_nv_surround', 'args': {'action': 'ys', 'replacement': '}',     'motion': {'motion': '_vi_e', 'motion_args': {'mode': INTERNAL_NORMAL, 'count': 1}}}},  # noqa: E241,E501
    'ysiw"':        {'command': '_nv_surround', 'args': {'action': 'ys', 'replacement': '"',     'motion': {'motion': '_vi_select_text_object', 'motion_args': {'text_object': 'w', 'mode': INTERNAL_NORMAL, 'count': 1, 'inclusive': False}}}},  # noqa: E241,E501
    'ysiw(':        {'command': '_nv_surround', 'args': {'action': 'ys', 'replacement': '(',     'motion': {'motion': '_vi_select_text_object', 'motion_args': {'text_object': 'w', 'mode': INTERNAL_NORMAL, 'count': 1, 'inclusive': False}}}},  # noqa: E241,E501
    'ysiw)':        {'command': '_nv_surround', 'args': {'action': 'ys', 'replacement': ')',     'motion': {'motion': '_vi_select_text_object', 'motion_args': {'text_object': 'w', 'mode': INTERNAL_NORMAL, 'count': 1, 'inclusive': False}}}},  # noqa: E241,E501
    'ysiw2':        {'command': '_nv_surround', 'args': {'action': 'ys', 'replacement': '2',     'motion': {'motion': '_vi_select_text_object', 'motion_args': {'text_object': 'w', 'mode': INTERNAL_NORMAL, 'count': 1, 'inclusive': False}}}},  # noqa: E241,E501
    'ysiw<foo>':    {'command': '_nv_surround', 'args': {'action': 'ys', 'replacement': '<foo>', 'motion': {'motion': '_vi_select_text_object', 'motion_args': {'text_object': 'w', 'mode': INTERNAL_NORMAL, 'count': 1, 'inclusive': False}}}},  # noqa: E241,E501
    'ysiw[':        {'command': '_nv_surround', 'args': {'action': 'ys', 'replacement': '[',     'motion': {'motion': '_vi_select_text_object', 'motion_args': {'text_object': 'w', 'mode': INTERNAL_NORMAL, 'count': 1, 'inclusive': False}}}},  # noqa: E241,E501
    'ysiw\'':       {'command': '_nv_surround', 'args': {'action': 'ys', 'replacement': '\'',    'motion': {'motion': '_vi_select_text_object', 'motion_args': {'text_object': 'w', 'mode': INTERNAL_NORMAL, 'count': 1, 'inclusive': False}}}},  # noqa: E241,E501
    'ysiw]':        {'command': '_nv_surround', 'args': {'action': 'ys', 'replacement': ']',     'motion': {'motion': '_vi_select_text_object', 'motion_args': {'text_object': 'w', 'mode': INTERNAL_NORMAL, 'count': 1, 'inclusive': False}}}},  # noqa: E241,E501
    'ysiwafoo>':    {'command': '_nv_surround', 'args': {'action': 'ys', 'replacement': '<foo>', 'motion': {'motion': '_vi_select_text_object', 'motion_args': {'text_object': 'w', 'mode': INTERNAL_NORMAL, 'count': 1, 'inclusive': False}}}},  # noqa: E241,E501
    'ysiwb':        {'command': '_nv_surround', 'args': {'action': 'ys', 'replacement': 'b',     'motion': {'motion': '_vi_select_text_object', 'motion_args': {'text_object': 'w', 'mode': INTERNAL_NORMAL, 'count': 1, 'inclusive': False}}}},  # noqa: E241,E501
    'ysiwB':        {'command': '_nv_surround', 'args': {'action': 'ys', 'replacement': 'B',     'motion': {'motion': '_vi_select_text_object', 'motion_args': {'text_object': 'w', 'mode': INTERNAL_NORMAL, 'count': 1, 'inclusive': False}}}},  # noqa: E241,E501
    'ysiwr':        {'command': '_nv_surround', 'args': {'action': 'ys', 'replacement': 'r',     'motion': {'motion': '_vi_select_text_object', 'motion_args': {'text_object': 'w', 'mode': INTERNAL_NORMAL, 'count': 1, 'inclusive': False}}}},  # noqa: E241,E501
    'ysiw{':        {'command': '_nv_surround', 'args': {'action': 'ys', 'replacement': '{',     'motion': {'motion': '_vi_select_text_object', 'motion_args': {'text_object': 'w', 'mode': INTERNAL_NORMAL, 'count': 1, 'inclusive': False}}}},  # noqa: E241,E501
    'ysiw}':        {'command': '_nv_surround', 'args': {'action': 'ys', 'replacement': '}',     'motion': {'motion': '_vi_select_text_object', 'motion_args': {'text_object': 'w', 'mode': INTERNAL_NORMAL, 'count': 1, 'inclusive': False}}}},  # noqa: E241,E501
    'yss)':         {'command': '_nv_surround', 'args': {'action': 'ys', 'replacement': ')',     'motion': {'motion': '_vi_select_text_object', 'motion_args': {'text_object': 'l', 'mode': INTERNAL_NORMAL, 'count': 1, 'inclusive': False}}}},  # noqa: E241,E501
    'yy':           {'command': '_vi_yy', 'args': {'register': '"'}},  # noqa: E241
    '|':            {'command': '_vi_pipe'},  # noqa: E241
    '~':            {'command': '_vi_tilde'},  # noqa: E241

}  # type: dict
