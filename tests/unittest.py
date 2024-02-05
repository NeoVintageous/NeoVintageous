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

from string import ascii_uppercase
from unittest import TestCase  # noqa: F401
from unittest import expectedFailure  # noqa: F401
from unittest import mock  # noqa: F401
from unittest import skip  # noqa: F401
from unittest import skipIf  # noqa: F401
import copy
import os
import re
import sys
import tempfile
import textwrap
import unittest

# Use aliases to indicate that they are not public testing APIs.
from sublime import Region
from sublime import active_window as _active_window
from sublime import get_clipboard as _get_clipboard
from sublime import platform as _platform
from sublime import set_clipboard as _set_clipboard
from sublime import version as _version

from NeoVintageous.nv import macros
from NeoVintageous.nv.cmdline import Cmdline
from NeoVintageous.nv.ex_cmds import do_ex_cmdline
from NeoVintageous.nv.mappings import _mappings
from NeoVintageous.nv.marks import _get_key
from NeoVintageous.nv.marks import get_mark
from NeoVintageous.nv.marks import get_marks
from NeoVintageous.nv.marks import set_mark
from NeoVintageous.nv.options import get_option
from NeoVintageous.nv.options import set_option
from NeoVintageous.nv.polyfill import view_to_region
from NeoVintageous.nv.polyfill import view_to_str
from NeoVintageous.nv.registers import _get as _get_register
from NeoVintageous.nv.registers import _is_register_linewise
from NeoVintageous.nv.registers import _reset
from NeoVintageous.nv.registers import _set_data
from NeoVintageous.nv.registers import _set_numbered_register
from NeoVintageous.nv.settings import get_mode
from NeoVintageous.nv.settings import get_setting
from NeoVintageous.nv.settings import get_visual_block_direction
from NeoVintageous.nv.settings import get_xpos
from NeoVintageous.nv.settings import reset_setting
from NeoVintageous.nv.settings import set_last_search_pattern
from NeoVintageous.nv.settings import set_mode
from NeoVintageous.nv.settings import set_reset_during_init
from NeoVintageous.nv.settings import set_setting
from NeoVintageous.nv.settings import set_visual_block_direction
from NeoVintageous.nv.settings import set_xpos
from NeoVintageous.nv.vim import DIRECTION_DOWN
from NeoVintageous.nv.vim import DIRECTION_UP
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


_MODES = (
    NORMAL,
    OPERATOR_PENDING,
    SELECT,
    VISUAL,
    VISUAL_BLOCK,
    VISUAL_LINE
)


ST_VERSION = int(_version())


def is_py38() -> bool:
    return sys.version_info >= (3, 8)


def is_osx() -> bool:
    return _platform() == 'osx'


def is_windows() -> bool:
    return _platform() == 'windows'


class ViewTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.view = _active_window().new_file()

    def tearDown(self) -> None:
        if self.view:
            self.view.set_scratch(True)
            self.view.close()

    def platform(self) -> str:
        return _platform()

    def view_to_region(self):
        return view_to_region(self.view)

    def content(self) -> str:
        return view_to_str(self.view)

    def Region(self, a: int, b: int = None) -> Region:
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

    def select(self, selections) -> None:
        # Create selection in the view.
        #
        # Args:
        #   selections (int|tuple|Region|list<int|tuple|Region>)
        #
        # Existing selections are cleared.
        #
        # Integers and tuples are converted to Regions:
        #
        # >>> select(3)
        #
        # is the short for:
        #
        # >>> select(sublime.Region(3))
        #
        # >>> select((3, 5))
        #
        # is short for:
        #
        # >>> select(sublime.Region(3, 5))
        #
        # INT
        #
        # Select a single point:
        #
        # >>> select(3)
        #
        # TUPLE
        #
        # Select a region, for example, point 3 to 5:
        #
        # >>> select((3, 5))
        #
        # LIST of INTS
        #
        # Select multiple selections, for example, points, 3, 5, and 7:
        #
        # >>> select([3, 5, 7])
        #
        # LIST of TUPLES
        #
        # Select multiple text selections:
        #
        # >>> select([(3, 5), (7, 11)])
        #
        # MIXED LIST
        #
        # Select multiple points, and text selections:
        #
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

    def set_setting(self, name: str, value) -> None:
        set_setting(self.view, name, value)

    def get_setting(self, name: str):
        return get_setting(self.view, name)

    def reset_setting(self, name: str) -> None:
        reset_setting(self.view, name)

    def set_wrap(self, width: int) -> None:
        self.settings().set('word_wrap', True)
        self.set_wrap_width(width)

    def set_wrap_width(self, width: int) -> None:
        # Wrap width has some issues in Sublime Text 4.
        v = int(_version())
        if v >= 4000 and (v < 4129 or v >= 4148):
            width -= 1

        self.settings().set('wrap_width', width)

    def dedent(self, text: str) -> str:
        return textwrap.dedent(text)

    def assertSetting(self, name: str, expected) -> None:
        self.assertEqual(self.settings().get(name), expected)

    def assertNotSetting(self, name: str) -> None:
        self.assertFalse(self.settings().has(name))
        # NOTE Some settings prefixes are deprecated.
        self.assertFalse(self.settings().has('_neovintageous_%s' % name))
        self.assertFalse(self.settings().has('_vi_%s' % name))
        self.assertFalse(self.settings().has('_vintageous_%s' % name))
        self.assertFalse(self.settings().has('neovintageous_%s' % name))
        self.assertFalse(self.settings().has('vi_%s' % name))
        self.assertFalse(self.settings().has('vintageous_%s' % name))

    def set_option(self, name: str, value, setting: bool = True) -> None:
        set_option(self.view, name, value)
        if setting:  # DEPRECATED Options via settings is deprecated
            set_setting(self.view, name, value)

    def get_option(self, name: str, view=None):
        return get_option(self.view if view is None else view, name)

    def assertOption(self, name: str, expected, msg: str = None) -> None:
        self.assertEqual(self.get_option(name), expected, msg=msg)

    def syntax(self, syntax_file: str) -> None:
        self.view.assign_syntax(syntax_file)

    def fixturePath(self, *args) -> str:
        return os.path.realpath(os.path.join(os.path.dirname(__file__), 'fixtures', *args))

    def rootPath(self) -> str:
        return os.path.realpath(os.path.dirname(os.path.dirname(__file__)))

    def assignFileName(self, rel_file_name) -> None:
        with tempfile.TemporaryDirectory() as tmpdirname:
            self.view.retarget(os.path.join(tmpdirname, rel_file_name))

    def write(self, text: str) -> None:
        self.view.run_command('nv_test_write', {'text': text})

    def _setupView(self, text: str, mode: str, reverse: bool = False, vblock_direction: int = None):
        if mode in (VISUAL, VISUAL_BLOCK, VISUAL_LINE, INTERNAL_NORMAL, SELECT):
            self.view.run_command('nv_test_write', {'text': text.replace('|', '')})
            sels = [i for i, c in enumerate(text) if c == '|']
            sel_len = len(sels)

            if sel_len == 1:
                sels.append(sels[0] + 2)
            elif sel_len % 2 != 0 or sel_len == 0:
                raise Exception('invalid visual selection: mode=%s reverse=%s' % (mode, reverse))

            if sels:
                v_sels = []  # type: list
                a = None
                for i, x in enumerate(sels):
                    if a is None:
                        a = x - i
                    else:
                        v_sels.append(Region(a, x - i))  # type: ignore[unreachable]
                        a = None

                self.view.sel().clear()

                if reverse:
                    v_sels.sort(reverse=True)
                    for s in v_sels:
                        self.view.sel().add(Region(s.b, s.a))
                else:
                    self.view.sel().add_all(v_sels)  # type: ignore[arg-type]

            # This is required because the cursor in VISUAL mode is a block
            # cursor. Without this setting some tests will pass when the window
            # running the tests has focus and fail when it doesn't have focus.
            # This happens because Sublime doesn't fire events for views when
            # the window loses focus (usually the on_activated() event fixes
            # VISUAL mode selections that don't have a correct cursor state).
            self.view.settings().set('inverse_caret_state', True)

            if mode == VISUAL_BLOCK:
                if vblock_direction:
                    set_visual_block_direction(self.view, vblock_direction)
                elif len(self.view.sel()) > 1:
                    set_visual_block_direction(self.view, DIRECTION_DOWN)
        else:
            self.view.run_command('nv_test_write', {'text': text.replace('|', '')})
            sels = [i for i, c in enumerate(text) if c == '|']
            if sels:
                self.view.sel().clear()
                for i, x in enumerate(sels):
                    self.view.sel().add(x - i)

        set_mode(self.view, mode)

    def setNormalMode(self):
        set_mode(self.view, NORMAL)

    def setVisualMode(self):
        set_mode(self.view, VISUAL)

    def insert(self, text: str) -> None:
        self._setupView(text, INSERT)

    def internalNormal(self, text: str) -> None:
        self._setupView(text, INTERNAL_NORMAL)

    def rinternalNormal(self, text: str) -> None:
        self._setupView(text, INTERNAL_NORMAL, reverse=True)

    def normal(self, text: str) -> None:
        self._setupView(text, NORMAL)

    def visual(self, text: str) -> None:
        self._setupView(text, VISUAL)

    def rvisual(self, text: str) -> None:
        self._setupView(text, VISUAL, reverse=True)

    def vselect(self, text: str) -> None:
        self._setupView(text, SELECT)

    def rvselect(self, text: str) -> None:
        self._setupView(text, SELECT, reverse=True)

    def vblock(self, text: str, direction: int = DIRECTION_DOWN) -> None:
        self._setupView(text, VISUAL_BLOCK, vblock_direction=direction)

    def rvblock(self, text: str, direction: int = DIRECTION_DOWN) -> None:
        self._setupView(text, VISUAL_BLOCK, reverse=True, vblock_direction=direction)

    def vline(self, text: str) -> None:
        self._setupView(text, VISUAL_LINE)

    def rvline(self, text: str) -> None:
        self._setupView(text, VISUAL_LINE, reverse=True)

    def register(self, name: str, value=None, linewise: bool = False) -> None:
        if value is None:
            value = name[1:]
            name = name[0]

        if not isinstance(value, list):
            value = [value]

        if name.isdigit() and name != '0':
            _set_numbered_register(name, value, linewise)
        else:
            _set_data(name, value, linewise)

    def registerLinewise(self, name: str, value=None) -> None:
        self.register(name, value, linewise=True)

    def resetRegisters(self, values=None) -> None:
        _reset()
        _set_clipboard('')

    def resetMarks(self):
        window = self.view.window()
        if window:
            for view in window.views():
                for character in ascii_uppercase:
                    view.erase_regions(_get_key(character))

    def resetMacros(self) -> None:
        macros._data.clear()

    def setMark(self, name: str, pt: int) -> None:
        sels = list(self.view.sel())
        self.select(pt)
        set_mark(self.view, name)
        self.view.sel().clear()
        self.view.sel().add_all(sels)  # type: ignore[arg-type]

    def assertHasMarks(self, expected: str) -> None:
        self.assertEqual([m for m in expected], sorted([m for m in get_marks(self.view)]))

    def assertNoMark(self, name: str) -> None:
        self.assertIsNone(get_mark(self.view, name))

    def assertNoMarks(self) -> None:
        self.assertEqual([], [m for m in get_marks(self.view)])

    def assertMarkContent(self, name: str, expected) -> None:
        self._assertContentSelection([get_mark(self.view, name)], expected)

    def assertMarksOutput(self, expected: str):
        self.assertEquals('mark line  col file/text\n' +
                          expected + ('' if expected == '' else '\n') +
                          '\nPress ENTER to continue',
                          self.commandLineOutput())

    def assertNoMarksOutput(self):
        self.assertMarksOutput('')

    def assertMapping(self, mode: str, lhs: str, rhs: str) -> None:
        self.assertIn(lhs, _mappings[mode])
        self.assertEqual(_mappings[mode][lhs], rhs)

    def assertMappings(self, expected: dict) -> None:
        self.assertEqual(_mappings, expected)

    def assertMappingsEmpty(self) -> None:
        self.assertEqual(_mappings, {
            INSERT: {},
            NORMAL: {},
            OPERATOR_PENDING: {},
            SELECT: {},
            VISUAL_BLOCK: {},
            VISUAL_LINE: {},
            VISUAL: {},
        })

    def assertNotMapping(self, lhs: str, mode: str = None) -> None:
        if mode is None:
            for m in _MODES:
                self.assertNotIn(lhs, _mappings[m])
        else:
            self.assertNotIn(lhs, _mappings[mode])

    def assertContent(self, expected, msg: str = None) -> None:
        self.assertEqual(self.content(), expected, msg)

    def commandLineOutput(self) -> str:
        return view_to_str(self.view.window().find_output_panel('Command-line'))  # type: ignore[union-attr]

    def assertCommandLineOutput(self, expected, msg: str = None) -> None:
        self.view.window().focus_group(self.view.window().active_group())  # type: ignore[union-attr]
        self.assertEqual(self.commandLineOutput(), expected + "\nPress ENTER to continue", msg)

    def closeExPrintOutputViews(self) -> None:
        for v in self.view.window().views():  # type: ignore[union-attr]
            if v.is_scratch() and v.settings().get('nv_ex_print_output'):
                v.close()

    def exPrintOutputView(self):
        for v in self.view.window().views():  # type: ignore[union-attr]
            if v.is_scratch() and v.settings().get('nv_ex_print_output'):
                return v

    def exPrintOutput(self) -> str:
        v = self.exPrintOutputView()
        if v:
            return view_to_str(v)

        return ''

    def assertExPrintOutput(self, expected, msg: str = None) -> None:
        self.assertEqual(self.exPrintOutput(), expected, msg)

    def assertContentRegex(self, expected_regex: str, msg: str = None) -> None:
        self.assertRegex(self.content(), expected_regex, msg=msg)

    def assertViewRegionsEmpty(self, key: str, msg: str = None) -> None:
        self.assertEqual([], self.view.get_regions(key))

    def _assertContentSelection(self, sels: list, expected: str, msg: str = None) -> None:
        content = list(self.view.substr(Region(0, self.view.size())))
        counter = 0
        for sel in sels:
            content.insert(sel.begin() + counter, '|')
            counter += 1
            if sel.end() != sel.begin():
                content.insert(sel.end() + counter, '|')
                counter += 1

        self.assertEquals(expected, ''.join(content), msg)

    def _assertContentRegion(self, key: str, expected, msg: str = None) -> None:
        self._assertContentSelection(self.view.get_regions(key), expected, msg)

    def _assertView(self, expected, mode: str, msg: str) -> None:
        self._assertContentSelection(list(self.view.sel()), expected, msg)
        self._assertMode(mode)

    def assertSearch(self, expected: str, msg: str = None) -> None:
        self._assertContentRegion('_nv_search_occ', expected, msg)

    def assertSearchCurrent(self, expected: str, msg: str = None) -> None:
        self._assertContentRegion('_nv_search_cur', expected, msg)

    def assertSearchIncremental(self, expected: str, msg: str = None) -> None:
        self._assertContentRegion('_nv_search_inc', expected, msg)

    def assertNoSearch(self) -> None:
        content = self.content()
        self.assertSearch(content)
        self.assertSearchCurrent(content)
        self.assertSearchIncremental(content)

    def setLastSearchPattern(self, pattern: str, command: str) -> None:
        set_last_search_pattern(self.view, pattern, command)

    def assertHighlightedYank(self, expected: str, msg: str = None) -> None:
        self._assertContentRegion('highlightedyank', expected, msg)

    def assertNoHighlightedYank(self, msg: str = None) -> None:
        self.assertViewRegionsEmpty('highlightedyank', msg)

    def assertInsert(self, expected, msg: str = None) -> None:
        self._assertView(expected, INSERT, msg)  # type: ignore[arg-type]
        for sel in self.view.sel():
            self.assertTrue(sel.b == sel.a, 'failed asserting selection is a valid INSERT mode selection')

    def assertInternalNormal(self, expected, strict: bool = False, msg: str = None) -> None:
        self._assertView(expected, INTERNAL_NORMAL if strict else NORMAL, msg)  # type: ignore[arg-type]
        self.assertSelectionIsNotReversed()

    def assertRInternalNormal(self, expected, strict: bool = False, msg: str = None) -> None:
        self._assertView(expected, INTERNAL_NORMAL if strict else NORMAL, msg)  # type: ignore[arg-type]
        self.assertSelectionIsReversed()

    def assertNormal(self, expected, msg: str = None) -> None:
        self._assertView(expected, NORMAL, msg)  # type: ignore[arg-type]
        for sel in self.view.sel():
            self.assertTrue(sel.b == sel.a, 'failed asserting selection is a valid NORMAL mode selection')

    def assertReplace(self, expected, msg: str = None) -> None:
        self._assertView(expected, REPLACE, msg)  # type: ignore[arg-type]
        for sel in self.view.sel():
            self.assertTrue(sel.b == sel.a, 'failed asserting selection is a valid REPLACE mode selection')

    def assertVisual(self, expected, msg: str = None) -> None:
        self._assertView(expected, VISUAL, msg)  # type: ignore[arg-type]
        self.assertSelectionIsNotReversed()

    def assertRVisual(self, expected, msg: str = None) -> None:
        self._assertView(expected, VISUAL, msg)  # type: ignore[arg-type]
        self.assertSelectionIsReversed()

    def assertVselect(self, expected, msg: str = None) -> None:
        self._assertView(expected, SELECT, msg)  # type: ignore[arg-type]
        self.assertSelectionIsNotReversed()

    def assertRVselect(self, expected, msg: str = None) -> None:
        self._assertView(expected, SELECT, msg)  # type: ignore[arg-type]
        self.assertSelectionIsReversed()

    def assertVblock(self, expected, direction: int = DIRECTION_DOWN, msg: str = None) -> None:
        self._assertView(expected, VISUAL_BLOCK, msg)  # type: ignore[arg-type]
        self.assertSelectionIsNotReversed()
        self.assertVblockDirection(direction)

    def assertRVblock(self, expected, direction: int = DIRECTION_DOWN, msg: str = None) -> None:
        self._assertView(expected, VISUAL_BLOCK, msg)  # type: ignore[arg-type]
        self.assertSelectionIsReversed()
        self.assertVblockDirection(direction, msg)

    def assertVline(self, expected, msg: str = None) -> None:
        self._assertView(expected, VISUAL_LINE, msg)  # type: ignore[arg-type]
        self.assertSelectionIsNotReversed()

    def assertRVline(self, expected, msg: str = None) -> None:
        self._assertView(expected, VISUAL_LINE, msg)  # type: ignore[arg-type]
        self.assertSelectionIsReversed()

    def _assertMode(self, mode: str) -> None:
        self.assertEquals(mode, get_mode(self.view))

    def assertInsertMode(self) -> None:
        self._assertMode(INSERT)

    def assertInternalNormalMode(self) -> None:
        self._assertMode(INTERNAL_NORMAL)

    def assertNormalMode(self) -> None:
        self._assertMode(NORMAL)

    def assertReplaceMode(self) -> None:
        self._assertMode(REPLACE)

    def assertSelectMode(self) -> None:
        self._assertMode(SELECT)

    def assertVisualMode(self) -> None:
        self._assertMode(VISUAL)

    def assertVblockMode(self) -> None:
        self._assertMode(VISUAL_BLOCK)

    def assertVlineMode(self) -> None:
        self._assertMode(VISUAL_LINE)

    def assertRegion(self, actual, expected) -> None:
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

    def assertVisibleRegion(self, expected) -> None:
        self.assertRegion(self.view.visible_region(), expected)

    def _assertRegister(self, name: str, expected, linewise: bool = False, msg: str = None) -> None:
        if expected is not None and not isinstance(expected, list):
            expected = [expected]

        self.assertEqual(_get_register(self.view, name), expected, msg or 'for register "' + name + '"')

        if expected is not None:
            self.assertEqual(_is_register_linewise(name), linewise, msg or 'register (linewise) = "' + name)

    def assertRegister(self, name: str, expected=None, linewise: bool = False, msg: str = None) -> None:
        """Test that value for the register content for name and expected are equal.

        Args:
          name (str): The name of the register.
          expected (str|list|None): The expected registered content.

        Usage:
          self.assertRegister('"text')
          self.assertRegister('"', 'text')
          self.assertRegister('"', ['x', 'y'])  # multiple cursors
        """
        if expected is None:
            expected = name[1:]
            name = name[0]

        self._assertRegister(name, expected, linewise, msg)

    def assertRegisters(self, names: str, expected=None, empty_names: str = '', msg: str = None) -> None:
        """Test that value for the register content for names and expected are equal.

        Usage:
          self.assertRegisters('ab', 'text')
          self.assertRegisters('ab', ['x', 'y'])  # multiple cursors
        """
        for name in names:
            self.assertRegister(name, expected, msg=msg)

        for name in empty_names:
            self.assertRegisterEmpty(name, msg)

    def assertLinewiseRegister(self, name: str, expected=None, msg: str = None) -> None:
        if expected is None:
            expected = name[1:]
            name = name[0]

        self._assertRegister(name, expected, linewise=True, msg=msg)

    def assertLinewiseRegisters(self, names: str, expected=None, empty_names: str = '', msg: str = None) -> None:
        for name in names:
            self.assertLinewiseRegister(name, expected, msg)

        for name in empty_names:
            self.assertRegisterEmpty(name, msg)

    def assertRegisterEmpty(self, name: str, msg: str = None) -> None:
        self._assertRegister(name, None, msg=msg)

    def assertRegistersEmpty(self, names: str, msg: str = None) -> None:
        for name in names:
            self.assertRegisterEmpty(name, msg)

    def assertClipboard(self, expected: str, msg: str = None) -> None:
        self.assertEqual(expected, _get_clipboard(), msg)

    def assertClipboardEmpty(self, msg: str = None) -> None:
        self.assertEqual('', _get_clipboard(), msg)

    def assertSelection(self, expected, msg: str = None) -> None:
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

    def assertSelectionCount(self, expected) -> None:
        self.assertEqual(expected, len(self.view.sel()))

    def assertSelectionIsNotReversed(self) -> None:
        for sel in self.view.sel():
            self.assertTrue(sel.b >= sel.a, 'failed asserting selection is not reversed')

    def assertSelectionIsReversed(self) -> None:
        for sel in self.view.sel():
            self.assertGreater(sel.a, sel.b, 'failed asserting selection is reversed')

    def assertSize(self, expected) -> None:
        self.assertEqual(expected, self.view.size())

    def assertVblockDirection(self, expected, msg: str = None) -> None:
        self.assertEqual(self.getVblockDirection(), expected, msg=msg)

    def getVblockDirection(self):
        return get_visual_block_direction(self.view)

    def _statusLine(self) -> str:
        return (
            self.view.get_status('vim-mode') + ' ' +
            self.view.get_status('vim-seq') + ' ' +
            self.view.get_status('vim-recording')).strip()

    def assertStatusLineEqual(self, expected, msg: str = None) -> None:
        self.assertEqual(expected, self._statusLine(), msg=msg)

    def assertStatusLineRegex(self, expected_regex: str, msg: str = None) -> None:
        self.assertRegex(self._statusLine(), expected_regex, msg=msg)

    def assertStatusLineIsBlank(self, msg: str = None) -> None:
        self.assertStatusLineEqual('', msg)

    def assertStatusLineIsInsert(self, msg: str = None) -> None:
        self.assertStatusLineEqual('-- INSERT --', msg)

    def assertStatusLineIsNormal(self, msg: str = None) -> None:
        self.assertStatusLineEqual('', msg)

    def assertStatusLineIsReplace(self, msg: str = None) -> None:
        self.assertStatusLineEqual('-- REPLACE --', msg)

    def assertStatusLineIsSelect(self, msg: str = None) -> None:
        self.assertStatusLineEqual('-- SELECT --', msg)

    def assertStatusLineIsVisual(self, msg: str = None) -> None:
        self.assertStatusLineEqual('-- VISUAL --', msg)

    def assertStatusLineIsVisualLine(self, msg: str = None) -> None:
        self.assertStatusLineEqual('-- VISUAL LINE --', msg)

    def assertStatusLineIsVisualBlock(self, msg: str = None) -> None:
        self.assertStatusLineEqual('-- VISUAL BLOCK --', msg)

    def assertXpos(self, expected, msg: str = None) -> None:
        self.assertEqual(get_xpos(self.view), expected, msg)

    # >>> assertFolded([Region(5, 14)])
    # >>> assertFolded(Region(5, 14))
    # >>> assertFolded('<div>|\n    xxxx|\n</div>')
    def assertFolded(self, expected) -> None:
        if isinstance(expected, str):
            self._assertContentSelection(self.view.folded_regions(), expected)
        else:
            if isinstance(expected, Region):
                expected = [expected]

            self.assertEqual(expected, self.view.folded_regions())

    def assertNotFolded(self):
        self.assertEqual([], self.view.folded_regions())

    def setXpos(self, xpos: int) -> None:
        set_xpos(self.view, xpos)

    def assertMockNotCalled(self, mock) -> None:
        # https://docs.python.org/3/library/unittest.mock.html
        # Polyfill for a new mock method added in version 3.5.
        if sys.version_info >= (3, 5):  # pragma: no cover
            mock.assert_not_called()
        else:
            self.assertEqual(mock.call_count, 0)

    def initCmdlineSearchMock(self, mock, type: str, event: str, pattern: str = None) -> None:
        class MockCmdlineOnDone(Cmdline):
            _mock_pattern = None

            def prompt(cmdline, pattern: str) -> None:
                args = []  # type: list
                if cmdline._mock_pattern is not None:
                    args.append(cmdline._mock_pattern)  # type: ignore[unreachable]

                cmdline._callbacks[cmdline._mock_event](*args)  # type: ignore[attr-defined]
                set_reset_during_init(self.view, True)

        if type == '?':
            mock.SEARCH_BACKWARD = '?'
        elif type == '/':
            mock.SEARCH_FORWARD = '/'

        if pattern is not None:
            MockCmdlineOnDone._mock_pattern = pattern  # type: ignore[assignment]

        MockCmdlineOnDone._mock_event = event  # type: ignore[attr-defined]
        mock.side_effect = MockCmdlineOnDone

    # DEPRECATED Use newer APIs e.g. self.Region(), unittest.Region.
    def _R(self, a: int, b: int = None) -> Region:  # type: ignore[valid-type]
        return _make_region(self.view, a, b)

    # DEPRECATED Use newer APIs e.g. assertRegion(), assertSelection(), and assertContent().
    def _assertRegionsEqual(self, expected_region, actual_region, msg: str = None) -> None:
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
    'V': VISUAL_LINE,
    'b': VISUAL_BLOCK
}


