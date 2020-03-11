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


class Test_z_equal(unittest.FunctionalTestCase):

    @unittest.mock_run_commands('context_menu')
    @unittest.mock.patch('sublime.View.text_to_window')
    def test_n(self, text_to_window):
        text_to_window.return_value = (1.3, 5.7)
        self.eq('fi|zz', 'n_z=', 'fi|zz')
        self.assertRunCommand('context_menu', {'event': {'button': 2, 'x': 1.3, 'y': 5.7}})
