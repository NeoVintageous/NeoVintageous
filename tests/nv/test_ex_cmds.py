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

import sublime

from NeoVintageous.tests import unittest

from NeoVintageous.nv.ex.nodes import RangeNode
from NeoVintageous.nv.ex.tokens import TokenComma
from NeoVintageous.nv.ex.tokens import TokenDigits
from NeoVintageous.nv.ex.tokens import TokenDollar
from NeoVintageous.nv.ex_cmds import do_ex_command
from NeoVintageous.nv.ex_cmds import do_ex_cmdline
from NeoVintageous.nv.ex_cmds import do_ex_user_cmdline


_mock = {}


def _mock_ex_copy(view, edit, address, line_range, *args, **kwargs):
    _mock['view'] = view
    _mock['edit'] = edit
    _mock['address'] = address
    _mock['line_range'] = line_range
    _mock['args'] = args
    _mock['kwargs'] = kwargs


def _mock_ex_help(window, subject=None, forceit=False, *args, **kwargs):
    _mock['window'] = window
    _mock['subject'] = subject
    _mock['forceit'] = forceit
    _mock['args'] = args
    _mock['kwargs'] = kwargs


def _mock_ex_with_edit(edit, *args, **kwargs):
    _mock['edit'] = edit
    _mock['args'] = args
    _mock['kwargs'] = kwargs


def _mock_ex_with_no_args(*args, **kwargs):
    _mock['args'] = args
    _mock['kwargs'] = kwargs


def _mock_ex_with_view(view, *args, **kwargs):
    _mock['view'] = view
    _mock['args'] = args
    _mock['kwargs'] = kwargs


def _mock_ex_with_view_and_edit(view, edit, *args, **kwargs):
    _mock['view'] = view
    _mock['edit'] = edit
    _mock['args'] = args
    _mock['kwargs'] = kwargs


def _mock_ex_with_window(window, *args, **kwargs):
    _mock['window'] = window
    _mock['args'] = args
    _mock['kwargs'] = kwargs


def _mock_ex_with_window_and_view(window, view, *args, **kwargs):
    _mock['window'] = window
    _mock['view'] = view
    _mock['args'] = args
    _mock['kwargs'] = kwargs


