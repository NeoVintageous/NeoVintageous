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

from NeoVintageous.nv.vim import COMMAND_LINE  # noqa: F401
from NeoVintageous.nv.vim import CTRL_X  # noqa: F401
from NeoVintageous.nv.vim import INSERT  # noqa: F401
from NeoVintageous.nv.vim import INTERNAL_NORMAL  # noqa: F401
from NeoVintageous.nv.vim import NORMAL  # noqa: F401
from NeoVintageous.nv.vim import NORMAL_INSERT  # noqa: F401
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
        #   a (int): The first end of the region.
        #   b (int, optional): The second end of the region. Defaults to the
        #       same as the a end of the region. May be less that a, in
        #       which case the region is a reversed one.
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

    def _fixture(self, text, mode):
        if mode in (VISUAL, VISUAL_BLOCK, VISUAL_LINE):
            self.view.run_command('_nv_test_write', {'text': text.replace('|', '')})
            sels = [i for i, c in enumerate(text) if c == '|']
            sel_len = len(sels)

            if sel_len == 1:
                sels.append(sels[0] + 2)
            elif sel_len % 2 != 0 or sel_len == 0:
                raise Exception('invalid fixture visual selection')

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
                self.view.sel().add_all(v_sels)
        else:
            self.view.run_command('_nv_test_write', {'text': text.replace('|', '')})
            sels = [i for i, c in enumerate(text) if c == '|']
            if sels:
                self.view.sel().clear()
                for i, x in enumerate(sels):
                    self.view.sel().add(x - i)

        self.state.mode = mode

    def fixture(self, text):
        # Args:
        #   text (str)
        self._fixture(text, NORMAL)

    def iFixture(self, text):
        # Args:
        #   text (str)
        self._fixture(text, INSERT)

    def vFixture(self, text):
        # Args:
        #   text (str)
        self._fixture(text, VISUAL)

    def vLineFixture(self, text):
        # Args:
        #   text (str)
        self._fixture(text, VISUAL_LINE)

    def vBlockFixture(self, text):
        # Args:
        #   text (str)
        self._fixture(text, VISUAL_BLOCK)

    def _expects(self, expected, mode, msg):
        # Args:
        #   expected (str)
        #   mode (str)
        #   msg (str)
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

    def expects(self, expected, msg=None):
        # Args:
        #   expected (str)
        #   msg (str)
        self._expects(expected, NORMAL, msg)

    def expectsI(self, expected, msg=None):
        # Args:
        #   expected (str)
        #   msg (str)
        self._expects(expected, INSERT, msg)

    def expectsV(self, expected, msg=None):
        # Args:
        #   expected (str)
        #   msg (str)
        self._expects(expected, VISUAL, msg)

    def expectsVLine(self, expected, msg=None):
        # Args:
        #   expected (str)
        #   msg (str)
        self._expects(expected, VISUAL_LINE, msg)

    def expectsVBlock(self, expected, msg=None):
        # Args:
        #   expected (str)
        #   msg (str)
        self._expects(expected, VISUAL_BLOCK, msg)

    def assertContent(self, expected, msg=None):
        # Test that view contents and *expected* are equal.
        #
        # Args:
        #   expected (str): Expected view contents.
        #   msg (str, optional): If specified, is used as the error message on
        #       failure.
        self.assertEqual(self.content(), expected, msg)

    def assertContentRegex(self, expected, msg=None):
        # Test that view contents matches (or does not match) *expected*.
        #
        # Args:
        #   expected (str): Expected regular expression that should match view
        #       contents.
        #   msg (str, optional): If specified, is used as the error message on
        #       failure.
        self.assertRegex(self.content(), expected, msg=msg)

    def _assertMode(self, mode):
        self.assertEquals(self.state.mode, mode)

    def assertInsertMode(self):
        self._assertMode(INSERT)

    def assertNormalMode(self):
        self._assertMode(NORMAL)

    def assertVisualMode(self):
        self._assertMode(VISUAL)

    def assertVisualBlockMode(self):
        self._assertMode(VISUAL_BLOCK)

    def assertVisualLineMode(self):
        self._assertMode(VISUAL_LINE)

    def assertRegion(self, expected, actual):
        # Test that *actual* and *expected* are equal.
        #
        # Args:
        #   expected (str|int|tuple|Region): If the expected value is a str,
        #       int, or a tuple, it will be converted to a Region before
        #       evaluating against the actual value.
        #   actual (Region): Actual region.
        if isinstance(expected, str):
            self.assertEqual(expected, self.view.substr(actual))
        elif isinstance(expected, int):
            self.assertEqual(Region(expected), actual)
        elif isinstance(expected, tuple):
            self.assertEqual(Region(expected[0], expected[1]), actual)
        else:
            self.assertEqual(expected, actual)

    def assertSelection(self, expected):
        # Test that view selection and *expected* are equal.
        #
        # Args:
        #   expected (int|tuple|Region|list<Region>):
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
            self.assertEqual([Region(expected)], list(self.view.sel()))
        elif isinstance(expected, tuple):
            self.assertEqual([Region(expected[0], expected[1])], list(self.view.sel()))
        elif isinstance(expected, Region):
            self.assertEqual([expected], list(self.view.sel()))
        else:
            # Defaults to expect a list of Regions.
            self.assertEqual(expected, list(self.view.sel()))

    def assertSelectionCount(self, expected):
        # Test that view selection count and *expected* are equal.
        #
        # Args:
        #   expected (int): Expected number of selections in view.
        self.assertEqual(expected, len(self.view.sel()))

    def assertSize(self, expected):
        # Test that number of view characters and *expected* are equal.
        #
        # Args:
        #   expected (int): Expected number of characters in view.
        self.assertEqual(expected, self.view.size())

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
    'v': VISUAL
}


