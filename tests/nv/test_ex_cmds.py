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

from unittest.mock import call

import sublime

from NeoVintageous.tests import unittest

from NeoVintageous.nv.ex.nodes import RangeNode
from NeoVintageous.nv.ex.tokens import TokenComma
from NeoVintageous.nv.ex.tokens import TokenDigits
from NeoVintageous.nv.ex.tokens import TokenDollar
from NeoVintageous.nv.ex_cmds import _parse_user_cmdline
from NeoVintageous.nv.ex_cmds import do_ex_cmdline
from NeoVintageous.nv.ex_cmds import do_ex_command
from NeoVintageous.nv.ex_cmds import do_ex_user_cmdline


_mock = {}


def _mock_ex_cmd(cmd: str):
    def _mock_inner_ex_cmd(**kwargs) -> None:
        _mock[cmd] = kwargs

    return _mock_inner_ex_cmd


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
    def test_can_run_default_command(self, _default_ex_cmd):
        _default_ex_cmd.return_value = None

        do_ex_cmdline(self.view.window(), ':215')
        _default_ex_cmd.assert_called_with(window=self.view.window(),
                                           view=self.view,
                                           line_range=RangeNode([TokenDigits('215')]))

        do_ex_cmdline(self.view.window(), ':$')
        _default_ex_cmd.assert_called_with(window=self.view.window(),
                                           view=self.view,
                                           line_range=RangeNode([TokenDollar()]))

    @unittest.mock_status_message()
    def test_raises_exception_on_unknown_ex_cmd(self):
        do_ex_cmdline(self.view.window(), ':foo')
        self.assertStatusMessage('E492: Not an editor command: foo')

    @unittest.mock_bell()
    def test_rings_bell_on_unknown_ex_cmd(self):
        do_ex_cmdline(self.view.window(), ':foo')
        self.assertBell('E492: Not an editor command: foo')

    @unittest.mock.patch('NeoVintageous.nv.ex_cmds.ex_pwd', 'ex_pwd')
    def test_raises_exception_on_unknown_ex_cmd_type(self):
        with self.assertRaisesRegex(RuntimeError, "unknown ex cmd type 'pwd'"):
            do_ex_cmdline(self.view.window(), ':pwd')

    @unittest.mock.patch('NeoVintageous.nv.ex_cmds.ex_pwd', _mock_ex_with_no_args)
    def test_cmd(self):
        do_ex_cmdline(self.view.window(), ':pwd')

        self.assertEqual(_mock['args'], ())
        self.assertIsInstance(_mock['kwargs']['window'], sublime.Window)
        self.assertIsInstance(_mock['kwargs']['view'], sublime.View)
        self.assertEqual(_mock['kwargs']['line_range'], RangeNode())
        self.assertEqual(_mock['kwargs']['forceit'], False)
        self.assertEqual(len(_mock['kwargs']), 4)
        self.assertEqual(len(_mock), 2)

    @unittest.mock.patch('NeoVintageous.nv.ex_cmds.ex_help', _mock_ex_help)
    def test_forceit_cmd(self):
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
    def test_cmd_with_argument(self):
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
    def test_cmd_with_argument_requires_line_range(self):
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
    def test_line_range_cmd(self):
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
    def test_line_range_start_to_end_cmd(self):
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

    @unittest.mock.patch('NeoVintageous.nv.ex_cmds._default_ex_cmd')
    def test_can_run_user_commands(self, default_ex_cmd):
        window = unittest.mock.Mock()
        window.run_command.return_value = None
        mem = {'run_command_count': 0}

        def assert_runs_cmd(line, expected_cmd, expected_args):
            do_ex_cmdline(window, line)
            mem['run_command_count'] += 1
            window.run_command.assert_called_with(expected_cmd, expected_args)
            self.assertEqual(window.run_command.call_count, mem['run_command_count'])
            self.assertEqual(default_ex_cmd.call_count, 0)

        assert_runs_cmd(':Fizz', 'fizz', None)
        assert_runs_cmd(':FizzBuzz', 'fizz_buzz', None)
        assert_runs_cmd(':FizzBuzzFizz', 'fizz_buzz_fizz', None)

        # With arguments.
        assert_runs_cmd(':Buzz foo=bar', 'buzz', {'foo': 'bar'})
        assert_runs_cmd(':CommandName foo=bar fizz=buzz', 'command_name', {'foo': 'bar', 'fizz': 'buzz'})
        assert_runs_cmd(':FizzBuzzFooBar a=b c=d e=f', 'fizz_buzz_foo_bar', {'a': 'b', 'c': 'd', 'e': 'f'})
        assert_runs_cmd(':N FOO=BAR', 'n', {'FOO': 'BAR'})
        assert_runs_cmd(':Name FooBar=FizzBuzz', 'name', {'FooBar': 'FizzBuzz'})
        assert_runs_cmd(':N a_b_c=d_e_f', 'n', {'a_b_c': 'd_e_f'})

        # Non-printable argument values.
        assert_runs_cmd(':N characters=\n', 'n', {'characters': '\n'})
        assert_runs_cmd(':N characters=\t', 'n', {'characters': '\t'})
        assert_runs_cmd(':ShowOverlay overlay=goto text=@', 'show_overlay', {'overlay': 'goto', 'text': '@'})
        assert_runs_cmd(':Exec hide_phantoms_only=true', 'exec', {'hide_phantoms_only': True})

        # Booleans argument values.
        assert_runs_cmd(':N x=true', 'n', {'x': True})
        assert_runs_cmd(':N x=false', 'n', {'x': False})
        assert_runs_cmd(':N x=true y=false', 'n', {'x': True, 'y': False})

        # Integer argument values.
        assert_runs_cmd(':N x=-100', 'n', {'x': -100})
        assert_runs_cmd(':N x=-3', 'n', {'x': -3})
        assert_runs_cmd(':N x=-1', 'n', {'x': -1})
        assert_runs_cmd(':N x=0', 'n', {'x': 0})
        assert_runs_cmd(':N x=1', 'n', {'x': 1})
        assert_runs_cmd(':N x=42', 'n', {'x': 42})
        assert_runs_cmd(':N x=4 y=2', 'n', {'x': 4, 'y': 2})

    @unittest.mock.patch('NeoVintageous.nv.ex_cmds._default_ex_cmd')
    def test_invalid_user_commands_dont_execute_any_commands(self, default_ex_cmd):
        window = unittest.mock.Mock()

        def assert_is_none(line):
            do_ex_cmdline(window, line)
            self.assertEqual(window.run_command.call_count, 0)
            self.assertEqual(default_ex_cmd.call_count, 0)

        assert_is_none(':Name$')
        assert_is_none(':Name foo')
        assert_is_none(':Name foo<CR>')
        assert_is_none(':Name foo')
        assert_is_none(':Name foo<CR>')
        assert_is_none(':Name foo=<CR>')
        assert_is_none(':Name =<barCR>')
        assert_is_none(':Name bar=>barCR>')
        assert_is_none(':Name bar barCR>')


