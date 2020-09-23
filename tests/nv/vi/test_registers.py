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

from collections import deque
from unittest import mock

from sublime import get_clipboard
from sublime import set_clipboard

from NeoVintageous.tests import unittest

from NeoVintageous.nv.registers import _ALL
from NeoVintageous.nv.registers import _ALTERNATE_FILE
from NeoVintageous.nv.registers import _BLACK_HOLE
from NeoVintageous.nv.registers import _CLIPBOARD
from NeoVintageous.nv.registers import _CLIPBOARD_PLUS
from NeoVintageous.nv.registers import _CLIPBOARD_STAR
from NeoVintageous.nv.registers import _CLIPBOARD_TILDA
from NeoVintageous.nv.registers import _CURRENT_FILE_NAME
from NeoVintageous.nv.registers import _EXPRESSION
from NeoVintageous.nv.registers import _LAST_EXECUTED_COMMAND
from NeoVintageous.nv.registers import _LAST_INSERTED_TEXT
from NeoVintageous.nv.registers import _LAST_SEARCH_PATTERN
from NeoVintageous.nv.registers import _NAMED
from NeoVintageous.nv.registers import _NUMBERED
from NeoVintageous.nv.registers import _READ_ONLY
from NeoVintageous.nv.registers import _SELECTION_AND_DROP
from NeoVintageous.nv.registers import _SMALL_DELETE
from NeoVintageous.nv.registers import _SPECIAL
from NeoVintageous.nv.registers import _UNNAMED
from NeoVintageous.nv.registers import _data
from NeoVintageous.nv.registers import _get_selected_text
from NeoVintageous.nv.registers import _is_register_linewise
from NeoVintageous.nv.registers import _reset
from NeoVintageous.nv.registers import _set_unnamed
from NeoVintageous.nv.registers import registers_get
from NeoVintageous.nv.registers import registers_get_all
from NeoVintageous.nv.registers import registers_get_for_paste
from NeoVintageous.nv.registers import registers_op_change
from NeoVintageous.nv.registers import registers_op_delete
from NeoVintageous.nv.registers import registers_op_yank
from NeoVintageous.nv.registers import registers_set
from NeoVintageous.nv.registers import set_expression_register


