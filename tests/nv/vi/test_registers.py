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

from NeoVintageous.nv.vi import registers
from NeoVintageous.nv.vi.registers import _ALL
from NeoVintageous.nv.vi.registers import _ALTERNATE_FILE
from NeoVintageous.nv.vi.registers import _BLACK_HOLE
from NeoVintageous.nv.vi.registers import _CLIPBOARD
from NeoVintageous.nv.vi.registers import _CLIPBOARD_PLUS
from NeoVintageous.nv.vi.registers import _CLIPBOARD_STAR
from NeoVintageous.nv.vi.registers import _CLIPBOARD_TILDA
from NeoVintageous.nv.vi.registers import _CURRENT_FILE_NAME
from NeoVintageous.nv.vi.registers import _EXPRESSION
from NeoVintageous.nv.vi.registers import _is_register_linewise
from NeoVintageous.nv.vi.registers import _LAST_EXECUTED_COMMAND
from NeoVintageous.nv.vi.registers import _LAST_INSERTED_TEXT
from NeoVintageous.nv.vi.registers import _LAST_SEARCH_PATTERN
from NeoVintageous.nv.vi.registers import _NAMED
from NeoVintageous.nv.vi.registers import _NUMBERED
from NeoVintageous.nv.vi.registers import _READ_ONLY
from NeoVintageous.nv.vi.registers import _SELECTION_AND_DROP
from NeoVintageous.nv.vi.registers import _SMALL_DELETE
from NeoVintageous.nv.vi.registers import _SPECIAL
from NeoVintageous.nv.vi.registers import _UNNAMED
from NeoVintageous.nv.vi.registers import Registers
from NeoVintageous.nv.vi.settings import SettingsManager


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


