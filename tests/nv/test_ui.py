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
