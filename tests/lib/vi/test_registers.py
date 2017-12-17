from unittest import mock
import builtins

import sublime

from NeoVintageous.tests import unittest

from NeoVintageous.lib.state import State
from NeoVintageous.lib.vi import registers


class TestCaseRegistersConstants(unittest.TestCase):

    def test_unnamed_constant_value(self):
        self.assertEqual(registers.REG_UNNAMED, '"')

    def test_small_delete_constant_value(self):
        self.assertEqual(registers.REG_SMALL_DELETE, '-')

    def test_black_hole_constant_value(self):
        self.assertEqual(registers.REG_BLACK_HOLE, '_')

    def test_last_inserted_text_constant_value(self):
        self.assertEqual(registers.REG_LAST_INSERTED_TEXT, '.')

    def test_file_name_constant_value(self):
        self.assertEqual(registers.REG_FILE_NAME, '%')

    def test_alt_file_name_constant_value(self):
        self.assertEqual(registers.REG_ALT_FILE_NAME, '#')

    def test_expression_constant_value(self):
        self.assertEqual(registers.REG_EXPRESSION, '=')

    def test_sys_clipboard1_constant_value(self):
        self.assertEqual(registers.REG_SYS_CLIPBOARD_1, '*')

    def test_sys_clipboard2_constant_value(self):
        self.assertEqual(registers.REG_SYS_CLIPBOARD_2, '+')

    def test_sys_clipboard_all_constant_value(self):
        self.assertEqual(registers.REG_SYS_CLIPBOARD_ALL,
                         (registers.REG_SYS_CLIPBOARD_1,
                          registers.REG_SYS_CLIPBOARD_2,))

    def test_valid_register_names_constant_value(self):
        names = tuple("{0}".format(c) for c in "abcdefghijklmnopqrstuvwxyz")
        self.assertEqual(registers.REG_VALID_NAMES, names)

    def test_valid_number_names_constant_value(self):
        names = tuple("{0}".format(c) for c in "0123456789")
        self.assertEqual(registers.REG_VALID_NUMBERS, names)

    def test_sys_clipboard_all_constant_value2(self):
        self.assertEqual(registers.REG_SPECIAL,
                         (registers.REG_UNNAMED,
                          registers.REG_SMALL_DELETE,
                          registers.REG_BLACK_HOLE,
                          registers.REG_LAST_INSERTED_TEXT,
                          registers.REG_FILE_NAME,
                          registers.REG_ALT_FILE_NAME,
                          registers.REG_SYS_CLIPBOARD_1,
                          registers.REG_SYS_CLIPBOARD_2,))

    def test_all_constant_value(self):
        self.assertEqual(registers.REG_ALL,
                         (registers.REG_SPECIAL +
                          registers.REG_VALID_NUMBERS +
                          registers.REG_VALID_NAMES))