class RegistersTestCase(unittest.ResetRegisters, unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        self.settings().erase('vintage')
        self.settings().erase('vintageous_use_sys_clipboard')
        self.settings().set('vintageous_use_sys_clipboard', False)
        set_clipboard('')
        registers._reset_data()
        self.registers = Registers()
        self.registers.view = self.view
        self.registers.settings = SettingsManager(self.view)

    def tearDown(self):
        super().tearDown()
        registers._reset_data()

    def assertEmptyRegisters(self):
        self.assertEqual(registers._data, {'0': None, '1-9': deque([None] * 9, maxlen=9)})


class TestRegister(RegistersTestCase):

    def test_black_hole_register(self):
        self.registers.op_change(register='_')
        self.registers.op_delete(register='_')
        self.registers.op_yank(register='_')
        self.assertEmptyRegisters()

    def test_set_invalid_register_name_should_not_fill_any_registers(self):
        for register in _READ_ONLY:
            self.registers[register] = ['x']
        self.registers[':'] = ['x']
        self.registers['.'] = ['x']
        self.registers['%'] = ['x']
        self.registers['#'] = ['x']
        self.registers['/'] = ['x']
        self.registers['$'] = ['x']
        self.registers['!'] = ['x']
        self.assertEmptyRegisters()

    def test_can_set_get_alpha_register(self):
        self.registers['a'] = ['x']
        self.assertEqual(self.registers['a'], ['x'])

    def test_can_set_get_alpha_uppercase_register(self):
        self.registers['B'] = ['x']
        self.assertEqual(self.registers['B'], ['x'])
        self.assertEqual(self.registers['b'], ['x'])

    def test_set_get_uppercase_appends_to_register(self):
        self.registers['b'] = ['x']
        self.registers['B'] = ['y']
        self.registers['B'] = ['z']
        self.assertEqual(self.registers['B'], ['xyz'])
        self.assertEqual(self.registers['b'], ['xyz'])

    def test_can_set_get_zero_register(self):
        self.registers['0'] = ['x']
        self.assertEqual(self.registers['0'], ['x'])

    def test_can_set_get_digit_register(self):
        self.registers['4'] = ['x']
        self.assertEqual(self.registers['4'], ['x'])

    def test_can_set_get_unnamed_register(self):
        self.registers['"'] = ['x']
        self.assertEqual(self.registers['"'], ['x'])

    def test_can_set_get_clipboard_star_register(self):
        self.registers['*'] = ['x']
        self.assertEqual(self.registers['*'], ['x'])

    def test_can_set_get_clipboard_plus_register(self):
        self.registers['+'] = ['x']
        self.assertEqual(self.registers['+'], ['x'])

    def test_can_set_get_expression_register(self):
        self.registers['='] = ['x']
        self.assertEqual(self.registers['='], ['x'])
        self.registers.set_expression(['y'])
        self.assertEqual(self.registers['='], ['y'])

    def test_can_initialize_class(self):
        self.assertEqual(self.registers.view, self.view)
        self.assertTrue(getattr(self.registers, 'settings'))

    def test_can_set_unanmed_register(self):
        self.registers._set_unnamed(["foo"])
        self.assertEqual(self.registers[_UNNAMED], ["foo"])

    def test_setting_long_register_name_throws_assertion_error(self):
        with self.assertRaisesRegex(AssertionError, 'names must be 1 char long'):
            self.registers['aa'] = 'foo'

    def test_setting_non_list_value_throws_assertion_error(self):
        with self.assertRaisesRegex(AssertionError, 'values must be inside a list'):
            self.registers['a'] = 'foo'

    def test_register_data_is_always_stored_as_string(self):
        self.registers['"'] = [100]
        self.assertEqual(self.registers[_UNNAMED], ["100"])

    def test_setting_black_hole_register_does_nothing(self):
        self.registers[_UNNAMED] = ["bar"]
        # In this case it doesn't matter whether we're setting a list or not,
        # because we are discarding the value anyway.
        self.registers[_BLACK_HOLE] = "foo"
        self.assertEqual(self.registers[_BLACK_HOLE], None)
        self.assertEqual(self.registers[_UNNAMED], ["bar"])

    def test_setting_expression_register_doesnt_populate_unnamed_register(self):
        self.registers["="] = [100]
        self.assertEqual(self.registers[_EXPRESSION], ["100"])

    def test_can_set_normal_registers(self):
        for name in _NAMED:
            self.registers[name] = [name]

        for number in _NUMBERED:
            self.registers[number] = [number]

        for name in _NAMED:
            self.assertEqual(self.registers[name], [name])

        for number in _NUMBERED:
            self.assertEqual(self.registers[number], [number])

    def test_setting_normal_register_sets_unnamed_register_too(self):
        self.registers['a'] = [100]
        self.assertEqual(self.registers[_UNNAMED], ['100'])

        self.registers['0'] = [200]
        self.assertEqual(self.registers[_UNNAMED], ['200'])

    def test_setting_register_sets_clipboard_if_needed(self):
        self.settings().set('vintageous_use_sys_clipboard', True)
        self.registers['a'] = [100]
        self.assertEqual(get_clipboard(), '100')

    def test_can_append_to_single_value(self):
        self.registers['a'] = ['foo']
        self.registers['A'] = ['bar']
        self.assertEqual(self.registers['a'], ['foobar'])

    def test_can_append_to_multiple_balanced_values(self):
        self.registers['a'] = ['foo', 'bar']
        self.registers['A'] = ['fizz', 'buzz']
        self.assertEqual(self.registers['a'], ['foofizz', 'barbuzz'])

    def test_can_append_to_multiple_values_more_existing_values(self):
        self.registers['a'] = ['foo', 'bar']
        self.registers['A'] = ['fizz']
        self.assertEqual(self.registers['a'], ['foofizz', 'bar'])

    def test_can_append_to_multiple_values_more_new_values(self):
        self.registers['a'] = ['foo']
        self.registers['A'] = ['fizz', 'buzz']
        self.assertEqual(self.registers['a'], ['foofizz', 'buzz'])

    def test_appending_sets_default_register(self):
        self.registers['a'] = ['foo']
        self.registers['A'] = ['bar']
        self.assertEqual(self.registers[_UNNAMED], ['foobar'])

    def test_append_sets_clipboard_if_needed(self):
        self.settings().set('vintageous_use_sys_clipboard', True)
        self.registers['a'] = ['foo']
        self.registers['A'] = ['bar']
        self.assertEqual(get_clipboard(), 'foobar')

    def test_get_default_to_unnamed_register(self):
        self.registers['"'] = ['foo']
        self.view.settings().set('vintageous_use_sys_clipboard', False)
        self.assertEqual(self.registers[_UNNAMED], ['foo'])

    def test_getting_black_hole_register_returns_none(self):
        self.assertEqual(self.registers[_BLACK_HOLE], None)

    def test_can_get_file_name_register(self):
        self.assertEqual(self.registers[_CURRENT_FILE_NAME], [self.view.file_name()])

    def test_returns_empty_string_if_file_name_not_found_or_error(self):
        self.view.file_name = mock.Mock(side_effect=AttributeError('error'))
        self.assertEqual(self.registers[_CURRENT_FILE_NAME], '')

    def test_can_get_clipboard_registers(self):
        self.registers[_CLIPBOARD_STAR] = ['foo']
        self.assertEqual(self.registers[_CLIPBOARD_STAR], ['foo'])
        self.assertEqual(self.registers[_CLIPBOARD_PLUS], ['foo'])

        self.registers[_CLIPBOARD_PLUS] = ['bar']
        self.assertEqual(self.registers[_CLIPBOARD_STAR], ['bar'])
        self.assertEqual(self.registers[_CLIPBOARD_PLUS], ['bar'])

    def test_get_sys_clipboard_always_if_requested(self):
        self.settings().set('vintageous_use_sys_clipboard', True)
        set_clipboard('foo')
        self.assertEqual(self.registers[_UNNAMED], ['foo'])

    def test_getting_expression_register_clears_expression_register(self):
        self.registers[_EXPRESSION] = ['100']
        self.view.settings().set('vintageous_use_sys_clipboard', False)
        self.assertEqual(self.registers[_UNNAMED], ['100'])
        self.assertEqual(self.registers[_EXPRESSION], '')

    def test_can_get_number_register(self):
        self.registers[4] = ['foo']
        self.assertEqual(self.registers['4'], ['foo'])

    def test_can_get_register_even_if_requesting_it_through_a_capital_letter(self):
        self.registers['a'] = ['foo']
        self.assertEqual(self.registers['A'], ['foo'])

    def test_can_get_registers_with_dict_syntax(self):
        self.registers['a'] = ['foo']
        self.assertEqual(self.registers['a'], self.registers['a'])

    def test_can_set_registers_with_dict_syntax(self):
        self.registers['a'] = ['100']
        self.assertEqual(self.registers['a'], ['100'])

    def test_can_append_to_registe_with_dict_syntax(self):
        self.registers['a'] = ['100']
        self.registers['A'] = ['100']
        self.assertEqual(self.registers['a'], ['100100'])

    def test_can_convert_to_dict(self):
        self.registers['a'] = ['100']
        self.registers['b'] = ['200']
        values = {name: self.registers[name] for name in _ALL}
        values.update({'a': ['100'], 'b': ['200']})
        self.assertEqual(self.registers.to_dict(), values)

    def test_getting_empty_register_returns_none(self):
        self.assertEqual(self.registers['a'], None)

    def test_can_set_small_delete_register(self):
        self.registers[_SMALL_DELETE] = ['foo']
        self.assertEqual(self.registers[_SMALL_DELETE], ['foo'])

    def test_can_get_small_delete_register(self):
        self.registers[_SMALL_DELETE] = ['foo']
        self.assertEqual(self.registers[_SMALL_DELETE], ['foo'])


class Test_get_selected_text(RegistersTestCase):

    def setUp(self):
        super().setUp()
        self.registers.view = mock.Mock()

    def test_extracts_substrings(self):
        self.registers.view.sel.return_value = [10, 20, 30]
        self.registers._get_selected_text()
        self.assertEqual(self.registers.view.substr.call_count, 3)

    def test_returns_fragments(self):
        self.registers.view.sel.return_value = [10, 20, 30]
        self.registers.view.substr.side_effect = lambda x: x

        rv = self.registers._get_selected_text(new_line_at_eof=False, linewise=False)
        self.assertEqual(rv, [10, 20, 30])

    def test_can_add_new_line_at_eof(self):
        self.registers.view.substr.return_value = "AAA"
        self.registers.view.sel.return_value = [self.Region(10, 10), self.Region(10, 10)]
        self.registers.view.size.return_value = 0

        rv = self.registers._get_selected_text(new_line_at_eof=True, linewise=False)
        self.assertEqual(rv, ["AAA", "AAA\n"])

    def test_doesnt_add_new_line_at_eof_if_not_needed(self):
        self.registers.view.substr.return_value = "AAA\n"
        self.registers.view.sel.return_value = [self.Region(10, 10), self.Region(10, 10)]
        self.registers.view.size.return_value = 0

        rv = self.registers._get_selected_text(new_line_at_eof=True, linewise=False)
        self.assertEqual(rv, ["AAA\n", "AAA\n"])

    def test_doesnt_add_new_line_at_eof_if_not_at_eof(self):
        self.registers.view.substr.return_value = "AAA"
        self.registers.view.sel.return_value = [self.Region(10, 10), self.Region(10, 10)]
        self.registers.view.size.return_value = 100

        rv = self.registers._get_selected_text(new_line_at_eof=True, linewise=False)
        self.assertEqual(rv, ["AAA", "AAA"])

    def test_can_yank_linewise(self):
        self.registers.view.substr.return_value = "AAA"
        self.registers.view.sel.return_value = [self.Region(10, 10), self.Region(10, 10)]

        rv = self.registers._get_selected_text(new_line_at_eof=False, linewise=True)
        self.assertEqual(rv, ["AAA\n", "AAA\n"])

    def test_does_not_yank_linewise_if_non_empty_string_followed_by_new_line(self):
        self.registers.view.substr.return_value = "AAA\n"
        self.registers.view.sel.return_value = [self.Region(10, 10), self.Region(10, 10)]

        rv = self.registers._get_selected_text(new_line_at_eof=False, linewise=True)
        self.assertEqual(rv, ["AAA\n", "AAA\n"])

    def test_yank_linewise_if_empty_string_followed_by_new_line(self):
        self.registers.view.substr.return_value = "\n"
        self.registers.view.sel.return_value = [self.Region(10, 10), self.Region(10, 10)]

        rv = self.registers._get_selected_text(new_line_at_eof=False, linewise=True)
        self.assertEqual(rv, ["\n", "\n"])

    def test_yank_linewise_if_two_trailing_new_lines(self):
        self.registers.view.substr.return_value = "\n\n"
        self.registers.view.sel.return_value = [self.Region(10, 10), self.Region(10, 10)]

        rv = self.registers._get_selected_text(new_line_at_eof=False, linewise=True)
        self.assertEqual(rv, ["\n\n\n", "\n\n\n"])


class Test_op_change(RegistersTestCase):

    def test_op_yank(self):
        self.visual('fi|zz bu|zz')
        self.registers.op_change()
        self.assertEqual(self.registers['"'], ['zz bu'])
        self.assertEqual(self.registers['-'], ['zz bu'])
        self.assertEqual(self.registers['0'], None)
        self.assertEqual(self.registers['1'], None)


class Test_op_delete(RegistersTestCase):

    def test_op_delete(self):
        self.visual('fi|zz bu|zz')
        self.registers.op_delete()
        self.assertEqual(self.registers['"'], ['zz bu'])
        self.assertEqual(self.registers['-'], ['zz bu'])
        self.assertEqual(self.registers['0'], None)
        self.assertEqual(self.registers['1'], None)
        self.assertEqual(self.registers['2'], None)
        self.assertEqual(self.registers['3'], None)
        self.assertEqual(self.registers['4'], None)
        self.assertEqual(self.registers['5'], None)
        self.assertEqual(self.registers['6'], None)
        self.assertEqual(self.registers['7'], None)
        self.assertEqual(self.registers['8'], None)
        self.assertEqual(self.registers['9'], None)

    def test_op_delete_multiline(self):
        self.visual('fi|zz\nbu|zz')
        self.registers.op_delete()
        self.assertEqual(self.registers['"'], ['zz\nbu'])
        self.assertEqual(self.registers['-'], None)
        self.assertEqual(self.registers['0'], None)
        self.assertEqual(self.registers['1'], ['zz\nbu'])
        self.assertEqual(self.registers['2'], None)
        self.assertEqual(self.registers['3'], None)
        self.assertEqual(self.registers['4'], None)
        self.assertEqual(self.registers['5'], None)
        self.assertEqual(self.registers['6'], None)
        self.assertEqual(self.registers['7'], None)
        self.assertEqual(self.registers['8'], None)
        self.assertEqual(self.registers['9'], None)

    def test_op_delete_linewise(self):
        self.visual('f|iz|z')
        self.registers.op_delete(linewise=True)
        self.assertEqual(self.registers['"'], ['iz\n'])
        self.assertEqual(self.registers['-'], None)
        self.assertEqual(self.registers['0'], None)
        self.assertEqual(self.registers['1'], ['iz\n'])

    def test_op_delete_into_alpha_register(self):
        self.visual('fi|zz\nbu|zz')
        self.registers.op_delete(register='d')
        self.assertEqual(self.registers['"'], ['zz\nbu'])
        self.assertEqual(self.registers['-'], None)
        self.assertEqual(self.registers['d'], ['zz\nbu'])
        self.assertEqual(self.registers['0'], None)
        self.assertEqual(self.registers['1'], None)

    def test_op_delete_into_numbered_register(self):
        self.visual('fi|zz\nbu|zz')
        self.registers.op_delete(register='8')
        self.assertEqual(self.registers['"'], ['zz\nbu'])
        self.assertEqual(self.registers['-'], None)
        self.assertEqual(self.registers['8'], ['zz\nbu'])
        self.assertEqual(self.registers['0'], None)
        self.assertEqual(self.registers['1'], None)

    def test_op_delete_shifts_numbered(self):
        # Run delete operations descending from 15.
        # With each successive deletion or change, Vim shifts the previous
        # contents of register 1 into register 2, 2 into 3, and so forth, losing
        # the previous contents of register 9.
        for i in reversed(range(1, 15)):
            self.visual('a|x\n{}|b'.format(i))
            self.registers.op_delete()

        self.assertEqual(self.registers['"'], ['x\n1'])
        self.assertEqual(self.registers['-'], None)
        self.assertEqual(self.registers['0'], None)
        self.assertEqual(self.registers['1'], ['x\n1'])
        self.assertEqual(self.registers['2'], ['x\n2'])
        self.assertEqual(self.registers['3'], ['x\n3'])
        self.assertEqual(self.registers['4'], ['x\n4'])
        self.assertEqual(self.registers['5'], ['x\n5'])
        self.assertEqual(self.registers['6'], ['x\n6'])
        self.assertEqual(self.registers['7'], ['x\n7'])
        self.assertEqual(self.registers['8'], ['x\n8'])
        self.assertEqual(self.registers['9'], ['x\n9'])
        self.assertEqual(len(registers._data['1-9']), 9)


class Test_op_yank(RegistersTestCase):

    def test_op_yank(self):
        self.visual('fi|zz bu|zz')
        self.registers.op_yank()
        self.assertEqual(self.registers['"'], ['zz bu'])
        self.assertEqual(self.registers['-'], None)
        self.assertEqual(self.registers['0'], ['zz bu'])
        self.assertEqual(self.registers['1'], None)
        self.assertFalse(_is_register_linewise('"'))
        self.assertFalse(_is_register_linewise('-'))
        self.assertFalse(_is_register_linewise('0'))
        self.assertFalse(_is_register_linewise('1'))

    def test_op_yank_multiline(self):
        self.visual('fi|zz\nbu|zz')
        self.registers.op_yank()
        self.assertEqual(self.registers['"'], ['zz\nbu'])
        self.assertEqual(self.registers['-'], None)
        self.assertEqual(self.registers['0'], ['zz\nbu'])
        self.assertEqual(self.registers['1'], None)
        self.assertFalse(_is_register_linewise('"'))
        self.assertFalse(_is_register_linewise('-'))
        self.assertFalse(_is_register_linewise('0'))
        self.assertFalse(_is_register_linewise('1'))

    def test_op_yank_linewise(self):
        self.visual('fi|zz bu|zz')
        self.registers.op_yank(linewise=True)
        self.assertEqual(self.registers['"'], ['zz bu\n'])
        self.assertEqual(self.registers['-'], None)
        self.assertEqual(self.registers['0'], ['zz bu\n'])
        self.assertEqual(self.registers['1'], None)

    def test_op_yank_linewise_maybe_when_no_newline(self):
        self.visual('fi|zz bu|zz')
        self.registers.op_yank(linewise='maybe')
        self.assertEqual(self.registers['"'], ['zz bu'])
        self.assertEqual(self.registers['-'], None)
        self.assertEqual(self.registers['0'], ['zz bu'])
        self.assertEqual(self.registers['1'], None)
        self.assertFalse(_is_register_linewise('"'))
        self.assertFalse(_is_register_linewise('-'))
        self.assertFalse(_is_register_linewise('0'))
        self.assertFalse(_is_register_linewise('1'))

    def test_op_yank_linewise_maybe_when_newline(self):
        self.visual('fi|zz bu\n|zz')
        self.registers.op_yank(linewise='maybe')
        self.assertEqual(self.registers['"'], ['zz bu\n'])
        self.assertEqual(self.registers['-'], None)
        self.assertEqual(self.registers['0'], ['zz bu\n'])
        self.assertEqual(self.registers['1'], None)
        self.assertTrue(_is_register_linewise('"'))
        self.assertTrue(_is_register_linewise('0'))

    def test_op_yank_into_alpha_register(self):
        self.visual('fi|zzxbu|zz')
        self.registers.op_yank(register='x')
        self.assertEqual(self.registers['"'], ['zzxbu'])
        self.assertEqual(self.registers['-'], None)
        self.assertEqual(self.registers['x'], ['zzxbu'])
        self.assertEqual(self.registers['0'], None)
        self.assertEqual(self.registers['1'], None)

    def test_op_yank_into_numbered_register(self):
        self.visual('fi|zz bu|zz')
        self.registers.op_yank(register='4')
        self.assertEqual(self.registers['"'], ['zz bu'])
        self.assertEqual(self.registers['-'], None)
        self.assertEqual(self.registers['0'], None)
        self.assertEqual(self.registers['1'], None)
        self.assertEqual(self.registers['2'], None)
        self.assertEqual(self.registers['3'], None)
        self.assertEqual(self.registers['4'], ['zz bu'])
        self.assertEqual(self.registers['5'], None)
        self.assertEqual(self.registers['6'], None)
        self.assertEqual(self.registers['7'], None)
        self.assertEqual(self.registers['8'], None)
        self.assertEqual(self.registers['9'], None)
