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

from sublime import OP_EQUAL

from NeoVintageous.tests import unittest

from NeoVintageous.nv.events import _is_cmdline_at_fs_completion
from NeoVintageous.nv.events import _is_cmdline_at_setting_completion
from NeoVintageous.nv.events import _is_cmdline_mode
from NeoVintageous.nv.events import _is_command_mode
from NeoVintageous.nv.events import _is_insert_mode


class TestEvents(unittest.ViewTestCase):

    def test_is_cmdline(self):
        self.assertFalse(_is_cmdline_mode(self.view, OP_EQUAL, True, False))
        self.view.assign_syntax('Packages/NeoVintageous/res/Command-line mode.sublime-syntax')
        self.assertTrue(_is_cmdline_mode(self.view, OP_EQUAL, True, False))

    def test_vi_cmdline_at_fs_completion(self):
        self.assertFalse(_is_cmdline_at_fs_completion(self.view, OP_EQUAL, True, False))

        self.view.assign_syntax('Packages/NeoVintageous/res/Command-line mode.sublime-syntax')
        self.assertFalse(_is_cmdline_at_fs_completion(self.view, OP_EQUAL, True, False))

        self.write(':write ')
        self.assertTrue(_is_cmdline_at_fs_completion(self.view, OP_EQUAL, True, False))

    def test_vi_cmdline_at_setting_completion(self):
        self.assertFalse(_is_cmdline_at_setting_completion(self.view, OP_EQUAL, True, False))

        self.view.assign_syntax('Packages/NeoVintageous/res/Command-line mode.sublime-syntax')
        self.assertFalse(_is_cmdline_at_setting_completion(self.view, OP_EQUAL, True, False))

        self.write(':set ')
        self.assertTrue(_is_cmdline_at_setting_completion(self.view, OP_EQUAL, True, False))

        self.view.assign_syntax('Packages/NeoVintageous/tests/fixtures/Command-line mode foobar.sublime-syntax')
        self.assertFalse(_is_cmdline_at_setting_completion(self.view, OP_EQUAL, True, False))

    def test_vi_command_mode_aware_can_return_true(self):
        self.settings().set('command_mode', True)
        self.assertTrue(_is_command_mode(self.view, OP_EQUAL, True, True))
        self.settings().set('command_mode', False)
        self.assertTrue(_is_command_mode(self.view, OP_EQUAL, False, True))

    def test_vi_command_mode_aware_can_return_false(self):
        self.settings().set('command_mode', False)
        self.assertFalse(_is_command_mode(self.view, OP_EQUAL, True, True))
        self.settings().set('command_mode', True)
        self.assertFalse(_is_command_mode(self.view, OP_EQUAL, False, True))

    def test_vi_command_mode_aware_can_return_false_for_panels(self):
        panel = self.view.window().create_output_panel('test_context', unlisted=True)
        panel.settings().set('command_mode', True)
        self.assertFalse(_is_command_mode(panel, OP_EQUAL, True, True))

        panel = self.view.window().create_output_panel('test_context', unlisted=True)
        panel.settings().set('command_mode', False)
        self.assertFalse(_is_command_mode(panel, OP_EQUAL, True, True))

    def test_vi_command_mode_aware_can_return_true_for_panels(self):
        panel = self.view.window().create_output_panel('test_context', unlisted=True)
        panel.settings().set('command_mode', True)
        self.assertTrue(_is_command_mode(panel, OP_EQUAL, False, True))

        panel = self.view.window().create_output_panel('test_context', unlisted=True)
        panel.settings().set('command_mode', False)
        self.assertTrue(_is_command_mode(panel, OP_EQUAL, False, True))

    def test_vi_insert_mode_aware_can_return_true(self):
        self.settings().set('command_mode', False)
        self.assertTrue(_is_insert_mode(self.view, OP_EQUAL, True, True))
        self.settings().set('command_mode', True)
        self.assertTrue(_is_insert_mode(self.view, OP_EQUAL, False, True))

    def test_vi_insert_mode_aware_can_return_false(self):
        self.settings().set('command_mode', True)
        self.assertFalse(_is_insert_mode(self.view, OP_EQUAL, True, True))
        self.settings().set('command_mode', False)
        self.assertFalse(_is_insert_mode(self.view, OP_EQUAL, False, True))

    def test_vi_insert_mode_aware_can_return_false_for_panels(self):
        panel = self.view.window().create_output_panel('test_context', unlisted=True)
        panel.settings().set('command_mode', False)
        self.assertFalse(_is_insert_mode(self.view, OP_EQUAL, True, True))

        panel = self.view.window().create_output_panel('test_context', unlisted=True)
        panel.settings().set('command_mode', True)
        self.assertFalse(_is_insert_mode(self.view, OP_EQUAL, True, True))

    def test_vi_insert_mode_aware_can_return_true_for_panels(self):
        panel = self.view.window().create_output_panel('test_context', unlisted=True)
        panel.settings().set('command_mode', False)
        self.assertTrue(_is_insert_mode(self.view, OP_EQUAL, False, True))

        panel = self.view.window().create_output_panel('test_context', unlisted=True)
        panel.settings().set('command_mode', True)
        self.assertTrue(_is_insert_mode(self.view, OP_EQUAL, False, True))
