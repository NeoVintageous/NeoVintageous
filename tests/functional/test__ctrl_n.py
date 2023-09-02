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

from NeoVintageous.tests import unittest


class Test_ctrl_n(unittest.FunctionalTestCase):

    @unittest.mock_commands('auto_complete')
    def test_i_triggers_auto_complete(self):
        self.eq('fi|\n', 'i_<C-n>', 'i_fi|\n')
        self.assertRunCommand('auto_complete')

    @unittest.mock_commands('move')
    @unittest.mock.patch('sublime.View.is_auto_complete_visible')
    def test_i_when_auto_complete_visibe(self, is_auto_complete_visible):
        is_auto_complete_visible.return_value = True
        self.eq('fi|\n', 'i_<C-n>', 'i_fi|\n')
        self.assertRunCommand('move', {'by': 'lines', 'forward': True})
