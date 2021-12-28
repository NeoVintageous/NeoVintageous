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

from NeoVintageous.tests import unittest

from NeoVintageous.nv.cmdline import Cmdline


class TestCmdline(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        self.window = unittest.mock.Mock()
        self.window.show_input_panel.return_value = self.view
        self.view.window = lambda: self.window
        self.on_done = unittest.mock.Mock()
        self.on_change = unittest.mock.Mock()
        self.on_cancel = unittest.mock.Mock()

    def createCmdline(self, type=Cmdline.EX):
        return Cmdline(
            self.view,
            type,
            self.on_done,
            self.on_change,
            self.on_cancel
        )

    def test_contructor_invalid_type(self):
        with self.assertRaisesRegex(ValueError, 'invalid cmdline type'):
            Cmdline(self.window, 'foobar')

    def test_callbacks(self):
        cmdline = self.createCmdline()
        cmdline._on_done(':done')
        cmdline._on_change(':change')
        cmdline._on_cancel()

        self.assertEqual(self.window.run_command.call_count, 0)

        self.on_done.assert_called_once_with('done')
        self.on_change.assert_called_once_with('change')
        self.on_cancel.assert_called_once_with()

    def test_on_change_should_not_be_called_on_initial_empty_input(self):
        self.createCmdline(Cmdline.SEARCH_FORWARD)._on_change('/')
        self.assertEqual(self.on_change.call_count, 0)

    def test_invalid_on_done_input_forces_cancel(self):
        self.createCmdline()._on_done('invalid done input')
        self.on_cancel.assert_called_once_with()
        self.window.run_command.assert_called_once_with('hide_panel', {'cancel': True})

    def test_invalid_on_change_input_forces_cancel(self):
        self.createCmdline()._on_change('invalid change input')
        self.on_cancel.assert_called_once_with()
        self.window.run_command.assert_called_once_with('hide_panel', {'cancel': True})

    def test_on_done_receives_input_with_leading_type_stripped(self):
        self.createCmdline(Cmdline.SEARCH_FORWARD)._on_done('/pattern')
        self.on_done.assert_called_once_with('pattern')

    def test_on_change_receives_input_with_leading_type_stripped(self):
        self.createCmdline(Cmdline.SEARCH_BACKWARD)._on_change('?pattern')
        self.on_change.assert_called_once_with('pattern')

    def test_search_forward_incsearch_enabled(self):
        self.set_option('incsearch', True)
        self.createCmdline(Cmdline.SEARCH_FORWARD)._on_change('/change')
        self.on_change.assert_called_once_with('change')
        self.assertMockNotCalled(self.on_cancel)
        self.assertMockNotCalled(self.on_done)

    def test_search_backward_incsearch_enabled(self):
        self.set_option('incsearch', True)
        self.createCmdline(Cmdline.SEARCH_BACKWARD)._on_change('?change')
        self.on_change.assert_called_once_with('change')
        self.assertMockNotCalled(self.on_cancel)
        self.assertMockNotCalled(self.on_done)

    def test_search_backward_incsearch_disabled(self):
        self.set_option('incsearch', False)
        cmdline = self.createCmdline(Cmdline.SEARCH_BACKWARD)
        self.assertEqual(cmdline._callbacks['on_change'], None)

    def test_unknown_callback_does_not_raise_error(self):
        self.createCmdline(Cmdline.EX)._callback('foobar')

    def test_search_forward_incsearch_disabled(self):
        self.set_option('incsearch', False)
        cmdline = self.createCmdline(Cmdline.SEARCH_FORWARD)
        self.assertEqual(cmdline._callbacks['on_change'], None)

    def test_prompt(self):
        cmdline = self.createCmdline(Cmdline.SEARCH_FORWARD)
        cmdline.prompt('test')
        self.window.show_input_panel.assert_called_once_with(
            initial_text='/test',
            on_change=cmdline._on_change,
            caption='',
            on_done=cmdline._on_done,
            on_cancel=cmdline._on_cancel
        )
        self.assertEqual(self.view.name(), 'Command-line mode')
        self.assertTrue(self.view.settings().get('_nv_ex_mode'))
        self.assertTrue(self.view.settings().get('is_widget'))