_FEEDCHAR2KEY = {
    ' ': '<space>',
    '<': '<lt>',
    '|': '<bar>'
}


_SEQ_PARSER = re.compile('(?:([vinVbs])_)?([1-9][0-9]*)?(.+)')


_MODE_PREFIXES = (
    'N_',
    'R_',
    'V_',
    'b_',
    'i_',
    'n_',
    's_',
    'v_'
)


_MODE_METHODS = {
    'N': 'internalNormal',
    'R': 'replace',
    'V': 'vline',
    'b': 'vblock',
    'i': 'insert',
    'n': 'normal',
    's': 'vselect',
    'v': 'visual'
}


class FunctionalTestCase(ViewTestCase):

    def feed(self, seq: str, check_user_mappings: bool = False) -> None:
        # Args:
        #   seq (str):
        #       A command sequence e.g. 3w, <C-a>, cs'", :pwd
        #
        # The seq can be prefixed to specify a mode:
        #
        # **The default mode is Internal Normal.**
        #
        # * n_ - Normal
        # * i_ - Insert
        # * v_ - Visual
        # * V_ - Visual line
        # * b_ - Visual block
        # * s_ - Select
        # * R_ - Replace
        # * :<','> - Visual Command-line
        # * N_ - Internal Normal
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
        # >>> feed('V_w')
        # >>> feed('b_w')
        # >>> feed('<Esc>')
        # >>> feed('i_<Esc>')
        # >>> feed('<C-v>')
        # >>> feed('n_<C-e>')
        # >>> feed('<CR>')
        # >>> feed(':pwd')
        # >>> feed(':copy 2')
        # >>> feed(':2,4yank')

        if seq[0] == ':':
            return do_ex_cmdline(self.view.window(), seq)

        orig_seq = seq
        seq, seq_args = _parse_seq(seq)

        try:
            # The reason for this try catch is because  some sequences map to
            # different commands by mode. For example n_u -> nv_vi_visual_u, and
            # all other modes u -> nv_vi_u (in other words all other modes).
            if orig_seq in _SEQ2CMD:
                seq = orig_seq

            command = _SEQ2CMD[seq]['command']

            if 'args' in _SEQ2CMD[seq]:
                args = copy.deepcopy(_SEQ2CMD[seq]['args'])
            else:
                args = {}

            if 'mode' not in args:
                args['mode'] = INTERNAL_NORMAL

            # If a count was given and the command has a motion, then the count
            # of the motion needs updating. This is a bit hacky.
            if 'count' in seq_args and seq_args['count'] > 1:
                try:
                    args['motion']['motion_args']['count'] = seq_args['count']
                    seq_args['count'] = 1
                except KeyError:
                    pass

            args.update(seq_args)
        except KeyError as e:
            raise KeyError('test command definition not found for feed %s' % str(e)) from None

        self.onRunFeedCommand(command, args)

        window = self.view.window()
        if not window:
            raise Exception('window not found')

        if command == 'nv_feed_key':
            if 'count' in args and args['count'] >= 1:
                window.run_command('nv_feed_key', {'key': str(args['count']), 'check_user_mappings': check_user_mappings})  # noqa: E501

            if 'key' in args:
                window.run_command('nv_feed_key', {'key': args['key'], 'check_user_mappings': check_user_mappings})
            elif 'keys' in args:
                for key in args['keys']:
                    window.run_command('nv_feed_key', {'key': key, 'check_user_mappings': check_user_mappings})
            else:
                for key in seq:
                    try:
                        key = _FEEDCHAR2KEY[key]
                    except Exception:
                        pass

                    window.run_command('nv_feed_key', {'key': key, 'check_user_mappings': check_user_mappings})
        else:
            window.run_command(command, args)

    def feedWithUserMappings(self, seq: str) -> None:
        self.feed(seq, check_user_mappings=True)

    def onRunFeedCommand(self, command: str, args) -> None:
        pass

    def eq(self, text: str, feed: str, expected=None, msg: str = None) -> None:
        # The text, feed, and expected arguments can use the following special
        # prefixes to indicate a specific mode. The text and expected modes
        # default to the feed mode, otherwise the default is Internal Normal.
        #
        # * n_ - Normal
        # * i_ - Insert
        # * v_ - Visual
        # * V_ - Visual line
        # * b_ - Visual block
        # * s_ - Select
        # * R_ - Replace
        # * :<','> - Visual Command-line
        # * N_ - Internal Normal
        #
        # The {text} and {expected} arguments also accept prefixes:
        #
        # * r_ - Reversed selection (must be first e.g. "r_d_*")
        # * d_ - Visual block direction down (only valid in visual block)
        # * u_ - Visual block direction up (only valid in visual block)
        #
        # Usage:
        #
        # >>> eq('|Hello world!', 'n_w', 'Hello |world!')
        # >>> eq('|H|ello world!', 'v_w', '|Hello w|orld!')
        # >>> eq('xxx\nbu|zz\nxxx', 'n_cc', 'i_xxx\n|\nxxx')

        if expected is None:
            expected = text

        if feed[:2] in _MODE_PREFIXES:
            default_mode = feed[0]
        elif feed[:6] == ':\'<,\'>':
            default_mode = 'v'
        else:
            default_mode = 'n'

        text, text_mode, reverse_text = _parse(text, default_mode)
        expected, expected_mode, reverse_expected = _parse(expected, default_mode)

        if text_mode in _MODE_METHODS:
            method_name = _MODE_METHODS[text_mode]
        else:
            self.assertTrue(False, 'invalid text mode')

        if reverse_text:
            method_name = 'r' + method_name

        args = []
        if text_mode == 'b':
            text, arg = self._filter_vblock_direction(text)
            args.append(arg)

        getattr(self, method_name)(text, *args)

        self.feed(feed)

        if expected_mode in _MODE_METHODS:
            method_name = _MODE_METHODS[expected_mode]
        else:
            self.assertTrue(False, 'invalid expected mode')

        if reverse_expected:
            method_name = 'r' + method_name[0].upper() + method_name[1:]

        args = []
        if expected_mode == 'b':
            expected, arg = self._filter_vblock_direction(expected)
            args.append(arg)

        method_name = 'assert' + method_name[0].upper() + method_name[1:]
        args.append(msg)
        getattr(self, method_name)(expected, *args)

    def _filter_vblock_direction(self, content):
        if content[:2] in ('d_', 'u_'):
            direction = DIRECTION_DOWN if content[:2] == 'd_' else DIRECTION_UP
            content = content[2:]
        else:
            direction = DIRECTION_DOWN

        return content, direction


