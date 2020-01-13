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
from sublime import OP_REGEX_CONTAINS
from sublime import OP_REGEX_MATCH

from NeoVintageous.tests import unittest

from NeoVintageous.nv.cmdline import CmdlineOutput
from NeoVintageous.nv.events import _is_command_mode
from NeoVintageous.nv.events import _is_insert_mode


class TestContextCheckers(unittest.ViewTestCase):

    def test_is_command_mode(self):
        self.settings().set('command_mode', True)
        self.assertEqual(_is_command_mode(self.view), True)
        self.assertEqual(_is_command_mode(self.view, operator=OP_EQUAL, operand=True), True)
        self.assertEqual(_is_command_mode(self.view, operator=OP_EQUAL, operand=False), False)
        self.settings().set('command_mode', False)
        self.assertEqual(_is_command_mode(self.view), False)
        self.assertEqual(_is_command_mode(self.view, operator=OP_EQUAL, operand=False), True)
        self.assertEqual(_is_command_mode(self.view, operator=OP_EQUAL, operand=True), False)

    def test_is_command_mode_for_cmdline_output(self):
        panel = CmdlineOutput(self.view.window())._output
        panel.settings().set('command_mode', True)
        self.assertEqual(_is_command_mode(panel), False)
        self.assertEqual(_is_command_mode(panel, operator=OP_EQUAL, operand=True), False)
        self.assertEqual(_is_command_mode(panel, operator=OP_EQUAL, operand=False), True)
        panel.settings().set('command_mode', False)
        self.assertEqual(_is_command_mode(panel), False)
        self.assertEqual(_is_command_mode(panel, operator=OP_EQUAL, operand=False), True)
        self.assertEqual(_is_command_mode(panel, operator=OP_EQUAL, operand=True), False)

    def test_is_command_mode_returns_false_by_default(self):
        self.settings().set('command_mode', False)
        self.assertEqual(_is_command_mode(self.view, operator=OP_REGEX_CONTAINS), False)
        self.settings().set('command_mode', True)
        self.assertEqual(_is_command_mode(self.view, operator=OP_REGEX_CONTAINS), False)

    def test_is_insert_mode(self):
        self.settings().set('command_mode', False)
        self.assertEqual(_is_insert_mode(self.view, operator=OP_EQUAL, operand=True, match_all=True), True)
        self.assertEqual(_is_insert_mode(self.view, operator=OP_EQUAL, operand=False, match_all=True), False)
        self.settings().set('command_mode', True)
        self.assertEqual(_is_insert_mode(self.view, operator=OP_EQUAL, operand=False, match_all=True), True)
        self.assertEqual(_is_insert_mode(self.view, operator=OP_EQUAL, operand=True, match_all=True), False)

    def test_is_insert_mode_for_cmdline_output(self):
        panel = CmdlineOutput(self.view.window())._output
        panel.settings().set('command_mode', True)
        self.assertEqual(_is_insert_mode(panel, operator=OP_EQUAL, operand=True, match_all=True), False)
        self.assertEqual(_is_insert_mode(panel, operator=OP_EQUAL, operand=False, match_all=True), True)
        panel.settings().set('command_mode', False)
        self.assertEqual(_is_insert_mode(panel, operator=OP_EQUAL, operand=False, match_all=True), True)
        self.assertEqual(_is_insert_mode(panel, operator=OP_EQUAL, operand=True, match_all=True), False)

    def test_is_insert_mode_false_by_default(self):
        self.assertEqual(_is_insert_mode(self.view, operator=OP_REGEX_MATCH, operand=True, match_all=True), False)
        self.assertEqual(_is_insert_mode(self.view, operator=OP_REGEX_MATCH, operand=False, match_all=True), False)

    @unittest.mock.patch('NeoVintageous.nv.events.is_view')
    def test_is_command_mode_should_return_early_if_not_command_mode(self, is_view):
        self.settings().set('command_mode', True)
        _is_command_mode(self.view)
        self.assertEqual(is_view.call_count, 1)
        self.settings().set('command_mode', False)
        _is_command_mode(self.view)
        self.assertEqual(is_view.call_count, 1)

    @unittest.mock.patch('NeoVintageous.nv.events.is_view')
    def test_is_insert_mode_should_return_early_if_not_command_mode(self, is_view):
        self.settings().set('command_mode', False)
        _is_insert_mode(self.view, operator=OP_EQUAL, operand=True, match_all=False)
        self.assertEqual(is_view.call_count, 1)
        self.settings().set('command_mode', True)
        _is_insert_mode(self.view, operator=OP_EQUAL, operand=True, match_all=False)
        self.assertEqual(is_view.call_count, 1)

    def test_query_contexts_can_be_disabled_by_external_plugins(self):
        self.settings().set('command_mode', True)
        self.settings().set('is_widget', False)
        self.settings().set('__vi_external_disable', True)
        self.assertEqual(_is_command_mode(self.view), False)
        self.assertEqual(_is_command_mode(self.view, operator=OP_EQUAL, operand=True), False)
        self.assertEqual(_is_command_mode(self.view, operator=OP_EQUAL, operand=False), True)
        self.assertEqual(_is_insert_mode(self.view, operator=OP_EQUAL, operand=True, match_all=True), False)
        self.assertEqual(_is_insert_mode(self.view, operator=OP_EQUAL, operand=False, match_all=True), True)

    def test_query_contexts_are_disabled_for_widgets(self):
        self.settings().set('command_mode', True)
        self.settings().set('is_widget', True)
        self.settings().set('__vi_external_disable', False)
        self.assertEqual(_is_command_mode(self.view), False)
        self.assertEqual(_is_command_mode(self.view, operator=OP_EQUAL, operand=True), False)
        self.assertEqual(_is_command_mode(self.view, operator=OP_EQUAL, operand=False), True)
        self.assertEqual(_is_insert_mode(self.view, operator=OP_EQUAL, operand=True, match_all=True), False)
        self.assertEqual(_is_insert_mode(self.view, operator=OP_EQUAL, operand=False, match_all=True), True)
