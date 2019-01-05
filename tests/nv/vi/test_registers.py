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

from unittest import mock
import builtins

from sublime import get_clipboard
from sublime import set_clipboard

from NeoVintageous.tests import unittest

from NeoVintageous.nv.state import State
from NeoVintageous.nv.vi import registers


class TestCaseRegistersConstants(unittest.TestCase):

    def test_unnamed_constant_value(self):
        self.assertEqual(registers._UNNAMED, '"')

    def test_small_delete_constant_value(self):
        self.assertEqual(registers._SMALL_DELETE, '-')

    def test_black_hole_constant_value(self):
        self.assertEqual(registers._BLACK_HOLE, '_')

    def test_last_inserted_text_constant_value(self):
        self.assertEqual(registers._LAST_INSERTED_TEXT, '.')

    def test_file_name_constant_value(self):
        self.assertEqual(registers._CURRENT_FILE_NAME, '%')

    def test_alt_file_name_constant_value(self):
        self.assertEqual(registers._ALT_FILE, '#')

    def test_expression_constant_value(self):
        self.assertEqual(registers._EXPRESSION, '=')

    def test_sys_clipboard1_constant_value(self):
        self.assertEqual(registers._CLIPBOARD_STAR, '*')

    def test_sys_clipboard2_constant_value(self):
        self.assertEqual(registers._CLIPBOARD_PLUS, '+')

    def test_sys_clipboard_all_constant_value(self):
        self.assertEqual(registers._CLIPBOARD_ALL, ('*', '+'))

    def test_valid_register_names_constant_value(self):
        self.assertEqual(registers._NAMES, ('a', 'b', 'c', 'd', 'e', 'f', 'g',
                                            'h', 'i', 'j', 'k', 'l', 'm', 'n',
                                            'o', 'p', 'q', 'r', 's', 't', 'u',
                                            'v', 'w', 'x', 'y', 'z'))

    def test_valid_number_names_constant_value(self):
        self.assertEqual(registers._NUMBERS, ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'))

    def test_sys_clipboard_all_constant_value2(self):
        self.assertEqual(registers._SPECIAL,
                         (registers._UNNAMED,
                          registers._SMALL_DELETE,
                          registers._BLACK_HOLE,
                          registers._LAST_INSERTED_TEXT,
                          registers._LAST_EXECUTED_COMMAND,
                          registers._LAST_SEARCH_PATTERN,
                          registers._CURRENT_FILE_NAME,
                          registers._ALT_FILE,
                          registers._CLIPBOARD_STAR,
                          registers._CLIPBOARD_PLUS,
                          registers._CLIPBOARD_TILDA,
                          ))

    def test_all_constant_value(self):
        self.assertEqual(registers._ALL,
                         (registers._SPECIAL +
                          registers._NUMBERS +
                          registers._NAMES))


class TestCaseRegisters(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        set_clipboard('')
        registers._data = registers._init_register_data()
        self.view.settings().erase('vintage')
        self.view.settings().erase('vintageous_use_sys_clipboard')
        self.regs = State(self.view).registers

    def tearDown(self):
        super().tearDown()
        registers._data = registers._init_register_data()

    def test_can_initialize_class(self):
        self.assertEqual(self.regs.view, self.view)
        self.assertTrue(getattr(self.regs, 'settings'))

    def test_can_set_unanmed_register(self):
        self.regs._set_default_register(["foo"])
        self.assertEqual(registers._data[registers._UNNAMED], ["foo"])

    def test_setting_long_register_name_throws_assertion_error(self):
        with self.assertRaisesRegex(AssertionError, 'names must be 1 char long'):
            self.regs.set('aa', 'foo')

    def test_setting_non_list_value_throws_assertion_error(self):
        with self.assertRaisesRegex(AssertionError, 'values must be inside a list'):
            self.regs.set('a', 'foo')

    def test_register_data_is_always_stored_as_string(self):
        self.regs.set('"', [100])
        self.assertEqual(registers._data[registers._UNNAMED], ["100"])

    def test_setting_black_hole_register_does_nothing(self):
        registers._data[registers._UNNAMED] = ["bar"]
        # In this case it doesn't matter whether we're setting a list or not,
        # because we are discarding the value anyway.
        self.regs.set(registers._BLACK_HOLE, "foo")
        self.assertTrue(registers._BLACK_HOLE not in registers._data)
        self.assertTrue(registers._data[registers._UNNAMED], ["bar"])

    def test_setting_expression_register_doesnt_populate_unnamed_register(self):
        self.regs.set("=", [100])
        self.assertTrue(registers._UNNAMED not in registers._data)
        self.assertEqual(registers._data[registers._EXPRESSION], ["100"])

    def test_can_set_normal_registers(self):
        for name in registers._NAMES:
            self.regs.set(name, [name])

        for number in registers._NUMBERS:
            self.regs.set(number, [number])

        for name in registers._NAMES:
            self.assertEqual(registers._data[name], [name])

        for number in registers._NUMBERS:
            self.assertEqual(registers._data[number], [number])

    def test_setting_normal_register_sets_unnamed_register_too(self):
        self.regs.set('a', [100])
        self.assertEqual(registers._data[registers._UNNAMED], ['100'])

        self.regs.set('0', [200])
        self.assertEqual(registers._data[registers._UNNAMED], ['200'])

    def test_setting_register_sets_clipboard_if_needed(self):
        self.settings().set('vintageous_use_sys_clipboard', True)
        self.regs.set('a', [100])
        self.assertEqual(get_clipboard(), '100')

    def test_can_append_to_single_value(self):
        self.regs.set('a', ['foo'])
        self.regs.append_to('A', ['bar'])
        self.assertEqual(registers._data['a'], ['foobar'])

    def test_can_append_to_multiple_balanced_values(self):
        self.regs.set('a', ['foo', 'bar'])
        self.regs.append_to('A', ['fizz', 'buzz'])
        self.assertEqual(registers._data['a'], ['foofizz', 'barbuzz'])

    def test_can_append_to_multiple_values_more_existing_values(self):
        self.regs.set('a', ['foo', 'bar'])
        self.regs.append_to('A', ['fizz'])
        self.assertEqual(registers._data['a'], ['foofizz', 'bar'])

    def test_can_append_to_multiple_values_more_new_values(self):
        self.regs.set('a', ['foo'])
        self.regs.append_to('A', ['fizz', 'buzz'])
        self.assertEqual(registers._data['a'], ['foofizz', 'buzz'])

    def test_appending_sets_default_register(self):
        self.regs.set('a', ['foo'])
        self.regs.append_to('A', ['bar'])
        self.assertEqual(registers._data[registers._UNNAMED], ['foobar'])

    def test_append_sets_clipboard_if_needed(self):
        self.settings().set('vintageous_use_sys_clipboard', True)
        self.regs.set('a', ['foo'])
        self.regs.append_to('A', ['bar'])
        self.assertEqual(get_clipboard(), 'foobar')

    def test_get_default_to_unnamed_register(self):
        registers._data['"'] = ['foo']
        self.view.settings().set('vintageous_use_sys_clipboard', False)
        self.assertEqual(self.regs.get(), ['foo'])

    def test_getting_black_hole_register_returns_none(self):
        self.assertEqual(self.regs.get(registers._BLACK_HOLE), None)

    def test_can_get_file_name_register(self):
        self.assertEqual(self.regs.get(registers._CURRENT_FILE_NAME), [self.view.file_name()])

    def test_can_get_clipboard_registers(self):
        self.regs.set(registers._CLIPBOARD_STAR, ['foo'])
        self.assertEqual(self.regs.get(registers._CLIPBOARD_STAR), ['foo'])
        self.assertEqual(self.regs.get(registers._CLIPBOARD_PLUS), ['foo'])

        self.regs.set(registers._CLIPBOARD_PLUS, ['bar'])
        self.assertEqual(self.regs.get(registers._CLIPBOARD_STAR), ['bar'])
        self.assertEqual(self.regs.get(registers._CLIPBOARD_PLUS), ['bar'])

    def test_get_sys_clipboard_always_if_requested(self):
        self.settings().set('vintageous_use_sys_clipboard', True)
        set_clipboard('foo')
        self.assertEqual(self.regs.get(), ['foo'])

    def test_getting_expression_register_clears_expression_register(self):
        registers._data[registers._EXPRESSION] = ['100']
        self.view.settings().set('vintageous_use_sys_clipboard', False)
        self.assertEqual(self.regs.get(), ['100'])
        self.assertEqual(registers._data[registers._EXPRESSION], '')

    def test_can_get_number_register(self):
        registers._data['1-9'][4] = ['foo']
        self.assertEqual(self.regs.get('5'), ['foo'])

    def test_can_get_register_even_if_requesting_it_through_a_capital_letter(self):
        registers._data['a'] = ['foo']
        self.assertEqual(self.regs.get('A'), ['foo'])

    def test_can_get_registers_with_dict_syntax(self):
        registers._data['a'] = ['foo']
        self.assertEqual(self.regs.get('a'), self.regs['a'])

    def test_can_set_registers_with_dict_syntax(self):
        self.regs['a'] = ['100']
        self.assertEqual(self.regs['a'], ['100'])

    def test_can_append_to_registe_with_dict_syntax(self):
        self.regs['a'] = ['100']
        self.regs['A'] = ['100']
        self.assertEqual(self.regs['a'], ['100100'])

    def test_can_convert_to_dict(self):
        self.regs['a'] = ['100']
        self.regs['b'] = ['200']
        values = {name: self.regs.get(name) for name in registers._ALL}
        values.update({'a': ['100'], 'b': ['200']})
        self.assertEqual(self.regs.to_dict(), values)

    def test_getting_empty_register_returns_none(self):
        self.assertEqual(self.regs.get('a'), None)

    def test_can_set_small_delete_register(self):
        self.regs[registers._SMALL_DELETE] = ['foo']
        self.assertEqual(registers._data[registers._SMALL_DELETE], ['foo'])

    def test_can_get_small_delete_register(self):
        registers._data[registers._SMALL_DELETE] = ['foo']
        self.assertEqual(self.regs.get(registers._SMALL_DELETE), ['foo'])


class Test_get_selected_text(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        set_clipboard('')
        registers._data = registers._init_register_data()
        self.view.settings().erase('vintage')
        self.view.settings().erase('vintageous_use_sys_clipboard')
        self.regs = State(self.view).registers
        self.regs.view = mock.Mock()

    def tearDown(self):
        super().tearDown()
        registers._data = registers._init_register_data()

    def test_extracts_substrings(self):
        self.regs.view.sel.return_value = [10, 20, 30]
        self.regs._get_selected_text()
        self.assertEqual(self.regs.view.substr.call_count, 3)

    def test_returns_fragments(self):
        self.regs.view.sel.return_value = [10, 20, 30]
        self.regs.view.substr.side_effect = lambda x: x

        rv = self.regs._get_selected_text(new_line_at_eof=False, linewise=False)
        self.assertEqual(rv, [10, 20, 30])

    def test_can_add_new_line_at_eof(self):
        self.regs.view.substr.return_value = "AAA"
        self.regs.view.sel.return_value = [self.Region(10, 10), self.Region(10, 10)]
        self.regs.view.size.return_value = 0

        rv = self.regs._get_selected_text(new_line_at_eof=True, linewise=False)
        self.assertEqual(rv, ["AAA", "AAA\n"])

    def test_doesnt_add_new_line_at_eof_if_not_needed(self):
        self.regs.view.substr.return_value = "AAA\n"
        self.regs.view.sel.return_value = [self.Region(10, 10), self.Region(10, 10)]
        self.regs.view.size.return_value = 0

        rv = self.regs._get_selected_text(new_line_at_eof=True, linewise=False)
        self.assertEqual(rv, ["AAA\n", "AAA\n"])

    def test_doesnt_add_new_line_at_eof_if_not_at_eof(self):
        self.regs.view.substr.return_value = "AAA"
        self.regs.view.sel.return_value = [self.Region(10, 10), self.Region(10, 10)]
        self.regs.view.size.return_value = 100

        rv = self.regs._get_selected_text(new_line_at_eof=True, linewise=False)
        self.assertEqual(rv, ["AAA", "AAA"])

    def test_can_yank_linewise(self):
        self.regs.view.substr.return_value = "AAA"
        self.regs.view.sel.return_value = [self.Region(10, 10), self.Region(10, 10)]

        rv = self.regs._get_selected_text(new_line_at_eof=False, linewise=True)
        self.assertEqual(rv, ["AAA\n", "AAA\n"])

    def test_does_not_yank_linewise_if_non_empty_string_followed_by_new_line(self):
        self.regs.view.substr.return_value = "AAA\n"
        self.regs.view.sel.return_value = [self.Region(10, 10), self.Region(10, 10)]

        rv = self.regs._get_selected_text(new_line_at_eof=False, linewise=True)
        self.assertEqual(rv, ["AAA\n", "AAA\n"])

    def test_yank_linewise_if_empty_string_followed_by_new_line(self):
        self.regs.view.substr.return_value = "\n"
        self.regs.view.sel.return_value = [self.Region(10, 10), self.Region(10, 10)]

        rv = self.regs._get_selected_text(new_line_at_eof=False, linewise=True)
        self.assertEqual(rv, ["\n", "\n"])

    def test_yank_linewise_if_two_trailing_new_lines(self):
        self.regs.view.substr.return_value = "\n\n"
        self.regs.view.sel.return_value = [self.Region(10, 10), self.Region(10, 10)]

        rv = self.regs._get_selected_text(new_line_at_eof=False, linewise=True)
        self.assertEqual(rv, ["\n\n\n", "\n\n\n"])


class Test_yank(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        set_clipboard('')
        registers._data = registers._init_register_data()
        self.view.settings().erase('vintage')
        self.view.settings().erase('vintageous_use_sys_clipboard')
        self.regs = State(self.view).registers
        self.regs.view = mock.Mock()

    def tearDown(self):
        super().tearDown()
        registers._data = registers._init_register_data()

    def test_yank_to_black_hole_register(self):
        self.regs.op_delete(register='_')
        self.assertEqual(registers._data, {
            '1-9': [None] * 9,
            '0': None,
        })

    def test_yanks_to_unnamed_register_if_no_register_name_provided(self):
        with mock.patch.object(self.regs, '_get_selected_text') as gst:
            gst.return_value = ['foo']
            self.regs.op_yank(linewise=True, register=None)
            self.assertEqual(registers._data, {
                '"': ['foo'],
                '0': ['foo'],
                '1-9': [None] * 9,
            })

    def test_yanks_to_registers(self):
        with mock.patch.object(self.regs, '_get_selected_text') as gst:
            gst.return_value = ['foo']
            self.regs.op_yank(register='a')
            self.assertEqual(registers._data, {
                '"': ['foo'],
                'a': ['foo'],
                '0': None,
                '1-9': [None] * 9,
            })

    def test_can_populate_small_delete_register(self):
        with mock.patch.object(builtins, 'all') as a, mock.patch.object(self.regs, '_get_selected_text') as gst:
            gst.return_value = ['foo']
            self.regs.view.sel.return_value = range(1)
            a.return_value = True
            self.regs.op_delete()
            self.assertEqual(registers._data, {
                '"': ['foo'],
                '-': ['foo'],
                '0': None,
                '1-9': [None] * 9})