def _parse(text, default_mode) -> tuple:
    text, is_reversed = _parse_reversed(text)
    text, mode = _parse_mode(text, default_mode)

    return text, mode, is_reversed


def _parse_reversed(text) -> tuple:
    if text[:2] == 'r_':
        return text[2:], True

    return text, False


def _parse_mode(text, default) -> tuple:
    if text[:2] in _MODE_PREFIXES:
        return text[2:], text[0]

    return text, default


def _parse_seq(seq: str) -> tuple:
    args = {}  # type: dict
    parsed_seq = _SEQ_PARSER.match(seq)
    if parsed_seq:
        if parsed_seq.group(1):
            args['mode'] = _CHAR2MODE[parsed_seq.group(1)]
        if parsed_seq.group(2):
            args['count'] = int(parsed_seq.group(2))
        seq = parsed_seq.group(3)

    return (seq, args)


# Test case mixin for commands like j and k that need to extract the xpos from
# the test fixture and then pass it to the command as an argument.
class PatchFeedCommandXpos(FunctionalTestCase):

    def onRunFeedCommand(self, command: str, args) -> None:
        sel = self.view.sel()[-1]
        xpos_pt = sel.b - 1 if sel.b > sel.a else sel.b
        xpos = self.view.rowcol(xpos_pt)[1]

        # Commands like k receive a motion xpos argument on operations like
        # "dk". This updates the command with whatever the test fixture xpos
        # should to be. It's a bit hacky, but just a temporary solution.
        if command == 'nv_feed_key':
            self.setXpos(xpos)
        else:
            if 'motion' in args and 'motion_args' in args['motion']:
                args['motion']['motion_args']['xpos'] = xpos
            else:
                args['xpos'] = xpos

        super().onRunFeedCommand(command, args)


class ResetCommandLineOutput(FunctionalTestCase):

    def tearDown(self) -> None:
        # XXX: Ugly hack to make sure that the output panels created in these
        # tests don't hide the overall progress panel.
        self.view.window().run_command('show_panel', {'panel': 'output.UnitTesting'})  # type: ignore[union-attr]
        self.view.window().focus_group(self.view.window().active_group())  # type: ignore[union-attr]
        super().tearDown()


class ResetRegisters(FunctionalTestCase):

    def setUp(self) -> None:
        super().setUp()
        self.resetRegisters()


class ResetMarks(FunctionalTestCase):

    def setUp(self) -> None:
        super().setUp()
        self.resetMarks()


# DEPRECATED Use newer APIs.
def _make_region(view, a: int, b: int = None) -> Region:
    try:
        pt_a = view.text_point(*a)
        pt_b = view.text_point(*b)

        return Region(pt_a, pt_b)
    except (TypeError, ValueError):
        pass

    if b is None:
        pass

    if b is not None:
        return Region(a, b)
    else:
        return Region(a)


def mock_bell():
    """Mock bells.

    Usage:

    @unittest.mock_bell()
    def test(self):
        self.assertBell()
        self.assertBell('message')
        self.assertBellCount(2)
        self.assertNoBell()

    """
    def wrapper(f):
        @mock.patch('NeoVintageous.nv.ui._ui_bell')
        def wrapped(self, *args, **kwargs):
            self.bell = args[-1]
            self.assert_bell_count = 0

            def _assertBell(*msg: str, count: int = 1) -> None:
                if msg:
                    self.bell.assert_called_with(*msg)
                else:
                    self.bell.assert_called_with()

                self.assert_bell_count += count
                self.assertEqual(
                    self.bell.call_count,
                    self.assert_bell_count,
                    'expects %s bell(s)' % self.assert_bell_count)

            def _assertBellCount(count: int) -> None:
                self.assertEquals(count, self.bell.call_count, 'expects %s bell' % count)

            def _assertNoBell() -> None:
                self.assertEquals(0, self.bell.call_count, 'expected no bell')

            self.assertBell = _assertBell
            self.assertBellCount = _assertBellCount
            self.assertNoBell = _assertNoBell

            return f(self, *args[:-2], **kwargs)
        return wrapped
    return wrapper


def mock_hide_panel():
    """Mock the hide panel API.

    Useful of you don't want the test to close the results panel during a test.

    Usage:

    @unittest.mock_hide_panel()
    def test(self):
        pass

    """
    def wrapper(f):
        @mock.patch('NeoVintageous.nv.commands.hide_panel')
        def wrapped(self, *args, **kwargs):
            self.hide_panel = args[-1]

            return f(self, *args[:-1], **kwargs)
        return wrapped
    return wrapper


def mock_session():
    """Mock the session.

    Usage:

    @unittest.mock_session()
    def test(self):
        self.assertSessionEmpty()
        self.assertSessionHasNoMacros()
        self.assertSession({'a': {'x': 'y'}, 'b': True})

    """
    def wrapper(f):
        @mock.patch.dict('NeoVintageous.nv.session._session', {}, clear=True)
        @mock.patch.dict('NeoVintageous.nv.history._storage', {}, clear=True)
        @mock.patch('NeoVintageous.nv.session.save_session')
        def wrapped(self, *args, **kwargs):
            save = args[-1]

            def _assertSessionEqual(*args) -> None:
                from NeoVintageous.nv import session
                from NeoVintageous.nv import history

                # TODO The history storage needs refactoring. This patches the
                # testable session as though it already contains the history
                # data when it's actually stored in the history module.
                patched_session = session._session
                if history._storage:
                    patched_session['history'] = history._storage

                if len(args) == 1:
                    self.assertEqual(
                        args[0],
                        patched_session,
                        'expects session')
                else:
                    self.assertEqual(
                        args[1],
                        patched_session[args[0]],
                        'expects session key value')

            def _assertSessionEmpty() -> None:
                _assertSessionEqual({'macros': {}})

            def _assertNotSaved() -> None:
                self.assertMockNotCalled(save)

            self.assertSessionNotSaved = _assertNotSaved
            self.assertSessionSaved = save.assert_called_once_with
            self.assertSession = _assertSessionEqual
            self.assertSessionEmpty = _assertSessionEmpty

            return f(self, *args[:-1], **kwargs)
        return wrapped
    return wrapper


def mock_status_message():
    """Mock status messages.

    Usage:

    @unittest.mock_status_message()
    def test(self):
        self.assertStatusMessage('message')
        self.assertStatusMessageCount(3)
        self.assertNoStatusMessage()

    """
    def wrapper(f):
        @mock.patch('NeoVintageous.nv.polyfill._status_message')
        def wrapped(self, *args, **kwargs):
            self.status_message = args[-1]
            self.assert_status_message_count = 0

            def _assertStatusMessage(msg: str, count: int = 1) -> None:
                self.status_message.assert_called_with(msg)

                self.assert_status_message_count += count
                self.assertEqual(
                    self.status_message.call_count,
                    self.assert_status_message_count,
                    'expects %s status message(s)' % self.assert_status_message_count)

            def _assertStatusMessageCount(expected) -> None:
                self.assertEqual(expected, self.status_message.call_count)

            def _assertNoStatusMessage() -> None:
                self.assertEqual(0, self.status_message.call_count)

            self.assertStatusMessage = _assertStatusMessage
            self.assertStatusMessageCount = _assertStatusMessageCount
            self.assertNoStatusMessage = _assertNoStatusMessage

            return f(self, *args[:-1], **kwargs)
        return wrapped
    return wrapper


def mock_mappings(*mappings):
    """Mock mappings.

    Usage:

    @unittest.mock_mappings((unittest.NORMAL, ',l', '3l'), (unittest.VISUAL, ',l', '3l'))
    def test(self):
        pass

    """
    def wrapper(f):

        from NeoVintageous.nv.mappings import _mappings
        from NeoVintageous.nv.mappings import mappings_add

        @unittest.mock.patch.dict('NeoVintageous.nv.mappings._mappings', {k: {} for k in _mappings}, clear=True)
        def wrapped(self, *args, **kwargs):
            for mapping in mappings:
                mappings_add(*mapping)
            return f(self, *args[:-1], **kwargs)
        return wrapped
    return wrapper


def mock_ui(screen_rows=None, visible_region=None, em_width=10.0, line_height=22.0):
    """Mock the UI.

    All arguments default to the view fixture values. For example, the number of
    screen rows, visible region, em width, and line height, all default to the
    fixture screen rows, visble rows, em width, and line height.

    Usage:

    @unittest.mock_ui()
    def test(self):
        pass

    @unittest.mock_ui(screen_rows=10)
    def test(self):
        pass

    @unittest.mock_ui(visible_region=(2, 7))
    def test(self):
        pass

    """
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
                # Fixes UI mocking issue in Sublime Text 4. It seems that
                # layout_extent() needs to be invoked whenever this mock is used
                # because it updates the layout extent to the correct value.
                self.view.layout_extent()

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
            def _visible_region() -> Region:
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


def mock_commands(*methods):
    """Mock commands.

    Useful to mock builtin Sublime Text commands.

    Usage:

    @unittest.mock_commands('redo', 'hide_panel')
    def test(self):

        # Assert command ran successfully.
        self.assertRunCommand('redo')

        # Assert command ran {count} times.
        self.assertRunCommand('redo', count=3)

        # Assert command and arguments.
        self.assertRunCommand('hide_panel', {'cancel': True})

        # Assert command and arguments ran {count} times..
        self.assertRunCommand('hide_panel', {'cancel': True}, count=3)

    """
    def wrapper(f):
        import sublime_api

        def _view_run_command(self, cmd: str, args: dict = None) -> None:
            """
            Monkey patch for view.run_command().

            This patch records information about calls to view.run_command() for
            any mocked commands and runs all other commands normally.
            """
            if cmd not in methods:
                sublime_api.view_run_command(self.id(), cmd, args)  # type: ignore[arg-type]
            else:
                f._mock_run_command_calls.append((cmd, args))

        def _window_run_command(self, cmd: str, args: dict = None) -> None:
            """
            Monkey patch for window.run_command().

            This patch records information about calls to window.run_command()
            for any mocked commands and runs all other commands normally.
            """
            if cmd not in methods:
                sublime_api.window_run_command(self.id(), cmd, args)  # type: ignore[arg-type]
            else:
                f._mock_run_command_calls.append((cmd, args))

        @mock.patch('sublime.View.run_command', new=_view_run_command)
        @mock.patch('sublime.Window.run_command', new=_window_run_command)
        def wrapped(self, *args, **kwargs):
            f._mock_run_command_calls = []

            def assertRunCommand(cmd: str, args: dict = None, count: int = 1) -> None:
                actual_count = 0
                for actual_cmd, actual_args in f._mock_run_command_calls:
                    if (cmd == actual_cmd) and (args == actual_args):
                        actual_count += 1

                self.assertEqual(
                    actual_count,
                    count,
                    'failed assert ran command {} with args {} {} time(s), actual calls: {}'.format(
                        cmd, args, count, f._mock_run_command_calls))

            self.assertRunCommand = assertRunCommand

            return f(self, *args, **kwargs)
        return wrapped
    return wrapper


