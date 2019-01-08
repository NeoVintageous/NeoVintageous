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

    def write(self, text):
        # type: (str) -> None
        self.view.run_command('_nv_test_write', {'text': text})

    def _setupView(self, text, mode, reverse=False):
        if mode in (VISUAL, VISUAL_BLOCK, VISUAL_LINE):
            self.view.run_command('_nv_test_write', {'text': text.replace('|', '')})
            sels = [i for i, c in enumerate(text) if c == '|']
            sel_len = len(sels)

            if sel_len == 1:
                sels.append(sels[0] + 2)
            elif sel_len % 2 != 0 or sel_len == 0:
                raise Exception('invalid visual selection')

            if sels:
                v_sels = []
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
        # Args:
        #   text (str)
        self._setupView(text, NORMAL)

    def insert(self, text):
        # Args:
        #   text (str)
        self._setupView(text, INSERT)

    def visual(self, text):
        # Args:
        #   text (str)
        self._setupView(text, VISUAL)

    def rvisual(self, text):
        # Args:
        #   text (str)
        self._setupView(text, VISUAL, reverse=True)

    def vline(self, text):
        # Args:
        #   text (str)
        self._setupView(text, VISUAL_LINE)

    def rvline(self, text):
        # Args:
        #   text (str)
        self._setupView(text, VISUAL_LINE, reverse=True)

    def vblock(self, text):
        # Args:
        #   text (str)
        self._setupView(text, VISUAL_BLOCK)

    def resetRegisters(self):
        registers._reset_data()

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

    def _assertView(self, expected, mode, msg):
        if mode in (VISUAL, VISUAL_BLOCK, VISUAL_LINE):
            content = list(self.view.substr(Region(0, self.view.size())))
            counter = 0
            for sel in self.view.sel():
                content.insert(sel.begin() + counter, '|')
                counter += 1
                if sel.end() != sel.begin():
                    # TODO should be assert that it looks like
                    # we're now in normal mode, otherwise visual mode?
                    content.insert(sel.end() + counter, '|')
                    counter += 1

            self.assertEquals(''.join(content), expected, msg)
        else:
            content = list(self.view.substr(Region(0, self.view.size())))
            for i, sel in enumerate(self.view.sel()):
                content.insert(sel.begin() + i, '|')

            self.assertEquals(''.join(content), expected, msg)

        self._assertMode(mode)

    def assertNormal(self, expected, msg=None):
        self._assertView(expected, NORMAL, msg)

    def assertInsert(self, expected, msg=None):
        self._assertView(expected, INSERT, msg)

    def assertVisual(self, expected, msg=None):
        self._assertView(expected, VISUAL, msg)

    def assertRVisual(self, expected, msg=None):
        self.assertVisual(expected, msg)
        self.assertSelectionIsReveresed()

    def assertVline(self, expected, msg=None):
        self._assertView(expected, VISUAL_LINE, msg)

    def assertRVline(self, expected, msg=None):
        self.assertVline(expected, msg)
        self.assertSelectionIsReveresed()

    def assertVblock(self, expected, msg=None):
        self._assertView(expected, VISUAL_BLOCK, msg)

    def assertRVblock(self, expected, msg=None):
        self.assertVblock(expected, msg)
        self.assertSelectionIsReveresed()

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
            # FIXME
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

    def assertSelectionIsReveresed(self):
        for sel in self.view.sel():
            self.assertGreater(sel.a, sel.b, 'failed asserting selection is reversed')

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
            expected_region = _make_region(self.view, expected_region.begin(),
                                           expected_region.end())
            actual_region = _make_region(self.view, actual_region.begin(),
                                         actual_region.end())

        self.assertEqual(expected_region, actual_region, msg)