class Test_do_ex_user_cmdline(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        _mock.clear()

    def createWindowAndViewMock(self) -> tuple:
        window = unittest.mock.Mock(spec=sublime.Window)
        view = unittest.mock.Mock(spec=sublime.View)
        window.active_view.return_value = view

        return (window, view)

    def createWindowMock(self) -> sublime.Window:
        return self.createWindowAndViewMock()[0]

    @unittest.mock.patch('NeoVintageous.nv.ex_cmds.do_ex_cmdline')
    @unittest.mock.patch('NeoVintageous.nv.ex_cmds.do_ex_command')
    @unittest.mock.patch('NeoVintageous.nv.ex_cmds._default_ex_cmd')
    def test_can_run_cmdline_with_no_initial_text(self, default_ex_cmd, do_ex_command, do_ex_cmdline):
        window = self.createWindowMock()

        do_ex_user_cmdline(window, ':')

        window.run_command.assert_called_with('nv_cmdline')
        self.assertEqual(default_ex_cmd.call_count, 0)
        self.assertEqual(do_ex_command.call_count, 0)
        self.assertEqual(do_ex_cmdline.call_count, 0)

    @unittest.mock.patch('NeoVintageous.nv.ex_cmds.do_ex_cmdline')
    @unittest.mock.patch('NeoVintageous.nv.ex_cmds.do_ex_command')
    @unittest.mock.patch('NeoVintageous.nv.ex_cmds._default_ex_cmd')
    def test_can_run_cmdline_with_initial_text(self, default_ex_cmd, do_ex_command, do_ex_cmdline):
        window = self.createWindowMock()

        do_ex_user_cmdline(window, ':reg')

        window.run_command.assert_called_with('nv_cmdline', args={'initial_text': ':reg'})
        self.assertEqual(default_ex_cmd.call_count, 0)
        self.assertEqual(do_ex_command.call_count, 0)
        self.assertEqual(do_ex_cmdline.call_count, 0)

    @unittest.mock.patch('NeoVintageous.nv.ex_cmds.do_ex_cmdline')
    @unittest.mock.patch('NeoVintageous.nv.ex_cmds.do_ex_command')
    @unittest.mock.patch('NeoVintageous.nv.ex_cmds._default_ex_cmd')
    def test_run_cmdline_with_initial_text_must_start_with_colon(self, default_ex_cmd, do_ex_command, do_ex_cmdline):
        window = self.createWindowMock()

        with self.assertRaisesRegex(RuntimeError, 'user cmdline must begin with a colon'):
            do_ex_user_cmdline(window, ' :')

        with self.assertRaisesRegex(RuntimeError, 'user cmdline must begin with a colon'):
            do_ex_user_cmdline(window, ' :reg')

        self.assertEqual(default_ex_cmd.call_count, 0)
        self.assertEqual(do_ex_command.call_count, 0)
        self.assertEqual(do_ex_cmdline.call_count, 0)
        self.assertEqual(window.run_command.call_count, 0)

    @unittest.mock.patch('NeoVintageous.nv.ex_cmds.ex_help', _mock_ex_help)
    @unittest.mock.patch('NeoVintageous.nv.ex_cmds.do_ex_command')
    @unittest.mock.patch('NeoVintageous.nv.ex_cmds._default_ex_cmd')
    def test_can_run_ex_command(self, default_ex_cmd, do_ex_command):
        window, view = self.createWindowAndViewMock()

        do_ex_user_cmdline(window, ':help hello<CR>')

        self.assertIsInstance(_mock['window'], sublime.Window)
        self.assertEqual(_mock['window'], window)
        self.assertEqual(_mock['subject'], 'hello')
        self.assertEqual(_mock['forceit'], False)
        self.assertEqual(_mock['args'], ())
        self.assertEqual(_mock['kwargs']['line_range'], RangeNode())
        self.assertEqual(_mock['kwargs']['view'], view)
        self.assertIsInstance(_mock['kwargs']['view'], sublime.View)
        self.assertEqual(len(_mock['kwargs']), 2)
        self.assertEqual(len(_mock), 5)
        self.assertEqual(default_ex_cmd.call_count, 0)
        self.assertEqual(do_ex_command.call_count, 0)
        self.assertEqual(window.run_command.call_count, 0)
        self.assertEqual(view.run_command.call_count, 0)

    @unittest.mock.patch('NeoVintageous.nv.ex_cmds.ex_copy', _mock_ex_with_window_and_view)
    @unittest.mock.patch('NeoVintageous.nv.ex_cmds.do_ex_command')
    @unittest.mock.patch('NeoVintageous.nv.ex_cmds._default_ex_cmd')
    def test_can_run_command_with_range(self, default_ex_cmd, do_ex_command):
        window, view = self.createWindowAndViewMock()

        do_ex_user_cmdline(window, ':2,$copy 3<CR>')

        self.assertIsInstance(_mock['window'], sublime.Window)
        self.assertEqual(_mock['window'], window)
        self.assertIsInstance(_mock['view'], sublime.View)
        self.assertEqual(_mock['view'], view)
        self.assertEqual(_mock['args'], ())
        self.assertEqual(_mock['kwargs']['line_range'], RangeNode([TokenDigits('2')], [TokenDollar()], TokenComma(',')))
        self.assertEqual(_mock['kwargs']['address'], '3')
        self.assertEqual(_mock['kwargs']['forceit'], False)
        self.assertEqual(len(_mock['kwargs']), 3)
        self.assertEqual(len(_mock), 4)
        self.assertEqual(default_ex_cmd.call_count, 0)
        self.assertEqual(do_ex_command.call_count, 0)
        self.assertEqual(window.run_command.call_count, 0)
        self.assertEqual(view.run_command.call_count, 0)

    @unittest.mock.patch('NeoVintageous.nv.ex_cmds.do_ex_command')
    @unittest.mock.patch('NeoVintageous.nv.ex_cmds._default_ex_cmd')
    def test_can_run_default_ex_command(self, default_ex_cmd, do_ex_command):
        window, view = self.createWindowAndViewMock()

        do_ex_user_cmdline(window, ':1<CR>')

        default_ex_cmd.assert_called_with(window=window, view=view, line_range=RangeNode([TokenDigits('1')]))
        self.assertEqual(do_ex_command.call_count, 0)
        self.assertEqual(window.run_command.call_count, 0)
        self.assertEqual(view.run_command.call_count, 0)

    @unittest.mock.patch('NeoVintageous.nv.ex_cmds.ex_help', _mock_ex_cmd('help'))
    @unittest.mock.patch('NeoVintageous.nv.ex_cmds.ex_only', _mock_ex_cmd('only'))
    def test_can_run_multiple_ex_commands(self):
        do_ex_user_cmdline(self.createWindowMock(), ':help<Bar>:only<CR>')
        self.assertTrue('help' in _mock)
        self.assertTrue('only' in _mock)

    @unittest.mock.patch('NeoVintageous.nv.ex_cmds.do_ex_command')
    @unittest.mock.patch('NeoVintageous.nv.ex_cmds._default_ex_cmd')
    def test_can_run_user_command(self, default_ex_cmd, do_ex_command):
        window = unittest.mock.Mock()
        mem = {'run_command_count': 0}

        def assert_run_command(line, expected_cmd, expected_args=None):
            do_ex_user_cmdline(window, line)
            if isinstance(expected_cmd, list):
                mem['run_command_count'] += len(expected_cmd)
                window.run_command.assert_has_calls(expected_cmd)
            else:
                mem['run_command_count'] += 1
                window.run_command.assert_called_with(expected_cmd, expected_args)

            self.assertEqual(window.run_command.call_count, mem['run_command_count'])
            self.assertEqual(default_ex_cmd.call_count, 0)
            self.assertEqual(do_ex_command.call_count, 0)

        assert_run_command(':Fizz<CR>', 'fizz', None)
        assert_run_command(':FizzBuzz<CR>', 'fizz_buzz', None)
        assert_run_command(':FizzBuzzFizz<CR>', 'fizz_buzz_fizz', None)
        # With arguments.
        assert_run_command(':Buzz foo=bar<CR>', 'buzz', {'foo': 'bar'})
        assert_run_command(':CommandName foo=bar fizz=buzz<CR>', 'command_name', {'foo': 'bar', 'fizz': 'buzz'})
        assert_run_command(':FizzBuzzFooBar a=b c=d e=f<CR>', 'fizz_buzz_foo_bar', {'a': 'b', 'c': 'd', 'e': 'f'})
        assert_run_command(':N FOO=BAR<CR>', 'n', {'FOO': 'BAR'})
        assert_run_command(':Name FooBar=FizzBuzz<CR>', 'name', {'FooBar': 'FizzBuzz'})
        assert_run_command(':N a_b_c=d_e_f<CR>', 'n', {'a_b_c': 'd_e_f'})
        assert_run_command(':Exec hide_phantoms_only=true<CR>', 'exec', {'hide_phantoms_only': True})
        # Non-printable argument values.
        assert_run_command(':N characters=\n<CR>', 'n', {'characters': '\n'})
        assert_run_command(':N characters=\t<CR>', 'n', {'characters': '\t'})

        assert_run_command(':OpenFile file=foo contents=bar,<CR>', 'open_file', {'file': 'foo', 'contents': 'bar,'})
        assert_run_command(':OpenFile file=foo contents=bar.<CR>', 'open_file', {'file': 'foo', 'contents': 'bar.'})
        assert_run_command(':ShowOverlay overlay=goto text=#<CR>', 'show_overlay', {'overlay': 'goto', 'text': '#'})
        assert_run_command(':ShowOverlay overlay=goto text=,<CR>', 'show_overlay', {'overlay': 'goto', 'text': ','})
        assert_run_command(':ShowOverlay overlay=goto text=.<CR>', 'show_overlay', {'overlay': 'goto', 'text': '.'})
        assert_run_command(':ShowOverlay overlay=goto text=:<CR>', 'show_overlay', {'overlay': 'goto', 'text': ':'})
        assert_run_command(':ShowOverlay overlay=goto text=@<CR>', 'show_overlay', {'overlay': 'goto', 'text': '@'})

        # Booleans argument values.
        assert_run_command(':N x=true<CR>', 'n', {'x': True})
        assert_run_command(':N x=false<CR>', 'n', {'x': False})
        assert_run_command(':N x=true y=false<CR>', 'n', {'x': True, 'y': False})
        # Integer argument values.
        assert_run_command(':N x=-100<CR>', 'n', {'x': -100})
        assert_run_command(':N x=-3<CR>', 'n', {'x': -3})
        assert_run_command(':N x=-1<CR>', 'n', {'x': -1})
        assert_run_command(':N x=0<CR>', 'n', {'x': 0})
        assert_run_command(':N x=1<CR>', 'n', {'x': 1})
        assert_run_command(':N x=42<CR>', 'n', {'x': 42})
        assert_run_command(':N x=4 y=2<CR>', 'n', {'x': 4, 'y': 2})

        # Multi commands
        assert_run_command(':Fizz<Bar>:Buzz<CR>', [call('fizz', None), call('buzz', None)])
        assert_run_command(':Fizz<Bar>:Buzz<Bar>:Fooo<CR>', [
            call('fizz', None),
            call('buzz', None),
            call('fooo', None),
        ])
        assert_run_command(':Fizz a=1 b=true<Bar>:Buzz c=false<CR>', [
            call('fizz', {'a': 1, 'b': True}),
            call('buzz', {'c': False})
        ])


class Test_parse_user_cmdline(unittest.TestCase):

    def assert_parsed(self, line, expected):
        parsed = _parse_user_cmdline(line)

        # TODO cleanup tests; The _parse_user_cmdline now returns a list of
        # commands and an empty list to represent none, previously this
        # function returned none or a dict.
        if parsed is not None:
            if len(parsed) == 1:
                parsed = parsed[0]
            elif len(parsed) == 0:
                parsed = None

        self.assertEqual(parsed, expected)

    def test_command_is_underscored(self):
        self.assert_parsed(':Fizz', {'cmd': 'fizz', 'args': None})
        self.assert_parsed(':FizzBuzz', {'cmd': 'fizz_buzz', 'args': None})
        self.assert_parsed(':FizzBuzzFizz', {'cmd': 'fizz_buzz_fizz', 'args': None})

    def test_arguments(self):
        self.assert_parsed(':Buzz foo=bar', {'cmd': 'buzz', 'args': {'foo': 'bar'}})
        self.assert_parsed(':CommandName foo=bar fizz=buzz', {'cmd': 'command_name', 'args': {'foo': 'bar', 'fizz': 'buzz'}})  # noqa: E501
        self.assert_parsed(':FizzBuzzFooBar a=b c=d e=f', {'cmd': 'fizz_buzz_foo_bar', 'args': {'a': 'b', 'c': 'd', 'e': 'f'}})  # noqa: E501
        self.assert_parsed(':N FOO=BAR', {'cmd': 'n', 'args': {'FOO': 'BAR'}})
        self.assert_parsed(':Name FooBar=FizzBuzz', {'cmd': 'name', 'args': {'FooBar': 'FizzBuzz'}})
        self.assert_parsed(':N a_b_c=d_e_f', {'cmd': 'n', 'args': {'a_b_c': 'd_e_f'}})

    def test_non_printable_argument_values(self):
        self.assert_parsed(':FizzBuzz characters=\n', {'cmd': 'fizz_buzz', 'args': {'characters': '\n'}})
        self.assert_parsed(':FizzBuzz characters=\t', {'cmd': 'fizz_buzz', 'args': {'characters': '\t'}})
        self.assert_parsed(':ShowOverlay overlay=goto text=@', {'cmd': 'show_overlay', 'args': {'overlay': 'goto', 'text': '@'}})  # noqa: E501
        self.assert_parsed(':Exec hide_phantoms_only=true', {'cmd': 'exec', 'args': {'hide_phantoms_only': True}})

    def test_boolean_argument_values(self):
        self.assert_parsed(':FizzBuzz x=true', {'cmd': 'fizz_buzz', 'args': {'x': True}})
        self.assert_parsed(':FizzBuzz x=false', {'cmd': 'fizz_buzz', 'args': {'x': False}})
        self.assert_parsed(':FizzBuzz x=true y=false', {'cmd': 'fizz_buzz', 'args': {'x': True, 'y': False}})

    def test_integer_argument_values(self):
        self.assert_parsed(':FizzBuzz x=-100', {'cmd': 'fizz_buzz', 'args': {'x': -100}})
        self.assert_parsed(':FizzBuzz x=-3', {'cmd': 'fizz_buzz', 'args': {'x': -3}})
        self.assert_parsed(':FizzBuzz x=-1', {'cmd': 'fizz_buzz', 'args': {'x': -1}})
        self.assert_parsed(':FizzBuzz x=0', {'cmd': 'fizz_buzz', 'args': {'x': 0}})
        self.assert_parsed(':FizzBuzz x=1', {'cmd': 'fizz_buzz', 'args': {'x': 1}})
        self.assert_parsed(':FizzBuzz x=42', {'cmd': 'fizz_buzz', 'args': {'x': 42}})
        self.assert_parsed(':FizzBuzz x=4 y=2', {'cmd': 'fizz_buzz', 'args': {'x': 4, 'y': 2}})

    def test_integer_float_values(self):
        self.assert_parsed(':FizzBuzz x=-0.1', {'cmd': 'fizz_buzz', 'args': {'x': -0.1}})
        self.assert_parsed(':FizzBuzz x=-4.2', {'cmd': 'fizz_buzz', 'args': {'x': -4.2}})
        self.assert_parsed(':FizzBuzz x=0.0', {'cmd': 'fizz_buzz', 'args': {'x': 0.0}})
        self.assert_parsed(':FizzBuzz x=0.9', {'cmd': 'fizz_buzz', 'args': {'x': 0.9}})
        self.assert_parsed(':FizzBuzz x=1.0', {'cmd': 'fizz_buzz', 'args': {'x': 1.0}})
        self.assert_parsed(':FizzBuzz x=4.1 y=2.3', {'cmd': 'fizz_buzz', 'args': {'x': 4.1, 'y': 2.3}})
        self.assert_parsed(':FizzBuzz x=42.0', {'cmd': 'fizz_buzz', 'args': {'x': 42.0}})

    def test_invalid_command(self):
        self.assert_parsed(':foobar', None)
        self.assert_parsed('foobar', None)
        self.assert_parsed('Foobar', None)
        self.assert_parsed(':Foobar<CR>', None)
        self.assert_parsed(': Foo', None)

    def test_range_is_not_valid(self):
        self.assert_parsed(' ', None)
        self.assert_parsed('$', None)
        self.assert_parsed(':$', None)
        self.assert_parsed(':$Foo', None)
        self.assert_parsed(':', None)
        self.assert_parsed(':1', None)
        self.assert_parsed(':1,$Copy', None)
        self.assert_parsed(':1Copy', None)
        self.assert_parsed(':2,$', None)
        self.assert_parsed(':2,$Foo', None)
        self.assert_parsed(':2Foo', None)
        self.assert_parsed(':_', None)
        self.assert_parsed(':_Foo', None)
        self.assert_parsed('x:Foo', None)

    def test_carriage_returns_are_not_valid(self):
        self.assert_parsed(' <CR>', None)
        self.assert_parsed('$<CR>', None)
        self.assert_parsed(':$<CR>', None)
        self.assert_parsed(':1<CR>', None)
        self.assert_parsed(':<CR>', None)
        self.assert_parsed(':<CR>', None)
        self.assert_parsed(':<CR>', None)
        self.assert_parsed('<CR>', None)

    def test_invalid_arguments(self):
        self.assert_parsed(':Name =<bar', None)
        self.assert_parsed(':Name bar bar', None)
        self.assert_parsed(':Name bar=>bar', None)
        self.assert_parsed(':Name foo', None)
        self.assert_parsed(':Name foo=', None)
        self.assert_parsed(':Name foo=<', None)
        self.assert_parsed(':Name$', None)

    def test_allow_alnum_arg_names(self):
        self.assert_parsed(':FizzBuzz a1=true test123=true', {
            'cmd': 'fizz_buzz',
            'args': {'a1': True, 'test123': True}
        })

    def test_multi_commands(self):
        self.assert_parsed(':Fizz<bar>:Buzz', [
            {'cmd': 'fizz', 'args': None},
            {'cmd': 'buzz', 'args': None},
        ])
        self.assert_parsed(':Fizz a=true b=3<bar>:Buzz c=val', [
            {'cmd': 'fizz', 'args': {'a': True, 'b': 3}},
            {'cmd': 'buzz', 'args': {'c': 'val'}},
        ])

    def test_multi_command_case_insensitive_bar_char(self):
        self.assert_parsed(':Fizz<BAR>:Buzz', [
            {'cmd': 'fizz', 'args': None},
            {'cmd': 'buzz', 'args': None},
        ])