class Test_do_ex_command(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        _mock.clear()

    def test_raise_exception_on_unknown_ex_cmd(self):
        with self.assertRaisesRegex(RuntimeError, "unknown ex cmd 'foobar'"):
            do_ex_command(self.view.window(), 'foobar')

    @unittest.mock.patch('NeoVintageous.nv.ex_cmds.ex_pwd', 'ex_pwd')
    def test_raise_exception_on_unknown_ex_cmd_type(self):
        with self.assertRaisesRegex(RuntimeError, "unknown ex cmd type 'pwd'"):
            do_ex_command(self.view.window(), 'pwd')

    @unittest.mock.patch('NeoVintageous.nv.ex_cmds.ex_pwd', _mock_ex_with_no_args)
    def test_can_do_ex_command_that_requires_no_args(self):
        do_ex_command(self.view.window(), 'pwd')

        self.assertEqual(_mock['args'], ())
        self.assertIsInstance(_mock['kwargs']['window'], sublime.Window)
        self.assertIsInstance(_mock['kwargs']['view'], sublime.View)
        self.assertEqual(_mock['kwargs']['line_range'], RangeNode())
        self.assertEqual(len(_mock['kwargs']), 3)
        self.assertEqual(len(_mock), 2)

    @unittest.mock.patch('NeoVintageous.nv.ex_cmds.ex_pwd', _mock_ex_with_edit)
    def test_can_do_ex_command_that_requires_edit(self):
        do_ex_command(self.view.window(), 'pwd')

        self.assertIsInstance(_mock['edit'], sublime.Edit)
        self.assertEqual(_mock['args'], ())
        self.assertIsInstance(_mock['kwargs']['view'], sublime.View)
        self.assertIsInstance(_mock['kwargs']['window'], sublime.Window)
        self.assertEqual(_mock['kwargs']['line_range'], RangeNode())
        self.assertEqual(len(_mock['kwargs']), 3)
        self.assertEqual(len(_mock), 3)

    @unittest.mock.patch('NeoVintageous.nv.ex_cmds.ex_pwd', _mock_ex_with_view)
    def test_can_do_ex_command_that_requires_view(self):
        do_ex_command(self.view.window(), 'pwd')

        self.assertIsInstance(_mock['view'], sublime.View)
        self.assertEqual(_mock['args'], ())
        self.assertIsInstance(_mock['kwargs']['window'], sublime.Window)
        self.assertEqual(_mock['kwargs']['line_range'], RangeNode())
        self.assertEqual(len(_mock['kwargs']), 2)
        self.assertEqual(len(_mock), 3)

    @unittest.mock.patch('NeoVintageous.nv.ex_cmds.ex_pwd', _mock_ex_with_view_and_edit)
    def test_can_do_ex_command_that_requires_view_and_edit(self):
        do_ex_command(self.view.window(), 'pwd')

        self.assertIsInstance(_mock['view'], sublime.View)
        self.assertIsInstance(_mock['edit'], sublime.Edit)
        self.assertEqual(_mock['args'], ())
        self.assertIsInstance(_mock['kwargs']['window'], sublime.Window)
        self.assertEqual(_mock['kwargs']['line_range'], RangeNode())
        self.assertEqual(len(_mock['kwargs']), 2)
        self.assertEqual(len(_mock), 4)

    @unittest.mock.patch('NeoVintageous.nv.ex_cmds.ex_pwd', _mock_ex_with_window)
    def test_can_do_ex_command_that_requires_window(self):
        do_ex_command(self.view.window(), 'pwd')

        self.assertIsInstance(_mock['window'], sublime.Window)
        self.assertEqual(_mock['args'], ())
        self.assertEqual(_mock['kwargs']['line_range'], RangeNode())
        self.assertIsInstance(_mock['kwargs']['view'], sublime.View)
        self.assertEqual(len(_mock['kwargs']), 2)
        self.assertEqual(len(_mock), 3)

    @unittest.mock.patch('NeoVintageous.nv.ex_cmds.ex_pwd', _mock_ex_with_window_and_view)
    def test_can_do_ex_command_that_requires_window_and_view(self):
        do_ex_command(self.view.window(), 'pwd')

        self.assertIsInstance(_mock['window'], sublime.Window)
        self.assertIsInstance(_mock['view'], sublime.View)
        self.assertEqual(_mock['args'], ())
        self.assertEqual(_mock['kwargs']['line_range'], RangeNode())
        self.assertEqual(len(_mock['kwargs']), 1)
        self.assertEqual(len(_mock), 4)

    @unittest.mock.patch('NeoVintageous.nv.ex_cmds.ex_help', _mock_ex_help)
    def test_can_do_ex_command_that_requires_optional_args(self):
        do_ex_command(self.view.window(), 'help')

        self.assertIsInstance(_mock['window'], sublime.Window)
        self.assertEqual(_mock['subject'], None)
        self.assertEqual(_mock['forceit'], False)
        self.assertEqual(_mock['args'], ())
        self.assertEqual(_mock['kwargs']['line_range'], RangeNode())
        self.assertIsInstance(_mock['kwargs']['view'], sublime.View)
        self.assertEqual(len(_mock['kwargs']), 2)
        self.assertEqual(len(_mock), 5)

    @unittest.mock.patch('NeoVintageous.nv.ex_cmds.ex_help', _mock_ex_help)
    def test_can_do_ex_command_that_requires_optional_args_receives_given_args(self):
        do_ex_command(self.view.window(), 'help', {'subject': 'hello', 'forceit': True})

        self.assertIsInstance(_mock['window'], sublime.Window)
        self.assertEqual(_mock['subject'], 'hello')
        self.assertEqual(_mock['forceit'], True)
        self.assertEqual(_mock['args'], ())
        self.assertEqual(_mock['kwargs']['line_range'], RangeNode())
        self.assertIsInstance(_mock['kwargs']['view'], sublime.View)
        self.assertEqual(len(_mock['kwargs']), 2)
        self.assertEqual(len(_mock), 5)

    @unittest.mock.patch('NeoVintageous.nv.ex_cmds.ex_help', _mock_ex_help)
    def test_can_do_ex_command_that_requires_optional_args_receives_given_args_2(self):
        do_ex_command(self.view.window(), 'help', {'subject': 'world', 'forceit': False})

        self.assertIsInstance(_mock['window'], sublime.Window)
        self.assertEqual(_mock['subject'], 'world')
        self.assertEqual(_mock['forceit'], False)
        self.assertEqual(_mock['args'], ())
        self.assertEqual(_mock['kwargs']['line_range'], RangeNode())
        self.assertIsInstance(_mock['kwargs']['view'], sublime.View)
        self.assertEqual(len(_mock['kwargs']), 2)
        self.assertEqual(len(_mock), 5)

    @unittest.mock.patch('NeoVintageous.nv.ex_cmds.ex_help', _mock_ex_with_edit)
    def test_can_do_ex_command_that_requires_edit_receives_given_args(self):
        do_ex_command(self.view.window(), 'help', {'subject': 'hello'})

        self.assertIsInstance(_mock['edit'], sublime.Edit)
        self.assertEqual(_mock['args'], ())
        self.assertEqual(_mock['kwargs']['line_range'], RangeNode())
        self.assertIsInstance(_mock['kwargs']['window'], sublime.Window)
        self.assertIsInstance(_mock['kwargs']['view'], sublime.View)
        self.assertEqual(_mock['kwargs']['subject'], 'hello')
        self.assertEqual(len(_mock['kwargs']), 4)
        self.assertEqual(len(_mock), 3)

    @unittest.mock.patch('NeoVintageous.nv.ex_cmds.ex_help', _mock_ex_with_edit)
    def test_can_do_ex_command_that_requires_edit_receives_args_2(self):
        do_ex_command(self.view.window(), 'help', {'subject': 'baley', 'forceit': True})

        self.assertIsInstance(_mock['edit'], sublime.Edit)
        self.assertEqual(_mock['args'], ())
        self.assertEqual(_mock['kwargs']['line_range'], RangeNode())
        self.assertIsInstance(_mock['kwargs']['window'], sublime.Window)
        self.assertIsInstance(_mock['kwargs']['view'], sublime.View)
        self.assertEqual(_mock['kwargs']['subject'], 'baley')
        self.assertEqual(_mock['kwargs']['forceit'], True)
        self.assertEqual(len(_mock['kwargs']), 5)
        self.assertEqual(len(_mock), 3)

    @unittest.mock.patch('NeoVintageous.nv.ex_cmds.ex_help', _mock_ex_with_edit)
    def test_can_do_ex_command_that_requires_edit_receives_args_3(self):
        do_ex_command(self.view.window(), 'help', {'subject': 'world', 'forceit': False})

        self.assertIsInstance(_mock['edit'], sublime.Edit)
        self.assertEqual(_mock['args'], ())
        self.assertEqual(_mock['kwargs']['line_range'], RangeNode())
        self.assertIsInstance(_mock['kwargs']['window'], sublime.Window)
        self.assertIsInstance(_mock['kwargs']['view'], sublime.View)
        self.assertEqual(_mock['kwargs']['subject'], 'world')
        self.assertEqual(_mock['kwargs']['forceit'], False)
        self.assertEqual(len(_mock['kwargs']), 5)
        self.assertEqual(len(_mock), 3)


class Test_do_ex_cmdline(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        _mock.clear()

    @unittest.mock.patch('NeoVintageous.nv.ex_cmds._default_ex_cmd')
    def test_can_do_default_ex_command(self, do_default_ex_cmd):
        do_ex_cmdline(self.view.window(), ':215')
        do_default_ex_cmd.assert_called_with(window=self.view.window(),
                                             view=self.view,
                                             line_range=RangeNode([TokenDigits('215')]))

        do_ex_cmdline(self.view.window(), ':$')
        do_default_ex_cmd.assert_called_with(window=self.view.window(),
                                             view=self.view,
                                             line_range=RangeNode([TokenDollar()]))

    def test_raises_exception_on_unknown_ex_cmd(self):
        # TODO Fix :foo actually calls :file (it shouldn't), this is why this test is using :zfoo instead.
        with self.assertRaisesRegex(Exception, "E492: Not an editor command"):
            do_ex_cmdline(self.view.window(), ':zfoo')

    @unittest.mock.patch('NeoVintageous.nv.ex_cmds.ex_pwd', 'ex_pwd')
    def test_raises_exception_on_unknown_ex_cmd_type(self):
        with self.assertRaisesRegex(RuntimeError, "unknown ex cmd type 'pwd'"):
            do_ex_cmdline(self.view.window(), ':pwd')

    @unittest.mock.patch('NeoVintageous.nv.ex_cmds.ex_pwd', _mock_ex_with_no_args)
    def test_can_do_ex_cmdline_that_requires_no_args(self):
        do_ex_cmdline(self.view.window(), ':pwd')

        self.assertEqual(_mock['args'], ())
        self.assertIsInstance(_mock['kwargs']['window'], sublime.Window)
        self.assertIsInstance(_mock['kwargs']['view'], sublime.View)
        self.assertEqual(_mock['kwargs']['line_range'], RangeNode())
        self.assertEqual(_mock['kwargs']['forceit'], False)
        self.assertEqual(len(_mock['kwargs']), 4)
        self.assertEqual(len(_mock), 2)

    @unittest.mock.patch('NeoVintageous.nv.ex_cmds.ex_help', _mock_ex_help)
    def test_can_do_ex_cmdline_with_bang(self):
        do_ex_cmdline(self.view.window(), ':help')

        self.assertIsInstance(_mock['window'], sublime.Window)
        self.assertEqual(_mock['subject'], None)
        self.assertEqual(_mock['forceit'], False)
        self.assertEqual(_mock['args'], ())
        self.assertIsInstance(_mock['kwargs']['view'], sublime.View)
        self.assertEqual(_mock['kwargs']['line_range'], RangeNode())
        self.assertEqual(len(_mock['kwargs']), 2)
        self.assertEqual(len(_mock), 5)

    @unittest.mock.patch('NeoVintageous.nv.ex_cmds.ex_help', _mock_ex_help)
    def test_can_do_ex_cmdline_with_bang_2(self):
        do_ex_cmdline(self.view.window(), ':help!')

        self.assertIsInstance(_mock['window'], sublime.Window)
        self.assertEqual(_mock['subject'], None)
        self.assertEqual(_mock['forceit'], True)
        self.assertEqual(_mock['args'], ())
        self.assertIsInstance(_mock['kwargs']['view'], sublime.View)
        self.assertEqual(_mock['kwargs']['line_range'], RangeNode())
        self.assertEqual(len(_mock['kwargs']), 2)
        self.assertEqual(len(_mock), 5)

    @unittest.mock.patch('NeoVintageous.nv.ex_cmds.ex_help', _mock_ex_help)
    def test_can_do_ex_cmdline_with_arg(self):
        do_ex_cmdline(self.view.window(), ':help neovintageous')

        self.assertIsInstance(_mock['window'], sublime.Window)
        self.assertEqual(_mock['subject'], 'neovintageous')
        self.assertEqual(_mock['forceit'], False)
        self.assertEqual(_mock['args'], ())
        self.assertIsInstance(_mock['kwargs']['view'], sublime.View)
        self.assertEqual(_mock['kwargs']['line_range'], RangeNode())
        self.assertEqual(len(_mock['kwargs']), 2)
        self.assertEqual(len(_mock), 5)

    @unittest.mock.patch('NeoVintageous.nv.ex_cmds.ex_copy', _mock_ex_copy)
    def test_can_do_ex_cmdline_with_line_range_and_address(self):
        do_ex_cmdline(self.view.window(), ':copy 3')

        self.assertIsInstance(_mock['view'], sublime.View)
        self.assertIsInstance(_mock['edit'], sublime.Edit)
        self.assertEqual(_mock['address'], '3')
        self.assertEqual(_mock['line_range'], RangeNode())
        self.assertEqual(_mock['args'], ())
        self.assertIsInstance(_mock['kwargs']['window'], sublime.Window)
        self.assertEqual(_mock['kwargs']['forceit'], False)
        self.assertEqual(len(_mock['kwargs']), 2)
        self.assertEqual(len(_mock), 6)

    @unittest.mock.patch('NeoVintageous.nv.ex_cmds.ex_copy', _mock_ex_copy)
    def test_can_do_ex_cmdline_with_line_range_and_address_2(self):
        do_ex_cmdline(self.view.window(), ':2copy 3')

        self.assertIsInstance(_mock['view'], sublime.View)
        self.assertIsInstance(_mock['edit'], sublime.Edit)
        self.assertEqual(_mock['address'], '3')
        self.assertEqual(_mock['line_range'], RangeNode([TokenDigits('2')]))
        self.assertEqual(_mock['args'], ())
        self.assertEqual(_mock['kwargs']['forceit'], False)
        self.assertIsInstance(_mock['kwargs']['window'], sublime.Window)
        self.assertEqual(len(_mock['kwargs']), 2)
        self.assertEqual(len(_mock), 6)

    @unittest.mock.patch('NeoVintageous.nv.ex_cmds.ex_copy', _mock_ex_copy)
    def test_can_do_ex_cmdline_with_line_range_and_address_3(self):
        do_ex_cmdline(self.view.window(), ':2,$copy 3')

        self.assertIsInstance(_mock['view'], sublime.View)
        self.assertIsInstance(_mock['edit'], sublime.Edit)
        self.assertEqual(_mock['address'], '3')
        self.assertEqual(_mock['line_range'], RangeNode([TokenDigits('2')], [TokenDollar()], TokenComma(',')))
        self.assertEqual(_mock['args'], ())
        self.assertIsInstance(_mock['kwargs']['window'], sublime.Window)
        self.assertEqual(_mock['kwargs']['forceit'], False)
        self.assertEqual(len(_mock['kwargs']), 2)
        self.assertEqual(len(_mock), 6)

    def test_can_run_user_sublime_text_command(self):
        window = unittest.mock.Mock()
        do_ex_cmdline(window, ':Fizz')
        window.run_command.assert_called_with('fizz')

        do_ex_cmdline(window, ':FizzBuzzFizz')
        window.run_command.assert_called_with('fizz_buzz_fizz')


class Test_do_ex_user_cmdline(unittest.ViewTestCase):

    @unittest.mock.patch('NeoVintageous.nv.ex_cmds.console_message')
    @unittest.mock.patch('NeoVintageous.nv.ex_cmds.do_ex_cmdline')
    def test_returns_false_for_invalid_cmdline(self, do_ex_cmdline, console_message):
        console_message.return_value = 'CONSOLE_MESSAGE_RETURN'
        window = unittest.mock.Mock()
        self.assertEqual(do_ex_user_cmdline(window, 'foobar'), 'CONSOLE_MESSAGE_RETURN')
        self.assertEqual(do_ex_user_cmdline(window, ':foobar'), 'CONSOLE_MESSAGE_RETURN')
        self.assertEqual(do_ex_user_cmdline(window, ' '), 'CONSOLE_MESSAGE_RETURN')
        self.assertEqual(do_ex_user_cmdline(window, ' :foo<CR>'), 'CONSOLE_MESSAGE_RETURN')
        self.assertEqual(do_ex_user_cmdline(window, ':'), 'CONSOLE_MESSAGE_RETURN')
        self.assertEqual(do_ex_user_cmdline(window, ':<CR>'), 'CONSOLE_MESSAGE_RETURN')
        self.assertEqual(do_ex_user_cmdline(window, '<CR>'), 'CONSOLE_MESSAGE_RETURN')
        self.assertEqual(do_ex_user_cmdline(window, ':_<CR>'), 'CONSOLE_MESSAGE_RETURN')
        self.assertEqual(do_ex_user_cmdline(window, ':2'), 'CONSOLE_MESSAGE_RETURN')
        self.assertEqual(do_ex_user_cmdline(window, ':2<CR>'), 'CONSOLE_MESSAGE_RETURN')
        self.assertEqual(do_ex_user_cmdline(window, ':$'), 'CONSOLE_MESSAGE_RETURN')
        self.assertEqual(do_ex_user_cmdline(window, ':$<CR>'), 'CONSOLE_MESSAGE_RETURN')
        self.assertEqual(do_ex_user_cmdline(window, ':2,$'), 'CONSOLE_MESSAGE_RETURN')
        self.assertEqual(do_ex_user_cmdline(window, ':2,$<CR>'), 'CONSOLE_MESSAGE_RETURN')
        self.assertEqual(do_ex_user_cmdline(window, ':2foo<CR>'), 'CONSOLE_MESSAGE_RETURN')
        self.assertEqual(do_ex_user_cmdline(window, ':$foo<CR>'), 'CONSOLE_MESSAGE_RETURN')
        self.assertEqual(do_ex_user_cmdline(window, ':2,$foo<CR>'), 'CONSOLE_MESSAGE_RETURN')
        self.assertEqual(do_ex_user_cmdline(window, 'x:foo<CR>'), 'CONSOLE_MESSAGE_RETURN')
        self.assertEqual(do_ex_user_cmdline(window, ':_foo<CR>'), 'CONSOLE_MESSAGE_RETURN')
        self.assertEqual(do_ex_user_cmdline(window, ':copy 3<CR>'), 'CONSOLE_MESSAGE_RETURN')
        self.assertEqual(do_ex_user_cmdline(window, ':1copy<CR>'), 'CONSOLE_MESSAGE_RETURN')
        self.assertEqual(do_ex_user_cmdline(window, ':1,$copy<CR>'), 'CONSOLE_MESSAGE_RETURN')
        window.assert_not_called()
        do_ex_cmdline.assert_not_called()

    @unittest.mock.patch('NeoVintageous.nv.ex_cmds.do_ex_cmdline')
    def test_can_do_ex_command(self, do_ex_cmdline):
        window = unittest.mock.Mock()

        # TODO Fix :foo actually calls :file (it shouldn't), this is why this test is using :zfoo instead.
        do_ex_user_cmdline(window, ':zfoo<CR>')

        do_ex_cmdline.assert_called_with(window, ':zfoo')
        window.assert_not_called()

    @unittest.mock.patch('NeoVintageous.nv.ex_cmds.do_ex_command')
    @unittest.mock.patch('NeoVintageous.nv.ex_cmds._default_ex_cmd')
    def test_can_do_user_command(self, do_ex_cmdline, do_default_ex_cmd):
        window = unittest.mock.Mock()

        do_ex_user_cmdline(window, ':Fizz<CR>')

        window.run_command.assert_called_with('fizz')
        do_ex_cmdline.assert_not_called()
        do_default_ex_cmd.assert_not_called()

        do_ex_user_cmdline(window, ':FizzBuzzFizz<CR>')

        window.run_command.assert_called_with('fizz_buzz_fizz')
        do_ex_cmdline.assert_not_called()
        do_default_ex_cmd.assert_not_called()