# A hardcoded map of sequences to commands. Ideally we wouldn't need this
# hardcoded map, some internal refactoring and redesign is required to make that
# happen. For now make-do with the hardcoded map. Refactoring later should not
# impact the existing tests.
_SEQ2CMD = {

    '"#yiw':        {'command': 'nv_feed_key'},  # noqa: E241
    '"%yiw':        {'command': 'nv_feed_key'},  # noqa: E241
    '"':            {'command': 'nv_feed_key'},  # noqa: E241
    '"*y':          {'command': 'nv_feed_key'},  # noqa: E241
    '"+y':          {'command': 'nv_feed_key'},  # noqa: E241
    '".yiw':        {'command': 'nv_feed_key'},  # noqa: E241
    '"1P':          {'command': 'nv_feed_key'},  # noqa: E241
    '"1Y':          {'command': 'nv_feed_key'},  # noqa: E241
    '"1p':          {'command': 'nv_feed_key'},  # noqa: E241
    '"1y':          {'command': 'nv_feed_key'},  # noqa: E241
    '"1yy':         {'command': 'nv_feed_key'},  # noqa: E241
    '"2P':          {'command': 'nv_feed_key'},  # noqa: E241
    '"2Y':          {'command': 'nv_feed_key'},  # noqa: E241
    '"2p':          {'command': 'nv_feed_key'},  # noqa: E241
    '"2y':          {'command': 'nv_feed_key'},  # noqa: E241
    '"2yy':         {'command': 'nv_feed_key'},  # noqa: E241
    '":yiw':        {'command': 'nv_feed_key'},  # noqa: E241
    '"Byy':         {'command': 'nv_feed_key'},  # noqa: E241
    '"_y':          {'command': 'nv_feed_key'},  # noqa: E241
    '"_yiw':        {'command': 'nv_feed_key'},  # noqa: E241
    '"a':           {'command': 'nv_feed_key'},  # noqa: E241
    '"aY':          {'command': 'nv_feed_key'},  # noqa: E241
    '"ay':          {'command': 'nv_feed_key'},  # noqa: E241
    '"ayy':         {'command': 'nv_feed_key'},  # noqa: E241
    '"bY':          {'command': 'nv_feed_key'},  # noqa: E241
    '"by':          {'command': 'nv_feed_key'},  # noqa: E241
    '"byy':         {'command': 'nv_feed_key'},  # noqa: E241
    '"x':           {'command': 'nv_feed_key'},  # noqa: E241
    '"xP':          {'command': 'nv_feed_key'},  # noqa: E241
    '"xY':          {'command': 'nv_feed_key'},  # noqa: E241
    '"xp':          {'command': 'nv_feed_key'},  # noqa: E241
    '"xy':          {'command': 'nv_feed_key'},  # noqa: E241
    '"xyiw':        {'command': 'nv_feed_key'},  # noqa: E241
    '"xyy':         {'command': 'nv_feed_key'},  # noqa: E241
    '#':            {'command': 'nv_feed_key'},  # noqa: E241
    '$':            {'command': 'nv_feed_key'},  # noqa: E241
    '%':            {'command': 'nv_feed_key'},  # noqa: E241
    '(':            {'command': 'nv_feed_key'},  # noqa: E241
    ')':            {'command': 'nv_feed_key'},  # noqa: E241
    '*':            {'command': 'nv_feed_key'},  # noqa: E241
    ',':            {'command': 'nv_feed_key'},  # noqa: E241
    '-':            {'command': 'nv_feed_key'},  # noqa: E241
    '.':            {'command': 'nv_feed_key'},  # noqa: E241
    '/':            {'command': 'nv_feed_key'},  # noqa: E241
    '/aBc':         {'command': 'nv_vi_slash_impl', 'args': {'pattern': 'aBc'}},  # noqa: E241
    '/abc':         {'command': 'nv_vi_slash_impl', 'args': {'pattern': 'abc'}},  # noqa: E241
    '/abc\\C':      {'command': 'nv_vi_slash_impl', 'args': {'pattern': 'abc\\C'}},  # noqa: E241
    '/abc\\c':      {'command': 'nv_vi_slash_impl', 'args': {'pattern': 'abc\\c'}},  # noqa: E241
    '/x':           {'command': 'nv_vi_slash_impl', 'args': {'pattern': 'x'}},  # noqa: E241
    '0':            {'command': 'nv_feed_key'},  # noqa: E241
    ';':            {'command': 'nv_feed_key'},  # noqa: E241
    '<':            {'command': 'nv_feed_key'},  # noqa: E241
    '<<':           {'command': 'nv_feed_key'},  # noqa: E241
    '<C-0>':        {'command': 'nv_feed_key', 'args': {'key': '<C-0>'}},  # noqa: E241
    '<C-1>':        {'command': 'nv_feed_key', 'args': {'key': '<C-1>'}},  # noqa: E241
    '<C-2>':        {'command': 'nv_feed_key', 'args': {'key': '<C-2>'}},  # noqa: E241
    '<C-3>':        {'command': 'nv_feed_key', 'args': {'key': '<C-3>'}},  # noqa: E241
    '<C-4>':        {'command': 'nv_feed_key', 'args': {'key': '<C-4>'}},  # noqa: E241
    '<C-5>':        {'command': 'nv_feed_key', 'args': {'key': '<C-5>'}},  # noqa: E241
    '<C-6>':        {'command': 'nv_feed_key', 'args': {'key': '<C-6>'}},  # noqa: E241
    '<C-7>':        {'command': 'nv_feed_key', 'args': {'key': '<C-7>'}},  # noqa: E241
    '<C-8>':        {'command': 'nv_feed_key', 'args': {'key': '<C-8>'}},  # noqa: E241
    '<C-9>':        {'command': 'nv_feed_key', 'args': {'key': '<C-9>'}},  # noqa: E241
    '<C-B>':        {'command': 'nv_feed_key', 'args': {'key': '<C-B>'}},  # noqa: E241
    '<C-F12>':      {'command': 'nv_feed_key', 'args': {'key': '<C-F12>'}},  # noqa: E241
    '<C-F2>':       {'command': 'nv_feed_key', 'args': {'key': '<C-F2>'}},  # noqa: E241
    '<C-F>':        {'command': 'nv_feed_key', 'args': {'key': '<C-F>'}},  # noqa: E241
    '<C-M-p>':      {'command': 'nv_feed_key', 'args': {'key': '<C-M-p>'}},  # noqa: E241
    '<C-P>':        {'command': 'nv_feed_key', 'args': {'key': '<C-P>'}},  # noqa: E241
    '<C-S-f12>':    {'command': 'nv_feed_key', 'args': {'key': '<C-S-f12>'}},  # noqa: E241
    '<C-S-f2>':     {'command': 'nv_feed_key', 'args': {'key': '<C-S-f2>'}},  # noqa: E241
    '<C-[>':        {'command': 'nv_feed_key', 'args': {'key': '<C-[>'}},  # noqa: E241
    '<C-]>':        {'command': 'nv_feed_key', 'args': {'key': '<C-]>'}},  # noqa: E241
    '<C-^>':        {'command': 'nv_feed_key', 'args': {'key': '<C-^>'}},  # noqa: E241
    '<C-a>':        {'command': 'nv_feed_key', 'args': {'key': '<C-a>'}},  # noqa: E241
    '<C-b>':        {'command': 'nv_feed_key', 'args': {'key': '<C-b>'}},  # noqa: E241
    '<C-c>':        {'command': 'nv_feed_key', 'args': {'key': '<C-c>'}},  # noqa: E241
    '<C-d>':        {'command': 'nv_feed_key', 'args': {'key': '<C-d>'}},  # noqa: E241
    '<C-e>':        {'command': 'nv_feed_key', 'args': {'key': '<C-e>'}},  # noqa: E241
    '<C-g>':        {'command': 'nv_feed_key', 'args': {'key': '<C-g>'}},  # noqa: E241
    '<C-i>':        {'command': 'nv_feed_key', 'args': {'key': '<C-i>'}},  # noqa: E241
    '<C-k>':        {'command': 'nv_feed_key', 'args': {'key': '<C-k>'}},  # noqa: E241
    '<C-n>':        {'command': 'nv_feed_key', 'args': {'key': '<C-n>'}},  # noqa: E241
    '<C-o>':        {'command': 'nv_feed_key', 'args': {'key': '<C-o>'}},  # noqa: E241
    '<C-p>':        {'command': 'nv_feed_key', 'args': {'key': '<C-p>'}},  # noqa: E241
    '<C-r>':        {'command': 'nv_feed_key', 'args': {'key': '<C-r>'}},  # noqa: E241
    '<C-u>':        {'command': 'nv_feed_key', 'args': {'key': '<C-u>'}},  # noqa: E241
    '<C-v>':        {'command': 'nv_feed_key', 'args': {'key': '<C-v>'}},  # noqa: E241
    '<C-w>':        {'command': 'nv_feed_key', 'args': {'key': '<C-w>'}},  # noqa: E241
    '<C-w>+':       {'command': 'nv_feed_key', 'args': {'keys': ['<C-w>', '+']}},  # noqa: E241
    '<C-w>-':       {'command': 'nv_feed_key', 'args': {'keys': ['<C-w>', '-']}},  # noqa: E241
    '<C-w><C-6>':   {'command': 'nv_feed_key', 'args': {'keys': ['<C-w>', '<C-6>']}},  # noqa: E241
    '<C-w><C-n>':   {'command': 'nv_feed_key', 'args': {'keys': ['<C-w>', '<C-n>']}},  # noqa: E241
    '<C-w><C-s>':   {'command': 'nv_feed_key', 'args': {'keys': ['<C-w>', '<C-s>']}},  # noqa: E241
    '<C-w><C-v>':   {'command': 'nv_feed_key', 'args': {'keys': ['<C-w>', '<C-v>']}},  # noqa: E241
    '<C-w><C-w>':   {'command': 'nv_feed_key', 'args': {'keys': ['<C-w>', '<C-w>']}},  # noqa: E241
    '<C-w><bar>':   {'command': 'nv_feed_key', 'args': {'keys': ['<C-w>', '<bar>']}},  # noqa: E241
    '<C-w><lt>':    {'command': 'nv_feed_key', 'args': {'keys': ['<C-w>', '<lt>']}},  # noqa: E241
    '<C-w>=':       {'command': 'nv_feed_key', 'args': {'keys': ['<C-w>', '=']}},  # noqa: E241
    '<C-w>>':       {'command': 'nv_feed_key', 'args': {'keys': ['<C-w>', '>']}},  # noqa: E241
    '<C-w>H':       {'command': 'nv_feed_key', 'args': {'keys': ['<C-w>', 'H']}},  # noqa: E241
    '<C-w>J':       {'command': 'nv_feed_key', 'args': {'keys': ['<C-w>', 'J']}},  # noqa: E241
    '<C-w>K':       {'command': 'nv_feed_key', 'args': {'keys': ['<C-w>', 'K']}},  # noqa: E241
    '<C-w>L':       {'command': 'nv_feed_key', 'args': {'keys': ['<C-w>', 'L']}},  # noqa: E241
    '<C-w>S':       {'command': 'nv_feed_key', 'args': {'keys': ['<C-w>', 'S']}},  # noqa: E241
    '<C-w>W':       {'command': 'nv_feed_key', 'args': {'keys': ['<C-w>', 'W']}},  # noqa: E241
    '<C-w>]':       {'command': 'nv_feed_key', 'args': {'keys': ['<C-w>', ']']}},  # noqa: E241
    '<C-w>^':       {'command': 'nv_feed_key', 'args': {'keys': ['<C-w>', '^']}},  # noqa: E241
    '<C-w>_':       {'command': 'nv_feed_key', 'args': {'keys': ['<C-w>', '_']}},  # noqa: E241
    '<C-w>b':       {'command': 'nv_feed_key', 'args': {'keys': ['<C-w>', 'b']}},  # noqa: E241
    '<C-w>c':       {'command': 'nv_feed_key', 'args': {'keys': ['<C-w>', 'c']}},  # noqa: E241
    '<C-w>h':       {'command': 'nv_feed_key', 'args': {'keys': ['<C-w>', 'h']}},  # noqa: E241
    '<C-w>j':       {'command': 'nv_feed_key', 'args': {'keys': ['<C-w>', 'j']}},  # noqa: E241
    '<C-w>k':       {'command': 'nv_feed_key', 'args': {'keys': ['<C-w>', 'k']}},  # noqa: E241
    '<C-w>l':       {'command': 'nv_feed_key', 'args': {'keys': ['<C-w>', 'l']}},  # noqa: E241
    '<C-w>n':       {'command': 'nv_feed_key', 'args': {'keys': ['<C-w>', 'n']}},  # noqa: E241
    '<C-w>o':       {'command': 'nv_feed_key', 'args': {'keys': ['<C-w>', 'o']}},  # noqa: E241
    '<C-w>q':       {'command': 'nv_feed_key', 'args': {'keys': ['<C-w>', 'q']}},  # noqa: E241
    '<C-w>s':       {'command': 'nv_feed_key', 'args': {'keys': ['<C-w>', 's']}},  # noqa: E241
    '<C-w>t':       {'command': 'nv_feed_key', 'args': {'keys': ['<C-w>', 't']}},  # noqa: E241
    '<C-w>v':       {'command': 'nv_feed_key', 'args': {'keys': ['<C-w>', 'v']}},  # noqa: E241
    '<C-w>w':       {'command': 'nv_feed_key', 'args': {'keys': ['<C-w>', 'w']}},  # noqa: E241
    '<C-w>x':       {'command': 'nv_feed_key', 'args': {'keys': ['<C-w>', 'x']}},  # noqa: E241
    '<C-x>':        {'command': 'nv_feed_key', 'args': {'key': '<C-x>'}},  # noqa: E241
    '<C-y>':        {'command': 'nv_feed_key', 'args': {'key': '<C-y>'}},  # noqa: E241
    '<CR>':         {'command': 'nv_feed_key', 'args': {'key': '<cr>'}},  # noqa: E241
    '<Esc>':        {'command': 'nv_feed_key', 'args': {'key': '<esc>'}},  # noqa: E241
    '<F11>':        {'command': 'nv_feed_key', 'args': {'key': '<F11>'}},  # noqa: E241
    '<F12>':        {'command': 'nv_feed_key', 'args': {'key': '<F12>'}},  # noqa: E241
    '<F2>':         {'command': 'nv_feed_key', 'args': {'key': '<F2>'}},  # noqa: E241
    '<F3>':         {'command': 'nv_feed_key', 'args': {'key': '<F3>'}},  # noqa: E241
    '<F4>':         {'command': 'nv_feed_key', 'args': {'key': '<F4>'}},  # noqa: E241
    '<F5>':         {'command': 'nv_feed_key', 'args': {'key': '<F5>'}},  # noqa: E241
    '<F6>':         {'command': 'nv_feed_key', 'args': {'key': '<F6>'}},  # noqa: E241
    '<F7>':         {'command': 'nv_feed_key', 'args': {'key': '<F7>'}},  # noqa: E241
    '<F8>':         {'command': 'nv_feed_key', 'args': {'key': '<F8>'}},  # noqa: E241
    '<F9>':         {'command': 'nv_feed_key', 'args': {'key': '<F9>'}},  # noqa: E241
    '<M-n>':        {'command': 'nv_feed_key', 'args': {'key': '<M-n>'}},  # noqa: E241
    '<S-f11>':      {'command': 'nv_feed_key', 'args': {'key': '<S-f11>'}},  # noqa: E241
    '<S-f2>':       {'command': 'nv_feed_key', 'args': {'key': '<S-f2>'}},  # noqa: E241
    '<S-f4>':       {'command': 'nv_feed_key', 'args': {'key': '<S-f4>'}},  # noqa: E241
    '<k0>':         {'command': 'nv_feed_key', 'args': {'key': '<k0>'}},  # noqa: E241
    '<k1>':         {'command': 'nv_feed_key', 'args': {'key': '<k1>'}},  # noqa: E241
    '<k2>':         {'command': 'nv_feed_key', 'args': {'key': '<k2>'}},  # noqa: E241
    '<k3>':         {'command': 'nv_feed_key', 'args': {'key': '<k3>'}},  # noqa: E241
    '<k4>':         {'command': 'nv_feed_key', 'args': {'key': '<k4>'}},  # noqa: E241
    '<k5>':         {'command': 'nv_feed_key', 'args': {'key': '<k5>'}},  # noqa: E241
    '<k6>':         {'command': 'nv_feed_key', 'args': {'key': '<k6>'}},  # noqa: E241
    '<k7>':         {'command': 'nv_feed_key', 'args': {'key': '<k7>'}},  # noqa: E241
    '<k8>':         {'command': 'nv_feed_key', 'args': {'key': '<k8>'}},  # noqa: E241
    '<k9>':         {'command': 'nv_feed_key', 'args': {'key': '<k9>'}},  # noqa: E241
    '<{':           {'command': 'nv_feed_key'},  # noqa: E241
    '=':            {'command': 'nv_feed_key'},  # noqa: E241
    '==':           {'command': 'nv_feed_key'},  # noqa: E241
    '=}':           {'command': 'nv_feed_key'},  # noqa: E241
    '>':            {'command': 'nv_feed_key'},  # noqa: E241
    '>>':           {'command': 'nv_feed_key'},  # noqa: E241
    '>G':           {'command': 'nv_feed_key'},  # noqa: E241
    '>ip':          {'command': 'nv_feed_key'},  # noqa: E241
    '?':            {'command': 'nv_feed_key'},  # noqa: E241
    '?aBc':         {'command': 'nv_vi_question_mark_impl', 'args': {'pattern': 'aBc'}},  # noqa: E241
    '?abc':         {'command': 'nv_vi_question_mark_impl', 'args': {'pattern': 'abc'}},  # noqa: E241
    '@!':           {'command': 'nv_feed_key'},  # noqa: E241
    '@#':           {'command': 'nv_feed_key'},  # noqa: E241
    '@%':           {'command': 'nv_feed_key'},  # noqa: E241
    '@-':           {'command': 'nv_feed_key'},  # noqa: E241
    '@@':           {'command': 'nv_feed_key'},  # noqa: E241
    '@A':           {'command': 'nv_feed_key'},  # noqa: E241
    '@a':           {'command': 'nv_feed_key'},  # noqa: E241
    'A':            {'command': 'nv_feed_key'},  # noqa: E241
    'B':            {'command': 'nv_feed_key'},  # noqa: E241
    'C':            {'command': 'nv_feed_key'},  # noqa: E241
    'D':            {'command': 'nv_feed_key'},  # noqa: E241
    'E':            {'command': 'nv_feed_key'},  # noqa: E241
    'F':            {'command': 'nv_feed_key'},  # noqa: E241
    'F0':           {'command': 'nv_feed_key'},  # noqa: E241
    'F4':           {'command': 'nv_feed_key'},  # noqa: E241
    'F5':           {'command': 'nv_feed_key'},  # noqa: E241
    'Ff':           {'command': 'nv_feed_key'},  # noqa: E241
    'Fr':           {'command': 'nv_feed_key'},  # noqa: E241
    'Fx':           {'command': 'nv_feed_key'},  # noqa: E241
    'G':            {'command': 'nv_feed_key'},  # noqa: E241
    'H':            {'command': 'nv_feed_key'},  # noqa: E241
    'I':            {'command': 'nv_feed_key'},  # noqa: E241
    'J':            {'command': 'nv_feed_key'},  # noqa: E241
    'L':            {'command': 'nv_feed_key'},  # noqa: E241
    'M':            {'command': 'nv_feed_key'},  # noqa: E241
    'N':            {'command': 'nv_feed_key'},  # noqa: E241
    'O':            {'command': 'nv_feed_key'},  # noqa: E241
    'P':            {'command': 'nv_feed_key'},  # noqa: E241
    'Q':            {'command': 'nv_feed_key'},  # noqa: E241
    'R':            {'command': 'nv_feed_key'},  # noqa: E241
    'S"':           {'command': 'nv_feed_key'},  # noqa: E241
    'S$t':          {'command': 'nv_feed_key'},  # noqa: E241
    'S':            {'command': 'nv_feed_key'},  # noqa: E241
    'S<CR>':        {'command': 'nv_feed_key', 'args': {'keys': ['S', '<CR>']}},  # noqa: E241
    'Sab':          {'command': 'nv_feed_key'},  # noqa: E241
    'Siz':          {'command': 'nv_feed_key'},  # noqa: E241
    'Sx<CR>':       {'command': 'nv_feed_key', 'args': {'keys': ['S', 'x', '<CR>']}},  # noqa: E241
    'T0':           {'command': 'nv_feed_key'},  # noqa: E241
    'T4':           {'command': 'nv_feed_key'},  # noqa: E241
    'T5':           {'command': 'nv_feed_key'},  # noqa: E241
    'Tf':           {'command': 'nv_feed_key'},  # noqa: E241
    'Tr':           {'command': 'nv_feed_key'},  # noqa: E241
    'Tx':           {'command': 'nv_feed_key'},  # noqa: E241
    'U':            {'command': 'nv_feed_key'},  # noqa: E241
    'V':            {'command': 'nv_feed_key'},  # noqa: E241
    'W':            {'command': 'nv_feed_key'},  # noqa: E241
    'X':            {'command': 'nv_feed_key'},  # noqa: E241
    'Y':            {'command': 'nv_feed_key'},  # noqa: E241
    'Z<CR>':        {'command': 'nv_feed_key', 'args': {'keys': ['Z', '<CR>']}},  # noqa: E241
    'Ziz':          {'command': 'nv_feed_key'},  # noqa: E241
    'Zx<CR>':       {'command': 'nv_feed_key', 'args': {'keys': ['Z', 'x', '<CR>']}},  # noqa: E241
    '[ ':           {'command': 'nv_feed_key'},  # noqa: E241
    '[(':           {'command': 'nv_feed_key'},  # noqa: E241
    '[B':           {'command': 'nv_feed_key'},  # noqa: E241
    '[P':           {'command': 'nv_feed_key'},  # noqa: E241
    '[T':           {'command': 'nv_feed_key'},  # noqa: E241
    '[b':           {'command': 'nv_feed_key'},  # noqa: E241
    '[c':           {'command': 'nv_feed_key'},  # noqa: E241
    '[e':           {'command': 'nv_feed_key'},  # noqa: E241
    '[l':           {'command': 'nv_feed_key'},  # noqa: E241
    '[n':           {'command': 'nv_feed_key'},  # noqa: E241
    '[oa':          {'command': 'nv_feed_key'},  # noqa: E241
    '[oc':          {'command': 'nv_feed_key'},  # noqa: E241
    '[oe':          {'command': 'nv_feed_key'},  # noqa: E241
    '[oh':          {'command': 'nv_feed_key'},  # noqa: E241
    '[oi':          {'command': 'nv_feed_key'},  # noqa: E241
    '[ol':          {'command': 'nv_feed_key'},  # noqa: E241
    '[om':          {'command': 'nv_feed_key'},  # noqa: E241
    '[on':          {'command': 'nv_feed_key'},  # noqa: E241
    '[ot':          {'command': 'nv_feed_key'},  # noqa: E241
    '[ow':          {'command': 'nv_feed_key'},  # noqa: E241
    '[s':           {'command': 'nv_feed_key'},  # noqa: E241
    '[t':           {'command': 'nv_feed_key'},  # noqa: E241
    '[{':           {'command': 'nv_feed_key'},  # noqa: E241
    '\'':           {'command': 'nv_feed_key'},  # noqa: E241
    '\'a':          {'command': 'nv_feed_key'},  # noqa: E241
    '\'p':          {'command': 'nv_feed_key'},  # noqa: E241
    '\'x':          {'command': 'nv_feed_key'},  # noqa: E241
    '\\\\A':        {'command': 'nv_feed_key'},  # noqa: E241
    '] ':           {'command': 'nv_feed_key'},  # noqa: E241
    '])':           {'command': 'nv_feed_key'},  # noqa: E241
    ']B':           {'command': 'nv_feed_key'},  # noqa: E241
    ']P':           {'command': 'nv_feed_key'},  # noqa: E241
    ']T':           {'command': 'nv_feed_key'},  # noqa: E241
    ']b':           {'command': 'nv_feed_key'},  # noqa: E241
    ']c':           {'command': 'nv_feed_key'},  # noqa: E241
    ']e':           {'command': 'nv_feed_key'},  # noqa: E241
    ']l':           {'command': 'nv_feed_key'},  # noqa: E241
    ']n':           {'command': 'nv_feed_key'},  # noqa: E241
    ']oa':          {'command': 'nv_feed_key'},  # noqa: E241
    ']oc':          {'command': 'nv_feed_key'},  # noqa: E241
    ']oe':          {'command': 'nv_feed_key'},  # noqa: E241
    ']oh':          {'command': 'nv_feed_key'},  # noqa: E241
    ']oi':          {'command': 'nv_feed_key'},  # noqa: E241
    ']ol':          {'command': 'nv_feed_key'},  # noqa: E241
    ']om':          {'command': 'nv_feed_key'},  # noqa: E241
    ']on':          {'command': 'nv_feed_key'},  # noqa: E241
    ']ot':          {'command': 'nv_feed_key'},  # noqa: E241
    ']ow':          {'command': 'nv_feed_key'},  # noqa: E241
    ']s':           {'command': 'nv_feed_key'},  # noqa: E241
    ']t':           {'command': 'nv_feed_key'},  # noqa: E241
    ']}':           {'command': 'nv_feed_key'},  # noqa: E241
    '^':            {'command': 'nv_feed_key'},  # noqa: E241
    '_':            {'command': 'nv_feed_key'},  # noqa: E241
    '`':            {'command': 'nv_feed_key'},  # noqa: E241
    '`a':           {'command': 'nv_feed_key'},  # noqa: E241
    '`p':           {'command': 'nv_feed_key'},  # noqa: E241
    '`x':           {'command': 'nv_feed_key'},  # noqa: E241
    'a"':           {'command': 'nv_feed_key'},  # noqa: E241
    'a#':           {'command': 'nv_feed_key'},  # noqa: E241
    'a$':           {'command': 'nv_feed_key'},  # noqa: E241
    'a&':           {'command': 'nv_feed_key'},  # noqa: E241
    'a':            {'command': 'nv_feed_key'},  # noqa: E241
    'a(':           {'command': 'nv_feed_key'},  # noqa: E241
    'a)':           {'command': 'nv_feed_key'},  # noqa: E241
    'a*':           {'command': 'nv_feed_key'},  # noqa: E241
    'a+':           {'command': 'nv_feed_key'},  # noqa: E241
    'a,':           {'command': 'nv_feed_key'},  # noqa: E241
    'a-':           {'command': 'nv_feed_key'},  # noqa: E241
    'a.':           {'command': 'nv_feed_key'},  # noqa: E241
    'a/':           {'command': 'nv_feed_key'},  # noqa: E241
    'a:':           {'command': 'nv_feed_key'},  # noqa: E241
    'a;':           {'command': 'nv_feed_key'},  # noqa: E241
    'a<':           {'command': 'nv_feed_key'},  # noqa: E241
    'a=':           {'command': 'nv_feed_key'},  # noqa: E241
    'a>':           {'command': 'nv_feed_key'},  # noqa: E241
    'aB':           {'command': 'nv_feed_key'},  # noqa: E241
    'aI':           {'command': 'nv_feed_key'},  # noqa: E241
    'aW':           {'command': 'nv_feed_key'},  # noqa: E241
    'a[':           {'command': 'nv_feed_key'},  # noqa: E241
    'a\'':          {'command': 'nv_feed_key'},  # noqa: E241
    'a\\':          {'command': 'nv_feed_key'},  # noqa: E241
    'a]':           {'command': 'nv_feed_key'},  # noqa: E241
    'a_':           {'command': 'nv_feed_key'},  # noqa: E241
    'a`':           {'command': 'nv_feed_key'},  # noqa: E241
    'ab':           {'command': 'nv_feed_key'},  # noqa: E241
    'ai':           {'command': 'nv_feed_key'},  # noqa: E241
    'ap':           {'command': 'nv_feed_key'},  # noqa: E241
    'as':           {'command': 'nv_feed_key'},  # noqa: E241
    'at':           {'command': 'nv_feed_key'},  # noqa: E241
    'aw':           {'command': 'nv_feed_key'},  # noqa: E241
    'a{':           {'command': 'nv_feed_key'},  # noqa: E241
    'a|':           {'command': 'nv_feed_key'},  # noqa: E241
    'a}':           {'command': 'nv_feed_key'},  # noqa: E241
    'a~':           {'command': 'nv_feed_key'},  # noqa: E241
    'b':            {'command': 'nv_feed_key'},  # noqa: E241
    'c$':           {'command': 'nv_feed_key'},  # noqa: E241
    'c':            {'command': 'nv_feed_key'},  # noqa: E241
    'c0':           {'command': 'nv_feed_key'},  # noqa: E241
    'cM':           {'command': 'nv_feed_key'},  # noqa: E241
    'cZiz':         {'command': 'nv_feed_key'},  # noqa: E241
    'c^':           {'command': 'nv_feed_key'},  # noqa: E241
    'c_':           {'command': 'nv_feed_key'},  # noqa: E241
    'ca"':          {'command': 'nv_feed_key'},  # noqa: E241
    'ca#':          {'command': 'nv_feed_key'},  # noqa: E241
    'ca$':          {'command': 'nv_feed_key'},  # noqa: E241
    'ca&':          {'command': 'nv_feed_key'},  # noqa: E241
    'ca(':          {'command': 'nv_feed_key'},  # noqa: E241
    'ca)':          {'command': 'nv_feed_key'},  # noqa: E241
    'ca*':          {'command': 'nv_feed_key'},  # noqa: E241
    'ca+':          {'command': 'nv_feed_key'},  # noqa: E241
    'ca,':          {'command': 'nv_feed_key'},  # noqa: E241
    'ca-':          {'command': 'nv_feed_key'},  # noqa: E241
    'ca.':          {'command': 'nv_feed_key'},  # noqa: E241
    'ca/':          {'command': 'nv_feed_key'},  # noqa: E241
    'ca:':          {'command': 'nv_feed_key'},  # noqa: E241
    'ca;':          {'command': 'nv_feed_key'},  # noqa: E241
    'ca<':          {'command': 'nv_feed_key'},  # noqa: E241
    'ca=':          {'command': 'nv_feed_key'},  # noqa: E241
    'ca>':          {'command': 'nv_feed_key'},  # noqa: E241
    'caB':          {'command': 'nv_feed_key'},  # noqa: E241
    'caW':          {'command': 'nv_feed_key'},  # noqa: E241
    'ca[':          {'command': 'nv_feed_key'},  # noqa: E241
    'ca\'':         {'command': 'nv_feed_key'},  # noqa: E241
    'ca\\':         {'command': 'nv_feed_key'},  # noqa: E241
    'ca]':          {'command': 'nv_feed_key'},  # noqa: E241
    'ca_':          {'command': 'nv_feed_key'},  # noqa: E241
    'ca`':          {'command': 'nv_feed_key'},  # noqa: E241
    'cab':          {'command': 'nv_feed_key'},  # noqa: E241
    'cap':          {'command': 'nv_feed_key'},  # noqa: E241
    'cas':          {'command': 'nv_feed_key'},  # noqa: E241
    'cat':          {'command': 'nv_feed_key'},  # noqa: E241
    'caw':          {'command': 'nv_feed_key'},  # noqa: E241
    'ca{':          {'command': 'nv_feed_key'},  # noqa: E241
    'ca|':          {'command': 'nv_feed_key'},  # noqa: E241
    'ca}':          {'command': 'nv_feed_key'},  # noqa: E241
    'ca~':          {'command': 'nv_feed_key'},  # noqa: E241
    'cb':           {'command': 'nv_feed_key'},  # noqa: E241
    'cc':           {'command': 'nv_feed_key'},  # noqa: E241
    'ce':           {'command': 'nv_feed_key'},  # noqa: E241
    'cgE':          {'command': 'nv_feed_key'},  # noqa: E241
    'cgN':          {'command': 'nv_feed_key'},  # noqa: E241
    'cg_':          {'command': 'nv_feed_key'},  # noqa: E241
    'cge':          {'command': 'nv_feed_key'},  # noqa: E241
    'cgn':          {'command': 'nv_feed_key'},  # noqa: E241
    'ch':           {'command': 'nv_feed_key'},  # noqa: E241
    'ci"':          {'command': 'nv_feed_key'},  # noqa: E241
    'ci#':          {'command': 'nv_feed_key'},  # noqa: E241
    'ci$':          {'command': 'nv_feed_key'},  # noqa: E241
    'ci&':          {'command': 'nv_feed_key'},  # noqa: E241
    'ci(':          {'command': 'nv_feed_key'},  # noqa: E241
    'ci)':          {'command': 'nv_feed_key'},  # noqa: E241
    'ci*':          {'command': 'nv_feed_key'},  # noqa: E241
    'ci+':          {'command': 'nv_feed_key'},  # noqa: E241
    'ci,':          {'command': 'nv_feed_key'},  # noqa: E241
    'ci-':          {'command': 'nv_feed_key'},  # noqa: E241
    'ci.':          {'command': 'nv_feed_key'},  # noqa: E241
    'ci/':          {'command': 'nv_feed_key'},  # noqa: E241
    'ci:':          {'command': 'nv_feed_key'},  # noqa: E241
    'ci;':          {'command': 'nv_feed_key'},  # noqa: E241
    'ci<':          {'command': 'nv_feed_key'},  # noqa: E241
    'ci=':          {'command': 'nv_feed_key'},  # noqa: E241
    'ci>':          {'command': 'nv_feed_key'},  # noqa: E241
    'ciB':          {'command': 'nv_feed_key'},  # noqa: E241
    'ciW':          {'command': 'nv_feed_key'},  # noqa: E241
    'ci[':          {'command': 'nv_feed_key'},  # noqa: E241
    'ci\'':         {'command': 'nv_feed_key'},  # noqa: E241
    'ci\\':         {'command': 'nv_feed_key'},  # noqa: E241
    'ci]':          {'command': 'nv_feed_key'},  # noqa: E241
    'ci_':          {'command': 'nv_feed_key'},  # noqa: E241
    'ci`':          {'command': 'nv_feed_key'},  # noqa: E241
    'cib':          {'command': 'nv_feed_key'},  # noqa: E241
    'cip':          {'command': 'nv_feed_key'},  # noqa: E241
    'cis':          {'command': 'nv_feed_key'},  # noqa: E241
    'cit':          {'command': 'nv_feed_key'},  # noqa: E241
    'ciw':          {'command': 'nv_feed_key'},  # noqa: E241
    'ci{':          {'command': 'nv_feed_key'},  # noqa: E241
    'ci|':          {'command': 'nv_feed_key'},  # noqa: E241
    'ci}':          {'command': 'nv_feed_key'},  # noqa: E241
    'ci~':          {'command': 'nv_feed_key'},  # noqa: E241
    'cl':           {'command': 'nv_feed_key'},  # noqa: E241
    'cr ':          {'command': 'nv_feed_key'},  # noqa: E241
    'cr-':          {'command': 'nv_feed_key'},  # noqa: E241
    'cr.':          {'command': 'nv_feed_key'},  # noqa: E241
    'crU':          {'command': 'nv_feed_key'},  # noqa: E241
    'cr_':          {'command': 'nv_feed_key'},  # noqa: E241
    'crc':          {'command': 'nv_feed_key'},  # noqa: E241
    'cre':          {'command': 'nv_feed_key'},  # noqa: E241
    'crk':          {'command': 'nv_feed_key'},  # noqa: E241
    'crm':          {'command': 'nv_feed_key'},  # noqa: E241
    'crp':          {'command': 'nv_feed_key'},  # noqa: E241
    'crs':          {'command': 'nv_feed_key'},  # noqa: E241
    'crt':          {'command': 'nv_feed_key'},  # noqa: E241
    'cru':          {'command': 'nv_feed_key'},  # noqa: E241
    'cs""':         {'command': 'nv_feed_key'},  # noqa: E241
    'cs"(':         {'command': 'nv_feed_key'},  # noqa: E241
    'cs")':         {'command': 'nv_feed_key'},  # noqa: E241
    'cs"2':         {'command': 'nv_feed_key'},  # noqa: E241
    'cs"<':         {'command': 'nv_feed_key'},  # noqa: E241
    'cs"<i x="y">': {'command': 'nv_feed_key'},  # noqa: E241
    'cs"<x>':       {'command': 'nv_feed_key'},  # noqa: E241
    'cs">':         {'command': 'nv_feed_key'},  # noqa: E241
    'cs"[':         {'command': 'nv_feed_key'},  # noqa: E241
    'cs"\'':        {'command': 'nv_feed_key'},  # noqa: E241
    'cs"]':         {'command': 'nv_feed_key'},  # noqa: E241
    'cs"`':         {'command': 'nv_feed_key'},  # noqa: E241
    'cs"ti x="y">': {'command': 'nv_feed_key'},  # noqa: E241
    'cs"{':         {'command': 'nv_feed_key'},  # noqa: E241
    'cs("':         {'command': 'nv_feed_key'},  # noqa: E241
    'cs((':         {'command': 'nv_feed_key'},  # noqa: E241
    'cs()':         {'command': 'nv_feed_key'},  # noqa: E241
    'cs(2':         {'command': 'nv_feed_key'},  # noqa: E241
    'cs([':         {'command': 'nv_feed_key'},  # noqa: E241
    'cs(\'':        {'command': 'nv_feed_key'},  # noqa: E241
    'cs(]':         {'command': 'nv_feed_key'},  # noqa: E241
    'cs({':         {'command': 'nv_feed_key'},  # noqa: E241
    'cs(}':         {'command': 'nv_feed_key'},  # noqa: E241
    'cs)"':         {'command': 'nv_feed_key'},  # noqa: E241
    'cs)(':         {'command': 'nv_feed_key'},  # noqa: E241
    'cs))':         {'command': 'nv_feed_key'},  # noqa: E241
    'cs)2':         {'command': 'nv_feed_key'},  # noqa: E241
    'cs)[':         {'command': 'nv_feed_key'},  # noqa: E241
    'cs)\'':        {'command': 'nv_feed_key'},  # noqa: E241
    'cs)]':         {'command': 'nv_feed_key'},  # noqa: E241
    'cs){':         {'command': 'nv_feed_key'},  # noqa: E241
    'cs)}':         {'command': 'nv_feed_key'},  # noqa: E241
    'cs,`':         {'command': 'nv_feed_key'},  # noqa: E241
    'cs-_':         {'command': 'nv_feed_key'},  # noqa: E241
    'cs."':         {'command': 'nv_feed_key'},  # noqa: E241
    'cs>"':         {'command': 'nv_feed_key'},  # noqa: E241
    'cs>{':         {'command': 'nv_feed_key'},  # noqa: E241
    'cs>}':         {'command': 'nv_feed_key'},  # noqa: E241
    'csB"':         {'command': 'nv_feed_key'},  # noqa: E241
    'cs["':         {'command': 'nv_feed_key'},  # noqa: E241
    'cs\'"':        {'command': 'nv_feed_key'},  # noqa: E241
    'cs\'(':        {'command': 'nv_feed_key'},  # noqa: E241
    'cs\'<C-t>div<CR>': {'command': 'nv_feed_key', 'args': {'keys': ['c', 's', '\'', '<C-t>', 'd', 'i', 'v', '<CR>']}},  # noqa: E241,E501
    'cs\'<C-t>div>': {'command': 'nv_feed_key', 'args': {'keys': ['c', 's', '\'', '<C-t>', 'd', 'i', 'v', '>']}},  # noqa: E241,E501
    'cs\'<div<CR>': {'command': 'nv_feed_key', 'args': {'keys': ['c', 's', '\'', '<', 'd', 'i', 'v', '<CR>']}},  # noqa: E241,E501
    'cs\'<div>':    {'command': 'nv_feed_key'},  # noqa: E241
    'cs\'<q>':      {'command': 'nv_feed_key'},  # noqa: E241
    'cs\'`':        {'command': 'nv_feed_key'},  # noqa: E241
    'cs\'tdiv<CR>': {'command': 'nv_feed_key', 'args': {'keys': ['c', 's', '\'', 't', 'd', 'i', 'v', '<CR>']}},  # noqa: E241,E501
    'cs\'tdiv>':    {'command': 'nv_feed_key'},  # noqa: E241
    'cs\'tq>':      {'command': 'nv_feed_key'},  # noqa: E241
    'cs]"':         {'command': 'nv_feed_key'},  # noqa: E241
    'cs]>':         {'command': 'nv_feed_key'},  # noqa: E241
    'cs]{':         {'command': 'nv_feed_key'},  # noqa: E241
    'cs_-':         {'command': 'nv_feed_key'},  # noqa: E241
    'cs`"':         {'command': 'nv_feed_key'},  # noqa: E241
    'cs`\'':        {'command': 'nv_feed_key'},  # noqa: E241
    'csa"':         {'command': 'nv_feed_key'},  # noqa: E241
    'csb"':         {'command': 'nv_feed_key'},  # noqa: E241
    'csr"':         {'command': 'nv_feed_key'},  # noqa: E241
    'cst"':         {'command': 'nv_feed_key'},  # noqa: E241
    'cst<C-t>div<CR>': {'command': 'nv_feed_key', 'args': {'keys': ['c', 's', 't', '<C-t>', 'd', 'i', 'v', '<CR>']}},  # noqa: E241,E501
    'cst<a<CR>':    {'command': 'nv_feed_key', 'args': {'keys': ['c', 's', 't', '<', 'a', '<CR>']}},  # noqa: E241
    'cst<a>':       {'command': 'nv_feed_key'},  # noqa: E241
    'cst<div<CR>':  {'command': 'nv_feed_key', 'args': {'keys': ['c', 's', 't', '<', 'd', 'i', 'v', '<CR>']}},  # noqa: E241,E501
    'cst<div>':     {'command': 'nv_feed_key'},  # noqa: E241
    'cstta>':       {'command': 'nv_feed_key'},  # noqa: E241
    'cs{(':         {'command': 'nv_feed_key'},  # noqa: E241
    'cs{)':         {'command': 'nv_feed_key'},  # noqa: E241
    'cs}(':         {'command': 'nv_feed_key'},  # noqa: E241
    'cs})':         {'command': 'nv_feed_key'},  # noqa: E241
    'cw':           {'command': 'nv_feed_key'},  # noqa: E241
    'cziz':         {'command': 'nv_feed_key'},  # noqa: E241
    'c|':           {'command': 'nv_feed_key'},  # noqa: E241
    'd#':           {'command': 'nv_feed_key'},  # noqa: E241
    'd$':           {'command': 'nv_feed_key'},  # noqa: E241
    'd%':           {'command': 'nv_feed_key'},  # noqa: E241
    'd':            {'command': 'nv_feed_key'},  # noqa: E241
    'd(':           {'command': 'nv_feed_key'},  # noqa: E241
    'd)':           {'command': 'nv_feed_key'},  # noqa: E241
    'd*':           {'command': 'nv_feed_key'},  # noqa: E241
    'd-':           {'command': 'nv_feed_key'},  # noqa: E241
    'd/abc':        {'command': 'nv_vi_d', 'args': {'motion': {'motion_args': {'count': 1, 'mode': INTERNAL_NORMAL, 'pattern': 'abc'}, 'motion': 'nv_vi_slash_impl'}}},  # noqa: E241,E501
    'd0':           {'command': 'nv_feed_key'},  # noqa: E241
    'd2ft':         {'command': 'nv_feed_key'},  # noqa: E241
    'd<C-d>':       {'command': 'nv_feed_key', 'args': {'keys': ['d', '<C-d>']}},  # noqa: E241
    'd<C-u>':       {'command': 'nv_feed_key', 'args': {'keys': ['d', '<C-u>']}},  # noqa: E241
    'd?abc':        {'command': 'nv_vi_d', 'args': {'motion': {'motion_args': {'count': 1, 'mode': INTERNAL_NORMAL, 'pattern': 'abc'}, 'motion': 'nv_vi_question_mark_impl'}}},  # noqa: E241,E501
    'dB':           {'command': 'nv_feed_key'},  # noqa: E241
    'dE':           {'command': 'nv_feed_key'},  # noqa: E241
    'dFx':          {'command': 'nv_feed_key'},  # noqa: E241
    'dG':           {'command': 'nv_feed_key'},  # noqa: E241
    'dH':           {'command': 'nv_feed_key'},  # noqa: E241
    'dL':           {'command': 'nv_feed_key'},  # noqa: E241
    'dM':           {'command': 'nv_feed_key'},  # noqa: E241
    'dTx':          {'command': 'nv_feed_key'},  # noqa: E241
    'dW':           {'command': 'nv_feed_key'},  # noqa: E241
    'dZiz':         {'command': 'nv_feed_key'},  # noqa: E241
    'd[{':          {'command': 'nv_feed_key'},  # noqa: E241
    'd\'a':         {'command': 'nv_feed_key'},  # noqa: E241
    'd\'x':         {'command': 'nv_feed_key'},  # noqa: E241
    'd]}':          {'command': 'nv_feed_key'},  # noqa: E241
    'd^':           {'command': 'nv_feed_key'},  # noqa: E241
    'd_':           {'command': 'nv_feed_key'},  # noqa: E241
    'd`a':          {'command': 'nv_feed_key'},  # noqa: E241
    'd`x':          {'command': 'nv_feed_key'},  # noqa: E241
    'da"':          {'command': 'nv_feed_key'},  # noqa: E241
    'da#':          {'command': 'nv_feed_key'},  # noqa: E241
    'da$':          {'command': 'nv_feed_key'},  # noqa: E241
    'da&':          {'command': 'nv_feed_key'},  # noqa: E241
    'da(':          {'command': 'nv_feed_key'},  # noqa: E241
    'da)':          {'command': 'nv_feed_key'},  # noqa: E241
    'da*':          {'command': 'nv_feed_key'},  # noqa: E241
    'da+':          {'command': 'nv_feed_key'},  # noqa: E241
    'da,':          {'command': 'nv_feed_key'},  # noqa: E241
    'da-':          {'command': 'nv_feed_key'},  # noqa: E241
    'da.':          {'command': 'nv_feed_key'},  # noqa: E241
    'da/':          {'command': 'nv_feed_key'},  # noqa: E241
    'da:':          {'command': 'nv_feed_key'},  # noqa: E241
    'da;':          {'command': 'nv_feed_key'},  # noqa: E241
    'da<':          {'command': 'nv_feed_key'},  # noqa: E241
    'da=':          {'command': 'nv_feed_key'},  # noqa: E241
    'da>':          {'command': 'nv_feed_key'},  # noqa: E241
    'daB':          {'command': 'nv_feed_key'},  # noqa: E241
    'daW':          {'command': 'nv_feed_key'},  # noqa: E241
    'da[':          {'command': 'nv_feed_key'},  # noqa: E241
    'da\'':         {'command': 'nv_feed_key'},  # noqa: E241
    'da\\':         {'command': 'nv_feed_key'},  # noqa: E241
    'da]':          {'command': 'nv_feed_key'},  # noqa: E241
    'da_':          {'command': 'nv_feed_key'},  # noqa: E241
    'da`':          {'command': 'nv_feed_key'},  # noqa: E241
    'dab':          {'command': 'nv_feed_key'},  # noqa: E241
    'dap':          {'command': 'nv_feed_key'},  # noqa: E241
    'das':          {'command': 'nv_feed_key'},  # noqa: E241
    'dat':          {'command': 'nv_feed_key'},  # noqa: E241
    'daw':          {'command': 'nv_feed_key'},  # noqa: E241
    'da{':          {'command': 'nv_feed_key'},  # noqa: E241
    'da|':          {'command': 'nv_feed_key'},  # noqa: E241
    'da}':          {'command': 'nv_feed_key'},  # noqa: E241
    'da~':          {'command': 'nv_feed_key'},  # noqa: E241
    'dd':           {'command': 'nv_feed_key'},  # noqa: E241
    'de':           {'command': 'nv_feed_key'},  # noqa: E241
    'df=':          {'command': 'nv_feed_key'},  # noqa: E241
    'dft':          {'command': 'nv_feed_key'},  # noqa: E241
    'dfx':          {'command': 'nv_feed_key'},  # noqa: E241
    'dgE':          {'command': 'nv_feed_key'},  # noqa: E241
    'dg_':          {'command': 'nv_feed_key'},  # noqa: E241
    'dge':          {'command': 'nv_feed_key'},  # noqa: E241
    'dgg':          {'command': 'nv_feed_key'},  # noqa: E241
    'dh':           {'command': 'nv_feed_key'},  # noqa: E241
    'di"':          {'command': 'nv_feed_key'},  # noqa: E241
    'di#':          {'command': 'nv_feed_key'},  # noqa: E241
    'di$':          {'command': 'nv_feed_key'},  # noqa: E241
    'di&':          {'command': 'nv_feed_key'},  # noqa: E241
    'di(':          {'command': 'nv_feed_key'},  # noqa: E241
    'di)':          {'command': 'nv_feed_key'},  # noqa: E241
    'di*':          {'command': 'nv_feed_key'},  # noqa: E241
    'di+':          {'command': 'nv_feed_key'},  # noqa: E241
    'di,':          {'command': 'nv_feed_key'},  # noqa: E241
    'di-':          {'command': 'nv_feed_key'},  # noqa: E241
    'di.':          {'command': 'nv_feed_key'},  # noqa: E241
    'di/':          {'command': 'nv_feed_key'},  # noqa: E241
    'di:':          {'command': 'nv_feed_key'},  # noqa: E241
    'di;':          {'command': 'nv_feed_key'},  # noqa: E241
    'di=':          {'command': 'nv_feed_key'},  # noqa: E241
    'di>':          {'command': 'nv_feed_key'},  # noqa: E241
    'diB':          {'command': 'nv_feed_key'},  # noqa: E241
    'diW':          {'command': 'nv_feed_key'},  # noqa: E241
    'di[':          {'command': 'nv_feed_key'},  # noqa: E241
    'di\'':         {'command': 'nv_feed_key'},  # noqa: E241
    'di\\':         {'command': 'nv_feed_key'},  # noqa: E241
    'di]':          {'command': 'nv_feed_key'},  # noqa: E241
    'di_':          {'command': 'nv_feed_key'},  # noqa: E241
    'di`':          {'command': 'nv_feed_key'},  # noqa: E241
    'dib':          {'command': 'nv_feed_key'},  # noqa: E241
    'dip':          {'command': 'nv_feed_key'},  # noqa: E241
    'dis':          {'command': 'nv_feed_key'},  # noqa: E241
    'dit':          {'command': 'nv_feed_key'},  # noqa: E241
    'diw':          {'command': 'nv_feed_key'},  # noqa: E241
    'di{':          {'command': 'nv_feed_key'},  # noqa: E241
    'di|':          {'command': 'nv_feed_key'},  # noqa: E241
    'di}':          {'command': 'nv_feed_key'},  # noqa: E241
    'di~':          {'command': 'nv_feed_key'},  # noqa: E241
    'dj':           {'command': 'nv_feed_key'},  # noqa: E241
    'dk':           {'command': 'nv_feed_key'},  # noqa: E241
    'dl':           {'command': 'nv_feed_key'},  # noqa: E241
    'ds ':          {'command': 'nv_feed_key'},  # noqa: E241
    'ds"':          {'command': 'nv_feed_key'},  # noqa: E241
    'ds#':          {'command': 'nv_feed_key'},  # noqa: E241
    'ds$':          {'command': 'nv_feed_key'},  # noqa: E241
    'ds&':          {'command': 'nv_feed_key'},  # noqa: E241
    'ds(':          {'command': 'nv_feed_key'},  # noqa: E241
    'ds)':          {'command': 'nv_feed_key'},  # noqa: E241
    'ds*':          {'command': 'nv_feed_key'},  # noqa: E241
    'ds+':          {'command': 'nv_feed_key'},  # noqa: E241
    'ds,':          {'command': 'nv_feed_key'},  # noqa: E241
    'ds-':          {'command': 'nv_feed_key'},  # noqa: E241
    'ds.':          {'command': 'nv_feed_key'},  # noqa: E241
    'ds0':          {'command': 'nv_feed_key'},  # noqa: E241
    'ds2':          {'command': 'nv_feed_key'},  # noqa: E241
    'ds:':          {'command': 'nv_feed_key'},  # noqa: E241
    'ds;':          {'command': 'nv_feed_key'},  # noqa: E241
    'ds<':          {'command': 'nv_feed_key'},  # noqa: E241
    'ds=':          {'command': 'nv_feed_key'},  # noqa: E241
    'ds>':          {'command': 'nv_feed_key'},  # noqa: E241
    'dsB':          {'command': 'nv_feed_key'},  # noqa: E241
    'dsW':          {'command': 'nv_feed_key'},  # noqa: E241
    'ds[':          {'command': 'nv_feed_key'},  # noqa: E241
    'ds\'':         {'command': 'nv_feed_key'},  # noqa: E241
    'ds\\':         {'command': 'nv_feed_key'},  # noqa: E241
    'ds]':          {'command': 'nv_feed_key'},  # noqa: E241
    'ds_':          {'command': 'nv_feed_key'},  # noqa: E241
    'ds`':          {'command': 'nv_feed_key'},  # noqa: E241
    'dsa':          {'command': 'nv_feed_key'},  # noqa: E241
    'dsb':          {'command': 'nv_feed_key'},  # noqa: E241
    'dse':          {'command': 'nv_feed_key'},  # noqa: E241
    'dsp':          {'command': 'nv_feed_key'},  # noqa: E241
    'dsq':          {'command': 'nv_feed_key'},  # noqa: E241
    'dsr':          {'command': 'nv_feed_key'},  # noqa: E241
    'dss':          {'command': 'nv_feed_key'},  # noqa: E241
    'dst':          {'command': 'nv_feed_key'},  # noqa: E241
    'dsw':          {'command': 'nv_feed_key'},  # noqa: E241
    'ds{':          {'command': 'nv_feed_key'},  # noqa: E241
    'ds}':          {'command': 'nv_feed_key'},  # noqa: E241
    'ds~':          {'command': 'nv_feed_key'},  # noqa: E241
    'dtx':          {'command': 'nv_feed_key'},  # noqa: E241
    'dw':           {'command': 'nv_feed_key'},  # noqa: E241
    'dziz':         {'command': 'nv_feed_key'},  # noqa: E241
    'd{':           {'command': 'nv_feed_key'},  # noqa: E241
    'd|':           {'command': 'nv_feed_key'},  # noqa: E241
    'd}':           {'command': 'nv_feed_key'},  # noqa: E241
    'e':            {'command': 'nv_feed_key'},  # noqa: E241
    'f':            {'command': 'nv_feed_key'},  # noqa: E241
    'f2':           {'command': 'nv_feed_key'},  # noqa: E241
    'f6':           {'command': 'nv_feed_key'},  # noqa: E241
    'f8':           {'command': 'nv_feed_key'},  # noqa: E241
    'f:':           {'command': 'nv_feed_key'},  # noqa: E241
    'f<k4>':        {'command': 'nv_feed_key', 'args': {'keys': ['f', '<k4>']}},  # noqa: E241
    'f<kminus>':    {'command': 'nv_feed_key', 'args': {'keys': ['f', '<kminus>']}},  # noqa: E241
    'f\\':          {'command': 'nv_feed_key'},  # noqa: E241
    'ff':           {'command': 'nv_feed_key'},  # noqa: E241
    'fr':           {'command': 'nv_feed_key'},  # noqa: E241
    'fx':           {'command': 'nv_feed_key'},  # noqa: E241
    'f|':           {'command': 'nv_feed_key'},  # noqa: E241
    'g':            {'command': 'nv_feed_key'},  # noqa: E241
    'gC':           {'command': 'nv_feed_key'},  # noqa: E241
    'gC}':          {'command': 'nv_feed_key'},  # noqa: E241
    'gD':           {'command': 'nv_feed_key'},  # noqa: E241
    'gE':           {'command': 'nv_feed_key'},  # noqa: E241
    'gF':           {'command': 'nv_feed_key'},  # noqa: E241
    'gH':           {'command': 'nv_feed_key'},  # noqa: E241
    'gJ':           {'command': 'nv_feed_key'},  # noqa: E241
    'gN':           {'command': 'nv_feed_key'},  # noqa: E241
    'gP':           {'command': 'nv_feed_key'},  # noqa: E241
    'gT':           {'command': 'nv_feed_key'},  # noqa: E241
    'gU':           {'command': 'nv_feed_key'},  # noqa: E241
    'gUU':          {'command': 'nv_feed_key'},  # noqa: E241
    'gUb':          {'command': 'nv_feed_key'},  # noqa: E241
    'gUip':         {'command': 'nv_feed_key'},  # noqa: E241
    'g_':           {'command': 'nv_feed_key'},  # noqa: E241
    'ga':           {'command': 'nv_feed_key'},  # noqa: E241
    'gc':           {'command': 'nv_feed_key'},  # noqa: E241
    'gc7G':         {'command': 'nv_feed_key'},  # noqa: E241
    'gcG':          {'command': 'nv_feed_key'},  # noqa: E241
    'gcc':          {'command': 'nv_feed_key'},  # noqa: E241
    'gd':           {'command': 'nv_feed_key'},  # noqa: E241
    'ge':           {'command': 'nv_feed_key'},  # noqa: E241
    'gf':           {'command': 'nv_feed_key'},  # noqa: E241
    'gg':           {'command': 'nv_feed_key'},  # noqa: E241
    'gh':           {'command': 'nv_feed_key'},  # noqa: E241
    'gj':           {'command': 'nv_feed_key'},  # noqa: E241
    'gk':           {'command': 'nv_feed_key'},  # noqa: E241
    'gn':           {'command': 'nv_feed_key'},  # noqa: E241
    'gp':           {'command': 'nv_feed_key'},  # noqa: E241
    'gq$':          {'command': 'nv_feed_key'},  # noqa: E241
    'gq':           {'command': 'nv_feed_key'},  # noqa: E241
    'gqgq':         {'command': 'nv_feed_key'},  # noqa: E241
    'gqip':         {'command': 'nv_feed_key'},  # noqa: E241
    'gqq':          {'command': 'nv_feed_key'},  # noqa: E241
    'gq}':          {'command': 'nv_feed_key'},  # noqa: E241
    'gt':           {'command': 'nv_feed_key'},  # noqa: E241
    'gu':           {'command': 'nv_feed_key'},  # noqa: E241
    'gub':          {'command': 'nv_feed_key'},  # noqa: E241
    'guis':         {'command': 'nv_feed_key'},  # noqa: E241
    'guu':          {'command': 'nv_feed_key'},  # noqa: E241
    'gv':           {'command': 'nv_feed_key'},  # noqa: E241
    'gx':           {'command': 'nv_feed_key'},  # noqa: E241
    'g~$':          {'command': 'nv_feed_key'},  # noqa: E241
    'g~':           {'command': 'nv_feed_key'},  # noqa: E241
    'g~~':          {'command': 'nv_feed_key'},  # noqa: E241
    'h':            {'command': 'nv_feed_key'},  # noqa: E241
    'i"':           {'command': 'nv_feed_key'},  # noqa: E241
    'i#':           {'command': 'nv_feed_key'},  # noqa: E241
    'i$':           {'command': 'nv_feed_key'},  # noqa: E241
    'i&':           {'command': 'nv_feed_key'},  # noqa: E241
    'i':            {'command': 'nv_feed_key'},  # noqa: E241
    'i(':           {'command': 'nv_feed_key'},  # noqa: E241
    'i)':           {'command': 'nv_feed_key'},  # noqa: E241
    'i*':           {'command': 'nv_feed_key'},  # noqa: E241
    'i+':           {'command': 'nv_feed_key'},  # noqa: E241
    'i,':           {'command': 'nv_feed_key'},  # noqa: E241
    'i-':           {'command': 'nv_feed_key'},  # noqa: E241
    'i.':           {'command': 'nv_feed_key'},  # noqa: E241
    'i/':           {'command': 'nv_feed_key'},  # noqa: E241
    'i:':           {'command': 'nv_feed_key'},  # noqa: E241
    'i;':           {'command': 'nv_feed_key'},  # noqa: E241
    'i<':           {'command': 'nv_feed_key'},  # noqa: E241
    'i=':           {'command': 'nv_feed_key'},  # noqa: E241
    'i>':           {'command': 'nv_feed_key'},  # noqa: E241
    'iB':           {'command': 'nv_feed_key'},  # noqa: E241
    'iI':           {'command': 'nv_feed_key'},  # noqa: E241
    'iW':           {'command': 'nv_feed_key'},  # noqa: E241
    'i[':           {'command': 'nv_feed_key'},  # noqa: E241
    'i\'':          {'command': 'nv_feed_key'},  # noqa: E241
    'i\\':          {'command': 'nv_feed_key'},  # noqa: E241
    'i]':           {'command': 'nv_feed_key'},  # noqa: E241
    'i_':           {'command': 'nv_feed_key'},  # noqa: E241
    'i`':           {'command': 'nv_feed_key'},  # noqa: E241
    'ib':           {'command': 'nv_feed_key'},  # noqa: E241
    'ii':           {'command': 'nv_feed_key'},  # noqa: E241
    'ip':           {'command': 'nv_feed_key'},  # noqa: E241
    'is':           {'command': 'nv_feed_key'},  # noqa: E241
    'it':           {'command': 'nv_feed_key'},  # noqa: E241
    'iw':           {'command': 'nv_feed_key'},  # noqa: E241
    'i{':           {'command': 'nv_feed_key'},  # noqa: E241
    'i|':           {'command': 'nv_feed_key'},  # noqa: E241
    'i}':           {'command': 'nv_feed_key'},  # noqa: E241
    'i~':           {'command': 'nv_feed_key'},  # noqa: E241
    'j':            {'command': 'nv_feed_key'},  # noqa: E241
    'k':            {'command': 'nv_feed_key'},  # noqa: E241
    'l':            {'command': 'nv_feed_key'},  # noqa: E241
    'm':            {'command': 'nv_feed_key'},  # noqa: E241
    'ma':           {'command': 'nv_feed_key'},  # noqa: E241
    'mx':           {'command': 'nv_feed_key'},  # noqa: E241
    'n':            {'command': 'nv_feed_key'},  # noqa: E241
    'o':            {'command': 'nv_feed_key'},  # noqa: E241
    'p':            {'command': 'nv_feed_key'},  # noqa: E241
    'q':            {'command': 'nv_feed_key'},  # noqa: E241
    'q-':           {'command': 'nv_feed_key'},  # noqa: E241
    'q@':           {'command': 'nv_feed_key'},  # noqa: E241
    'qA':           {'command': 'nv_feed_key'},  # noqa: E241
    'qa':           {'command': 'nv_feed_key'},  # noqa: E241
    'qx':           {'command': 'nv_feed_key'},  # noqa: E241
    'r':            {'command': 'nv_feed_key'},  # noqa: E241
    'r<cr>':        {'command': 'nv_feed_key', 'args': {'keys': ['r', '<cr>']}},  # noqa: E241
    'r<k0>':        {'command': 'nv_feed_key', 'args': {'keys': ['r', '<k0>']}},  # noqa: E241
    'r<k1>':        {'command': 'nv_feed_key', 'args': {'keys': ['r', '<k1>']}},  # noqa: E241
    'r<k2>':        {'command': 'nv_feed_key', 'args': {'keys': ['r', '<k2>']}},  # noqa: E241
    'r<k3>':        {'command': 'nv_feed_key', 'args': {'keys': ['r', '<k3>']}},  # noqa: E241
    'r<k4>':        {'command': 'nv_feed_key', 'args': {'keys': ['r', '<k4>']}},  # noqa: E241
    'r<k5>':        {'command': 'nv_feed_key', 'args': {'keys': ['r', '<k5>']}},  # noqa: E241
    'r<k6>':        {'command': 'nv_feed_key', 'args': {'keys': ['r', '<k6>']}},  # noqa: E241
    'r<k7>':        {'command': 'nv_feed_key', 'args': {'keys': ['r', '<k7>']}},  # noqa: E241
    'r<k8>':        {'command': 'nv_feed_key', 'args': {'keys': ['r', '<k8>']}},  # noqa: E241
    'r<k9>':        {'command': 'nv_feed_key', 'args': {'keys': ['r', '<k9>']}},  # noqa: E241
    'r<kdivide>':   {'command': 'nv_feed_key', 'args': {'keys': ['r', '<kdivide>']}},  # noqa: E241
    'r<kenter>':    {'command': 'nv_feed_key', 'args': {'keys': ['r', '<kenter>']}},  # noqa: E241
    'r<kminus>':    {'command': 'nv_feed_key', 'args': {'keys': ['r', '<kminus>']}},  # noqa: E241
    'r<kmultiply>': {'command': 'nv_feed_key', 'args': {'keys': ['r', '<kmultiply>']}},  # noqa: E241
    'r<kperiod>':   {'command': 'nv_feed_key', 'args': {'keys': ['r', '<kperiod>']}},  # noqa: E241
    'r<kplus>':     {'command': 'nv_feed_key', 'args': {'keys': ['r', '<kplus>']}},  # noqa: E241
    'rx':           {'command': 'nv_feed_key'},  # noqa: E241
    's$t':          {'command': 'nv_feed_key'},  # noqa: E241
    's':            {'command': 'nv_feed_key'},  # noqa: E241
    's<CR>':        {'command': 'nv_feed_key', 'args': {'keys': ['s', '<CR>']}},  # noqa: E241
    'sIZ':          {'command': 'nv_feed_key'},  # noqa: E241
    'sab':          {'command': 'nv_feed_key'},  # noqa: E241
    'siz':          {'command': 'nv_feed_key'},  # noqa: E241
    'sx<CR>':       {'command': 'nv_feed_key', 'args': {'keys': ['s', 'x', '<CR>']}},  # noqa: E241
    'sxy':          {'command': 'nv_feed_key'},  # noqa: E241
    't2':           {'command': 'nv_feed_key'},  # noqa: E241
    't6':           {'command': 'nv_feed_key'},  # noqa: E241
    't8':           {'command': 'nv_feed_key'},  # noqa: E241
    't:':           {'command': 'nv_feed_key'},  # noqa: E241
    't<kmultiply>': {'command': 'nv_feed_key', 'args': {'keys': ['t', '<kmultiply>']}},  # noqa: E241
    't\\':          {'command': 'nv_feed_key'},  # noqa: E241
    'tf':           {'command': 'nv_feed_key'},  # noqa: E241
    'tr':           {'command': 'nv_feed_key'},  # noqa: E241
    'tx':           {'command': 'nv_feed_key'},  # noqa: E241
    't|':           {'command': 'nv_feed_key'},  # noqa: E241
    'u':            {'command': 'nv_feed_key'},  # noqa: E241
    'v':            {'command': 'nv_feed_key'},  # noqa: E241
    'w':            {'command': 'nv_feed_key'},  # noqa: E241
    'x':            {'command': 'nv_feed_key'},  # noqa: E241
    'y$':           {'command': 'nv_feed_key'},  # noqa: E241
    'y':            {'command': 'nv_feed_key'},  # noqa: E241
    'ya"':          {'command': 'nv_feed_key'},  # noqa: E241
    'ya#':          {'command': 'nv_feed_key'},  # noqa: E241
    'ya$':          {'command': 'nv_feed_key'},  # noqa: E241
    'ya&':          {'command': 'nv_feed_key'},  # noqa: E241
    'ya(':          {'command': 'nv_feed_key'},  # noqa: E241
    'ya)':          {'command': 'nv_feed_key'},  # noqa: E241
    'ya*':          {'command': 'nv_feed_key'},  # noqa: E241
    'ya+':          {'command': 'nv_feed_key'},  # noqa: E241
    'ya,':          {'command': 'nv_feed_key'},  # noqa: E241
    'ya-':          {'command': 'nv_feed_key'},  # noqa: E241
    'ya.':          {'command': 'nv_feed_key'},  # noqa: E241
    'ya/':          {'command': 'nv_feed_key'},  # noqa: E241
    'ya:':          {'command': 'nv_feed_key'},  # noqa: E241
    'ya;':          {'command': 'nv_feed_key'},  # noqa: E241
    'ya<':          {'command': 'nv_feed_key'},  # noqa: E241
    'ya=':          {'command': 'nv_feed_key'},  # noqa: E241
    'ya>':          {'command': 'nv_feed_key'},  # noqa: E241
    'yaB':          {'command': 'nv_feed_key'},  # noqa: E241
    'yaW':          {'command': 'nv_feed_key'},  # noqa: E241
    'ya[':          {'command': 'nv_feed_key'},  # noqa: E241
    'ya\'':         {'command': 'nv_feed_key'},  # noqa: E241
    'ya\\':         {'command': 'nv_feed_key'},  # noqa: E241
    'ya]':          {'command': 'nv_feed_key'},  # noqa: E241
    'ya_':          {'command': 'nv_feed_key'},  # noqa: E241
    'ya`':          {'command': 'nv_feed_key'},  # noqa: E241
    'yab':          {'command': 'nv_feed_key'},  # noqa: E241
    'yap':          {'command': 'nv_feed_key'},  # noqa: E241
    'yas':          {'command': 'nv_feed_key'},  # noqa: E241
    'yat':          {'command': 'nv_feed_key'},  # noqa: E241
    'yaw':          {'command': 'nv_feed_key'},  # noqa: E241
    'ya{':          {'command': 'nv_feed_key'},  # noqa: E241
    'ya|':          {'command': 'nv_feed_key'},  # noqa: E241
    'ya}':          {'command': 'nv_feed_key'},  # noqa: E241
    'ya~':          {'command': 'nv_feed_key'},  # noqa: E241
    'yi"':          {'command': 'nv_feed_key'},  # noqa: E241
    'yi#':          {'command': 'nv_feed_key'},  # noqa: E241
    'yi$':          {'command': 'nv_feed_key'},  # noqa: E241
    'yi&':          {'command': 'nv_feed_key'},  # noqa: E241
    'yi(':          {'command': 'nv_feed_key'},  # noqa: E241
    'yi)':          {'command': 'nv_feed_key'},  # noqa: E241
    'yi*':          {'command': 'nv_feed_key'},  # noqa: E241
    'yi+':          {'command': 'nv_feed_key'},  # noqa: E241
    'yi,':          {'command': 'nv_feed_key'},  # noqa: E241
    'yi-':          {'command': 'nv_feed_key'},  # noqa: E241
    'yi.':          {'command': 'nv_feed_key'},  # noqa: E241
    'yi/':          {'command': 'nv_feed_key'},  # noqa: E241
    'yi:':          {'command': 'nv_feed_key'},  # noqa: E241
    'yi;':          {'command': 'nv_feed_key'},  # noqa: E241
    'yi<':          {'command': 'nv_feed_key'},  # noqa: E241
    'yi=':          {'command': 'nv_feed_key'},  # noqa: E241
    'yi>':          {'command': 'nv_feed_key'},  # noqa: E241
    'yiB':          {'command': 'nv_feed_key'},  # noqa: E241
    'yiW':          {'command': 'nv_feed_key'},  # noqa: E241
    'yi[':          {'command': 'nv_feed_key'},  # noqa: E241
    'yi\'':         {'command': 'nv_feed_key'},  # noqa: E241
    'yi\\':         {'command': 'nv_feed_key'},  # noqa: E241
    'yi]':          {'command': 'nv_feed_key'},  # noqa: E241
    'yi_':          {'command': 'nv_feed_key'},  # noqa: E241
    'yi`':          {'command': 'nv_feed_key'},  # noqa: E241
    'yib':          {'command': 'nv_feed_key'},  # noqa: E241
    'yip':          {'command': 'nv_feed_key'},  # noqa: E241
    'yis':          {'command': 'nv_feed_key'},  # noqa: E241
    'yit':          {'command': 'nv_feed_key'},  # noqa: E241
    'yiw':          {'command': 'nv_feed_key'},  # noqa: E241
    'yi{':          {'command': 'nv_feed_key'},  # noqa: E241
    'yi|':          {'command': 'nv_feed_key'},  # noqa: E241
    'yi}':          {'command': 'nv_feed_key'},  # noqa: E241
    'yi~':          {'command': 'nv_feed_key'},  # noqa: E241
    'yj':           {'command': 'nv_feed_key'},  # noqa: E241
    'yk':           {'command': 'nv_feed_key'},  # noqa: E241
    'yoa':          {'command': 'nv_feed_key'},  # noqa: E241
    'yoc':          {'command': 'nv_feed_key'},  # noqa: E241
    'yoe':          {'command': 'nv_feed_key'},  # noqa: E241
    'yoh':          {'command': 'nv_feed_key'},  # noqa: E241
    'yoi':          {'command': 'nv_feed_key'},  # noqa: E241
    'yol':          {'command': 'nv_feed_key'},  # noqa: E241
    'yom':          {'command': 'nv_feed_key'},  # noqa: E241
    'yon':          {'command': 'nv_feed_key'},  # noqa: E241
    'yot':          {'command': 'nv_feed_key'},  # noqa: E241
    'yow':          {'command': 'nv_feed_key'},  # noqa: E241
    'yse"':         {'command': 'nv_feed_key'},  # noqa: E241
    'yse(':         {'command': 'nv_feed_key'},  # noqa: E241
    'yse)':         {'command': 'nv_feed_key'},  # noqa: E241
    'yse2':         {'command': 'nv_feed_key'},  # noqa: E241
    'yse<foo>':     {'command': 'nv_feed_key'},  # noqa: E241
    'yse[':         {'command': 'nv_feed_key'},  # noqa: E241
    'yse\'':        {'command': 'nv_feed_key'},  # noqa: E241
    'yse]':         {'command': 'nv_feed_key'},  # noqa: E241
    'yse{':         {'command': 'nv_feed_key'},  # noqa: E241
    'yse}':         {'command': 'nv_feed_key'},  # noqa: E241
    'ysiw"':        {'command': 'nv_feed_key'},  # noqa: E241
    'ysiw(':        {'command': 'nv_feed_key'},  # noqa: E241
    'ysiw)':        {'command': 'nv_feed_key'},  # noqa: E241
    'ysiw2':        {'command': 'nv_feed_key'},  # noqa: E241
    'ysiw<C-f>print<CR>': {'command': 'nv_feed_key', 'args': {"keys": ['y', 's', 'i', 'w', '<C-f>', 'p', 'r', 'i', 'n', 't', '<CR>']}},  # noqa: E231,E241,E501
    'ysiw<C-t>div<CR>': {'command': 'nv_feed_key', 'args': {'keys': ['y', 's', 'i', 'w', '<C-t>', 'd', 'i', 'v', '<CR>']}},  # noqa: E231,E241,E501
    'ysiw<C-t>div>': {'command': 'nv_feed_key', 'args': {'keys': ['y', 's', 'i', 'w', '<C-t>', 'd', 'i', 'v', '>']}},  # noqa: E231,E241,E501
    'ysiw<div<CR>': {'command': 'nv_feed_key', 'args': {"keys": ['y', 's', 'i', 'w', '<', 'd', 'i', 'v', '<CR>']}},  # noqa: E231,E501
    'ysiw<div>':    {'command': 'nv_feed_key'},  # noqa: E231,E241
    'ysiw<foo>':    {'command': 'nv_feed_key'},  # noqa: E241
    'ysiw<i x="y">':{'command': 'nv_feed_key'},  # noqa: E231,E241
    'ysiw>':        {'command': 'nv_feed_key'},  # noqa: E241
    'ysiwB':        {'command': 'nv_feed_key'},  # noqa: E241
    'ysiwFprint<CR>': {'command': 'nv_feed_key', 'args': {"keys": ['y', 's', 'i', 'w', 'F', 'p', 'r', 'i', 'n', 't', '<CR>']}},  # noqa: E231,E501
    'ysiw[':        {'command': 'nv_feed_key'},  # noqa: E241
    'ysiw\'':       {'command': 'nv_feed_key'},  # noqa: E241
    'ysiw]':        {'command': 'nv_feed_key'},  # noqa: E241
    'ysiwa':        {'command': 'nv_feed_key'},  # noqa: E241
    'ysiwafoo>':    {'command': 'nv_feed_key'},  # noqa: E241
    'ysiwb':        {'command': 'nv_feed_key'},  # noqa: E241
    'ysiwfprint<CR>': {'command': 'nv_feed_key', 'args': {"keys": ['y', 's', 'i', 'w', 'f', 'p', 'r', 'i', 'n', 't', '<CR>']}},  # noqa: E231,E501
    'ysiwr':        {'command': 'nv_feed_key'},  # noqa: E241
    'ysiwtdiv<CR>': {'command': 'nv_feed_key', 'args': {"keys": ['y', 's', 'i', 'w', '<', 'd', 'i', 'v', '<CR>']}},  # noqa: E231,E501
    'ysiwtdiv>':    {'command': 'nv_feed_key'},  # noqa: E231,E241
    'ysiwti x="y">': {'command': 'nv_feed_key'},  # noqa: E231
    'ysiw{':        {'command': 'nv_feed_key'},  # noqa: E241
    'ysiw}':        {'command': 'nv_feed_key'},  # noqa: E241
    'yss)':         {'command': 'nv_feed_key'},  # noqa: E241
    'yy':           {'command': 'nv_feed_key'},  # noqa: E241
    'z-':           {'command': 'nv_feed_key'},  # noqa: E241
    'z.':           {'command': 'nv_feed_key'},  # noqa: E241
    'z<CR>':        {'command': 'nv_feed_key', 'args': {"keys": ['z', '<CR>']}},  # noqa: E241
    'z=':           {'command': 'nv_feed_key'},  # noqa: E241
    'zC':           {'command': 'nv_feed_key'},  # noqa: E241
    'zM':           {'command': 'nv_feed_key'},  # noqa: E241
    'zO':           {'command': 'nv_feed_key'},  # noqa: E241
    'zR':           {'command': 'nv_feed_key'},  # noqa: E241
    'zb':           {'command': 'nv_feed_key'},  # noqa: E241
    'zc':           {'command': 'nv_feed_key'},  # noqa: E241
    'zg':           {'command': 'nv_feed_key'},  # noqa: E241
    'zo':           {'command': 'nv_feed_key'},  # noqa: E241
    'zt':           {'command': 'nv_feed_key'},  # noqa: E241
    'zug':          {'command': 'nv_feed_key'},  # noqa: E241
    'zz':           {'command': 'nv_feed_key'},  # noqa: E241
    '{':            {'command': 'nv_feed_key'},  # noqa: E241
    '|':            {'command': 'nv_feed_key'},  # noqa: E241
    '}':            {'command': 'nv_feed_key'},  # noqa: E241
    '~':            {'command': 'nv_feed_key'},  # noqa: E241

}  # type: dict