class FunctionalTestCase(ViewTestCase):

    def feed(self, seq):
        # Args:
        #   seq (str): A command sequence e.g. 3w, <C-a>, cs'", :pwd
        #
        # The seq can be prefixed to specify a mode:
        #
        #   * n_ - Normal
        #   * i_ - Insert
        #   * v_ - Visual
        #
        # The default mode is Internal Normal.
        #
        # NOTE: This function currently uses a **hardcoded** map of sequences to
        # commands. You may need to add the a sequence to command map value. See
        # the _feedseq2cmd variable.
        #
        # Examples:
        #
        # >>> feed('w')
        # >>> feed('3w')
        # >>> feed('v_w')
        # >>> feed('<Esc>')
        # >>> feed(':pwd')
        # >>> feed(':help neovintageous')

        if seq == '<Esc>':
            return self.view.window().run_command('_nv_feed_key', {'key': '<esc>'})

        if seq[0] == ':':
            return _do_ex_cmdline(self.view.window(), seq)

        seq_args = {}

        if seq[0] in 'vin' and seq[1] == '_':
            seq_args['mode'] = _char2mode[seq[0]]
            seq = seq[2:]

        if seq[0].isdigit():
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

    def eq(self, fixture, feed, expected=None, msg=None):
        # Args:
        #   fixture (str):
        #   feed (str):
        #   expected (str):
        #   msg (str):
        #
        # The feed and expected can be prefixed to specify a mode:
        #
        #   * n_ - Normal
        #   * i_ - Insert
        #   * v_ - Visual
        #   * :<','> - Visual cmdline (only valid for feed)
        #
        # The default mode is Normal.
        #
        # Examples:
        #
        # >>> eq('|Hello world!', 'w', 'Hello |world!')
        # >>> eq('|H|ello world!', 'v_w', '|Hello w|orld!')
        # >>> eq('a\nx|y\nb', 'cc', 'i_a\n|\nb')

        if expected is None:
            expected = fixture

        if feed[0] in ('v', ':') and (feed[1] == '_' or feed.startswith(':\'<,\'>')):
            self.vFixture(fixture)
            self.feed(feed)
            if expected[:2] == 'n_':
                self.expects(expected[2:], msg)
            elif expected[:2] == 'i_':
                self.expectsI(expected[2:], msg)
            else:
                self.expectsV(expected, msg)
        else:
            self.fixture(fixture)
            self.feed(feed)
            if expected[:2] == 'v_':
                self.expectsV(expected[2:], msg)
            elif expected[:2] == 'i_':
                self.expectsI(expected[2:], msg)
            else:
                self.expects(expected, msg)


# A hardcoded map of sequences to commands. Ideally we wouldn't need this
# hardcoded map, some internal refactoring and redesign is required to make that
# happen. For now make-do with the hardcoded map. Refactoring later should not
# impact the existing tests.
_feedseq2cmd = {

    '$':            {'command': '_vi_dollar', 'args': {'mode': 'mode_normal'}},  # noqa: E241
    'b':            {'command': '_vi_b', 'args': {'mode': 'mode_normal'}},  # noqa: E241
    'cc':           {'command': '_vi_cc'},  # noqa: E241

}