class RegistersTestCase(unittest.ResetRegisters, unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        self.settings().erase('vintage')
        self.reset_setting('use_sys_clipboard')
        self.set_setting('use_sys_clipboard', False)
        set_clipboard('')
        _reset()

    def tearDown(self):
        super().tearDown()
        _reset()

    def assertEmptyRegisters(self):
        self.assertEqual(_data, {'0': None, '1-9': deque([None] * 9, maxlen=9)})


class Test_get_for_paste(RegistersTestCase):

    def test_get_empty(self):
        self.assertEqual(registers_get_for_paste(self.view, '"', unittest.INTERNAL_NORMAL), ([], False))
        self.assertEqual(registers_get_for_paste(self.view, '-', unittest.INTERNAL_NORMAL), ([], False))
        self.assertEqual(registers_get_for_paste(self.view, '0', unittest.INTERNAL_NORMAL), ([], False))
        self.assertEqual(registers_get_for_paste(self.view, '1', unittest.INTERNAL_NORMAL), ([], False))

    def test_get_for_paste_fills_existing_visual_selection(self):
        self.visual('x|fizz|x')
        registers_op_yank(self.view)
        self.visual('x|buzz|x')
        self.assertEqual(registers_get_for_paste(self.view, '"', unittest.VISUAL), (['fizz'], False))
        self.assertEqual(registers_get(self.view, '"'), ['buzz'])
        self.visual('x|fizz|x')
        self.assertEqual(registers_get_for_paste(self.view, '"', unittest.VISUAL), (['buzz'], False))
        self.assertEqual(registers_get(self.view, '"'), ['fizz'])

    def test_get_for_paste_fills_existing_visual_selection_patched_linewise(self):
        self.visual('x|fizz|x')
        registers_op_yank(self.view)
        self.vline('x\n|buzz\n|x')
        self.assertEqual(registers_get_for_paste(self.view, '"', unittest.VISUAL_LINE), (['fizz\n'], False))
        self.assertEqual(registers_get_for_paste(self.view, '"', unittest.VISUAL_LINE), (['buzz\n'], True))
        self.vline('x\n|fizz|x')
        self.assertEqual(registers_get_for_paste(self.view, '"', unittest.VISUAL), (['\nbuzz\n'], True))
        self.assertEqual(registers_get_for_paste(self.view, '"', unittest.VISUAL_LINE), (['fizz\n'], False))


class TestConstants(unittest.TestCase):

    def test_clipboard(self):
        self.assertEqual(_CLIPBOARD, ('+', '*'))
        self.assertEqual(_SELECTION_AND_DROP, ('+', '*', '~'))

    def test_numbers(self):
        self.assertEqual(_NUMBERED, ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'))

    def test_readonly(self):
        self.assertEqual(_READ_ONLY, ('#', '~', '%', ':', '.'))

    def test_special(self):
        self.assertTupleEqual(_SPECIAL, (
            _ALTERNATE_FILE,
            _BLACK_HOLE,
            _CLIPBOARD_PLUS,
            _CLIPBOARD_STAR,
            _CLIPBOARD_TILDA,
            _CURRENT_FILE_NAME,
            _LAST_EXECUTED_COMMAND,
            _LAST_INSERTED_TEXT,
            _LAST_SEARCH_PATTERN,
            _SMALL_DELETE,
            _UNNAMED
        ))

    def test_all(self):
        self.assertSetEqual(set(_ALL), set((
            _SPECIAL +
            _READ_ONLY +
            _SELECTION_AND_DROP +
            _NUMBERED +
            _NAMED
        )))


class TestRegister(RegistersTestCase):

    def test_black_hole_register(self):
        registers_op_change(self.view, register='_')
        registers_op_delete(self.view, register='_')
        registers_op_yank(self.view, register='_')
        self.assertEmptyRegisters()

    def test_set_invalid_register_name_should_not_fill_any_registers(self):
        for register in _READ_ONLY:
            registers_set(self.view, register, ['x'])

        registers_set(self.view, ':', ['x'])
        registers_set(self.view, '.', ['x'])
        registers_set(self.view, '%', ['x'])
        registers_set(self.view, '#', ['x'])
        registers_set(self.view, '/', ['x'])
        registers_set(self.view, '$', ['x'])
        registers_set(self.view, '!', ['x'])
        self.assertEmptyRegisters()

    def test_can_set_get_alpha_register(self):
        registers_set(self.view, 'a', ['x'])
        self.assertEqual(registers_get(self.view, 'a'), ['x'])

    def test_can_set_get_alpha_uppercase_register(self):
        registers_set(self.view, 'B', ['x'])
        self.assertEqual(registers_get(self.view, 'B'), ['x'])
        self.assertEqual(registers_get(self.view, 'b'), ['x'])

    def test_set_get_uppercase_appends_to_register(self):
        registers_set(self.view, 'b', ['x'])
        registers_set(self.view, 'B', ['y'])
        registers_set(self.view, 'B', ['z'])
        self.assertEqual(registers_get(self.view, 'B'), ['xyz'])
        self.assertEqual(registers_get(self.view, 'b'), ['xyz'])

    def test_can_set_get_zero_register(self):
        registers_set(self.view, '0', ['x'])
        self.assertEqual(registers_get(self.view, '0'), ['x'])

    def test_can_set_get_digit_register(self):
        registers_set(self.view, '4', ['x'])
        self.assertEqual(registers_get(self.view, '4'), ['x'])

    def test_can_set_get_unnamed_register(self):
        registers_set(self.view, '"', ['x'])
        self.assertEqual(registers_get(self.view, '"'), ['x'])

    def test_can_set_get_clipboard_star_register(self):
        registers_set(self.view, '*', ['x'])
        self.assertEqual(registers_get(self.view, '*'), ['x'])

    def test_can_set_get_clipboard_plus_register(self):
        registers_set(self.view, '+', ['x'])
        self.assertEqual(registers_get(self.view, '+'), ['x'])

    def test_can_set_get_expression_register(self):
        registers_set(self.view, '=', ['x'])
        self.assertEqual(registers_get(self.view, '='), ['x'])
        set_expression_register(['y'])
        self.assertEqual(registers_get(self.view, '='), ['y'])

    def test_can_set_unanmed_register(self):
        _set_unnamed(["foo"])
        self.assertEqual(registers_get(self.view, _UNNAMED), ["foo"])

    def test_setting_long_register_name_throws_assertion_error(self):
        with self.assertRaisesRegex(ValueError, 'Register names must be 1 char long: name'):
            registers_set(self.view, 'name', 'foo')  # type: ignore

    def test_setting_non_list_value_throws_assertion_error(self):
        with self.assertRaisesRegex(ValueError, 'Register values must be inside a list'):
            registers_set(self.view, 'a', 'foo')  # type: ignore

    def test_register_data_is_always_stored_as_string(self):
        registers_set(self.view, '"', [100])
        self.assertEqual(registers_get(self.view, _UNNAMED), ["100"])

    def test_setting_black_hole_register_does_nothing(self):
        registers_set(self.view, _UNNAMED, ["bar"])
        # In this case it doesn't matter whether we're setting a list or not,
        # because we are discarding the value anyway.
        registers_set(self.view, _BLACK_HOLE, "foo")  # type: ignore
        self.assertEqual(registers_get(self.view, _BLACK_HOLE), None)
        self.assertEqual(registers_get(self.view, _UNNAMED), ["bar"])

    def test_setting_expression_register_doesnt_populate_unnamed_register(self):
        registers_set(self.view, "=", [100])
        self.assertEqual(registers_get(self.view, _EXPRESSION), ["100"])

    def test_can_set_normal_registers(self):
        for name in _NAMED:
            registers_set(self.view, name, [name])

        for number in _NUMBERED:
            registers_set(self.view, number, [number])

        for name in _NAMED:
            self.assertEqual(registers_get(self.view, name), [name])

        for number in _NUMBERED:
            self.assertEqual(registers_get(self.view, number), [number])

    def test_setting_normal_register_sets_unnamed_register_too(self):
        registers_set(self.view, 'a', [100])
        self.assertEqual(registers_get(self.view, _UNNAMED), ['100'])

        registers_set(self.view, '0', [200])
        self.assertEqual(registers_get(self.view, _UNNAMED), ['200'])

    def test_setting_register_sets_clipboard_if_needed(self):
        self.set_setting('use_sys_clipboard', True)
        registers_set(self.view, 'a', [100])
        self.assertEqual(get_clipboard(), '100')

    def test_can_append_to_single_value(self):
        registers_set(self.view, 'a', ['foo'])
        registers_set(self.view, 'A', ['bar'])
        self.assertEqual(registers_get(self.view, 'a'), ['foobar'])

    def test_can_append_to_multiple_balanced_values(self):
        registers_set(self.view, 'a', ['foo', 'bar'])
        registers_set(self.view, 'A', ['fizz', 'buzz'])
        self.assertEqual(registers_get(self.view, 'a'), ['foofizz', 'barbuzz'])

    def test_can_append_to_multiple_values_more_existing_values(self):
        registers_set(self.view, 'a', ['foo', 'bar'])
        registers_set(self.view, 'A', ['fizz'])
        self.assertEqual(registers_get(self.view, 'a'), ['foofizz', 'bar'])

    def test_can_append_to_multiple_values_more_new_values(self):
        registers_set(self.view, 'a', ['foo'])
        registers_set(self.view, 'A', ['fizz', 'buzz'])
        self.assertEqual(registers_get(self.view, 'a'), ['foofizz', 'buzz'])

    def test_appending_sets_default_register(self):
        registers_set(self.view, 'a', ['foo'])
        registers_set(self.view, 'A', ['bar'])
        self.assertEqual(registers_get(self.view, _UNNAMED), ['foobar'])

    def test_append_sets_clipboard_if_needed(self):
        self.set_setting('use_sys_clipboard', True)
        registers_set(self.view, 'a', ['foo'])
        registers_set(self.view, 'A', ['bar'])
        self.assertEqual(get_clipboard(), 'foobar')

    def test_get_default_to_unnamed_register(self):
        registers_set(self.view, '"', ['foo'])
        self.set_setting('use_sys_clipboard', False)
        self.assertEqual(registers_get(self.view, _UNNAMED), ['foo'])

    def test_getting_black_hole_register_returns_none(self):
        self.assertEqual(registers_get(self.view, _BLACK_HOLE), None)

    def test_can_get_file_name_register(self):
        def fn(): return 'fizz'  # noqa: E704
        self.view.file_name = fn
        self.assertEqual(registers_get(self.view, _CURRENT_FILE_NAME), ['fizz'])

    def test_can_get_file_name_register_none(self):
        def fn(): return None  # noqa: E704
        self.view.file_name = fn
        self.assertEqual(registers_get(self.view, _CURRENT_FILE_NAME), None)

    def test_returns_empty_string_if_file_name_not_found_or_error(self):
        self.view.file_name = mock.Mock(side_effect=AttributeError('error'))
        self.assertEqual(registers_get(self.view, _CURRENT_FILE_NAME), None)

    def test_can_get_clipboard_registers(self):
        registers_set(self.view, _CLIPBOARD_STAR, ['foo'])
        self.assertEqual(registers_get(self.view, _CLIPBOARD_STAR), ['foo'])
        self.assertEqual(registers_get(self.view, _CLIPBOARD_PLUS), ['foo'])

        registers_set(self.view, _CLIPBOARD_PLUS, ['bar'])
        self.assertEqual(registers_get(self.view, _CLIPBOARD_STAR), ['bar'])
        self.assertEqual(registers_get(self.view, _CLIPBOARD_PLUS), ['bar'])

    def test_get_sys_clipboard_always_if_requested(self):
        self.set_setting('use_sys_clipboard', True)
        set_clipboard('foo')
        self.assertEqual(registers_get(self.view, _UNNAMED), ['foo'])

    def test_getting_expression_register_clears_expression_register(self):
        registers_set(self.view, _EXPRESSION, ['100'])
        self.set_setting('use_sys_clipboard', False)
        self.assertEqual(registers_get(self.view, _UNNAMED), ['100'])
        self.assertEqual(registers_get(self.view, _EXPRESSION), None)

    def test_can_get_number_register(self):
        registers_set(self.view, '4', ['foo'])
        self.assertEqual(registers_get(self.view, '4'), ['foo'])

    def test_can_get_register_even_if_requesting_it_through_a_capital_letter(self):
        registers_set(self.view, 'a', ['foo'])
        self.assertEqual(registers_get(self.view, 'A'), ['foo'])

    def test_can_get_registers_with_dict_syntax(self):
        registers_set(self.view, 'a', ['foo'])
        self.assertEqual(registers_get(self.view, 'a'), registers_get(self.view, 'a'))

    def test_can_set_registers_with_dict_syntax(self):
        registers_set(self.view, 'a', ['100'])
        self.assertEqual(registers_get(self.view, 'a'), ['100'])

    def test_can_append_to_registe_with_dict_syntax(self):
        registers_set(self.view, 'a', ['100'])
        registers_set(self.view, 'A', ['100'])
        self.assertEqual(registers_get(self.view, 'a'), ['100100'])

    def test_can_convert_to_dict(self):
        registers_set(self.view, 'a', ['100'])
        registers_set(self.view, 'b', ['200'])
        values = {name: registers_get(self.view, name) for name in _ALL}
        values.update({'a': ['100'], 'b': ['200']})
        self.assertEqual(registers_get_all(self.view), values)

    def test_getting_empty_register_returns_none(self):
        self.assertEqual(registers_get(self.view, 'a'), None)

    def test_can_set_small_delete_register(self):
        registers_set(self.view, _SMALL_DELETE, ['foo'])
        self.assertEqual(registers_get(self.view, _SMALL_DELETE), ['foo'])

    def test_can_get_small_delete_register(self):
        registers_set(self.view, _SMALL_DELETE, ['foo'])
        self.assertEqual(registers_get(self.view, _SMALL_DELETE), ['foo'])


class Test_get_selected_text(RegistersTestCase):

    def setUp(self):
        super().setUp()
        self.mock_view = mock.Mock()

    def test_extracts_substrings(self):
        self.mock_view.sel.return_value = [10, 20, 30]
        _get_selected_text(self.mock_view)
        self.assertEqual(self.mock_view.substr.call_count, 3)

    def test_returns_fragments(self):
        self.mock_view.sel.return_value = [10, 20, 30]
        self.mock_view.substr.side_effect = lambda x: x

        rv = _get_selected_text(self.mock_view, new_line_at_eof=False, linewise=False)
        self.assertEqual(rv, [10, 20, 30])

    def test_can_add_new_line_at_eof(self):
        self.mock_view.substr.return_value = "AAA"
        self.mock_view.sel.return_value = [self.Region(10, 10), self.Region(10, 10)]
        self.mock_view.size.return_value = 0

        rv = _get_selected_text(self.mock_view, new_line_at_eof=True, linewise=False)
        self.assertEqual(rv, ["AAA", "AAA\n"])

    def test_doesnt_add_new_line_at_eof_if_not_needed(self):
        self.mock_view.substr.return_value = "AAA\n"
        self.mock_view.sel.return_value = [self.Region(10, 10), self.Region(10, 10)]
        self.mock_view.size.return_value = 0

        rv = _get_selected_text(self.mock_view, new_line_at_eof=True, linewise=False)
        self.assertEqual(rv, ["AAA\n", "AAA\n"])

    def test_doesnt_add_new_line_at_eof_if_not_at_eof(self):
        self.mock_view.substr.return_value = "AAA"
        self.mock_view.sel.return_value = [self.Region(10, 10), self.Region(10, 10)]
        self.mock_view.size.return_value = 100

        rv = _get_selected_text(self.mock_view, new_line_at_eof=True, linewise=False)
        self.assertEqual(rv, ["AAA", "AAA"])

    def test_can_yank_linewise(self):
        self.mock_view.substr.return_value = "AAA"
        self.mock_view.sel.return_value = [self.Region(10, 10), self.Region(10, 10)]

        rv = _get_selected_text(self.mock_view, new_line_at_eof=False, linewise=True)
        self.assertEqual(rv, ["AAA\n", "AAA\n"])

    def test_does_not_yank_linewise_if_non_empty_string_followed_by_new_line(self):
        self.mock_view.substr.return_value = "AAA\n"
        self.mock_view.sel.return_value = [self.Region(10, 10), self.Region(10, 10)]

        rv = _get_selected_text(self.mock_view, new_line_at_eof=False, linewise=True)
        self.assertEqual(rv, ["AAA\n", "AAA\n"])

    def test_yank_linewise_if_empty_string_followed_by_new_line(self):
        self.mock_view.substr.return_value = "\n"
        self.mock_view.sel.return_value = [self.Region(10, 10), self.Region(10, 10)]

        rv = _get_selected_text(self.mock_view, new_line_at_eof=False, linewise=True)
        self.assertEqual(rv, ["\n", "\n"])

    def test_yank_linewise_if_two_trailing_new_lines(self):
        self.mock_view.substr.return_value = "\n\n"
        self.mock_view.sel.return_value = [self.Region(10, 10), self.Region(10, 10)]

        rv = _get_selected_text(self.mock_view, new_line_at_eof=False, linewise=True)
        self.assertEqual(rv, ["\n\n\n", "\n\n\n"])


class Test_op_change(RegistersTestCase):

    def test_op_change(self):
        self.visual('fi|zz bu|zz')
        registers_op_change(self.view)
        self.assertEqual(registers_get(self.view, '"'), ['zz bu'])
        self.assertEqual(registers_get(self.view, '-'), ['zz bu'])
        self.assertEqual(registers_get(self.view, '0'), None)
        self.assertEqual(registers_get(self.view, '1'), None)
        self.assertFalse(_is_register_linewise('"'))
        self.assertFalse(_is_register_linewise('-'))
        self.assertEqual(registers_get_for_paste(self.view, '"', unittest.INTERNAL_NORMAL), (['zz bu'], False))
        self.assertEqual(registers_get_for_paste(self.view, '-', unittest.INTERNAL_NORMAL), (['zz bu'], False))


class Test_op_delete(RegistersTestCase):

    def test_op_delete(self):
        self.visual('fi|zz bu|zz')
        registers_op_delete(self.view)
        self.assertEqual(registers_get(self.view, '"'), ['zz bu'])
        self.assertEqual(registers_get(self.view, '-'), ['zz bu'])
        self.assertEqual(registers_get(self.view, '0'), None)
        self.assertEqual(registers_get(self.view, '1'), None)
        self.assertEqual(registers_get(self.view, '2'), None)
        self.assertEqual(registers_get(self.view, '3'), None)
        self.assertEqual(registers_get(self.view, '4'), None)
        self.assertEqual(registers_get(self.view, '5'), None)
        self.assertEqual(registers_get(self.view, '6'), None)
        self.assertEqual(registers_get(self.view, '7'), None)
        self.assertEqual(registers_get(self.view, '8'), None)
        self.assertEqual(registers_get(self.view, '9'), None)
        self.assertFalse(_is_register_linewise('"'))
        self.assertFalse(_is_register_linewise('-'))
        self.assertEqual(registers_get_for_paste(self.view, '"', unittest.INTERNAL_NORMAL), (['zz bu'], False))
        self.assertEqual(registers_get_for_paste(self.view, '-', unittest.INTERNAL_NORMAL), (['zz bu'], False))

    def test_op_delete_multiline(self):
        self.visual('fi|zz\nbu|zz')
        registers_op_delete(self.view)
        self.assertEqual(registers_get(self.view, '"'), ['zz\nbu'])
        self.assertEqual(registers_get(self.view, '-'), None)
        self.assertEqual(registers_get(self.view, '0'), None)
        self.assertEqual(registers_get(self.view, '1'), ['zz\nbu'])
        self.assertEqual(registers_get(self.view, '2'), None)
        self.assertEqual(registers_get(self.view, '3'), None)
        self.assertEqual(registers_get(self.view, '4'), None)
        self.assertEqual(registers_get(self.view, '5'), None)
        self.assertEqual(registers_get(self.view, '6'), None)
        self.assertEqual(registers_get(self.view, '7'), None)
        self.assertEqual(registers_get(self.view, '8'), None)
        self.assertEqual(registers_get(self.view, '9'), None)
        self.assertFalse(_is_register_linewise('"'))
        self.assertFalse(_is_register_linewise('1'))
        self.assertEqual(registers_get_for_paste(self.view, '"', unittest.INTERNAL_NORMAL), (['zz\nbu'], False))
        self.assertEqual(registers_get_for_paste(self.view, '1', unittest.INTERNAL_NORMAL), (['zz\nbu'], False))

    def test_op_delete_linewise(self):
        self.visual('f|iz|z')
        registers_op_delete(self.view, linewise=True)
        self.assertEqual(registers_get(self.view, '"'), ['iz\n'])
        self.assertEqual(registers_get(self.view, '-'), None)
        self.assertEqual(registers_get(self.view, '0'), None)
        self.assertEqual(registers_get(self.view, '1'), ['iz\n'])
        self.assertTrue(_is_register_linewise('"'))
        self.assertTrue(_is_register_linewise('1'))
        self.assertEqual(registers_get_for_paste(self.view, '"', unittest.INTERNAL_NORMAL), (['iz\n'], True))
        self.assertEqual(registers_get_for_paste(self.view, '1', unittest.INTERNAL_NORMAL), (['iz\n'], True))

    def test_op_delete_into_alpha_register(self):
        self.visual('fi|zz\nbu|zz')
        registers_op_delete(self.view, register='d')
        self.assertEqual(registers_get(self.view, '"'), ['zz\nbu'])
        self.assertEqual(registers_get(self.view, '-'), None)
        self.assertEqual(registers_get(self.view, 'd'), ['zz\nbu'])
        self.assertEqual(registers_get(self.view, '0'), None)
        self.assertEqual(registers_get(self.view, '1'), None)
        self.assertFalse(_is_register_linewise('"'))
        self.assertFalse(_is_register_linewise('d'))
        self.assertEqual(registers_get_for_paste(self.view, '"', unittest.INTERNAL_NORMAL), (['zz\nbu'], False))
        self.assertEqual(registers_get_for_paste(self.view, 'd', unittest.INTERNAL_NORMAL), (['zz\nbu'], False))

    def test_op_delete_into_numbered_register(self):
        self.visual('fi|zz\nbu|zz')
        registers_op_delete(self.view, register='8')
        self.assertEqual(registers_get(self.view, '"'), ['zz\nbu'])
        self.assertEqual(registers_get(self.view, '-'), None)
        self.assertEqual(registers_get(self.view, '8'), ['zz\nbu'])
        self.assertEqual(registers_get(self.view, '0'), None)
        self.assertEqual(registers_get(self.view, '1'), None)
        self.assertFalse(_is_register_linewise('"'))
        self.assertFalse(_is_register_linewise('8'))
        self.assertEqual(registers_get_for_paste(self.view, '"', unittest.INTERNAL_NORMAL), (['zz\nbu'], False))
        self.assertEqual(registers_get_for_paste(self.view, '8', unittest.INTERNAL_NORMAL), (['zz\nbu'], False))

    def test_op_delete_shifts_numbered(self):
        # Run delete operations descending from 15.
        # With each successive deletion or change, Vim shifts the previous
        # contents of register 1 into register 2, 2 into 3, and so forth, losing
        # the previous contents of register 9.
        for i in reversed(range(1, 15)):
            self.visual('a|x\n{}|b'.format(i))
            registers_op_delete(self.view)

        self.assertEqual(registers_get(self.view, '"'), ['x\n1'])
        self.assertEqual(registers_get(self.view, '-'), None)
        self.assertEqual(registers_get(self.view, '0'), None)
        self.assertEqual(registers_get(self.view, '1'), ['x\n1'])
        self.assertEqual(registers_get(self.view, '2'), ['x\n2'])
        self.assertEqual(registers_get(self.view, '3'), ['x\n3'])
        self.assertEqual(registers_get(self.view, '4'), ['x\n4'])
        self.assertEqual(registers_get(self.view, '5'), ['x\n5'])
        self.assertEqual(registers_get(self.view, '6'), ['x\n6'])
        self.assertEqual(registers_get(self.view, '7'), ['x\n7'])
        self.assertEqual(registers_get(self.view, '8'), ['x\n8'])
        self.assertEqual(registers_get(self.view, '9'), ['x\n9'])
        self.assertEqual(len(_data['1-9']), 9)
        self.assertFalse(_is_register_linewise('"'))
        self.assertFalse(_is_register_linewise('8'))
        self.assertEqual(registers_get_for_paste(self.view, '"', unittest.INTERNAL_NORMAL), (['x\n1'], False))
        self.assertEqual(registers_get_for_paste(self.view, '1', unittest.INTERNAL_NORMAL), (['x\n1'], False))
        self.assertEqual(registers_get_for_paste(self.view, '2', unittest.INTERNAL_NORMAL), (['x\n2'], False))
        self.assertEqual(registers_get_for_paste(self.view, '3', unittest.INTERNAL_NORMAL), (['x\n3'], False))


class Test_op_yank(RegistersTestCase):

    def test_op_yank(self):
        self.visual('fi|zz bu|zz')
        registers_op_yank(self.view)
        self.assertEqual(registers_get(self.view, '"'), ['zz bu'])
        self.assertEqual(registers_get(self.view, '-'), None)
        self.assertEqual(registers_get(self.view, '0'), ['zz bu'])
        self.assertEqual(registers_get(self.view, '1'), None)
        self.assertFalse(_is_register_linewise('"'))
        self.assertFalse(_is_register_linewise('1'))
        self.assertEqual(registers_get_for_paste(self.view, '"', unittest.INTERNAL_NORMAL), (['zz bu'], False))
        self.assertEqual(registers_get_for_paste(self.view, '0', unittest.INTERNAL_NORMAL), (['zz bu'], False))

    def test_op_yank_multiline(self):
        self.visual('fi|zz\nbu|zz')
        registers_op_yank(self.view)
        self.assertEqual(registers_get(self.view, '"'), ['zz\nbu'])
        self.assertEqual(registers_get(self.view, '-'), None)
        self.assertEqual(registers_get(self.view, '0'), ['zz\nbu'])
        self.assertEqual(registers_get(self.view, '1'), None)
        self.assertFalse(_is_register_linewise('"'))
        self.assertFalse(_is_register_linewise('0'))
        self.assertEqual(registers_get_for_paste(self.view, '"', unittest.INTERNAL_NORMAL), (['zz\nbu'], False))
        self.assertEqual(registers_get_for_paste(self.view, '0', unittest.INTERNAL_NORMAL), (['zz\nbu'], False))

    def test_op_yank_linewise(self):
        self.visual('fi|zz bu|zz')
        registers_op_yank(self.view, linewise=True)
        self.assertEqual(registers_get(self.view, '"'), ['zz bu\n'])
        self.assertEqual(registers_get(self.view, '-'), None)
        self.assertEqual(registers_get(self.view, '0'), ['zz bu\n'])
        self.assertEqual(registers_get(self.view, '1'), None)
        self.assertTrue(_is_register_linewise('"'))
        self.assertTrue(_is_register_linewise('0'))

    def test_op_yank_linewise_maybe_when_no_newline(self):
        self.visual('fi|zz bu|zz')
        registers_op_yank(self.view, linewise='maybe')
        self.assertEqual(registers_get(self.view, '"'), ['zz bu'])
        self.assertEqual(registers_get(self.view, '-'), None)
        self.assertEqual(registers_get(self.view, '0'), ['zz bu'])
        self.assertEqual(registers_get(self.view, '1'), None)
        self.assertFalse(_is_register_linewise('"'))
        self.assertFalse(_is_register_linewise('0'))

    def test_op_yank_linewise_maybe_when_newline(self):
        self.visual('fi|zz bu\n|zz')
        registers_op_yank(self.view, linewise='maybe')
        self.assertEqual(registers_get(self.view, '"'), ['zz bu\n'])
        self.assertEqual(registers_get(self.view, '-'), None)
        self.assertEqual(registers_get(self.view, '0'), ['zz bu\n'])
        self.assertEqual(registers_get(self.view, '1'), None)
        self.assertTrue(_is_register_linewise('"'))
        self.assertTrue(_is_register_linewise('0'))

    def test_op_yank_into_alpha_register(self):
        self.visual('fi|zzxbu|zz')
        registers_op_yank(self.view, register='x')
        self.assertEqual(registers_get(self.view, '"'), ['zzxbu'])
        self.assertEqual(registers_get(self.view, '-'), None)
        self.assertEqual(registers_get(self.view, 'x'), ['zzxbu'])
        self.assertEqual(registers_get(self.view, '0'), None)
        self.assertEqual(registers_get(self.view, '1'), None)
        self.assertFalse(_is_register_linewise('"'))
        self.assertFalse(_is_register_linewise('x'))

    def test_op_yank_into_alpha_register_linewise(self):
        self.visual('fi\n|zz bu\n|zz')
        registers_op_yank(self.view, register='x', linewise=True)
        self.assertEqual(registers_get(self.view, '"'), ['zz bu\n'])
        self.assertEqual(registers_get(self.view, '-'), None)
        self.assertEqual(registers_get(self.view, 'x'), ['zz bu\n'])
        self.assertEqual(registers_get(self.view, '0'), None)
        self.assertEqual(registers_get(self.view, '1'), None)
        self.assertTrue(_is_register_linewise('"'))
        self.assertTrue(_is_register_linewise('x'))

    def test_op_yank_into_alpha_register_uppercase_append(self):
        self.visual('fizz\n|bu\n|zz')
        registers_op_yank(self.view, register='X')
        self.assertEqual(registers_get(self.view, '"'), ['bu\n'])
        self.assertEqual(registers_get(self.view, '-'), None)
        self.assertEqual(registers_get(self.view, 'x'), ['bu\n'])
        self.assertEqual(registers_get(self.view, '0'), None)
        self.assertEqual(registers_get(self.view, '1'), None)
        self.assertFalse(_is_register_linewise('"'))
        self.assertFalse(_is_register_linewise('x'))
        self.visual('fi\n|zz\n|buzz')
        registers_op_yank(self.view, register='X')
        self.assertEqual(registers_get(self.view, 'x'), ['bu\nzz\n'])
        self.assertFalse(_is_register_linewise('x'))

    def test_op_yank_into_alpha_register_uppercase_linewise_append(self):
        self.visual('fizz\n|bu\n|zz')
        registers_op_yank(self.view, register='X', linewise=True)
        self.assertEqual(registers_get(self.view, '"'), ['bu\n'])
        self.assertEqual(registers_get(self.view, '-'), None)
        self.assertEqual(registers_get(self.view, 'x'), ['bu\n'])
        self.assertEqual(registers_get(self.view, '0'), None)
        self.assertEqual(registers_get(self.view, '1'), None)
        self.assertTrue(_is_register_linewise('"'))
        self.assertTrue(_is_register_linewise('x'))
        self.visual('fi\n|zz\n|buzz')
        registers_op_yank(self.view, register='X', linewise=True)
        self.assertEqual(registers_get(self.view, 'x'), ['bu\nzz\n'])
        self.assertTrue(_is_register_linewise('x'))
        self.assertEqual(registers_get_for_paste(self.view, '"', unittest.INTERNAL_NORMAL), (['bu\nzz\n'], True))
        self.assertEqual(registers_get_for_paste(self.view, 'x', unittest.INTERNAL_NORMAL), (['bu\nzz\n'], True))

    def test_op_yank_into_numbered_register(self):
        self.visual('fi|zz bu|zz')
        registers_op_yank(self.view, register='4')
        self.assertEqual(registers_get(self.view, '"'), ['zz bu'])
        self.assertEqual(registers_get(self.view, '-'), None)
        self.assertEqual(registers_get(self.view, '0'), None)
        self.assertEqual(registers_get(self.view, '1'), None)
        self.assertEqual(registers_get(self.view, '2'), None)
        self.assertEqual(registers_get(self.view, '3'), None)
        self.assertEqual(registers_get(self.view, '4'), ['zz bu'])
        self.assertEqual(registers_get(self.view, '5'), None)
        self.assertEqual(registers_get(self.view, '6'), None)
        self.assertEqual(registers_get(self.view, '7'), None)
        self.assertEqual(registers_get(self.view, '8'), None)
        self.assertEqual(registers_get(self.view, '9'), None)
        self.assertFalse(_is_register_linewise('"'))
        self.assertFalse(_is_register_linewise('4'))

    def test_op_yank_into_linewise_numbered_register(self):
        self.visual('fi\n|zz bu\n|zz')
        registers_op_yank(self.view, register='3', linewise=True)
        self.assertEqual(registers_get(self.view, '"'), ['zz bu\n'])
        self.assertEqual(registers_get(self.view, '-'), None)
        self.assertEqual(registers_get(self.view, '0'), None)
        self.assertEqual(registers_get(self.view, '1'), None)
        self.assertEqual(registers_get(self.view, '2'), None)
        self.assertEqual(registers_get(self.view, '3'), ['zz bu\n'])
        self.assertEqual(registers_get(self.view, '4'), None)
        self.assertEqual(registers_get(self.view, '5'), None)
        self.assertEqual(registers_get(self.view, '6'), None)
        self.assertEqual(registers_get(self.view, '7'), None)
        self.assertEqual(registers_get(self.view, '8'), None)
        self.assertEqual(registers_get(self.view, '9'), None)
        self.assertTrue(_is_register_linewise('"'))
        self.assertTrue(_is_register_linewise('3'))