class TestCaseRegisters(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        sublime.set_clipboard('')
        registers._REGISTER_DATA = registers.init_register_data()
        self.view.settings().erase('vintage')
        self.view.settings().erase('vintageous_use_sys_clipboard')
        # self.regs = Registers(view=self.view, settings=SettingsManager(view=self.view))
        self.regs = State(self.view).registers

    def tearDown(self):
        super().tearDown()
        registers._REGISTER_DATA = registers.init_register_data()

    def test_can_initialize_class(self):
        self.assertEqual(self.regs.view, self.view)
        self.assertTrue(getattr(self.regs, 'settings'))

    def test_can_set_unanmed_register(self):
        self.regs._set_default_register(["foo"])
        self.assertEqual(registers._REGISTER_DATA[registers.REG_UNNAMED],
                         ["foo"])

    def test_setting_long_register_name_throws_assertion_error(self):
        self.assertRaises(AssertionError, self.regs.set, "aa", "foo")

    def test_setting_non_list_value_throws_assertion_error(self):
        self.assertRaises(AssertionError, self.regs.set, "a", "foo")

    def test_register_data_is_always_stored_as_string(self):
        self.regs.set('"', [100])
        self.assertEqual(registers._REGISTER_DATA[registers.REG_UNNAMED],
                         ["100"])

    def test_setting_black_hole_register_does_nothing(self):
        registers._REGISTER_DATA[registers.REG_UNNAMED] = ["bar"]
        # In this case it doesn't matter whether we're setting a list or not,
        # because we are discarding the value anyway.
        self.regs.set(registers.REG_BLACK_HOLE, "foo")
        self.assertTrue(registers.REG_BLACK_HOLE not in registers._REGISTER_DATA)
        self.assertTrue(registers._REGISTER_DATA[registers.REG_UNNAMED], ["bar"])

    def test_setting_expression_register_doesnt_populate_unnamed_register(self):
        self.regs.set("=", [100])
        self.assertTrue(registers.REG_UNNAMED not in registers._REGISTER_DATA)
        self.assertEqual(registers._REGISTER_DATA[registers.REG_EXPRESSION], ["100"])

    def test_can_set_normal_registers(self):
        for name in registers.REG_VALID_NAMES:
            self.regs.set(name, [name])

        for number in registers.REG_VALID_NUMBERS:
            self.regs.set(number, [number])

        for name in registers.REG_VALID_NAMES:
            self.assertEqual(registers._REGISTER_DATA[name], [name])

        for number in registers.REG_VALID_NUMBERS:
            self.assertEqual(registers._REGISTER_DATA[number], [number])

    def test_setting_normal_register_sets_unnamed_register_too(self):
        self.regs.set('a', [100])
        self.assertEqual(registers._REGISTER_DATA[registers.REG_UNNAMED], ['100'])

        self.regs.set('0', [200])
        self.assertEqual(registers._REGISTER_DATA[registers.REG_UNNAMED], ['200'])

    def test_setting_register_sets_clipboard_if_needed(self):
        self.regs.settings.view['vintageous_use_sys_clipboard'] = True
        self.regs.set('a', [100])
        self.assertEqual(sublime.get_clipboard(), '100')

    def test_can_append_to_single_value(self):
        self.regs.set('a', ['foo'])
        self.regs.append_to('A', ['bar'])
        self.assertEqual(registers._REGISTER_DATA['a'], ['foobar'])

    def test_can_append_to_multiple_balanced_values(self):
        self.regs.set('a', ['foo', 'bar'])
        self.regs.append_to('A', ['fizz', 'buzz'])
        self.assertEqual(registers._REGISTER_DATA['a'], ['foofizz', 'barbuzz'])

    def test_can_append_to_multiple_values_more_existing_values(self):
        self.regs.set('a', ['foo', 'bar'])
        self.regs.append_to('A', ['fizz'])
        self.assertEqual(registers._REGISTER_DATA['a'], ['foofizz', 'bar'])

    def test_can_append_to_multiple_values_more_new_values(self):
        self.regs.set('a', ['foo'])
        self.regs.append_to('A', ['fizz', 'buzz'])
        self.assertEqual(registers._REGISTER_DATA['a'], ['foofizz', 'buzz'])

    def test_appending_sets_default_register(self):
        self.regs.set('a', ['foo'])
        self.regs.append_to('A', ['bar'])
        self.assertEqual(registers._REGISTER_DATA[registers.REG_UNNAMED],
                         ['foobar'])

    def test_append_sets_clipboard_if_needed(self):
        self.regs.settings.view['vintageous_use_sys_clipboard'] = True
        self.regs.set('a', ['foo'])
        self.regs.append_to('A', ['bar'])
        self.assertEqual(sublime.get_clipboard(), 'foobar')

    def test_get_default_to_unnamed_register(self):
        registers._REGISTER_DATA['"'] = ['foo']
        self.view.settings().set('vintageous_use_sys_clipboard', False)
        self.assertEqual(self.regs.get(), ['foo'])

    def test_getting_black_hole_register_returns_none(self):
        self.assertEqual(self.regs.get(registers.REG_BLACK_HOLE), None)

    def test_can_get_file_name_register(self):
        fname = self.regs.get(registers.REG_FILE_NAME)
        self.assertEqual(fname, [self.view.file_name()])

    def test_can_get_clipboard_registers(self):
        self.regs.set(registers.REG_SYS_CLIPBOARD_1, ['foo'])
        self.assertEqual(self.regs.get(registers.REG_SYS_CLIPBOARD_1), ['foo'])
        self.assertEqual(self.regs.get(registers.REG_SYS_CLIPBOARD_2), ['foo'])

        self.regs.set(registers.REG_SYS_CLIPBOARD_2, ['bar'])
        self.assertEqual(self.regs.get(registers.REG_SYS_CLIPBOARD_1), ['bar'])
        self.assertEqual(self.regs.get(registers.REG_SYS_CLIPBOARD_2), ['bar'])

    def test_get_sys_clipboard_always_if_requested(self):
        self.regs.settings.view['vintageous_use_sys_clipboard'] = True
        sublime.set_clipboard('foo')
        self.assertEqual(self.regs.get(), ['foo'])

    def test_getting_expression_register_clears_expression_register(self):
        registers._REGISTER_DATA[registers.REG_EXPRESSION] = ['100']
        self.view.settings().set('vintageous_use_sys_clipboard', False)
        self.assertEqual(self.regs.get(), ['100'])
        self.assertEqual(registers._REGISTER_DATA[registers.REG_EXPRESSION], '')

    def test_can_get_number_register(self):
        registers._REGISTER_DATA['1-9'][4] = ['foo']
        self.assertEqual(self.regs.get('5'), ['foo'])

    def test_can_get_register_even_if_requesting_it_through_a_capital_letter(self):
        registers._REGISTER_DATA['a'] = ['foo']
        self.assertEqual(self.regs.get('A'), ['foo'])

    def test_can_get_registers_with_dict_syntax(self):
        registers._REGISTER_DATA['a'] = ['foo']
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
        values = {name: self.regs.get(name) for name in registers.REG_ALL}
        values.update({'a': ['100'], 'b': ['200']})
        self.assertEqual(self.regs.to_dict(), values)

    def test_getting_empty_register_returns_none(self):
        self.assertEqual(self.regs.get('a'), None)

    def test_can_set_small_delete_register(self):
        self.regs[registers.REG_SMALL_DELETE] = ['foo']
        self.assertEqual(registers._REGISTER_DATA[registers.REG_SMALL_DELETE], ['foo'])

    def test_can_get_small_delete_register(self):
        registers._REGISTER_DATA[registers.REG_SMALL_DELETE] = ['foo']
        self.assertEqual(self.regs.get(registers.REG_SMALL_DELETE), ['foo'])


class Test_get_selected_text(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        sublime.set_clipboard('')
        registers._REGISTER_DATA = registers.init_register_data()
        self.view.settings().erase('vintage')
        self.view.settings().erase('vintageous_use_sys_clipboard')
        self.regs = State(self.view).registers
        self.regs.view = mock.Mock()

    def tearDown(self):
        super().tearDown()
        registers._REGISTER_DATA = registers.init_register_data()

    def test_extracts_substrings(self):
        self.regs.view.sel.return_value = [10, 20, 30]

        class vi_cmd_data:
            _synthetize_new_line_at_eof = False
            _yanks_linewise = False

        self.regs.get_selected_text(vi_cmd_data)
        self.assertEqual(self.regs.view.substr.call_count, 3)

    def test_returns_fragments(self):
        self.regs.view.sel.return_value = [10, 20, 30]
        self.regs.view.substr.side_effect = lambda x: x

        class vi_cmd_data:
            _synthetize_new_line_at_eof = False
            _yanks_linewise = False

        rv = self.regs.get_selected_text(vi_cmd_data)
        self.assertEqual(rv, [10, 20, 30])

    def test_can_synthetize_new_line_at_eof(self):
        self.regs.view.substr.return_value = "AAA"
        self.regs.view.sel.return_value = [sublime.Region(10, 10), sublime.Region(10, 10)]
        self.regs.view.size.return_value = 0

        class vi_cmd_data:
            _synthetize_new_line_at_eof = True
            _yanks_linewise = False

        rv = self.regs.get_selected_text(vi_cmd_data)
        self.assertEqual(rv, ["AAA", "AAA\n"])

    def test_doesnt_synthetize_new_line_at_eof_if_not_needed(self):
        self.regs.view.substr.return_value = "AAA\n"
        self.regs.view.sel.return_value = [sublime.Region(10, 10), sublime.Region(10, 10)]
        self.regs.view.size.return_value = 0

        class vi_cmd_data:
            _synthetize_new_line_at_eof = True
            _yanks_linewise = False

        rv = self.regs.get_selected_text(vi_cmd_data)
        self.assertEqual(rv, ["AAA\n", "AAA\n"])

    def test_doesnt_synthetize_new_line_at_eof_if_not_at_eof(self):
        self.regs.view.substr.return_value = "AAA"
        self.regs.view.sel.return_value = [sublime.Region(10, 10), sublime.Region(10, 10)]
        self.regs.view.size.return_value = 100

        class vi_cmd_data:
            _synthetize_new_line_at_eof = True
            _yanks_linewise = False

        rv = self.regs.get_selected_text(vi_cmd_data)
        self.assertEqual(rv, ["AAA", "AAA"])

    def test_can_yank_linewise(self):
        self.regs.view.substr.return_value = "AAA"
        self.regs.view.sel.return_value = [sublime.Region(10, 10), sublime.Region(10, 10)]

        class vi_cmd_data:
            _synthetize_new_line_at_eof = False
            _yanks_linewise = True

        rv = self.regs.get_selected_text(vi_cmd_data)
        self.assertEqual(rv, ["AAA\n", "AAA\n"])

    def test_does_not_yank_linewise_if_non_empty_string_followed_by_new_line(self):
        self.regs.view.substr.return_value = "AAA\n"
        self.regs.view.sel.return_value = [sublime.Region(10, 10), sublime.Region(10, 10)]

        class vi_cmd_data:
            _synthetize_new_line_at_eof = False
            _yanks_linewise = True

        rv = self.regs.get_selected_text(vi_cmd_data)
        self.assertEqual(rv, ["AAA\n", "AAA\n"])

    def test_yank_linewise_if_empty_string_followed_by_new_line(self):
        self.regs.view.substr.return_value = "\n"
        self.regs.view.sel.return_value = [sublime.Region(10, 10), sublime.Region(10, 10)]

        class vi_cmd_data:
            _synthetize_new_line_at_eof = False
            _yanks_linewise = True

        rv = self.regs.get_selected_text(vi_cmd_data)
        self.assertEqual(rv, ["\n", "\n"])

    def test_yank_linewise_if_two_trailing_new_lines(self):
        self.regs.view.substr.return_value = "\n\n"
        self.regs.view.sel.return_value = [sublime.Region(10, 10), sublime.Region(10, 10)]

        class vi_cmd_data:
            _synthetize_new_line_at_eof = False
            _yanks_linewise = True

        rv = self.regs.get_selected_text(vi_cmd_data)
        self.assertEqual(rv, ["\n\n\n", "\n\n\n"])


class Test_yank(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        sublime.set_clipboard('')
        registers._REGISTER_DATA = registers.init_register_data()
        self.view.settings().erase('vintage')
        self.view.settings().erase('vintageous_use_sys_clipboard')
        self.regs = State(self.view).registers
        self.regs.view = mock.Mock()

    def tearDown(self):
        super().tearDown()
        registers._REGISTER_DATA = registers.init_register_data()

    def test_dont_yank_if_we_dont_have_to(self):
        class vi_cmd_data:
            _can_yank = False
            _populates_small_delete_register = False

        self.regs.yank(vi_cmd_data)
        self.assertEqual(registers._REGISTER_DATA, {
            '1-9': [None] * 9,
            '0': None,
        })

    def test_yanks_to_unnamed_register_if_no_register_name_provided(self):
        class vi_cmd_data:
            _can_yank = True
            _synthetize_new_line_at_eof = False
            _yanks_linewise = True
            register = None
            _populates_small_delete_register = False

        with mock.patch.object(self.regs, 'get_selected_text') as gst:
            gst.return_value = ['foo']
            self.regs.yank(vi_cmd_data)
            self.assertEqual(registers._REGISTER_DATA, {
                '"': ['foo'],
                '0': ['foo'],
                '1-9': [None] * 9,
            })

    def test_yanks_to_registers(self):
        class vi_cmd_data:
            _can_yank = True
            _populates_small_delete_register = False

        with mock.patch.object(self.regs, 'get_selected_text') as gst:
            gst.return_value = ['foo']
            self.regs.yank(vi_cmd_data, register='a')
            self.assertEqual(registers._REGISTER_DATA, {
                '"': ['foo'],
                'a': ['foo'],
                '0': None,
                '1-9': [None] * 9,
            })

    def test_can_populate_small_delete_register(self):
        class vi_cmd_data:
            _can_yank = True
            _populates_small_delete_register = True

        with mock.patch.object(builtins, 'all') as a, mock.patch.object(self.regs, 'get_selected_text') as gst:
            gst.return_value = ['foo']
            self.regs.view.sel.return_value = range(1)
            a.return_value = True
            self.regs.yank(vi_cmd_data)
            self.assertEqual(registers._REGISTER_DATA, {
                '"': ['foo'],
                '-': ['foo'],
                '0': ['foo'],
                '1-9': [None] * 9})

    def test_does_not_populate_small_delete_register_if_we_should_not(self):
        class vi_cmd_data:
            _can_yank = False
            _populates_small_delete_register = False

        with mock.patch.object(builtins, 'all') as a, mock.patch.object(self.regs, 'get_selected_text') as gst:
            gst.return_value = ['foo']
            self.regs.view.sel.return_value = range(1)
            a.return_value = False
            self.regs.yank(vi_cmd_data)
            self.assertEqual(registers._REGISTER_DATA, {
                '1-9': [None] * 9,
                '0': None,
            })
