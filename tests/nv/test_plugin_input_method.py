# Copyright (C) 2018-2023 The NeoVintageous Team (NeoVintageous).
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

from NeoVintageous.tests import unittest

from NeoVintageous.nv.plugin_input_method import IMSwitcher
from NeoVintageous.nv.plugin_input_method import Listener


class TestInputMethod(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        self.set_setting('auto_switch_input_method', False)
        self.set_setting('auto_switch_input_method_default', 'en')
        self.set_setting('auto_switch_input_method_get_cmd', '/path/to/im-get')
        self.set_setting('auto_switch_input_method_set_cmd', '/path/to/im-set {im}')

    @unittest.mock.patch('NeoVintageous.nv.plugin_input_method.read')
    def test_can_switch_to_default(self, shell):
        self.set_setting('auto_switch_input_method', True)
        shell.side_effect = ['call_1_return', 'call_2_return']

        switcher = IMSwitcher()
        switcher.run(self.view, unittest.NORMAL)

        self.assertEqual(2, shell.call_count)
        self.assertEqual('call_1_return', switcher.saved_im)

        shell.assert_has_calls([
            call(self.view, '/path/to/im-get'),
            call(self.view, '/path/to/im-set en'),
        ])

    @unittest.mock.patch('NeoVintageous.nv.plugin_input_method.read')
    def test_switch_to_default_is_noop_if_same_as_saved_im(self, shell):
        self.set_setting('auto_switch_input_method', True)
        self.set_setting('auto_switch_input_method_default', 'ie')
        shell.side_effect = ['ie', 'call_2_return']

        switcher = IMSwitcher()
        switcher.saved_im = 'xx'
        switcher.run(self.view, unittest.NORMAL)

        self.assertEqual(1, shell.call_count)
        self.assertEqual('ie', switcher.saved_im)
        shell.assert_has_calls([
            call(self.view, '/path/to/im-get'),
        ])

    @unittest.mock.patch('NeoVintageous.nv.plugin_input_method.read')
    def test_is_noop_when_disabled(self, shell):
        self.set_setting('auto_switch_input_method', False)
        shell.side_effect = ['call_1_return', 'call_2_return']

        switcher = IMSwitcher()
        switcher.run(self.view, unittest.NORMAL)

        self.assertMockNotCalled(shell)
        self.assertEqual('', switcher.saved_im)

    @unittest.mock.patch('NeoVintageous.nv.plugin_input_method.read')
    def test_can_resume(self, shell):
        self.set_setting('auto_switch_input_method', True)
        self.set_setting('auto_switch_input_method_default', 'en')
        shell.side_effect = ['call_1_return', 'call_2_return']

        switcher = IMSwitcher()
        switcher.saved_im = 'ie'
        switcher.run(self.view, unittest.INSERT)

        self.assertEqual(1, shell.call_count)
        self.assertEqual('ie', switcher.saved_im)

        shell.assert_has_calls([
            call(self.view, '/path/to/im-set ie'),
        ])

    @unittest.mock.patch('NeoVintageous.nv.plugin_input_method.read')
    def test_resume_is_noop_when_no_previously_saved_im(self, shell):
        self.set_setting('auto_switch_input_method', True)
        shell.side_effect = ['call_1_return', 'call_2_return']

        switcher = IMSwitcher()
        switcher.run(self.view, unittest.INSERT)

        self.assertMockNotCalled(shell)
        self.assertEqual('', switcher.saved_im)

    @unittest.mock.patch('NeoVintageous.nv.plugin_input_method.read')
    def test_resume_is_noop_if_saved_im_is_same_as_default(self, shell):
        self.set_setting('auto_switch_input_method', True)
        self.set_setting('auto_switch_input_method_default', 'ie')
        shell.side_effect = ['call_1_return', 'call_2_return']

        switcher = IMSwitcher()
        switcher.saved_im = 'ie'
        switcher.run(self.view, unittest.INSERT)

        self.assertMockNotCalled(shell)
        self.assertEqual('ie', switcher.saved_im)

    @unittest.mock.patch('NeoVintageous.nv.plugin_input_method.read')
    def test_listener(self, shell):
        # User == ie, Default == en
        self.set_setting('auto_switch_input_method', True)
        self.set_setting('auto_switch_input_method_default', 'en')
        shell.side_effect = ['ie', '', '', 'ie', '']

        switcher = IMSwitcher()
        listener = Listener(switcher)

        # 1. ENTER insert stay in "ie" (Insert mode)
        listener.on_insert_enter(self.view, prev_mode=unittest.NORMAL)

        self.assertMockNotCalled(shell)
        self.assertEqual('', switcher.saved_im)

        # 2. LEAVE insert switch to "en" (Normal mode)
        listener.on_insert_leave(self.view, new_mode=unittest.NORMAL)

        self.assertEqual(2, shell.call_count)
        self.assertEqual('ie', switcher.saved_im)
        shell.assert_has_calls([
            call(self.view, '/path/to/im-get'),
            call(self.view, '/path/to/im-set en'),
        ])

        # 3. ENTER insert switch to "ie" (Insert mode)
        listener.on_insert_enter(self.view, prev_mode=unittest.NORMAL)
        self.assertEqual(3, shell.call_count)
        self.assertEqual('ie', switcher.saved_im)
        shell.assert_has_calls([
            call(self.view, '/path/to/im-set ie'),
        ])

        # 4. LEAVE insert switch to "en" (Normal mode)
        listener.on_insert_leave(self.view, new_mode=unittest.NORMAL)

        self.assertEqual(5, shell.call_count)
        self.assertEqual('ie', switcher.saved_im)
        shell.assert_has_calls([
            call(self.view, '/path/to/im-get'),
            call(self.view, '/path/to/im-set en'),
        ])
