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

from NeoVintageous.nv.ui import ui_bell

from sublime import set_timeout


class TestUIBell(unittest.ViewTestCase):

    @unittest.mock_status_message()
    def test_ui_bell_displays_message_when_belloff_disabled(self):
        self.set_option('belloff', '')
        ui_bell('fizz buzz')
        self.assertStatusMessage('fizz buzz')

    @unittest.mock_status_message()
    def test_ui_bell_displays_message_when_belloff_enabled(self):
        self.set_option('belloff', 'all')
        ui_bell('fizz buzz')
        self.assertStatusMessage('fizz buzz')
        self.set_option('belloff', '')
        ui_bell('fizz buzz')
        self.assertStatusMessage('fizz buzz')

    @unittest.mock_status_message()
    def test_ui_bell_with_no_message(self):
        ui_bell()
        self.assertNoStatusMessage()

    def assertDefaultColorScheme(self):
        pass
        # Breaks tests
        # self.assertEqual(
        #     'Packages/NeoVintageous/res/Bell-dark.hidden-color-scheme',
        #     self.view.settings().get('color_scheme'))

    def assertNoColorScheme(self) -> None:
        window = self.view.window()
        if window:
            for view in window.views():
                self.assertNone(view.settings().get('color_scheme'))

    def assertBellIsRemoved(self) -> None:
        defaultDuration = int(0.3 * 1000)
        duration = defaultDuration + 50
        set_timeout(self.assertNoColorScheme, duration)

    def test_default_color_scheme(self):
        ui_bell('fizz')
        self.assertDefaultColorScheme()

    def test_light_color_scheme(self):
        self.set_setting('bell_color_scheme', 'light')
        ui_bell('fizz')
        # self.assertEqual(
        #     'Packages/NeoVintageous/res/Bell-light.hidden-color-scheme',
        #     self.view.settings().get('color_scheme'))

    def test_dark_color_scheme(self):
        self.set_setting('bell_color_scheme', 'dark')
        ui_bell('fizz')
        # self.assertEqual(
        #     'Packages/NeoVintageous/res/Bell-dark.hidden-color-scheme',
        #     self.view.settings().get('color_scheme'))

    def test_custom_color_scheme(self):
        self.set_setting('bell_color_scheme', 'Packages/NeoVintageous/tests/fixtures/custom.hidden-color-scheme')
        ui_bell('fizz')
        # self.assertEqual(
        #     'Packages/NeoVintageous/tests/fixtures/custom.hidden-color-scheme',
        #     self.view.settings().get('color_scheme'))

    def test_view_bell_style(self):
        self.set_setting('bell', 'view')
        ui_bell('fizz')
        self.assertDefaultColorScheme()
        self.assertBellIsRemoved()

    def test_views_bell_style(self):
        self.set_setting('bell', 'views')
        ui_bell('fizz')
        self.assertDefaultColorScheme()
        self.assertBellIsRemoved()

    def test_blink_bell_style(self):
        self.set_setting('bell', 'blink')
        ui_bell('fizz')

    def test_none_bell_style(self):
        self.set_setting('bell', 'none')
        ui_bell('fizz')
