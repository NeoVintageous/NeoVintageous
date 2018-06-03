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
from sublime import OP_NOT_EQUAL
from sublime import OP_NOT_REGEX_MATCH
from sublime import OP_REGEX_CONTAINS
from sublime import OP_REGEX_MATCH

from NeoVintageous.tests import unittest

from NeoVintageous.nv.events import _is_cmdline_at_fs_completion
from NeoVintageous.nv.events import _is_cmdline_at_setting_completion
from NeoVintageous.nv.events import _is_cmdline_mode
from NeoVintageous.nv.events import _is_command_mode
from NeoVintageous.nv.events import _is_insert_mode


class TestContextCheckers(unittest.ViewTestCase):

    def test_is_cmdline(self):
        self.assertEqual(_is_cmdline_mode(self.view, operator=OP_EQUAL, operand=True, match_all=False), False)
        self.assertEqual(_is_cmdline_mode(self.view, operator=OP_EQUAL, operand=False, match_all=False), True)
        self.assertEqual(_is_cmdline_mode(self.view, operator=OP_NOT_EQUAL, operand=True, match_all=False), True)
        self.assertEqual(_is_cmdline_mode(self.view, operator=OP_NOT_EQUAL, operand=False, match_all=False), False)
        self.view.assign_syntax('Packages/NeoVintageous/res/Command-line mode.sublime-syntax')
        self.assertTrue(_is_cmdline_mode(self.view, operator=OP_EQUAL, operand=True, match_all=False))
        self.assertTrue(_is_cmdline_mode(self.view, operator=OP_NOT_EQUAL, operand=False, match_all=False))

    def test_is_cmdline_returns_false_by_default(self):
        self.assertEqual(_is_cmdline_mode(self.view, operator=OP_REGEX_MATCH, operand='', match_all=False), False)
        self.assertEqual(_is_cmdline_mode(self.view, operator=OP_NOT_REGEX_MATCH, operand='', match_all=False), False)

    def test_is_cmdline_at_fs_completion(self):
        self.assertEqual(_is_cmdline_at_fs_completion(self.view, operator=OP_EQUAL, operand=True, match_all=False), False)  # noqa: E501
        self.assertEqual(_is_cmdline_at_fs_completion(self.view, operator=OP_EQUAL, operand=False, match_all=False), True)  # noqa: E501
        self.view.assign_syntax('Packages/NeoVintageous/res/Command-line mode.sublime-syntax')
        self.assertEqual(_is_cmdline_at_fs_completion(self.view, operator=OP_EQUAL, operand=True, match_all=False), False)  # noqa: E501
        self.write(':write ')
        self.assertEqual(_is_cmdline_at_fs_completion(self.view, operator=OP_EQUAL, operand=True, match_all=False), True)  # noqa: E501

    def test_is_cmdline_at_fs_completion_returns_false_by_default(self):
        self.assertEqual(_is_cmdline_at_fs_completion(self.view, operator=OP_REGEX_CONTAINS, operand=True, match_all=False), False)  # noqa: E501
        self.assertEqual(_is_cmdline_at_fs_completion(self.view, operator=OP_REGEX_CONTAINS, operand=False, match_all=False), False)  # noqa: E501

    def test_is_cmdline_at_setting_completion(self):
        self.assertEqual(_is_cmdline_at_setting_completion(self.view, operator=OP_EQUAL, operand=True, match_all=False), False)  # noqa: E501

        self.view.assign_syntax('Packages/NeoVintageous/res/Command-line mode.sublime-syntax')
        self.assertEqual(_is_cmdline_at_setting_completion(self.view, operator=OP_EQUAL, operand=True, match_all=False), False)  # noqa: E501

        self.write(':set ')
        self.assertEqual(_is_cmdline_at_setting_completion(self.view, operator=OP_EQUAL, operand=True, match_all=False), True)  # noqa: E501

        self.view.assign_syntax('Packages/NeoVintageous/tests/fixtures/Command-line mode foobar.sublime-syntax')
        self.assertEqual(_is_cmdline_at_setting_completion(self.view, operator=OP_EQUAL, operand=True, match_all=False), False)  # noqa: E501

    def test_is_cmdline_at_setting_completion_returns_false_by_default(self):
        self.assertEqual(_is_cmdline_at_fs_completion(self.view, operator=OP_REGEX_CONTAINS, operand=True, match_all=False), False)  # noqa: E501
        self.assertEqual(_is_cmdline_at_fs_completion(self.view, operator=OP_REGEX_CONTAINS, operand=False, match_all=False), False)  # noqa: E501

    def test_is_command_mode_can_return_true(self):
        self.settings().set('command_mode', True)
        self.assertEqual(_is_command_mode(self.view, operator=OP_EQUAL, operand=True, match_all=True), True)
        self.settings().set('command_mode', False)
        self.assertEqual(_is_command_mode(self.view, operator=OP_EQUAL, operand=False, match_all=True), True)

    def test_is_command_mode_can_return_false(self):
        self.settings().set('command_mode', False)
        self.assertEqual(_is_command_mode(self.view, operator=OP_EQUAL, operand=True, match_all=True), False)
        self.settings().set('command_mode', True)
        self.assertEqual(_is_command_mode(self.view, operator=OP_EQUAL, operand=False, match_all=True), False)

    def test_is_command_mode_can_return_false_for_panels(self):
        panel = self.view.window().create_output_panel('test_context', unlisted=True)
        panel.settings().set('command_mode', True)
        self.assertEqual(_is_command_mode(panel, operator=OP_EQUAL, operand=True, match_all=True), False)

        panel = self.view.window().create_output_panel('test_context', unlisted=True)
        panel.settings().set('command_mode', False)
        self.assertEqual(_is_command_mode(panel, operator=OP_EQUAL, operand=True, match_all=True), False)

    def test_is_command_mode_can_return_true_for_panels(self):
        panel = self.view.window().create_output_panel('test_context', unlisted=True)
        panel.settings().set('command_mode', True)
        self.assertEqual(_is_command_mode(panel, operator=OP_EQUAL, operand=False, match_all=True), True)

        panel = self.view.window().create_output_panel('test_context', unlisted=True)
        panel.settings().set('command_mode', False)
        self.assertEqual(_is_command_mode(panel, operator=OP_EQUAL, operand=False, match_all=True), True)

    def test_is_command_mode_returns_false_by_default(self):
        self.settings().set('command_mode', False)
        self.assertEqual(_is_command_mode(self.view, operator=OP_REGEX_CONTAINS, operand=True, match_all=True), False)
        self.settings().set('command_mode', True)
        self.assertEqual(_is_command_mode(self.view, operator=OP_REGEX_CONTAINS, operand=False, match_all=True), False)

    def test_is_insert_mode_can_return_true(self):
        self.settings().set('command_mode', False)
        self.assertEqual(_is_insert_mode(self.view, operator=OP_EQUAL, operand=True, match_all=True), True)
        self.settings().set('command_mode', True)
        self.assertEqual(_is_insert_mode(self.view, operator=OP_EQUAL, operand=False, match_all=True), True)

    def test_is_insert_mode_can_return_false(self):
        self.settings().set('command_mode', True)
        self.assertEqual(_is_insert_mode(self.view, operator=OP_EQUAL, operand=True, match_all=True), False)
        self.settings().set('command_mode', False)
        self.assertEqual(_is_insert_mode(self.view, operator=OP_EQUAL, operand=False, match_all=True), False)

    def test_is_insert_mode_can_return_false_for_panels(self):
        panel = self.view.window().create_output_panel('test_context', unlisted=True)
        panel.settings().set('command_mode', False)
        self.assertEqual(_is_insert_mode(self.view, operator=OP_EQUAL, operand=True, match_all=True), False)

        panel = self.view.window().create_output_panel('test_context', unlisted=True)
        panel.settings().set('command_mode', True)
        self.assertEqual(_is_insert_mode(self.view, operator=OP_EQUAL, operand=True, match_all=True), False)

    def test_is_insert_mode_can_return_true_for_panels(self):
        panel = self.view.window().create_output_panel('test_context', unlisted=True)
        panel.settings().set('command_mode', False)
        self.assertEqual(_is_insert_mode(self.view, operator=OP_EQUAL, operand=False, match_all=True), True)

        panel = self.view.window().create_output_panel('test_context', unlisted=True)
        panel.settings().set('command_mode', True)
        self.assertEqual(_is_insert_mode(self.view, operator=OP_EQUAL, operand=False, match_all=True), True)

    def test_is_insert_mode_false_by_default(self):
        self.assertEqual(_is_insert_mode(self.view, operator=OP_REGEX_MATCH, operand=True, match_all=True), False)
        self.assertEqual(_is_insert_mode(self.view, operator=OP_REGEX_MATCH, operand=False, match_all=True), False)