_char2mode = {
    'i': INSERT,
    'n': NORMAL,
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
        # a sequence to command map value. See the _feedseq2cmd variable.
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

        seq_args = {}

        if seq[0] in 'vinlb' and (len(seq) > 1 and seq[1] == '_'):
            seq_args['mode'] = _char2mode[seq[0]]
            seq = seq[2:]

        if seq[0].isdigit():
            if seq != '0':  # Special case motion.
                seq_args['count'] = int(seq[0])
                seq = seq[1:]

        try:
            command = _feedseq2cmd[seq]['command']
            if 'args' in _feedseq2cmd[seq]:
                args = _feedseq2cmd[seq]['args'].copy()
            else:
                args = {}

            if 'mode' not in args:
                args['mode'] = INTERNAL_NORMAL

            args.update(seq_args)
        except KeyError as e:
            raise KeyError('test command definition not found for feed %s' % str(e)) from None

        self.view.run_command(command, args)

    # The same as eq(), except also assert selections are also reversed
    def eqr(self, text, feed, expected=None, msg=None):
        self.eq(text, feed, expected, msg)
        self.assertSelectionIsReveresed()

    def eq(self, text, feed, expected=None, msg=None):
        # Args:
        #   text (str)
        #   feed (str)
        #   expected (str)
        #   msg (str)
        #
        # The feed and expected can be prefixed to specify a mode:
        #
        #   * n_ - Normal
        #   * i_ - Insert
        #   * v_ - Visual
        #   * l_ - Visual line
        #   * b_ - Visual block
        #   * :<','> - Visual cmdline (only valid for feed)
        #
        # The default mode is Internal Normal.
        #
        # When a mode is specified by feed, it iss used as the default mode for
        # text and expected.
        #
        # Examples:
        #
        # >>> eq('|Hello world!', 'w', 'Hello |world!')
        # >>> eq('|H|ello world!', 'v_w', '|Hello w|orld!')
        # >>> eq('a\nx|y\nb', 'cc', 'i_a\n|\nb')

        if expected is None:
            expected = text

        if feed[0] in 'vlb:' and (len(feed) > 1 and (feed[1] == '_') or feed.startswith(':\'<,\'>')):
            if feed[0] == 'l':
                self.vline(text)
            elif feed[0] == 'b':
                self.vblock(text)
            else:
                self.visual(text)

            self.feed(feed)

            if expected[:2] == 'n_':
                self.assertNormal(expected[2:], msg)
            elif expected[:2] == 'l_':
                self.assertVline(expected[2:], msg)
            elif expected[:2] == 'b_':
                self.assertVblock(expected[2:], msg)
            elif expected[:2] == 'i_':
                self.assertInsert(expected[2:], msg)
            elif expected[:2] == 'v_':
                self.assertVisual(expected[2:], msg)
            elif feed[0] == 'l':
                self.assertVline(expected, msg)
            elif feed[0] == 'b':
                self.assertVblock(expected, msg)
            else:
                self.assertVisual(expected, msg)
        else:
            self.normal(text)

            self.feed(feed)

            if expected[:2] == 'v_':
                self.assertVisual(expected[2:], msg)
            elif expected[:2] == 'l_':
                self.assertVline(expected[2:], msg)
            elif expected[:2] == 'b_':
                self.assertVblock(expected[2:], msg)
            elif expected[:2] == 'i_':
                self.assertInsert(expected[2:], msg)
            else:
                self.assertNormal(expected, msg)


# A hardcoded map of sequences to commands. Ideally we wouldn't need this
# hardcoded map, some internal refactoring and redesign is required to make that
# happen. For now make-do with the hardcoded map. Refactoring later should not
# impact the existing tests.
_feedseq2cmd = {

    '$':            {'command': '_vi_dollar', 'args': {'mode': 'mode_normal'}},  # noqa: E241
    '%':            {'command': '_vi_percent', 'args': {'percent': None, 'mode': 'mode_normal'}},  # noqa: E241
    '0':            {'command': '_vi_zero'},  # noqa: E241
    '<':            {'command': '_vi_less_than'},  # noqa: E241
    '<C-a>':        {'command': '_vi_modify_numbers'},  # noqa: E241
    '<C-x>':        {'command': '_vi_modify_numbers', 'args': {'subtract': True}},  # noqa: E241
    '>':            {'command': '_vi_greater_than'},  # noqa: E241
    '[ ':           {'command': '_nv_unimpaired', 'args': {'action': 'blank_up'}},  # noqa: E241
    '[(':           {'command': '_vi_left_square_bracket_target', 'args': {'mode': 'mode_normal', 'target': '('}},  # noqa: E241,E501
    '[e':           {'command': '_nv_unimpaired', 'args': {'action': 'move_up'}},  # noqa: E241
    '[{':           {'command': '_vi_left_square_bracket_target', 'args': {'mode': 'mode_normal', 'target': '{'}},  # noqa: E241,E501
    '] ':           {'command': '_nv_unimpaired', 'args': {'action': 'blank_down'}},  # noqa: E241
    '])':           {'command': '_vi_right_square_bracket_target', 'args': {'mode': 'mode_normal', 'target': ')'}},  # noqa: E241,E501
    ']e':           {'command': '_nv_unimpaired', 'args': {'action': 'move_down'}},  # noqa: E241
    ']}':           {'command': '_vi_right_square_bracket_target', 'args': {'mode': 'mode_normal', 'target': '}'}},  # noqa: E241,E501
    'A':            {'command': '_vi_big_a'},  # noqa: E241
    'at':           {'command': '_vi_select_text_object', 'args': {'text_object': 't', 'inclusive': True}},  # noqa: E241,E501
    'b':            {'command': '_vi_b'},  # noqa: E241
    'c$':           {'command': '_vi_c', 'args': {'motion': {'motion_args': {'count': 1, 'mode': 'mode_internal_normal'}, 'motion': '_vi_dollar', 'is_jump': True}}},  # noqa: E241,E501
    'C':            {'command': '_vi_big_c', 'args': {'register': '"'}},  # noqa: E241
    'c':            {'command': '_vi_c'},  # noqa: E241
    'cc':           {'command': '_vi_cc'},  # noqa: E241
    'ce':           {'command': '_vi_c', 'args': {'motion': {'motion_args': {'count': 1, 'mode': 'mode_internal_normal'}, 'motion': '_vi_e'}}},  # noqa: E241,E501
    'ci"':          {'command': '_vi_c', 'args': {'motion': {'motion_args': {'text_object': "\"", 'inclusive': False, 'mode': 'mode_internal_normal', 'count': 1}, 'motion': '_vi_select_text_object'}}},  # noqa: E241,E501
    'cr ':          {'command': '_nv_abolish', 'args': {'to': 'spacecase'}},  # noqa: E241
    'cr-':          {'command': '_nv_abolish', 'args': {'to': 'dashcase'}},  # noqa: E241
    'cr.':          {'command': '_nv_abolish', 'args': {'to': 'dotcase'}},  # noqa: E241
    'cr_':          {'command': '_nv_abolish', 'args': {'to': 'snakecase'}},  # noqa: E241
    'crc':          {'command': '_nv_abolish', 'args': {'to': 'camelcase'}},  # noqa: E241
    'crk':          {'command': '_nv_abolish', 'args': {'to': 'dashcase'}},  # noqa: E241
    'crm':          {'command': '_nv_abolish', 'args': {'to': 'mixedcase'}},  # noqa: E241
    'crs':          {'command': '_nv_abolish', 'args': {'to': 'snakecase'}},  # noqa: E241
    'crt':          {'command': '_nv_abolish', 'args': {'to': 'titlecase'}},  # noqa: E241
    'cru':          {'command': '_nv_abolish', 'args': {'to': 'uppercase'}},  # noqa: E241
    'crU':          {'command': '_nv_abolish', 'args': {'to': 'uppercase'}},  # noqa: E241
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
    'cst"':         {'command': '_nv_surround', 'args': {'action': 'cs', 'target': 't', 'replacement': '"'}},  # noqa: E241,E501
    'cst<a>':       {'command': '_nv_surround', 'args': {'action': 'cs', 'target': 't', 'replacement': '<a>'}},  # noqa: E241,E501
    'cstta>':       {'command': '_nv_surround', 'args': {'action': 'cs', 'target': 't', 'replacement': 'ta>'}},  # noqa: E241,E501
    'cs{(':         {'command': '_nv_surround', 'args': {'action': 'cs', 'target': '{', 'replacement': '('}},  # noqa: E241,E501
    'cs{)':         {'command': '_nv_surround', 'args': {'action': 'cs', 'target': '{', 'replacement': ')'}},  # noqa: E241,E501
    'cs}(':         {'command': '_nv_surround', 'args': {'action': 'cs', 'target': '}', 'replacement': '('}},  # noqa: E241,E501
    'cs})':         {'command': '_nv_surround', 'args': {'action': 'cs', 'target': '}', 'replacement': ')'}},  # noqa: E241,E501
    'cw':           {'command': '_vi_c', 'args': {'motion': {'motion_args': {'count': 1, 'mode': 'mode_internal_normal'}, 'motion': '_vi_w'}}},  # noqa: E241,E501
    'd$':           {'command': '_vi_d', 'args': {'motion': {'motion_args': {'count': 1, 'mode': 'mode_internal_normal'}, 'motion': '_vi_dollar', 'is_jump': True}}},  # noqa: E241,E501
    'D':            {'command': '_vi_big_d'},  # noqa: E241
    'd':            {'command': '_vi_d'},  # noqa: E241
    'd2ft':         {'command': '_vi_d', 'args': {'motion': {'motion_args': {'count': 2, 'mode': 'mode_internal_normal', 'inclusive': True, 'char': 't'}, 'motion': '_vi_find_in_line'}}},  # noqa: E241,E501
    'dd':           {'command': '_vi_dd'},  # noqa: E241,E501
    'de':           {'command': '_vi_d', 'args': {'motion': {'motion_args': {'count': 1, 'mode': 'mode_internal_normal'}, 'motion': '_vi_e'}}},  # noqa: E241,E501
    'df=':          {'command': '_vi_d', 'args': {'motion': {'motion_args': {'count': 1, 'mode': 'mode_internal_normal', 'inclusive': True, 'char': '='}, 'motion': '_vi_find_in_line'}}},  # noqa: E241,E501
    'dft':          {'command': '_vi_d', 'args': {'motion': {'motion_args': {'count': 1, 'mode': 'mode_internal_normal', 'inclusive': True, 'char': 't'}, 'motion': '_vi_find_in_line'}}},  # noqa: E241,E501
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
    'dw':           {'command': '_vi_d', 'args': {'motion': {'motion_args': {'count': 1, 'mode': 'mode_internal_normal'}, 'motion': '_vi_w'}}},  # noqa: E241,E501
    'e':            {'command': '_vi_e'},  # noqa: E241
    'G':            {'command': '_vi_big_g'},  # noqa: E241
    'gc':           {'command': '_vi_gc'},  # noqa: E241
    'gcc':          {'command': '_vi_gcc_action'},  # noqa: E241
    'gcG':          {'command': '_vi_gc', 'args': {'motion': {'motion_args': {'mode': 'mode_internal_normal'}, 'motion': '_vi_big_g'}}},  # noqa: E241,E501
    'gg':           {'command': '_vi_gg'},  # noqa: E241
    'gJ':           {'command': '_vi_big_j', 'args': {'dont_insert_or_remove_spaces': True}},  # noqa: E241
    'gj':           {'command': '_vi_gj', 'args': {'mode': 'mode_normal'}},  # noqa: E241
    'gk':           {'command': '_vi_gk', 'args': {'mode': 'mode_normal'}},  # noqa: E241
    'gq':           {'command': '_vi_gq', 'args': {'mode': 'mode_visual', 'count': 1}},  # noqa: E241
    'gqip':         {'command': '_vi_gq', 'args': {'motion': {'motion_args': {'inclusive': False, 'mode': 'mode_internal_normal', 'count': 1, 'text_object': 'p'}, 'motion': '_vi_select_text_object'}}},  # noqa: E241,E501
    'gq}':          {'command': '_vi_gq', 'args': {'motion': {'motion_args': {'mode': 'mode_internal_normal', 'count': 1}, 'is_jump': True, 'motion': '_vi_right_brace'}}},  # noqa: E241,E501
    'gU':           {'command': '_vi_g_big_u'},  # noqa: E241
    'gUip':         {'command': '_vi_g_big_u', 'args': {'motion': {'motion_args': {'inclusive': False, 'mode': 'mode_internal_normal', 'count': 1, 'text_object': 'p'}, 'motion': '_vi_select_text_object'}}},  # noqa: E241,E501
    'guis':         {'command': '_vi_gu', 'args': {'motion': {'motion_args': {'inclusive': False, 'mode': 'mode_internal_normal', 'count': 1, 'text_object': 's'}, 'motion': '_vi_select_text_object'}}},  # noqa: E241,E501
    'gv':           {'command': '_vi_gv'},  # noqa: E241
    'h':            {'command': '_vi_h', 'args': {'mode': 'mode_internal_normal', 'count': 1}},  # noqa: E241
    'I':            {'command': '_vi_big_i'},  # noqa: E241
    'it':           {'command': '_vi_select_text_object', 'args': {'text_object': 't', 'inclusive': False}},  # noqa: E241,E501
    'i{':           {'command': '_vi_select_text_object', 'args': {'text_object': '{', 'inclusive': False}},  # noqa: E241,E501
    'i}':           {'command': '_vi_select_text_object', 'args': {'text_object': '}', 'inclusive': False}},  # noqa: E241,E501
    'J':            {'command': '_vi_big_j'},  # noqa: E241
    'l':            {'command': '_vi_l', 'args': {'mode': 'mode_internal_normal', 'count': 1}},  # noqa: E241
    'O':            {'command': '_vi_big_o'},  # noqa: E241
    'o':            {'command': '_vi_o'},  # noqa: E241
    'P':            {'command': '_vi_big_p', 'args': {'register': '"'}},  # noqa: E241
    'p':            {'command': '_vi_p', 'args': {'register': '"'}},  # noqa: E241
    'rx':           {'command': '_vi_r', 'args': {'char': 'x'}},  # noqa: E241
    'S"':           {'command': '_nv_surround_ys', 'args': {'surround_with': '"'}},  # noqa: E241
    'S':            {'command': '_vi_big_s'},  # noqa: E241
    's':            {'command': '_vi_s', 'args': {'register': '"'}},  # noqa: E241
    'U__v__':       {'command': '_vi_visual_big_u'},  # NOTE __v__ is used because several u commands are in separate commands rather than one # noqa: E241,E501
    'u__v__':       {'command': '_vi_visual_u'},  # NOTE __v__ is used because several u commands are in separate commands rather than one # noqa: E241,E501
    'w':            {'command': '_vi_w', 'args': {'mode': 'mode_normal'}},  # noqa: E241
    'X':            {'command': '_vi_big_x'},  # noqa: E241
    'x':            {'command': '_vi_x'},  # noqa: E241
    'y$':           {'command': '_vi_y', 'args': {'register': '"', 'motion': {'is_jump': True, 'motion_args': {'mode': 'mode_internal_normal', 'count': 1}, 'motion': '_vi_dollar'}}},  # noqa: E241,E501
    'y':            {'command': '_vi_y', 'args': {'register': '"'}},  # noqa: E241
    'Y':            {'command': '_vi_yy', 'args': {'register': '"'}},  # noqa: E241
    'yiw':          {'command': '_vi_y', 'args': {'register': '"', 'motion': {'motion_args': {'inclusive': False, 'text_object': 'w', 'mode': 'mode_internal_normal', 'count': 1}, 'motion': '_vi_select_text_object'}}},  # noqa: E241,E501
    'yse"':         {'command': '_nv_surround_ys', 'args': {'surround_with': '"',     'motion': {'motion': '_vi_e', 'motion_args': {'mode': 'mode_internal_normal', 'count': 1}}}},  # noqa: E241,E501
    'yse(':         {'command': '_nv_surround_ys', 'args': {'surround_with': '(',     'motion': {'motion': '_vi_e', 'motion_args': {'mode': 'mode_internal_normal', 'count': 1}}}},  # noqa: E241,E501
    'yse)':         {'command': '_nv_surround_ys', 'args': {'surround_with': ')',     'motion': {'motion': '_vi_e', 'motion_args': {'mode': 'mode_internal_normal', 'count': 1}}}},  # noqa: E241,E501
    'yse2':         {'command': '_nv_surround_ys', 'args': {'surround_with': '2',     'motion': {'motion': '_vi_e', 'motion_args': {'mode': 'mode_internal_normal', 'count': 1}}}},  # noqa: E241,E501
    'yse<foo>':     {'command': '_nv_surround_ys', 'args': {'surround_with': '<foo>', 'motion': {'motion': '_vi_e', 'motion_args': {'mode': 'mode_internal_normal', 'count': 1}}}},  # noqa: E241,E501
    'yse[':         {'command': '_nv_surround_ys', 'args': {'surround_with': '[',     'motion': {'motion': '_vi_e', 'motion_args': {'mode': 'mode_internal_normal', 'count': 1}}}},  # noqa: E241,E501
    'yse\'':        {'command': '_nv_surround_ys', 'args': {'surround_with': '\'',    'motion': {'motion': '_vi_e', 'motion_args': {'mode': 'mode_internal_normal', 'count': 1}}}},  # noqa: E241,E501
    'yse]':         {'command': '_nv_surround_ys', 'args': {'surround_with': ']',     'motion': {'motion': '_vi_e', 'motion_args': {'mode': 'mode_internal_normal', 'count': 1}}}},  # noqa: E241,E501
    'yse{':         {'command': '_nv_surround_ys', 'args': {'surround_with': '{',     'motion': {'motion': '_vi_e', 'motion_args': {'mode': 'mode_internal_normal', 'count': 1}}}},  # noqa: E241,E501
    'yse}':         {'command': '_nv_surround_ys', 'args': {'surround_with': '}',     'motion': {'motion': '_vi_e', 'motion_args': {'mode': 'mode_internal_normal', 'count': 1}}}},  # noqa: E241,E501
    'ysiw"':        {'command': '_nv_surround_ys', 'args': {'surround_with': '"',     'motion': {'motion': '_vi_select_text_object', 'motion_args': {'text_object': 'w', 'mode': 'mode_internal_normal', 'count': 1, 'inclusive': False}}}},  # noqa: E241,E501
    'ysiw(':        {'command': '_nv_surround_ys', 'args': {'surround_with': '(',     'motion': {'motion': '_vi_select_text_object', 'motion_args': {'text_object': 'w', 'mode': 'mode_internal_normal', 'count': 1, 'inclusive': False}}}},  # noqa: E241,E501
    'ysiw)':        {'command': '_nv_surround_ys', 'args': {'surround_with': ')',     'motion': {'motion': '_vi_select_text_object', 'motion_args': {'text_object': 'w', 'mode': 'mode_internal_normal', 'count': 1, 'inclusive': False}}}},  # noqa: E241,E501
    'ysiw2':        {'command': '_nv_surround_ys', 'args': {'surround_with': '2',     'motion': {'motion': '_vi_select_text_object', 'motion_args': {'text_object': 'w', 'mode': 'mode_internal_normal', 'count': 1, 'inclusive': False}}}},  # noqa: E241,E501
    'ysiw<foo>':    {'command': '_nv_surround_ys', 'args': {'surround_with': '<foo>', 'motion': {'motion': '_vi_select_text_object', 'motion_args': {'text_object': 'w', 'mode': 'mode_internal_normal', 'count': 1, 'inclusive': False}}}},  # noqa: E241,E501
    'ysiw[':        {'command': '_nv_surround_ys', 'args': {'surround_with': '[',     'motion': {'motion': '_vi_select_text_object', 'motion_args': {'text_object': 'w', 'mode': 'mode_internal_normal', 'count': 1, 'inclusive': False}}}},  # noqa: E241,E501
    'ysiw\'':       {'command': '_nv_surround_ys', 'args': {'surround_with': '\'',    'motion': {'motion': '_vi_select_text_object', 'motion_args': {'text_object': 'w', 'mode': 'mode_internal_normal', 'count': 1, 'inclusive': False}}}},  # noqa: E241,E501
    'ysiw]':        {'command': '_nv_surround_ys', 'args': {'surround_with': ']',     'motion': {'motion': '_vi_select_text_object', 'motion_args': {'text_object': 'w', 'mode': 'mode_internal_normal', 'count': 1, 'inclusive': False}}}},  # noqa: E241,E501
    'ysiw{':        {'command': '_nv_surround_ys', 'args': {'surround_with': '{',     'motion': {'motion': '_vi_select_text_object', 'motion_args': {'text_object': 'w', 'mode': 'mode_internal_normal', 'count': 1, 'inclusive': False}}}},  # noqa: E241,E501
    'ysiw}':        {'command': '_nv_surround_ys', 'args': {'surround_with': '}',     'motion': {'motion': '_vi_select_text_object', 'motion_args': {'text_object': 'w', 'mode': 'mode_internal_normal', 'count': 1, 'inclusive': False}}}},  # noqa: E241,E501
    'yy':           {'command': '_vi_yy', 'args': {'register': '"'}},  # noqa: E241

}
